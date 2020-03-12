
import csv
import logging
import pika
import random
from datetime import datetime

class Simulator(object):
    def __init__(self, broker_host, broker_port, queue_name, outfile):
        self._logger = logging.getLogger("pvsimulator.simulator")
        self._broker_host = broker_host
        self._broker_port = broker_port
        self._queue_name = queue_name
        self._outfile = outfile
        
    def start(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self._broker_host, 
                port=self._broker_port))
        channel = connection.channel()
        channel.queue_declare(queue=self._queue_name)
        channel.basic_consume(
            queue=self._queue_name, 
            on_message_callback=self.__receive, 
            auto_ack=True)
        self._logger.info(f"Reading messages from {self._queue_name}")
        try:
            channel.start_consuming()
        except KeyboardInterrupt as ex:
            self._logger.info("Operation stoped by user. Connection closed")
    
    def __receive(self, channel, method, properties, body):
        self._logger.info(f"Received {body}")
        meter_value = float(body)
        pv_value = random.uniform(0, 9000)
        record = {
            "timestampt": datetime.now(),
            "meter_value": meter_value,
            "pv_value": pv_value,
            "sum": meter_value + pv_value
        }

        with open(self._outfile, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=record.keys())
            writer.writerow(record)