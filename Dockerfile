FROM python:3.11-slim
WORKDIR /app
RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc python3-dev \
  && rm -rf /var/lib/apt/lists/*
RUN pip install poetry
COPY README.md /app/README.md
COPY pyproject.toml poetry.lock* /app/
COPY application /app/application
COPY database /app/database
COPY models /app/models
COPY daily.csv /app
COPY monthly.csv /app
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
