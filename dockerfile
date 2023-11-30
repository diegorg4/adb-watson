FROM python:3.11

RUN mkdir -p /home/watson-api

ENV PYTHONPATH=$PYTHONPATH:/home/watson-api

WORKDIR /home/watson-api

# Set noninteractive mode and default locales
ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=es_MX.UTF-8 \
    LANG=es_MX.UTF-8 \
    LANGUAGE=es_MX.UTF-8

# Install locales package and configure locales
RUN apt-get update && apt-get install -y locales \
    && echo "es_MX.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen es_MX.UTF-8 \
    && update-locale LANG=es_MX.UTF-8

# Install requirements file so the python app can run as usual
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY . .

WORKDIR /home/watson-api/app

# Command to run the FastAPI application using Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
