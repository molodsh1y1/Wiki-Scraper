ARG PYTHON_VERSION=3.11.9
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gnupg \
    wget \
    curl \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN CHROME_VERSION=$(google-chrome --product-version) && \
    wget -q --continue -P /chromedriver "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /usr/local/bin/ && \
    rm -rf /chromedriver

ARG UID=1001

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --uid "${UID}" \
    appuser

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["alembic", "upgrade", "head"]
