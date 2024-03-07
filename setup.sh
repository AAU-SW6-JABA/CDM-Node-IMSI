#!/bin/sh

pip install grpcio-tools
python3 -m grpc_tools.protoc -I CDM-ProtocolBuffer --python_out=. --pyi_out=. --grpc_python_out=. CDM-ProtocolBuffer/route_guide.proto