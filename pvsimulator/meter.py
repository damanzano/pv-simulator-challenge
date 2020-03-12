
import logging
import pika
import random

class Meter(object):
    """Meter class objects connect to a broker queue and publish random
    power values to it continously
    """
    def __init__(self, broker_host, broker_port, queue_name):
        self._logger = logging.getLogger("pvsimulator.simulator")
        self._broker_host = broker_host
        self._broker_port = broker_port
        self._queue_name = queue_name
        
    def start(self):
        """This method is in charge of establishing connection with desired 
        broker and start sending message to the queue
        """
        try:
            # Establish connection
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self._broker_host, 
                    port=self._broker_port))
            channel = connection.channel()
            # Ensure provided queue is avaialable to publish messages
            channel.queue_declare(queue=self._queue_name, durable=True)
            channel.confirm_delivery()
            self.__publish(channel)
            connection.close()
        except pika.exceptions.ConnectionClosedByBroker:
            self._logger.error("Connection was closed unexpectedly")
        except pika.exceptions.AMQPChannelError as err:
            self._logger.error(f"Caught a channel error: {err}, stopping...")
        except pika.exceptions.AMQPConnectionError:
            self._logger.error("Unable to connect to broker")
    
    def __publish(self, channel):
        """This method is in charge of continuosly generate power values and
         write them to the queue using a given channel.
         Publishing stop in user interruption
        """
        self._logger.info("Generating raw PV values")
        while(True):
            # Generate random power value
            value = random.uniform(0, 9000)
            # Publish value to the queue
            try:
                channel.basic_publish(
                    exchange='', 
                    routing_key='raw', 
                    body=f"{value:.2f}",
                    mandatory=True,
                    properties=pika.BasicProperties(
                        delivery_mode = 2, # make message persistent
                    )
                )
                self._logger.info(f"Sent {value:.2f}")
            except pika.exceptions.UnroutableError:
                self._logger.warn('Message was returned')
                continue
            except KeyboardInterrupt as ex:
                self._logger.info("Operation stoped by user")
                break
