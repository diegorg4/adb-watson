from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from typing import Optional
import settings

# AdminToolsAdb123

# Define a Pydantic model for the request body
class RequestModel(BaseModel):
    model_config = ConfigDict(regex_engine='python-re')

    service: str = Field(validation_alias=AliasChoices('service', 'servicio'))
    origin: Optional[str] = Field(default=None, validation_alias=AliasChoices('origin','origen'))
    destination: Optional[str] = Field(default=None, validation_alias=AliasChoices('destination','destino'))
    leaving_date: Optional[str] = Field(default=None, validation_alias=AliasChoices('leaving_date','fecha_ida'))
    returning_date: Optional[str] = Field(default=None, validation_alias=AliasChoices('returning_date','fecha_regreso'))
    trip_type: Optional[str] = Field(default=None, validation_alias=AliasChoices('trip_type','tipo_viaje'), pattern=settings.TRIP_TYPE_PATTERN)
    leaving_price: Optional[float] = Field(default=None, validation_alias=AliasChoices('leaving_price','precio_ida'))
    returning_price: Optional[float] = Field(default=None, validation_alias=AliasChoices('returning_price','precio_vuelta'))
    channel: Optional[str] = Field(default=None, validation_alias=AliasChoices('channel','canal'))

    customer_name: Optional[str] = Field(default=None, validation_alias=AliasChoices('customer_name','nombre_cliente'))
    
    # For PHONE channel, customer_email field is not sent from the webhook calls on Watson Assistant
    customer_email: Optional[str] = Field(default="diego.roman@adbansys.com", validation_alias=AliasChoices('customer_email','email_cliente'), pattern=settings.EMAIL_PATTERN)
    
    customer_dn: Optional[str] = Field(default=None, validation_alias=AliasChoices('customer_dn','telefono_cliente'), pattern=settings.DN_PATTERN)
    
    wa_message: Optional[str] = Field(default=None, validation_alias=AliasChoices('wa_message','mensaje_wa'))
    