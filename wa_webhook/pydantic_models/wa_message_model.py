from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from typing import Optional

# AdminToolsAdb123 - twilio

# Define a Pydantic model for the request body
class WAMessageModel(BaseModel):    

    message: str = Field(default=None, validation_alias=AliasChoices('message','mensaje'))


