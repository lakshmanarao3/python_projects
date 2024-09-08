# use the official Python image from the Docker Hub
FROM python:3.9-slim
#
# # Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
#
# # Set the working directory
WORKDIR /app
#
# # Copy the requirements file
COPY requirements.txt /app/
#
# # Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
#
# # Copy the rest of the application code
COPY . /app/
#
# # Expose the port that the app runs on
EXPOSE 8080
#
# # Run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]
