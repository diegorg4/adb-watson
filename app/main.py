from fastapi import FastAPI
from pydantic import BaseModel, Field, AliasChoices

from datetime import datetime
import locale
import random

app = FastAPI()

# Neccesary to return date on spanish
locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')

# Define a Pydantic model for the request body
class TravelData(BaseModel):
    origin: str = Field(validation_alias=AliasChoices('origin','origen'))
    destination: str = Field(validation_alias=AliasChoices('destination','destino'))
    leaving_date: str = Field(default=None, validation_alias=AliasChoices('leaving_date','fecha-ida'))
    returning_date: str = Field(validation_alias=AliasChoices('returning_date','fecha-regreso'))
    trip_type: str = Field(validation_alias=AliasChoices('trip_type','tipo-viaje'))

# Create a POST endpoint at /list-trips/
@app.post("/list-trips/")
async def list_trips(travel_data: TravelData):

    # Leaving trip text
    parsed_leaving_date = datetime.strptime(travel_data.leaving_date , '%Y-%m-%d')
    formatted_leaving_date = parsed_leaving_date.strftime('%A, %d de %B')
    leaving_travel_text = f"Gracias por la espera. Por favor digite en su teléfono la opción deseada. Para su salida de {travel_data.origin} a {travel_data.destination} el próximo {formatted_leaving_date} contamos con los siguientes vuelos: \n"
    leaving_travel_text += f"1. Viaje en Aerobot con salida a las {random.randint(6, 9)} de la mañana \n 2. Viaje con Aeromex a las {random.randint(8, 11)} de la mañana \n 3. Viaje con Aviones Nacionales a las {random.randint(4, 10)} de la mañana."

    # Returning trip text
    if travel_data.trip_type == "redondo" and travel_data.returning_date != "":
        parsed_returning_date = datetime.strptime(travel_data.returning_date , '%Y-%m-%d')
        formatted_returning_date = parsed_returning_date.strftime('%A, %d de %B')
        returning_travel_text = f"Para su viaje de regreso de {travel_data.destination} a {travel_data.origin} el próximo {formatted_returning_date} contamos con los siguientes vuelos:\n"
        returning_travel_text += f"1. Viaje en Aviones Nacionales con salida a las {random.randint(4, 8)} de la mañana. \n 2. Viaje con Aerobot a las {random.randint(9, 11)} de la mañana. \n 3. Viaje con Aeromex a las {random.randint(6, 11)} de la mañana."
    else:
        returning_travel_text = ""

    return {"texto-viaje-ida":leaving_travel_text, "texto-viaje-regreso":returning_travel_text}

