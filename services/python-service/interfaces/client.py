"""
Client interface for the Python RabbitMQ service.
Handles outgoing RPC requests.
"""
import logging
import os
from typing import Dict, Any
from adapters.rabbitmq_adapter import RabbitMQAdapter
from usecases.echo_usecase import EchoUseCase
from domain.models import EchoRequest, EchoResponse

logger = logging.getLogger(__name__)


class EchoClient:
    """Client that sends echo RPC requests."""
    
    def __init__(self, rabbitmq_url: str, queue_name: str = "echo_queue"):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.adapter = RabbitMQAdapter(rabbitmq_url)
        self.echo_usecase = EchoUseCase(self.adapter)
    
    def connect(self) -> None:
        """Connect to RabbitMQ."""
        self.adapter.connect()
        self.adapter.declare_queue(self.queue_name)
        logger.info("Echo Client connected to RabbitMQ")
    
    def disconnect(self) -> None:
        """Disconnect from RabbitMQ."""
        self.adapter.disconnect()
        logger.info("Echo Client disconnected from RabbitMQ")
    
    def send_echo_request(self, payload: str) -> EchoResponse:
        """Send an echo request and return the response."""
        try:
            # Create echo request using use case
            request = self.echo_usecase.echo_message(payload)
            
            # Send RPC request
            response_data = self.adapter.rpc_call(
                self.queue_name,
                request.to_dict()
            )
            
            # Parse response
            response = EchoResponse.from_dict(response_data)
            
            logger.info(f"Echo request sent and response received: {response.to_dict()}")
            return response
            
        except Exception as e:
            logger.error(f"Error sending echo request: {e}")
            raise
    
    def send_demo_request(self) -> EchoResponse:
        """Send a demo echo request."""
        demo_payload = "Hello from Python client"
        logger.info("Sending demo echo request...")
        return self.send_echo_request(demo_payload)


def main():
    """Main entry point for the echo client."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get configuration from environment
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672')
    
    # Create client
    client = EchoClient(rabbitmq_url)
    
    try:
        # Connect to RabbitMQ
        client.connect()
        
        # Send demo request
        response = client.send_demo_request()
        
        print(f"Demo RPC response: {response.to_dict()}")
        
    except Exception as e:
        logger.error(f"Error in client: {e}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
