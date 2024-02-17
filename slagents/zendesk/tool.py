import base64

from gentopia.tools import *


class SubmitInternalCommentToZendeskTicket(BaseTool):
    name = "submit_internal_comment_to_zendesk_ticket"
    description = "A tool to submit internal comment to zendesk ticket"

    def _run(self, body: str) -> Any:
        zendesk_url = f"https://swiftlane.zendesk.com/api/v2/tickets/14546"
        payload = {
            "ticket": {
                "comment": {
                    "body": body,
                    "public": False,
                },
            }
        }

        api_token = os.getenv("ZENDESK_API_TOKEN")
        agent_email = "nagesh@swiftlane.com"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {base64.b64encode(f'{agent_email}/token:{api_token}'.encode()).decode()}",
        }

        res = requests.put(
            zendesk_url,
            json=payload,
            headers=headers,
        )
        return {
            "status_code": res.status_code,
            "response": res.json(),
        }

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
