import json
from typing import Any

import requests
from fastapi import APIRouter
from fastapi import Depends
import logging

from swiftlane import settings
from swiftlane.api.zendesk.api_model import ZendeskTicketRequestSchema
from swiftlane.auth import RequiresServiceAccountAuth

logger = logging.getLogger(__file__)

from gentopia import AgentAssembler

router = APIRouter()

service_account_auth_checker = RequiresServiceAccountAuth(
    service_accounts=settings.SERVICE_ACCOUNTS_FOR_CLOUD_TASK_HANDLER)


@router.post("/zendesk-support-bot")
async def debug_zendesk_support_ticket(
        payload: ZendeskTicketRequestSchema,
        # auth: Any = Depends(service_account_auth_checker),
):
    agent_output = await run_conversation(message=payload.ticket_description, user_id=payload.user_id,
                                          company_id=payload.company_id, ticket_id=payload.ticket_id)
    if agent_output:
        # store agent output in firebase
        pass
        # await tools_utitlity.post_internal_comment_on_ticket(payload.ticket_id, agent_output)
    return {"status": "success",
            "agent_output": agent_output.output if agent_output else None}


async def missing_intercom_call(user_id: int, company_id: int, ticket_id: int, message: str):
    agent = AgentAssembler(file='swiftlane/agents/intercom/agent.yaml').get_agent()
    response = agent.run(f"user_id:{user_id} , company_id:{company_id}, ticket_id:{ticket_id} {message}", ticket_id)
    return response


async def run_conversation(message, user_id, company_id, ticket_id):
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

    ]
    api_key = settings.OPENAI_API_KEY
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
            function_response = await function_to_call(**function_args)
            return function_response
    else:
        logger.info(
            f"Failed to make API call, status code: {response.status_code}, response: {response.text}"
        )
