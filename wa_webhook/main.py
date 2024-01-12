# API dependencies
from pydantic_models.request_model import RequestModel


from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse


from services.travels_service import travels_service
from services.send_tickets_service import send_tickets_service
from services.send_quadient_tickets import send_quadient_tickets

from common.log_event import log_event

from settings import LABEL_ERROR

# FastAPI server init
app = FastAPI()

# Create a POST endpoint at /list-trips/
@app.post("/ticket-sales-agent/")
async def ticket_sales_agent(request_data: RequestModel):
    
    log_event("Webhook Request Payload:" + request_data.model_dump_json())

    if request_data.service == "TRAVELS":
        return travels_service(request_data)
    
    elif request_data.service == "SENDTICKETS":
        return send_tickets_service(request_data)
    
    elif request_data.service == "QUADIENT":
        return send_quadient_tickets(request_data)
    else:
        return {
                "code":0, 
                "description":"Service not found"
            }

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
     
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	log_event(f"{request}: {exc_str}", LABEL_ERROR)
	content = {'code': 0, 'message': exc_str}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

