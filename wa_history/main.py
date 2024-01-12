from settings import LABEL_ERROR

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_models.request_model import RequestModel

from services.save_history import save_history
from common.log_event import log_event

# FastAPI server init
app = FastAPI()

# Create a POST endpoint at /list-trips/
@app.post("/wa-history/")
async def wa_history(request_data: RequestModel):

    # Log the entire request payload
    log_event("History Request Payload:" + request_data.model_dump_json())

    return save_history(request_data)
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
     
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	log_event(f"{request}: {exc_str}", LABEL_ERROR)
	content = {'code': 0, 'message': exc_str}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

