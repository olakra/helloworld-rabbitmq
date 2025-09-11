"""
Tests for domain models.
"""
import pytest
from datetime import datetime
from domain.models import EchoRequest, EchoResponse


class TestEchoRequest:
    """Test cases for EchoRequest model."""
    
    def test_create_echo_request(self):
        """Test creating an echo request."""
        payload = "test message"
        request = EchoRequest.create(payload)
        
        assert request.payload == payload
        assert request.id is not None
        assert isinstance(request.timestamp, datetime)
    
    def test_echo_request_to_dict(self):
        """Test converting echo request to dictionary."""
        request = EchoRequest.create("test message")
        request_dict = request.to_dict()
        
        assert request_dict["payload"] == "test message"
        assert request_dict["id"] == request.id
        assert "timestamp" in request_dict
    
    def test_echo_request_from_dict(self):
        """Test creating echo request from dictionary."""
        data = {
            "id": "test-id",
            "payload": "test message",
            "timestamp": "2023-01-01T12:00:00"
        }
        request = EchoRequest.from_dict(data)
        
        assert request.id == "test-id"
        assert request.payload == "test message"
        assert isinstance(request.timestamp, datetime)


class TestEchoResponse:
    """Test cases for EchoResponse model."""
    
    def test_create_echo_response(self):
        """Test creating an echo response from request."""
        request = EchoRequest.create("test message")
        response = EchoResponse.create(request)
        
        assert response.id == request.id
        assert response.payload == request.payload
        assert isinstance(response.echoed_at, datetime)
    
    def test_echo_response_to_dict(self):
        """Test converting echo response to dictionary."""
        request = EchoRequest.create("test message")
        response = EchoResponse.create(request)
        response_dict = response.to_dict()
        
        assert response_dict["id"] == request.id
        assert response_dict["payload"] == "test message"
        assert "echoed_at" in response_dict
    
    def test_echo_response_from_dict(self):
        """Test creating echo response from dictionary."""
        data = {
            "id": "test-id",
            "payload": "test message",
            "echoed_at": "2023-01-01T12:00:00"
        }
        response = EchoResponse.from_dict(data)
        
        assert response.id == "test-id"
        assert response.payload == "test message"
        assert isinstance(response.echoed_at, datetime)
