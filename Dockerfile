FROM python:3

WORKDIR /usr/src/app

COPY . .
#ADD . /usr/src/app

RUN pip install --no-cache-dir .
RUN python setup.py clean