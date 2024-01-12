from fastapi import FastAPI, HTTPException, status
from pydantic_models.request_model import RequestModel

from settings import WA_WEBOOK_NAME, WA_HISTORY_NAME, WA_DEFAULT_NAME
from services.custom_logger import WA_WEBHOOK_LOGGER, WA_HISTORY_LOGGER, WA_DEFAULT_LOGGER

app = FastAPI()

# Create a POST endpoint at /logging/
@app.post("/logging/")
async def logging_data(request_data: RequestModel):

    if request_data.service == WA_WEBOOK_NAME:
        WA_WEBHOOK_LOGGER.log(request_data.level, request_data.message)

    elif request_data.service == WA_HISTORY_NAME:
        WA_HISTORY_LOGGER.log(request_data.level, request_data.message)

    elif request_data.service == WA_DEFAULT_NAME:
        WA_DEFAULT_LOGGER.log(request_data.level, request_data.message)   

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not configured on logging manager",
        )

    return {
        "code":1,
        "message": request_data.message,
        "level": request_data.level
    }
