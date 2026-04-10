FROM python:3.11

WORKDIR /usr/src/app

COPY ./ ./

RUN mkdir /records

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "./main.py" ]
