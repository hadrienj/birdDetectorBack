# GRPC

# 1) Run the server
`pipenv run make server`

# 2) In another terminal, run the client
`pipenv run make client`

Don't forget to add an audiofile in repository for example.
And update line 30 `AUDIO_FILE_NAME = "SWIFT_20190725_080011_2_4.wav"` in `greeter_client.py`

# To update the gRPC code used by our application to use the new service definition.
`pipenv run make proto`

# To adapt client for web (react)
See (Write JS Client Code Section)[https://grpc.io/docs/tutorials/basic/web/]

### Fore more informations
See [GRPC offical documentations](https://grpc.io/)
