# API dependencies
from fastapi import FastAPI
from pydantic_models.request_model import RequestModel
from pydantic import RootModel

from services.travels_service import travels_service
from services.send_tickets_service import send_tickets_service

import logging

# FastAPI server init
app = FastAPI()

# Create a POST endpoint at /list-trips/
@app.post("/ticket-sales-agent/")
async def ticket_sales_agent(request_data: RequestModel):

    # Log the entire request payload
    print("Request Payload:", request_data.model_dump())

    if request_data.service == "TRAVELS":
        return travels_service(request_data)
    
    elif request_data.service == "SENDTICKETS":
        return send_tickets_service(request_data)
    
    else:
        return {
                "code":0, 
                "description":"Service not found"
            }
