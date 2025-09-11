"""
Tests for RabbitMQ adapter.
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from adapters.rabbitmq_adapter import RabbitMQAdapter


class TestRabbitMQAdapter:
    """Test cases for RabbitMQAdapter."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.connection_url = "amqp://guest:guest@localhost:5672"
        self.adapter = RabbitMQAdapter(self.connection_url)
    
    @patch('adapters.rabbitmq_adapter.pika.BlockingConnection')
    def test_connect(self, mock_connection):
        """Test connecting to RabbitMQ."""
        mock_conn = Mock()
        mock_channel = Mock()
        mock_connection.return_value = mock_conn
        mock_conn.channel.return_value = mock_channel
        
        self.adapter.connect()
        
        assert self.adapter.connection == mock_conn
        assert self.adapter.channel == mock_channel
        mock_connection.assert_called_once()
        mock_conn.channel.assert_called_once()
    
    def test_disconnect(self):
        """Test disconnecting from RabbitMQ."""
        mock_connection = Mock()
        mock_channel = Mock()
        mock_channel.is_closed = False
        mock_connection.is_closed = False
        
        self.adapter.connection = mock_connection
        self.adapter.channel = mock_channel
        
        self.adapter.disconnect()
        
        mock_channel.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    def test_declare_queue(self):
        """Test declaring a queue."""
        mock_channel = Mock()
        self.adapter.channel = mock_channel
        
        self.adapter.declare_queue("test_queue")
        
        mock_channel.queue_declare.assert_called_once_with(
            queue="test_queue", 
            durable=True
        )
    
    def test_declare_queue_not_connected(self):
        """Test declaring a queue when not connected."""
        with pytest.raises(RuntimeError, match="Not connected to RabbitMQ"):
            self.adapter.declare_queue("test_queue")
    
    def test_publish_message(self):
        """Test publishing a message."""
        mock_channel = Mock()
        self.adapter.channel = mock_channel
        
        message = {"test": "data"}
        self.adapter.publish_message("test_queue", message)
        
        mock_channel.basic_publish.assert_called_once()
        call_args = mock_channel.basic_publish.call_args
        assert call_args[1]["routing_key"] == "test_queue"
        assert json.loads(call_args[1]["body"]) == message
    
    def test_publish_message_not_connected(self):
        """Test publishing a message when not connected."""
        message = {"test": "data"}
        with pytest.raises(RuntimeError, match="Not connected to RabbitMQ"):
            self.adapter.publish_message("test_queue", message)
    
    def test_consume_messages(self):
        """Test setting up message consumption."""
        mock_channel = Mock()
        self.adapter.channel = mock_channel
        
        def test_callback(message):
            pass
        
        self.adapter.consume_messages("test_queue", test_callback)
        
        mock_channel.basic_consume.assert_called_once()
    
    def test_consume_messages_not_connected(self):
        """Test consuming messages when not connected."""
        def test_callback(message):
            pass
        
        with pytest.raises(RuntimeError, match="Not connected to RabbitMQ"):
            self.adapter.consume_messages("test_queue", test_callback)
    
    def test_start_consuming(self):
        """Test starting message consumption."""
        mock_channel = Mock()
        self.adapter.channel = mock_channel
        
        self.adapter.start_consuming()
        
        mock_channel.start_consuming.assert_called_once()
    
    def test_stop_consuming(self):
        """Test stopping message consumption."""
        mock_channel = Mock()
        self.adapter.channel = mock_channel
        
        self.adapter.stop_consuming()
        
        mock_channel.stop_consuming.assert_called_once()
    
    def test_rpc_call(self):
        """Test making an RPC call."""
        mock_channel = Mock()
        mock_connection = Mock()
        mock_channel.queue_declare.return_value = Mock(method=Mock(queue="callback_queue"))
        mock_connection.process_data_events.return_value = None
        
        self.adapter.channel = mock_channel
        self.adapter.connection = mock_connection
        
        # Mock the response handling
        response_data = {"id": "test", "payload": "response"}
        self.adapter.channel.basic_consume.side_effect = lambda **kwargs: setattr(
            self.adapter, '_test_response', response_data
        )
        
        # Mock the response callback
        def mock_on_response(channel, method, properties, body):
            if hasattr(self.adapter, '_test_response'):
                return self.adapter._test_response
        
        message = {"test": "data"}
        result = self.adapter.rpc_call("test_queue", message)
        
        mock_channel.basic_publish.assert_called_once()
        mock_connection.process_data_events.assert_called()
