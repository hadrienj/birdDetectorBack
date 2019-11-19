# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# TODO: FIX ERROR
# grpc._channel._Rendezvous: <_Rendezvous of RPC that terminated with:
#         status = StatusCode.RESOURCE_EXHAUSTED
#         details = "Received message larger than max (4194305 vs. 4194304)"
#         debug_error_string = "{"created":"@1574162543.663157000","description":"Error received from peer ipv6:[::1]:50051","file":"src/core/lib/surface/call.cc","file_line":1055,"grpc_message":"Received message larger than max (4194305 vs. 4194304)","grpc_status":8}
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc
import os

import helloworld_pb2
import helloworld_pb2_grpc

AUDIO_FILE_NAME = "SWIFT_20190725_080011_2_4.wav"
AUDIO_PATH = os.path.join(AUDIO_FILE_NAME)


def get_audio_bytes(path=AUDIO_PATH):
    with open(path, "rb") as fd:
        contents = fd.read()
    return contents


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)

        # Route Prediction
        audio = get_audio_bytes()
        print(len(audio))
        prediction = stub.GetPrediction(helloworld_pb2.AudioFile(
            audiofile=audio,
            filename=AUDIO_FILE_NAME))
        print(prediction)


if __name__ == '__main__':
    logging.basicConfig()
    run()
