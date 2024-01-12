import settings

from fastapi import FastAPI
from pydantic_models.request_model import RequestModel

from services.save_history import save_history
from common.log_event import log_event

# FastAPI server init
app = FastAPI()

# Create a POST endpoint at /list-trips/
@app.post("/wa-history/")
async def wa_history(request_data: RequestModel):

    # Log the entire request payload
    log_event("Request Payload:" + request_data.model_dump_json())

    return save_history(request_data)
    
    