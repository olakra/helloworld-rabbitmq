"""
Tests for echo server.
"""
import pytest
from unittest.mock import Mock, patch
from interfaces.server import EchoServer


class TestEchoServer:
    """Test cases for EchoServer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.rabbitmq_url = "amqp://guest:guest@localhost:5672"
        self.server = EchoServer(self.rabbitmq_url)
    
    def test_server_initialization(self):
        """Test server initialization."""
        assert self.server.rabbitmq_url == self.rabbitmq_url
        assert self.server.queue_name == "echo_queue"
        assert self.server.adapter is not None
        assert self.server.echo_usecase is not None
    
    def test_server_initialization_custom_queue(self):
        """Test server initialization with custom queue name."""
        custom_queue = "custom_queue"
        server = EchoServer(self.rabbitmq_url, custom_queue)
        assert server.queue_name == custom_queue
    
    @patch('interfaces.server.RabbitMQAdapter')
    def test_handle_echo_request(self, mock_adapter_class):
        """Test handling echo request."""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        server = EchoServer(self.rabbitmq_url)
        
        # Mock the use case
        mock_response = Mock()
        mock_response.to_dict.return_value = {"id": "test", "payload": "echo"}
        server.echo_usecase.process_echo_request = Mock(return_value=mock_response)
        
        # Test message
        test_message = {"id": "test", "payload": "hello", "timestamp": "2023-01-01T12:00:00"}
        
        # Should not raise an exception
        server._handle_echo_request(test_message)
        
        # Verify use case was called
        server.echo_usecase.process_echo_request.assert_called_once_with(test_message)
    
    @patch('interfaces.server.RabbitMQAdapter')
    def test_handle_echo_request_error(self, mock_adapter_class):
        """Test handling echo request with error."""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        server = EchoServer(self.rabbitmq_url)
        
        # Mock the use case to raise an exception
        server.echo_usecase.process_echo_request = Mock(side_effect=Exception("Test error"))
        
        # Test message
        test_message = {"id": "test", "payload": "hello", "timestamp": "2023-01-01T12:00:00"}
        
        # Should not raise an exception (error is logged)
        server._handle_echo_request(test_message)
        
        # Verify use case was called
        server.echo_usecase.process_echo_request.assert_called_once_with(test_message)
