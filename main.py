#!/usr/bin/env python3
from dotenv import load_dotenv
import os

from optparse import OptionParser

from queue import Queue
import asyncio
import logging

from common.imsi_sniffer import IMSISniffer
from common.grpc_routes import GrpcRoutes

from cdm_protobuf_pb2_grpc import RoutesStub

messageQueue: Queue = Queue()


class Main:
    options = None

    grpcRoutes: GrpcRoutes
    imsi_sniffer: IMSISniffer
    address: str
    x_coordinate: float
    y_coordinate: float



    def __init__(self):
        parser = OptionParser(usage="%prog: [options]")
        parser.add_option("-i", "--iface", dest="iface", default="lo", help="Interface (default : lo)")
        parser.add_option("-p", "--port", dest="port", default="4729", type="int", help="Port (default : 4729)")
        (options, args) = parser.parse_args()

        self.address = os.getenv("GRPC_SERVER_ADDRESS")
        self.x_coordinate = float(os.getenv("LOCATION_X"))
        self.y_coordinate = float(os.getenv("LOCATION_Y"))

        if not self.address:
            raise Exception("Failed to load address")
        
        self.options = options

    def run(self):
        self.grpcRoutes = GrpcRoutes(messageQueue, self.address, self.x_coordinate, self.y_coordinate)
        self.imsi_sniffer = IMSISniffer(messageQueue, self.options.port, self.options.iface)

        self.imsi_sniffer.start()
        asyncio.get_event_loop().run_until_complete(self.grpcRoutes.run())

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    main = Main()
    main.run()
