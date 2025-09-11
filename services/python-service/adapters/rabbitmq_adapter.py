"""
RabbitMQ adapter implementation using pika.
Handles connection, message publishing, and consumption.
"""
import json
import logging
from typing import Any, Callable, Dict, Optional
import pika
from pika.adapters.blocking_connection import BlockingConnection
from pika.channel import Channel
from pika.spec import BasicProperties

logger = logging.getLogger(__name__)


class RabbitMQAdapter:
    """RabbitMQ adapter for message queue operations."""
    
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.connection: Optional[BlockingConnection] = None
        self.channel: Optional[Channel] = None
    
    def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        try:
            logger.info(f"Connecting to RabbitMQ at {self.connection_url}")
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.connection_url)
            )
            self.channel = self.connection.channel()
            logger.info("Successfully connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def disconnect(self) -> None:
        """Close connection to RabbitMQ."""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("Disconnected from RabbitMQ")
        except Exception as e:
            logger.error(f"Error disconnecting from RabbitMQ: {e}")
    
    def declare_queue(self, queue_name: str, durable: bool = True) -> None:
        """Declare a queue."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        self.channel.queue_declare(queue=queue_name, durable=durable)
        logger.info(f"Declared queue: {queue_name}")
    
    def publish_message(self, queue_name: str, message: Dict[str, Any]) -> None:
        """Publish a message to a queue."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        try:
            message_body = json.dumps(message)
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message_body,
                properties=BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            logger.info(f"Published message to queue {queue_name}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise
    
    def consume_messages(self, queue_name: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Start consuming messages from a queue."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        def message_handler(channel, method, properties, body):
            try:
                message = json.loads(body.decode('utf-8'))
                logger.info(f"Received message from queue {queue_name}")
                callback(message)
                channel.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=message_handler
        )
        logger.info(f"Started consuming messages from queue {queue_name}")
    
    def start_consuming(self) -> None:
        """Start consuming messages."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        logger.info("Starting message consumption...")
        self.channel.start_consuming()
    
    def stop_consuming(self) -> None:
        """Stop consuming messages."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        self.channel.stop_consuming()
        logger.info("Stopped message consumption")
    
    def rpc_call(self, queue_name: str, message: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
        """Make an RPC call and wait for response."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        # Declare a temporary callback queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue
        
        # Generate correlation ID
        correlation_id = str(hash(str(message)))
        
        # Set up response handling
        response = None
        
        def on_response(channel, method, properties, body):
            nonlocal response
            if properties.correlation_id == correlation_id:
                response = json.loads(body.decode('utf-8'))
                channel.basic_ack(delivery_tag=method.delivery_tag)
        
        # Set up consumer for response
        self.channel.basic_consume(
            queue=callback_queue,
            on_message_callback=on_response
        )
        
        # Publish RPC request
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=BasicProperties(
                reply_to=callback_queue,
                correlation_id=correlation_id,
            ),
            body=json.dumps(message)
        )
        
        logger.info(f"Sent RPC request to queue {queue_name}")
        
        # Wait for response
        while response is None:
            self.connection.process_data_events(time_limit=timeout)
        
        logger.info("Received RPC response")
        return response
