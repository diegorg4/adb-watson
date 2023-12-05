from pydantic import BaseModel, Field, AliasChoices
from typing import Optional

# Define a Pydantic model for the request body
class RequestModel(BaseModel):
    service: str = Field(validation_alias=AliasChoices('service', 'servicio'))
    origin: Optional[str] = Field(validation_alias=AliasChoices('origin','origen'))
    destination: Optional[str] = Field(validation_alias=AliasChoices('destination','destino'))
    leaving_date: Optional[str] = Field(default=None, validation_alias=AliasChoices('leaving_date','fecha-ida'))
    returning_date: Optional[str] = Field(validation_alias=AliasChoices('returning_date','fecha-regreso'))
    trip_type: Optional[str] = Field(validation_alias=AliasChoices('trip_type','tipo-viaje'))
