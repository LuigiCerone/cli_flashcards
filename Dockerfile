FROM python:3.9 AS builder

WORKDIR /app

RUN apt update && apt install gcc -y && python -m venv venv && venv/bin/pip install --no-cache-dir -U pip setuptools
ADD ./requirements.txt /app/requirements.txt
RUN venv/bin/pip install --no-cache-dir -r requirements.txt && find /app/venv \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+

FROM python:3.9

WORKDIR /app
COPY --from=builder /app /app

ADD ./cli_flashcards.py /app
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PATH="/app/venv/bin:$PATH"

RUN chmod +x ./cli_flashcards.py

ENTRYPOINT [ "python", "-u", "./cli_flashcards.py" ]
