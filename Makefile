hello: 
	echo "plop"

proto:
	python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/helloworld.proto

server:
	python greeter_server.py

client:
	python greeter_client.py
