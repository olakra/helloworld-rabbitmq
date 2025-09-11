"""
Server interface for the Python RabbitMQ service.
Handles incoming RPC requests and processes them.
"""
import logging
import os
from typing import Dict, Any
from adapters.rabbitmq_adapter import RabbitMQAdapter
from usecases.echo_usecase import EchoUseCase
from domain.models import EchoRequest, EchoResponse

logger = logging.getLogger(__name__)


class EchoServer:
    """Server that handles echo RPC requests."""
    
    def __init__(self, rabbitmq_url: str, queue_name: str = "echo_queue"):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.adapter = RabbitMQAdapter(rabbitmq_url)
        self.echo_usecase = EchoUseCase(self.adapter)
    
    def start(self) -> None:
        """Start the echo server."""
        try:
            logger.info("Starting Echo Server...")
            
            # Connect to RabbitMQ
            self.adapter.connect()
            
            # Declare the echo queue
            self.adapter.declare_queue(self.queue_name)
            
            # Set up message consumption
            self.adapter.consume_messages(self.queue_name, self._handle_echo_request)
            
            logger.info(f"Echo Server started, listening on queue: {self.queue_name}")
            logger.info("Press Ctrl+C to stop the server")
            
            # Start consuming messages
            self.adapter.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
            self.stop()
        except Exception as e:
            logger.error(f"Error starting server: {e}")
            self.stop()
            raise
    
    def stop(self) -> None:
        """Stop the echo server."""
        try:
            logger.info("Stopping Echo Server...")
            self.adapter.stop_consuming()
            self.adapter.disconnect()
            logger.info("Echo Server stopped")
        except Exception as e:
            logger.error(f"Error stopping server: {e}")
    
    def _handle_echo_request(self, message: Dict[str, Any]) -> None:
        """Handle incoming echo request."""
        try:
            logger.info(f"Processing echo request: {message}")
            
            # Process the request using the use case
            response = self.echo_usecase.process_echo_request(message)
            
            # Send response back (in a real RPC implementation, this would use reply_to)
            logger.info(f"Echo response created: {response.to_dict()}")
            
        except Exception as e:
            logger.error(f"Error processing echo request: {e}")


def main():
    """Main entry point for the echo server."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get configuration from environment
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672')
    
    # Create and start server
    server = EchoServer(rabbitmq_url)
    server.start()


if __name__ == "__main__":
    main()
