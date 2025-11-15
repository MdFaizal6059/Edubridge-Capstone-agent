# Dockerfile for EduBridge Agent Deployment

# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependency files and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application code
COPY edubridge_agent.py .

# Expose the default port (optional, but standard for web services like Cloud Run)
EXPOSE 8080

# Environment variable for the API key (MUST be set securely during actual deployment)
ENV GEMINI_API_KEY="REPLACE_WITH_YOUR_CLOUD_SECRET"

# Command to run the agent (serving it as a continuous service for demonstration)
# Note: For a true ADK API server, the CMD would be 'adk serve', but this runs the core script.
CMD ["python", "edubridge_agent.py"]
