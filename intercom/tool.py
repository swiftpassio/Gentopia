from gentopia.tools import *


class GetUserData(BaseTool):
    name = "get_user_data"
    description = "A tool to get user data"

    def _run(self, user_id) -> Any:
        # read base url from .env file
        base_url = os.getenv("BASE_URL")
        # https://admin.swiftlane.com/api/v1/user/236154022679109146?company_id=82488426438216692
        url = "https://admin.swiftlane.com/api/v1/user/236154022679109146?company_id=82488426438216692"
        headers = {
            "Authorization": f"Bearer {os.getenv('API_TOKEN')}",
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
            "id_str": response.json()["data"]["id_str"],
            "status": response.json()["data"]["status"],
        }

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class GetIntercomHistoryForUser(BaseTool):
    name = "get_intercom_history_for_user"
    description = "A tool to get intercom history for user"

    def _run(self, user_id: str) -> Any:
        print(f"Getting user data for user_id: {user_id}")
        # read base url from .env file
        base_url = os.getenv("BASE_URL")
        # https://admin.swiftlane.com/api/v1/intercom/history/?company_id=82488426438216692&page=1&per_page=20&user_id=236154022679109146
        url = "https://admin.swiftlane.com/api/v1/intercom/history/?company_id=82488426438216692&page=1&per_page=10&user_id=236154022679109146"
        headers = {
            "Authorization": f"Bearer {os.getenv('API_TOKEN')}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get user data: {response.text}")
        return response.json()

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class GetCallLogOfLast3MissedCalls(BaseTool):
    name = "Get debugging Logs of Last 3 Missed Calls"
    description = "A tool to get the debugging logs of the last 3 missed calls"

    def _run(self, user_id: str) -> Any:
        base_url = os.getenv("BASE_URL")
        # https://admin.swiftlane.com/api/v1/intercom/history/?company_id=82488426438216692&page=1&per_page=20&user_id=236154022679109146
        url = "https://admin.swiftlane.com/api/v1/intercom/history/?company_id=82488426438216692&page=1&per_page=3&user_id=236154022679109146&status=missed"
        headers = {
            "Authorization": f"Bearer {os.getenv('API_TOKEN')}",
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
