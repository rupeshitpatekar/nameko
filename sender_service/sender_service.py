import time
from nameko.timer import timer
from nameko.standalone.rpc import ClusterRpcProxy
from nameko.rpc import rpc

class SenderService:
    name = "sender_service"

    @timer(interval=5)
    def scheduled_task(self):
        config = {'AMQP_URI': "pyamqp://guest:guest@rabbitmq"}
        message = {"message": "Hello, this is a scheduled message!", "timestamp": time.time()}

        # Retry mechanism
        for _ in range(5):  # Retry 5 times
            try:
                with ClusterRpcProxy(config) as rpc:
                    rpc.receiver_service.receive_message(message)
                    print(f"Sent: {message}")
                break
            except Exception as e:
                print(f"Error sending message: {e}")
                time.sleep(5)  # Wait 5 seconds before retrying