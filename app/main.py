# API dependencies
from fastapi import FastAPI
from request_model import RequestModel

# General dependencies
import locale
import random
from datetime import datetime

app = FastAPI()

# Neccesary to return date on spanish
locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')

# Create a POST endpoint at /list-trips/
@app.post("/ticket-sales-agent/")
async def ticket_sales_agent(request_data: RequestModel):

    if request_data.service == "TRAVELS":
        return travels_service(request_data)
    
    elif request_data.service == "PAYMENT":
        return payment_service(request_data)
    
    else:
        return {"code":0, "description":"Service not found"}    

def travels_service(request_data: RequestModel):
    # Leaving trip text
    parsed_leaving_date = datetime.strptime(request_data.leaving_date , '%Y-%m-%d')
    formatted_leaving_date = parsed_leaving_date.strftime('%A, %d de %B')
    leaving_travel_text = f"Gracias por la espera. Por favor digite en su teléfono la opción deseada. Para su salida de {request_data.origin} a {request_data.destination} el próximo {formatted_leaving_date} contamos con los siguientes vuelos: \n"
    leaving_travel_text += f"1. Viaje en Aerobot con salida a las {random.randint(6, 9)} de la mañana \n 2. Viaje con Aeromex a las {random.randint(8, 11)} de la mañana \n 3. Viaje con Aviones Nacionales a las {random.randint(4, 10)} de la mañana."

    # Returning trip text
    if request_data.trip_type == "redondo" and request_data.returning_date != "":
        parsed_returning_date = datetime.strptime(request_data.returning_date , '%Y-%m-%d')
        formatted_returning_date = parsed_returning_date.strftime('%A, %d de %B')
        returning_travel_text = f"Para su viaje de regreso de {request_data.destination} a {request_data.origin} el próximo {formatted_returning_date} contamos con los siguientes vuelos:\n"
        returning_travel_text += f"1. Viaje en Aviones Nacionales con salida a las {random.randint(4, 8)} de la mañana. \n 2. Viaje con Aerobot a las {random.randint(9, 11)} de la mañana. \n 3. Viaje con Aeromex a las {random.randint(6, 11)} de la mañana."
    else:
        returning_travel_text = ""

    return {"code":1,"texto-viaje-ida":leaving_travel_text, "texto-viaje-regreso":returning_travel_text}

def payment_service(request_data: RequestModel):
    return {"code":0,"":"Service not built yet :("}