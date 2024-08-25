# Use an official Python runtime as a parent image
FROM python:3.12-slim
#FROM public.ecr.aws/lambda/python:3.10

RUN apt-get update && apt-get install -y python3-distutils python3-dev

# Set the working directory in the container
WORKDIR /src
#WORKDIR /var/task

# Copy the requirements file and install dependencies
COPY requirements.txt /src/
#COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY src/ /src/
COPY Models/ /Models/

COPY . .

# Make port 80 available to the world outside this container
#EXPOSE 80

# Define environment variable, if needed
ENV NAME World

# Command to run the application
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

# Set the command to use Mangum with your FastAPI app as the handler for Lambda
#CMD ["app.handler"]
CMD ["streamlit", "run", "Webapp.py"]
