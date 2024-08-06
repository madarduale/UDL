# Use a slim Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Display the environment variables for debugging
RUN echo "SECRET_KEY: $SECRET_KEY"
RUN echo "DEBUG: $DEBUG"
RUN echo "ALLOWED_HOSTS: $ALLOWED_HOSTS"
RUN echo "DATABASE_URL: $DATABASE_URL"
RUN echo "PORT: $PORT"

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on (use the PORT environment variable)
EXPOSE 10000

# Define the command to run the application, using the PORT environment variable
# CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:10000", "UDL_project.wsgi:application"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "10000", "UDL_project.asgi:application"]