"""
Use case for echo functionality.
Implements business logic following Clean Architecture principles.
"""
from typing import Protocol
from domain.models import EchoRequest, EchoResponse


class MessageRepository(Protocol):
    """Protocol for message repository interface."""
    
    def send_message(self, queue: str, message: dict) -> None:
        """Send a message to a queue."""
        ...
    
    def receive_message(self, queue: str) -> dict:
        """Receive a message from a queue."""
        ...


class EchoUseCase:
    """Use case for echo functionality."""
    
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository
    
    def echo_message(self, payload: str) -> EchoResponse:
        """
        Echo a message by creating a request and response.
        
        Args:
            payload: The message to echo
            
        Returns:
            EchoResponse: The echoed response
        """
        # Create echo request
        request = EchoRequest.create(payload)
        
        # Create echo response
        response = EchoResponse.create(request)
        
        return response
    
    def process_echo_request(self, request_data: dict) -> EchoResponse:
        """
        Process an echo request from external data.
        
        Args:
            request_data: Dictionary containing request data
            
        Returns:
            EchoResponse: The processed response
        """
        # Parse request from data
        request = EchoRequest.from_dict(request_data)
        
        # Create response
        response = EchoResponse.create(request)
        
        return response
