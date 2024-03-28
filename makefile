setup: ./venv/bin/activate CDM-ProtocolBuffer/cdm_protobuf.proto
	. ./venv/bin/activate
	pip3 install -r python_module_requirements.txt
	python3 -m grpc_tools.protoc -I CDM-ProtocolBuffer --python_out=. --pyi_out=. --grpc_python_out=. CDM-ProtocolBuffer/cdm_protobuf.proto

run: main.py
	. ./venv/bin/activate
	python3 main.py

clean: setup run
	rm -rf *o setup
	rm -rf *o run
