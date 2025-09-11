"""
Tests for echo client.
"""
import pytest
from unittest.mock import Mock, patch
from interfaces.client import EchoClient


class TestEchoClient:
    """Test cases for EchoClient."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.rabbitmq_url = "amqp://guest:guest@localhost:5672"
        self.client = EchoClient(self.rabbitmq_url)
    
    def test_client_initialization(self):
        """Test client initialization."""
        assert self.client.rabbitmq_url == self.rabbitmq_url
        assert self.client.queue_name == "echo_queue"
        assert self.client.adapter is not None
        assert self.client.echo_usecase is not None
    
    def test_client_initialization_custom_queue(self):
        """Test client initialization with custom queue name."""
        custom_queue = "custom_queue"
        client = EchoClient(self.rabbitmq_url, custom_queue)
        assert client.queue_name == custom_queue
    
    @patch('interfaces.client.RabbitMQAdapter')
    def test_connect(self, mock_adapter_class):
        """Test client connection."""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        client = EchoClient(self.rabbitmq_url)
        
        client.connect()
        
        mock_adapter.connect.assert_called_once()
        mock_adapter.declare_queue.assert_called_once_with("echo_queue")
    
    @patch('interfaces.client.RabbitMQAdapter')
    def test_disconnect(self, mock_adapter_class):
        """Test client disconnection."""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        client = EchoClient(self.rabbitmq_url)
        
        client.disconnect()
        
        mock_adapter.disconnect.assert_called_once()
    
    @patch('interfaces.client.RabbitMQAdapter')
    def test_send_echo_request(self, mock_adapter_class):
        """Test sending echo request."""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        client = EchoClient(self.rabbitmq_url)
        
        # Mock the use case
        mock_request = Mock()
        mock_request.to_dict.return_value = {"id": "test", "payload": "hello"}
        client.echo_usecase.echo_message = Mock(return_value=mock_request)
        
        # Mock the adapter RPC call
        mock_response_data = {"id": "test", "payload": "hello", "echoed_at": "2023-01-01T12:00:00"}
        mock_adapter.rpc_call.return_value = mock_response_data
        
        # Mock EchoResponse.from_dict
        with patch('interfaces.client.EchoResponse') as mock_response_class:
            mock_response = Mock()
            mock_response_class.from_dict.return_value = mock_response
            
            result = client.send_echo_request("hello")
            
            assert result == mock_response
            client.echo_usecase.echo_message.assert_called_once_with("hello")
            mock_adapter.rpc_call.assert_called_once()
    
    @patch('interfaces.client.RabbitMQAdapter')
    def test_send_demo_request(self, mock_adapter_class):
        """Test sending demo request."""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        client = EchoClient(self.rabbitmq_url)
        
        # Mock send_echo_request
        mock_response = Mock()
        client.send_echo_request = Mock(return_value=mock_response)
        
        result = client.send_demo_request()
        
        assert result == mock_response
        client.send_echo_request.assert_called_once_with("Hello from Python client")
