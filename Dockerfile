FROM python:3.11-slim

WORKDIR /app

# install system deps
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# copy project
COPY . /app

# install poetry
RUN pip install --no-cache-dir "poetry>=1.2"

# install dependencies via poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
