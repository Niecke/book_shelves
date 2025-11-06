# Use a slim Python base image
FROM python:3.11-slim

RUN apt update && apt install -y python3-psycopg-c

# Set working directory
WORKDIR /app

# Copy all app files
COPY ./app .

# Install Flask and dependencies (add requirements.txt if present)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 (Cloud Run requirement)
EXPOSE 8080

# Run Flask app on all IPs, port 8080
CMD ["python", "app.py"]
