# Use a Python base image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and
# buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
# We use a two-step copy to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port used by your Flask app (8080 as seen in your logs)
EXPOSE 8080

# Command to run the application. We use run.py as the entrypoint.
# Railway automatically maps the external port to the $PORT variable.
# We will update run.py to respect this.
CMD ["python", "run.py"]
