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
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import os

import grpc

import helloworld_pb2
import helloworld_pb2_grpc
from microfaune_package.microfaune.detection import RNNDetector


def save_file_in_wave(response, file_name='myfile.wav'):
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, mode='bx') as f:
        f.write(response)


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def __init__(self):
        self.model = RNNDetector('models/model_weights-20190919_220113.h5')

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

    def GetPrediction(self, request, context):
        audiofile = request.audiofile
        save_file_in_wave(audiofile, file_name=request.filename)
        if os.path.exists(request.filename):
            print("FILE EXISTS")

        print(self.model)
        pred = self.model.predict_on_wav(request.filename)

        prediction_list = pred[1].tolist()
        return helloworld_pb2.Prediction(prediction_list=prediction_list)


def serve():
    options = [
        ('grpc.max_send_message_length', 50 * 1024 * 1024),
        ('grpc.max_receive_message_length', 50 * 1024 * 1024)
        ]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=options)
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
