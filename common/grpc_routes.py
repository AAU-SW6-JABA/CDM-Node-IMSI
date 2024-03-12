import asyncio
import logging

import grpc
from route_guide_pb2_grpc import RoutesStub
from route_guide_pb2 import RegisterAntennaRequest, RegisterAntennaResponse, LogMeasurementRequest


class GrpcRoutes:
    @staticmethod
    def register_antenna(stub: RoutesStub, x: int, y: int) -> int:
        response = stub.RegisterAntennaRoute(RegisterAntennaRequest(x=x, y=y))

        if type(response) is not RegisterAntennaResponse:
            logging.exception("Failed to register antenna")
            return -1
        else:
            typed_response: RegisterAntennaResponse = response
            logging.info("Correctly registered antenna with id %s", typed_response.aid)
            return typed_response.aid

    @staticmethod
    async def log_measurement(self, stub: RoutesStub, measurement: LogMeasurementRequest) -> None:
        await stub.LogMeasurementRoute(measurement)
