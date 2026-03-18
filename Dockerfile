FROM python:3.11

WORKDIR /usr/src/app

COPY ./ ./

RUN mkdir /records

RUN make deps

ENTRYPOINT [ "python", "./main.py" ]
