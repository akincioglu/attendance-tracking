# We use Python 3.11 as the base image
FROM python:3.11-slim

# Creating a working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# We define environment variables to provide database connections
ENV PYTHONUNBUFFERED 1

# We expose the application port
EXPOSE 8000

# We define the command that will run when the application is started
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
