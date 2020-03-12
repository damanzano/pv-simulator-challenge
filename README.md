# PV Simulator Challenge

## Requirements
- python3
- pip

## Installation
1. Clone or download this repo
2. Inside the project folder execute
```
pip install .
python setup.py clean
```

## How to run it
The program is dividen in two executable components that connect to an RabbitMQ broker (connections are established against the defaul vhost): the meter (producer) and the PV simulator (consumer), each one can be executed indepndently.

To run the simulator
```
python pvsimulator/app.py start-simulator -b <BROKER_URL> -p <BROKER_PORT> -q <QUEUE> -u <USERNAME> -x <PASSWORD> -o <OUTPUT_FILE>
```

Ensure to replace <BROKER_URL>, <BROKER_PORT>, <QUEUE>, <USERNAME>, <PASSWORD> and <OUTPUT_FILE> with the corresponding values for your environment. The -o argument is optional, in case you don't provide it simulator output file will be store in output.csv by default.

To run the meter
```
python pvsimulator/app.py start-meter -b <BROKER_URL> -p <BROKER_PORT> -q <QUEUE>
```

Ensure to replace <BROKER_URL>, <BROKER_PORT>, <QUEUE>, <USERNAME> and  <PASSWORD> with the corresponding values for your environment. All arguments are mandatory.

You can use the following command if you have doubts about how to use any of the features in the program
```
python pvsimulator/app.py --help
```

## Utilities
I you want to run in a Linux like environment I provide some docker utilities to do so. You need to have docker and docker-compose installed. Containers are created used the python:3 image from Dockerhub which are based on Debian.

1. Inside the repository folder run:
```
docker-compose build
```
2. Start the rabbitmq service
```
docker-compose run --name rabbit rabbit
```
wait some seconds to allow the service to star properly
3. In different terminals start the simulator service
```
docker-compose run simulator
```
or the meter service
```
docker-compose run meter
```
4. If you want to see the output file in simulator
```
docker-compose run simulator cat output.csv
```
