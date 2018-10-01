## RPC Server
To send picture from raspberrypi to PC.

## Files
> server.py: receiver for picture;

> client.py: sender for picture;

## Install
> sudo pip3 install grpcio protobuf grpcio-tools

> grpcio : google rpc server

> protobuf : ...

> grpcio-tools: commpile pb

## Compile
> python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. *.proto

> grpc_tools.protoc : compile tool
