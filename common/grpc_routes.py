import logging
import grpc
from threading import Thread
from queue import Queue
from common.Message import Message
import asyncio

from cdm_protobuf_pb2_grpc import RoutesStub
from cdm_protobuf_pb2 import RegisterAntennaRequest, RegisterAntennaResponse, LogMeasurementRequest, Empty


class GrpcRoutes():
    stub: RoutesStub
    dataQueue: Queue
    antenna_id: int

    address: str
    coordinate_x: float
    coordinate_y: float


    def __init__(self, dataQueue: Queue, address: str, coordinate_x: float, coordinate_y: float):
        self.dataQueue = dataQueue
        self.address = address
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y

    async def run(self):
        async with grpc.aio.insecure_channel(self.address) as channel:
            self.stub = RoutesStub(channel)

            # Registering antenna
            self.antenna_id = await self.register_antenna(self.coordinate_x, self.coordinate_y)
            if self.antenna_id < 0:
                raise Exception("Failed to register antenna")

            while True:
                message: Message = self.dataQueue.get(True)

                requestMessage: LogMeasurementRequest = LogMeasurementRequest(
                    aid = self.antenna_id,
                    identifier = message.identifier,
                    timestamp = message.timestamp,
                    signal_strength = message.signal_strength
                )

                await self.log_measurement(requestMessage)
        

    async def register_antenna(self, x: float, y: float) -> int:
        response = await self.stub.RegisterAntennaRoute(RegisterAntennaRequest(x=x, y=y))

        if type(response) is not RegisterAntennaResponse:
            logging.exception("Failed to register antenna")
            return -1
        else:
            typed_response: RegisterAntennaResponse = response
            logging.info("Correctly registered antenna with id %s", typed_response.aid)
            return typed_response.aid

    async def log_measurement(self, measurement: LogMeasurementRequest):
        try:
            response = await self.stub.LogMeasurementRoute(measurement)

            if type(response) is not Empty:
                logging.warning("WARNING: Server sent unrecognizable response")
        except:
            logging.warning("ERROR: Failed to send measurement. Server not responding")
