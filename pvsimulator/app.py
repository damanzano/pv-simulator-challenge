"""This module contains application entrypoints for using the library from the command line.
"""
import argparse
import logging
#import yaml
from pvsimulator.meter import Meter
from pvsimulator.simulator import Simulator

def start_meter(args):
    meter = Meter(args.broker, args.port, args.queue, args.username, args.password)
    meter.start()

def start_simulator(args):
    simulator = Simulator(args.broker, args.port, args.queue, args.username, args.password, args.outfile)
    simulator.start()

def main():
    # Sets up loggin configuration
    root_logger = logging.getLogger("pvsimulator")
    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s:%(name)s:%(created)f:%(message)s")
    shandler = logging.StreamHandler()
    shandler.setFormatter(formatter)
    root_logger.addHandler(shandler)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Photovoltaic simulator")
    
    subparsers = parser.add_subparsers(
        title="subcommands",
        description="valid subcommads",
        help="sub-command help")
    
    # Parser for "start-meter" command
    parser_meter = subparsers.add_parser("start-meter", help="Starts meter producer")
    parser_meter.add_argument("-b", "--broker", type=str, required=True, help="Broker url")
    parser_meter.add_argument("-p", "--port", type=int, required=True, help="Broker port")
    parser_meter.add_argument("-q", "--queue", type=str, required=True, help="Broker queue")
    parser_meter.add_argument("-u", "--username", type=str, required=True, help="username")
    parser_meter.add_argument("-x", "--password", type=str, required=True, help="password")
    parser_meter.set_defaults(func=start_meter)

    # Parser for "start-simulator" command
    parser_simulator = subparsers.add_parser("start-simulator", help="Starts PV simulator consumer")
    parser_simulator.add_argument("-b", "--broker", type=str, required=True, help="Broker url")
    parser_simulator.add_argument("-p", "--port", type=int, required=True, help="Broker port")
    parser_simulator.add_argument("-q", "--queue", type=str, required=True, help="Broker queue")
    parser_simulator.add_argument("-u", "--username", type=str, required=True, help="username")
    parser_simulator.add_argument("-x", "--password", type=str, required=True, help="password")
    parser_simulator.add_argument("-o", "--outfile", default="output.csv", help="Output file path")
    parser_simulator.set_defaults(func=start_simulator)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
