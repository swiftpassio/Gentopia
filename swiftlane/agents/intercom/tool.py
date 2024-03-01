from gentopia.tools import *
from google.cloud import bigquery
import logging
import ast

from swiftlane.utilities import tools_utitlity

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
        call_room_ids = [{
            "room_sid": call["room_id"],
            "id_str": call["id_str"]
        } for call in response.json()["data"]["call_history"]]
        logs = []
        for call_row_dict in call_room_ids:
            call_row_id = call_row_dict["id_str"]
            call_room_id = call_row_dict["room_sid"]
            # make api call and get missed call logs in parallel

            url = f"https://admin.swiftlane.com/api/v1/intercom-bq-logs?call_row_id={call_row_id}"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get user data: {response.text}")
            server_logs = response.json()
            mobile_log = get_missed_call_andriod_logs(call_room_id)
            logs.append({
                "server_logs": server_logs,
                "mobile_logs": mobile_log
            })

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


def get_missed_call_andriod_logs(room_sid):

    query = f"""
                    SELECT
  *
FROM (
  SELECT
    original_timestamp,
    CASE
      WHEN action = 'telecom_helper_create_incoming_call_account_error' THEN 'Telecom framework: telecom account is not initialized, app clear cache required'
      WHEN action = 'telecom_helper_create_incoming_call' THEN 'Telecom framework: requested to show incoming call'
      WHEN action = 'show_missed_call_notification' THEN 'Missed call notification shown'
      WHEN action = 'telecom_helper_decline_call' THEN 'Telecom framework: terminate call connection'
      WHEN action = 'telecom_service_on_create_incoming_connection' THEN 'Telecom framework: creating call connection'
      WHEN action = 'telecom_service_on_create_incoming_connection_error' THEN CONCAT('Telecom framework: create call connection failed: ', error_msg)
      WHEN action = 'telecom_service_on_create_incoming_connection_failed' THEN 'Telecom framework: create connection failed'
      WHEN action = 'telecom_conn_show_incoming_call_ui' THEN 'Telecom framework: showing incoming call UI'
      WHEN action = 'telecom_conn_timeout_reached' THEN 'Telecom framework: on ringing timeout, terminating'
      WHEN action = 'telecom_conn_hold' THEN 'Telecom framework: on hold'
      WHEN action = 'telecom_conn_unhold' THEN 'Telecom framework: on unhold'
      WHEN action = 'telecom_conn_answer' THEN 'Telecom framework: on answered'
      WHEN action = 'telecom_conn_reject' THEN 'Telecom framework: on rejected'
      WHEN action = 'telecom_conn_disconnect' THEN 'Telecom framework: on disconnect'
      WHEN action = 'telecom_conn_abort' THEN 'Telecom framework: on abort'
      WHEN action = 'telecom_conn_silence' THEN 'Telecom framework: on silence'
      WHEN action = 'telecom_conn_start_ringing' THEN 'Telecom framework: play ringtone'
      WHEN action = 'telecom_conn_stop_ringing' THEN 'Telecom framework: cancel ringtone'
      WHEN action = 'notification_unlock_action_btn_clicked' THEN 'On unlock clicked'
      WHEN action = 'notification_decline_action_btn_clicked' THEN 'On decline clicked'
      WHEN action LIKE 'telecom_conn_state_changed_%' THEN CONCAT('Telecom framework: connection status changed: ', SUBSTRING(action, 28))
      WHEN action = 'unlock'AND error_msg IS NOT NULL THEN CONCAT('Unlock failed=', error_msg)
      WHEN action ='unlock' THEN 'Unlock success'
      WHEN action = 'show_answer_screen' THEN 'Answer screen: shown'
      WHEN action = 'hide_answer_screen' THEN 'Answer screen: hide'
      WHEN action = 'answer_activity_destroyed' THEN 'Answer screen: destroy'
      WHEN action = 'answer_activity_back_pressed' THEN 'Answer screen: on back clicked'
      WHEN action = 'answer'
    AND error_msg IS NOT NULL THEN CONCAT('Answering failed=', error_msg)
      WHEN action = 'answer' THEN 'Answering'
      WHEN action = 'notification_answer_action_btn_clicked' THEN 'Notification: on answer'
      WHEN action = 'no_mic_permission_skip_answering' THEN 'Notification: answering, mic permission not accepted, skipping'
      WHEN action = 'video_activity_resumed' THEN 'OnCall screen: shown'
      WHEN action = 'video_activity_paused' THEN 'OnCall screen: hide'
      WHEN action = 'video_activity_destroyed' THEN 'OnCall screen: destroy'
      WHEN action = 'video_activity_on_end_call' THEN 'OnCall screen: on end call clicked'
      WHEN action = 'video_activity_on_unlock' THEN 'OnCall screen: on unlock clicked'
      WHEN action = 'video_service_on_command' THEN CONCAT('Video service: start failed=', error_msg)
      WHEN action = 'video_service_connecting'
    AND error_msg IS NOT NULL THEN CONCAT('Video service: connecting to room failed=', error_msg)
      WHEN action = 'video_service_connecting' THEN 'Video service: connecting to room'
      WHEN action = 'video_service_connected' THEN "Video service: room connected"
      WHEN action = 'onParticipantConnected' THEN "Video service: participan connected"
      WHEN action = 'onParticipantDisconnected' THEN "Video service: participan disconnected"
      WHEN action = 'video_service_disconnected' AND error_msg IS NOT NULL THEN CONCAT('Video service: room disconnected with error=', error_msg)
      WHEN action = 'video_service_disconnected' THEN 'Video service: room disconnected'
      WHEN action = 'first_time_remote_video_connected' THEN 'Video service: remove video connected'
      WHEN action = 'video_service_on_remote_video_disconnected' THEN 'Video service: remove video disconnected'
      WHEN action = 'video_service_on_local_audio_created' AND error_msg IS NOT NULL THEN CONCAT('Video service: local audio creating failed=', error_msg)
      WHEN action = 'video_service_on_local_audio_created' THEN 'Video service: local audio created'
      WHEN action = 'video_service_on_local_audio_released' THEN 'Video service: local audio released'
      WHEN action = 'video_service_on_local_video_created'
    AND error_msg IS NOT NULL THEN concat ('Video service: local video creation failed=',
      error_msg)
      WHEN action = 'video_service_on_local_video_created' THEN 'Video service: local video created'
      WHEN action = 'video_service_on_local_video_released' THEN 'Video service: local video released'
    ELSE
    action
  END
    AS action,
    context_app_version AS app_version,
    room_sid,
    CONCAT(context_device_manufacturer, ' / ', context_device_model) AS device,
    CONCAT('reachable=', network_reachable, '; cellular=', context_network_cellular, '; wifi=', context_network_wifi) AS network_status,
    CONCAT('is power saver eneabled=', power_save_mode_enabled, '', 'is idle mode enabled=', idle_mode_enabled) AS device_state_1,
    CONCAT('notification enabled=',is_notification_enabled,'','phone permission granted=',read_phone_state_permission_granted, '', 'is battery optimisation ignored=', is_battery_optimization_ignored) AS user_setting,
    CONCAT('is DND enabled=', is_dnd_enabled, '', 'is silent mode enabled=', is_silent_mode_enabled) AS device_state_2,
    CONCAT('') AS notification_config,
    context_traits_user_id,
    TIMESTAMP(DATETIME(original_timestamp, 'America/Los_Angeles')) AS US_LA_time,
  FROM
    `swiftpass.android_swiftlane_id.intercom_view`
  WHERE
    action IN ( 'telecom_helper_create_incoming_call_account_error',
      'telecom_helper_create_incoming_call',
      'show_missed_call_notification',
      'telecom_helper_decline_call',
      'telecom_service_on_create_incoming_connection',
      'telecom_service_on_create_incoming_connection_error',
      'telecom_service_on_create_incoming_connection_failed',
      'telecom_conn_show_incoming_call_ui',
      'telecom_conn_timeout_reached',
      'telecom_conn_hold',
      'telecom_conn_unhold',
      'telecom_conn_answer',
      'telecom_conn_reject',
      'telecom_conn_disconnect',
      'telecom_conn_abort',
      'telecom_conn_silence',
      'telecom_conn_start_ringing',
      'telecom_conn_stop_ringing',
      'notification_unlock_action_btn_clicked',
      'notification_decline_action_btn_clicked',
      'unlock',
      'show_answer_screen',
      'hide_answer_screen',
      'answer_activity_destroyed',
      'answer_activity_back_pressed',
      'answer',
      'notification_answer_action_btn_clicked',
      'no_mic_permission_skip_answering',
      'video_activity_resumed',
      'video_activity_paused',
      'video_activity_destroyed',
      'video_activity_on_end_call',
      'video_activity_on_unlock',
      'video_service_on_command',
      'video_service_connecting',
      'video_service_connected',
      'onParticipantConnected',
      'onParticipantDisconnected',
      'video_service_disconnected',
      'first_time_remote_video_connected',
      'video_service_on_remote_video_disconnected',
      'video_service_on_local_audio_created',
      'video_service_on_local_audio_released',
      'video_service_on_local_video_created',
      'video_service_on_local_video_released' )
    OR action LIKE 'telecom_conn_state_changed_%'
  UNION ALL
  SELECT
    original_timestamp,
    CASE action
      WHEN 'new_call' THEN 'FCM: new call'
      WHEN 'call_not_active' THEN 'FCM: call not active, skipping'
      WHEN 'cancel_call' THEN 'FCM: cancel call'
      WHEN 'missed_call' THEN CONCAT('FCM: missed call (status=', status, ')')
      WHEN 'failed' THEN 'FCM: failed whne checking call status, skipping'
      WHEN 'start_call_time_check_initiated' THEN 'FCM: call time check performed'
      WHEN 'call_time_check_failed' THEN 'FCM: call time check failed'
      WHEN 'incoming_call_request_notification' THEN 'FCM: In coming notification shown'
    ELSE
    action
  END
    AS action,
    context_app_version AS app_version,
    room_sid,
    CONCAT(context_device_manufacturer, ' / ', context_device_model) AS device,
    CONCAT('reachable=', network_reachable, '; cellular=', context_network_cellular, '; wifi=', context_network_wifi) AS network_status,
    CONCAT('is power saver enabled=', power_save_mode_enabled, '','is idle mode enabled=', idle_mode_enabled) AS device_state_1,
    CONCAT('notification enabled=',is_notification_enabled,'','phone permission granted=',read_phone_state_permission_granted, '', 'is battery optimisation ignored=', is_battery_optimization_ignored) AS user_setting,
    CONCAT('is DND enabled=', is_dnd_enabled, '', 'is silent mode enabled=', is_silent_mode_enabled) AS device_state_2,
    CONCAT('notification delay=', message_delivery_delay_seconds, '','is call start time valid=', is_call_start_time_valid, '','delay time threshold=', call_start_time_threshold) AS notification_config,
    context_traits_user_id,
    TIMESTAMP(DATETIME(original_timestamp, "America/Los_Angeles")) AS US_LA_time,
  FROM
    `swiftpass.android_swiftlane_id.fcm_view`
  WHERE
    action IN ('new_call',
      'cancel_call',
      'incoming_call_request_notification',
      'call_not_active',
      'start_call_time_check_initiated',
      'call_time_check_failed' )
    OR (action = 'failed'
      AND error_msg = 'error checking if call is active') )
WHERE
  -- context_traits_user_id = '631937167494661278'
   room_sid='{room_sid}'
ORDER BY
  original_timestamp DESC
LIMIT
  1000
    """


    # Note: Ensure you replace the placeholder and actual SQL syntax according to your requirements.

    client = get_google_bigquery_client()
    query_job = client.query(query)
    results = [
        {
            "original_timestamp": row.original_timestamp,
            "action": row.action,
            "app_version": row.app_version,
            "device": row.device,
            "network_status": row.network_status,
            "device_state_1": row.device_state_1,
            "user_setting": row.user_setting,
            "device_state_2": row.device_state_2,
            "notification_config": row.notification_config,
            "context_traits_user_id": row.context_traits_user_id,
            "US_LA_time": row.US_LA_time,
        }
        for row in query_job.result()
    ]
    return results if results else []


