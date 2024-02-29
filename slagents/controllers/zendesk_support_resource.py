from flask import request
from flask_restful import Resource

from slagents import settings
from slagents.auth import RequiresServiceAccountAuth
from gentopia.assembler.agent_assembler import AgentAssembler
import json
import logging
import requests

from slagents.schemas.zendesk_support_models import ZendeskTicketRequestSchema
from slagents.utilities import tools_utitlity

logger = logging.getLogger(__file__)


class ZendeskSupportCloudTaskHandler(Resource):
    @RequiresServiceAccountAuth(
        service_accounts=settings.SERVICE_ACCOUNTS_FOR_CLOUD_TASK_HANDLER
    )
    def post(self, token=None):
        ticket_request: ZendeskTicketRequestSchema = ZendeskTicketRequestSchema.load(request.json)
        agent_output = run_conversation(message=ticket_request.ticket_description, user_id=ticket_request.user_id,
                                        company_id=ticket_request.company_id, ticket_id=ticket_request.ticket_id)
        tools_utitlity.post_internal_comment_on_ticket(ticket_request.ticket_id, agent_output)


def missing_intercom_call(user_id: int, company_id: int, ticket_id: int, message: str):
    agent = AgentAssembler(file='intercom/agent.yaml').get_agent()
    response = agent.run(f"user_id:{user_id} , company_id:{company_id}, ticket_id:{ticket_id} {message}")
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
            function_response = function_to_call(**function_args)
            return function_response
    else:
        logger.info(
            f"Failed to make API call, status code: {response.status_code}, response: {response.text}"
        )

