FROM python:3.11-slim AS builder

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN pip3 install --no-cache-dir poetry=="1.5.1" && poetry config virtualenvs.create true

RUN python3 -m venv --copies /app/venv
RUN . /app/venv/bin/activate && poetry install

FROM python:3.11-slim

COPY --from=builder /app/venv /app/venv
ENV PATH /app/venv/bin:$PATH

COPY . /app

WORKDIR /app

EXPOSE 5000

CMD python src/app.py