#!/bin/sh

mkdir -p build/generated-grpc
pip install grpcio-tools
python3 -m grpc_tools.protoc -I CDM-ProtocolBuffer --python_out=build/generated-grpc --pyi_out=build/generated-grpc --grpc_python_out=build/generated-grpc CDM-ProtocolBuffer/route_guide.proto