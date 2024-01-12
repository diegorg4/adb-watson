from pydantic import BaseModel, Field, AliasChoices
from typing import Dict

class RequestModel(BaseModel):
    playload: Dict = Field(validation_alias=AliasChoices('playload', 'payload'))
