from pydantic_models.request_model import RequestModel

import json
import locale
import random
import settings
from common.log_event import log_event
from datetime import datetime

# Neccesary to return date on spanish
locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')

def travels_service(request_data: RequestModel):

    try: 
        # Leaving trip text
        parsed_leaving_date = datetime.strptime(request_data.leaving_date , '%Y-%m-%d')
        formatted_leaving_date = parsed_leaving_date.strftime('%A, %d de %B')
        leaving_travel_prices = [random.randint(800, 1200),random.randint(950, 1500),random.randint(900, 1130)]
        leaving_travel_hours = [random.randint(6, 9), random.randint(8, 11), random.randint(4, 10)]
        leaving_travel_dates = ["{} {}:00".format(request_data.leaving_date, day) for day in leaving_travel_hours]

        leaving_travel_text = f"Para su salida de {request_data.origin} a {request_data.destination} el próximo {formatted_leaving_date} contamos con los siguientes vuelos: \n"
        leaving_travel_text += f"1. Viaje en Aerobot con salida a las {leaving_travel_hours[0]} de la mañana con un costo de {leaving_travel_prices[0]} pesos. \n 2. Viaje con Aeromex a las {leaving_travel_hours[1]} de la mañana con un costo de {leaving_travel_prices[1]} pesos \n 3. Viaje con Aviones Nacionales a las {leaving_travel_hours[2]} de la mañana con un costo de {leaving_travel_prices[2]} pesos."

        # Returning trip text
        if request_data.trip_type == "redondo" and request_data.returning_date != "":
            parsed_returning_date = datetime.strptime(request_data.returning_date , '%Y-%m-%d')
            formatted_returning_date = parsed_returning_date.strftime('%A, %d de %B')
            returning_travel_prices = [random.randint(950, 1500),random.randint(1200, 1600),random.randint(800, 1100)]
            returning_travel_hours = [random.randint(4,8), random.randint(5,9 ), random.randint(10,11)]
            returning_travel_dates = ["{} {}:00".format(request_data.returning_date, day) for day in leaving_travel_hours]
            
            returning_travel_text = f"Para su viaje de regreso de {request_data.destination} a {request_data.origin} el próximo {formatted_returning_date} contamos con los siguientes vuelos:\n"
            returning_travel_text += f"1. Viaje en Aviones Nacionales con salida a las {returning_travel_hours[0]} de la mañana con un costo de {returning_travel_prices[0]} pesos. \n 2. Viaje con Aerobot a las {returning_travel_hours[1]} de la mañana con un costo de {returning_travel_prices[1]} pesos. \n 3. Viaje con Aeromex a las {returning_travel_hours[2]} de la mañana con un costo de {returning_travel_prices[2]} pesos."
        else:
            returning_travel_text = ""
            returning_travel_prices = []
            returning_travel_dates = []

        response = {
                "code":1,
                "leaving_travel":{
                    "sales_text":leaving_travel_text,
                    "prices": leaving_travel_prices,
                    "dates": leaving_travel_dates
                },
                "returning_travel": {
                    "sales_text": returning_travel_text,
                    "prices": returning_travel_prices,
                    "dates": returning_travel_dates
                }
        }
                
        log_event(json.dumps(response))

        return response
            
    except Exception as e:
        log_event(str(e), settings.LABEL_ERROR)
        
        return {
                "code":0,
                "description": str(e)
            }