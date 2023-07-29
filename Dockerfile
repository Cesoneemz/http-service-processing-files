FROM python:3.11

RUN apt-get update && apt-get install -y libgomp1

COPY . /app

RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /app
VOLUME /app/uploads

RUN $HOME/.local/bin/poetry install --no-root

EXPOSE 5000

CMD $HOME/.local/bin/poetry run python src/app.py