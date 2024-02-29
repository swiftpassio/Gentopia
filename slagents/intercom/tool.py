from gentopia.tools import *
from google.cloud import bigquery
import logging
import ast

from slagents.utilities import tools_utitlity

logger = logging.getLogger(__file__)

_bigquery_client = None


def get_google_bigquery_client():
    global _bigquery_client
    if not _bigquery_client:
        _bigquery_client = bigquery.Client(project="swiftpass")
    return _bigquery_client


class GetUserData(BaseTool):
    name = "get_user_data"
    # description with example
    description = "A tool to get user data , example: get_user_data {'user_id': 236154022679109146, 'company_id': 82488426438216692}"

    def _run(self, user_id_str: str) -> Any:
        user_data = ast.literal_eval(user_id_str)
        user_id = user_data["user_id"]
        company_id = user_data["company_id"]
        # https://admin.swiftlane.com/api/v1/user/236154022679109146?company_id=82488426438216692
        url = f"https://admin.swiftlane.com/api/v1/user/{user_id}?company_id={company_id}"
        access_token = tools_utitlity.check_and_refresh_access_token(doc_id="236154022679109146")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get user data: {response.text}")
        return {
            "email": response.json()["data"]["email"],
            "first_name": response.json()["data"]["first_name"],
            "last_name": response.json()["data"]["last_name"],
            "phone_number": response.json()["data"]["phone_number"],
            "intercom_settings": response.json()["data"]["intercom_settings"],
            "intercom_tokens": response.json()["data"]["intercom_tokens"],
            "workspace_id_str": response.json()["data"]["workspace_id_str"],
            "id_str": response.json()["data"]["id_str"],
            "status": response.json()["data"]["status"],
            "is_user_front_desk": response.json()["data"]["is_user_front_desk"],
            "is_intercom_directory_created": response.json()["data"]["is_intercom_directory_created"],
            "is_mobile_credentials_assigned": response.json()["data"]["is_mobile_credentials_assigned"],
            "is_pin_assigned": response.json()["data"]["is_pin_assigned"],
            "user_device_settings": get_user_phone_settings(user_id)
        }

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class GetIntercomHistoryForUser(BaseTool):
    name = "get_intercom_history_for_user"
    description = "A tool to get intercom history using user data from get_user_data tool"

    def _run(self, user_data) -> Any:
        print(f"Getting user data for user: {user_data}")
        user_json = ast.literal_eval(user_data)
        user_id = user_json["id_str"]
        company_id = user_json["workspace_id_str"]
        # read base url from .env file
        base_url = os.getenv("BASE_URL")
        # https://admin.swiftlane.com/api/v1/intercom/history/?company_id=82488426438216692&page=1&per_page=20&user_id=236154022679109146
        url = f"{base_url}/api/v1/intercom/history/?company_id={company_id}&page=1&per_page=5&user_id={user_id}"
        access_token = tools_utitlity.check_and_refresh_access_token(doc_id="236154022679109146")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get user data: {response.text}")
        return {
            "user_profile_data": user_data,
            "intercom_history": response.json()["data"]["call_history"]
        }

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class GetCallLogOfLast3MissedCalls(BaseTool):
    name = "Get debugging Logs of Last 3 Missed Calls"
    description = "A tool to get the debugging logs of the last 3 missed calls example: GetCallLogOfLast3MissedCalls {'user_id': 236154022679109146, 'company_id': 82488426438216692}"

    def _run(self, user_data: str) -> Any:
        base_url = os.getenv("BASE_URL")
        print(f"Getting user missed events data for user: {user_data}")
        user_data_obj = ast.literal_eval(user_data)
        user_id = user_data_obj["user_id"]
        company_id = user_data_obj["company_id"]
        # https://admin.swiftlane.com/api/v1/intercom/history/?company_id=82488426438216692&page=1&per_page=20&user_id=236154022679109146
        url = f"{base_url}/api/v1/intercom/history/?company_id={company_id}&page=1&per_page=3&user_id={user_id}&status=missed"
        access_token = tools_utitlity.check_and_refresh_access_token(doc_id="236154022679109146")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get user data: {response.text}")
        call_row_ids = [call["id_str"] for call in response.json()["data"]["call_history"]]
        logs = []
        for call_row_id in call_row_ids:
            url = f"https://admin.swiftlane.com/api/v1/intercom-bq-logs?call_row_id={call_row_id}"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get user data: {response.text}")
            logs.append(response.json())
        return logs

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


def get_user_phone_settings(user_id):
    query = f"""
                SELECT
  context_traits_user_id,
  context_traits_workspace_id,
  is_dnd_enabled,
  is_battery_optimization_ignored,
  is_silent_mode_enabled,
  is_notification_enabled,
  read_phone_state_permission_granted,
  network_reachable,
  context_app_version,
  context_device_model,
  context_device_manufacturer,
  idle_mode_enabled,
  power_save_mode_enabled,
  original_timestamp,
  screen_on
FROM
  `android_swiftlane_id.application`
                WHERE context_traits_user_id = '{str(user_id)}'
                ORDER BY timestamp DESC
                LIMIT 1
            """
    client = get_google_bigquery_client()
    query_job = client.query(query)
    # return only config and timestamp in same dict
    results = [
        {
            "is_dnd_enabled": row.is_dnd_enabled,
            "is_battery_optimization_ignored": row.is_battery_optimization_ignored,
            "is_silent_mode_enabled": row.is_silent_mode_enabled,
            "is_notification_enabled": row.is_notification_enabled,
            "read_phone_state_permission_granted": row.read_phone_state_permission_granted,
            "idle_mode_enabled": row.idle_mode_enabled,
            "power_save_mode_enabled": row.power_save_mode_enabled,
            "context_device_model": row.context_device_model,
            "context_app_version": row.context_app_version,
            "network_reachable": row.network_reachable,
        }
        for row in query_job.result()
    ]
    return results[0] if results else {}
