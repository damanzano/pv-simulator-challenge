
import logging
import pika
import random

class Meter(object):
    """This classs represent a meter generator for photovoltaic values
    """
    
    def __init__(self, broker_host, broker_port, queue_name):
        self._logger = logging.getLogger("pvsimulator.simulator")
        self._broker_host = broker_host
        self.__broker_port = broker_port
        self._queue_name = queue_name
        
    def start(self):
        self._logger.info("Generating raw PV values")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self._broker_host, 
                port=self.__broker_port))
        channel = connection.channel()
        channel.queue_declare(queue=self._queue_name)
        try:
            while(True):
                value = random.uniform(0, 9000)
                channel.basic_publish(
                    exchange='', 
                    routing_key='raw', 
                    body=f"{value:.2f}")
                self._logger.info(f"Sent {value:.2f}")
        except KeyboardInterrupt as ex:
            connection.close()
            self._logger.info("Operation stoped by user. Connection closed")