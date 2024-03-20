import logging

from cdm_protobuf_pb2_grpc import RoutesStub
from cdm_protobuf_pb2 import RegisterAntennaRequest, RegisterAntennaResponse, LogMeasurementRequest, Empty


class GrpcRoutes:
    @staticmethod
    async def register_antenna(stub: RoutesStub, x: float, y: float) -> int:
        response = await stub.RegisterAntennaRoute(RegisterAntennaRequest(x=x, y=y))

        if type(response) is not RegisterAntennaResponse:
            logging.exception("Failed to register antenna")
            return -1
        else:
            typed_response: RegisterAntennaResponse = response
            logging.info("Correctly registered antenna with id %s", typed_response.aid)
            return typed_response.aid

    @staticmethod
    async def log_measurement(stub: RoutesStub, measurement: LogMeasurementRequest):
        response = await stub.LogMeasurementRoute(measurement)

        if type(response) is not Empty:
            logging.exception("Failed to register antenna")

