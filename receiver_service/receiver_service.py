from nameko.rpc import rpc

class ReceiverService:
    name = "receiver_service"

    @rpc
    def receive_message(self, message):
        print(f"Received: {message}")
