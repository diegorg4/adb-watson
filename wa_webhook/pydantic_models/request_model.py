from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from typing import Optional

# AdminToolsAdb123

# Define a Pydantic model for the request body
class RequestModel(BaseModel):
    model_config = ConfigDict(regex_engine='python-re')

    service: str = Field(validation_alias=AliasChoices('service', 'servicio'))
    origin: Optional[str] = Field(default=None, validation_alias=AliasChoices('origin','origen'))
    destination: Optional[str] = Field(default=None, validation_alias=AliasChoices('destination','destino'))
    leaving_date: Optional[str] = Field(default=None, validation_alias=AliasChoices('leaving_date','fecha_ida'), pattern=r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$')
    returning_date: Optional[str] = Field(default=None, validation_alias=AliasChoices('returning_date','fecha_regreso'), pattern=r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$')
    trip_type: Optional[str] = Field(default=None, validation_alias=AliasChoices('trip_type','tipo_viaje'), pattern=r'^(sencillo|redondo)$')
    leaving_price: Optional[float] = Field(default=None, validation_alias=AliasChoices('leaving_price','precio_ida'))
    returning_price: Optional[float] = Field(default=None, validation_alias=AliasChoices('returning_price','precio_vuelta'))

    customer_name: Optional[str] = Field(default=None, validation_alias=AliasChoices('customer_name','nombre_cliente'))
    customer_email: Optional[str] = Field(default=None, validation_alias=AliasChoices('customer_email','email_cliente'), pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    customer_dn: Optional[str] = Field(default=None, validation_alias=AliasChoices('customer_dn','telefono_cliente'), pattern=r'^\d{10}$')
    
    wa_message: Optional[str] = Field(default=None, validation_alias=AliasChoices('wa_message','mensaje_wa'))
    


