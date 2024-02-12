# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.1
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy the source code into the container.
COPY . /app/

# Install Poetry and dependencies
RUN pip install poetry && \
    # Not necessary to creatae virtual environment in Docker
    poetry config virtualenvs.create false && \
    # Install dependencies listed in pyproject.toml without user interaction and without color codes in the output
    poetry install --no-interaction --no-ansi

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000
