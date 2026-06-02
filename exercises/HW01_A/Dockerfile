FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY requirements.txt .
COPY src ./src

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir .

CMD ["airbnb-ops", "run"]