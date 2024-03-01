import os
import dotenv
import firebase_admin

from gentopia.assembler.agent_assembler import AgentAssembler
import json
import logging

import requests

from swiftlane import settings

logger = logging.getLogger(__file__)
dotenv.load_dotenv(".env")  # load environmental keys
if len(firebase_admin._apps) == 0:
    firebase_admin.initialize_app(
        name="swiftlane-dev-instance",
        options={
            "projectId": "swiftlane-dev",
            "serviceAccountId": settings.SERVICE_ACCOUNTS_FOR_CLOUD_TASK_HANDLER,
        },
    )


def missing_intercom_call(user_id: int, company_id: int, ticket_id: int, message: str):
    agent = AgentAssembler(file='swiftlane/agents/intercom/agent.yaml').get_agent()
    response = agent.run(f"user_id:{user_id} , company_id:{company_id}, ticket_id:{ticket_id} {message}")
    print(response)
    return response


def run_conversation(message, user_id, company_id, ticket_id):
    logger.info(f"run_conversation:{message},{user_id},{company_id}")
    messages = [
        {"role": "user", "content": message},
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "missing_intercom_call",
                "description": "Check why the user is not receiving intercom calls or notifications",
                "parameters": {},
            },
        }
        # {
        #     "type": "function",
        #     "function": {
        #         "name": "intercom_reader_offline_or_frozen",
        #         "description": "Check if the intercom reader which also does face recognition is offline or frozen or not working",
        #         "parameters": {},
        #     },
        # },
        # {
        #     "type": "function",
        #     "function": {
        #         "name": "check_pin_creation_access",
        #         "description": "check why user unable to create visitor pin or personal pin",
        #         "parameters": {},
        #     },
        # },
        # {
        #     "type": "function",
        #     "function": {
        #         "name": "user_unable_to_login",
        #         "description": "check why user unable to login to the app or web dashboard",
        #         "parameters": {},
        #     },
        # },
        # {
        #     "type": "function",
        #     "function": {
        #         "name": "check_schedule",
        #         "description": "Check if the schedule is not working",
        #         "parameters": {},
        #     },
        # },
        # {
        #     "type": "function",
        #     "function": {
        #         "name": "access_method_not_working",
        #         "description": "Check if the access method is not working",
        #         "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "method": {
        #                     "type": "string",
        #                     "description": "access method like face recognition, card,fob, pin ,mobile unlock, app unlock, bluetooth,ble, remote unlock.",
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "type": "function",
        #     "function": {
        #         "name": "unlock_failed",
        #         "description": "check why the door unlock failed",
        #         "parameters": {},
        #     },
        # },
    ]
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # Define the endpoint URL for the ChatGPT model API call
    url = "https://api.openai.com/v1/chat/completions"

    # Construct the payload with your parameters
    payload = json.dumps(
        {
            "model": "gpt-4-0125-preview",
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
        }
    )

    # Make the API call using the requests library
    response = requests.post(url, headers=headers, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response data
        response_data = response.json()
        response_message = response_data["choices"][0]["message"]
        tool_calls = response_message.get("tool_calls", [])
        messages.append(response_message)  # Extend conversation with assistant's reply

        responses_list = []
        available_functions = {
            # Define your available functions here
            "missing_intercom_call": missing_intercom_call,

        }
        for tool_call in tool_calls:
            logger.info(f"tool_call: {tool_call}")
            function_name = tool_call["function"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call["function"]["arguments"])
            function_args["user_id"] = user_id
            function_args["company_id"] = company_id
            function_args["ticket_id"] = ticket_id
            function_args["message"] = message
            function_response = function_to_call(**function_args)
            return function_response
    else:
        logger.info(
            f"Failed to make API call, status code: {response.status_code}, response: {response.text}"
        )


run_conversation("not getting calls", 641245110265904786, 625933143218851574, 12345)
