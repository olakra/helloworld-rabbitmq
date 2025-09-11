"""
Main entry point for the Python RabbitMQ service.
Demonstrates both server and client functionality.
"""
import logging
import os
import sys
import time
from interfaces.server import EchoServer
from interfaces.client import EchoClient

logger = logging.getLogger(__name__)


def run_demo():
    """Run a demo of the echo service."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get configuration from environment
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672')
    
    logger.info("Starting Python RabbitMQ Echo Service Demo")
    
    # Create server
    server = EchoServer(rabbitmq_url)
    
    # Create client
    client = EchoClient(rabbitmq_url)
    
    try:
        # Start server in background (simplified for demo)
        logger.info("Starting echo server...")
        server.adapter.connect()
        server.adapter.declare_queue(server.queue_name)
        
        # Connect client
        logger.info("Connecting echo client...")
        client.connect()
        
        # Send demo request
        logger.info("Sending demo echo request...")
        response = client.send_demo_request()
        
        logger.info(f"Demo completed successfully!")
        logger.info(f"Response: {response.to_dict()}")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        sys.exit(1)
    finally:
        # Clean up
        try:
            client.disconnect()
            server.stop()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


if __name__ == "__main__":
    run_demo()
