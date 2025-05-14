FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]