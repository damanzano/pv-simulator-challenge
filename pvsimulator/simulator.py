
import csv
import logging
import pika
import random
from datetime import datetime

class Simulator(object):
    """Simulator class objects subscribes to a broker queue and generates
    simulated a PV power values each time a meter values is received from
    the queue. 
    """
    def __init__(self, broker_host, broker_port, queue_name, outfile):
        self._logger = logging.getLogger("pvsimulator.simulator")
        self._broker_host = broker_host
        self._broker_port = broker_port
        self._queue_name = queue_name
        self._outfile = outfile
        
    def start(self):
        """This method is in charge of establishing connection with desired 
        broker and continously listen for new values in the queue.
        """
        try:
            # Establish connection
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self._broker_host, 
                    port=self._broker_port))
            channel = connection.channel()
            # Ensure provided queue is available to listen
            channel.basic_qos(prefetch_count=1)
            channel.queue_declare(queue=self._queue_name, durable=True)

            # Configure  and start cosnsumption process
            channel.basic_consume(
                queue=self._queue_name, 
                on_message_callback=self.__receive)
            self._logger.info(f"Reading messages from {self._queue_name}")
            try:
                channel.start_consuming()
            except KeyboardInterrupt as ex:
                channel.stop_consuming()
                connection.close()
                self._logger.info("Operation stoped by user. Connection closed")
        
        except pika.exceptions.ConnectionClosedByBroker as err:
            self._logger.error("Connection was closed unexpectedly")
        except pika.exceptions.AMQPChannelError as err:
            self._logger.error(f"Caught a channel error: {err}, stopping...")
        except pika.exceptions.AMQPConnectionError as err:
            self._logger.error("Unable to connect to broker")
            self._logger.exception(err)
        
    
    def __receive(self, channel, method, properties, body):
        """This method is in charge of processing new values comming from queue
        and store results in the ouput file
        """
        self._logger.info(f"Received {body}")
        # Process received values
        meter_value = float(body)
        # Generate simulated PV value
        pv_value = random.uniform(0, 9000)
        # Create processed record and write it to output
        record = {
            "timestampt": datetime.now(),
            "meter_value": meter_value,
            "pv_value": pv_value,
            "sum": meter_value + pv_value
        }
        self.__write_record(record)
        # Confirm value has been received and processed
        channel.basic_ack(delivery_tag = method.delivery_tag)

    def __write_record(self, record):
        """This method write new records into output file
        """
        with open(self._outfile, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=record.keys())
            writer.writerow(record)
        
        