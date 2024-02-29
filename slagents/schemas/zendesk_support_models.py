from dataclasses import field
from typing import List
from typing import Optional

import marshmallow_dataclass as md

from slagents.schemas.base_schema import ClassWithSchema


@md.dataclass()
class ZendeskTicketRequestSchema(ClassWithSchema):
    ticket_id: str
    company_id: int
    user_id: int
    ticket_description: str
