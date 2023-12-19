import settings
import logging
from fastapi import FastAPI
from pydantic_models.request_model import RequestModel

app = FastAPI()

logging.basicConfig(level=logging.INFO, filename="/var/log/services.log")

# Create a POST endpoint at /list-trips/
@app.post("/logging/")
async def logging(request_data: RequestModel):

    logging.info(request_data.model_dump())

    return {
        "code":1,
        "message": request_data.message,
        "level": request_data.level
    }

