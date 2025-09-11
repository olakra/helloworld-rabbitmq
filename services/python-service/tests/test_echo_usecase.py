"""
Tests for echo use case.
"""
import pytest
from unittest.mock import Mock
from usecases.echo_usecase import EchoUseCase
from domain.models import EchoRequest, EchoResponse


class TestEchoUseCase:
    """Test cases for EchoUseCase."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_repository = Mock()
        self.echo_usecase = EchoUseCase(self.mock_repository)
    
    def test_echo_message(self):
        """Test echoing a message."""
        payload = "test message"
        response = self.echo_usecase.echo_message(payload)
        
        assert isinstance(response, EchoResponse)
        assert response.payload == payload
        assert response.id is not None
        assert response.echoed_at is not None
    
    def test_process_echo_request(self):
        """Test processing an echo request from data."""
        request_data = {
            "id": "test-id",
            "payload": "test message",
            "timestamp": "2023-01-01T12:00:00"
        }
        
        response = self.echo_usecase.process_echo_request(request_data)
        
        assert isinstance(response, EchoResponse)
        assert response.id == "test-id"
        assert response.payload == "test message"
        assert response.echoed_at is not None
