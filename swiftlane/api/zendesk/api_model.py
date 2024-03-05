from pydantic import BaseModel


class ZendeskTicketRequestSchema(BaseModel):
    ticket_id: str
    company_id: int
    user_id: int
    ticket_description: str
