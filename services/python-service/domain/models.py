"""
Domain models for the Python RabbitMQ service.
Following Clean Architecture principles with domain entities.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional
import uuid


@dataclass
class EchoRequest:
    """Domain model for echo request."""
    id: str
    payload: str
    timestamp: datetime

    @classmethod
    def create(cls, payload: str) -> "EchoRequest":
        """Factory method to create a new echo request."""
        return cls(
            id=str(uuid.uuid4()),
            payload=payload,
            timestamp=datetime.utcnow()
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EchoRequest":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            payload=data["payload"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )


@dataclass
class EchoResponse:
    """Domain model for echo response."""
    id: str
    payload: str
    echoed_at: datetime

    @classmethod
    def create(cls, request: EchoRequest) -> "EchoResponse":
        """Factory method to create echo response from request."""
        return cls(
            id=request.id,
            payload=request.payload,
            echoed_at=datetime.utcnow()
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "payload": self.payload,
            "echoed_at": self.echoed_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EchoResponse":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            payload=data["payload"],
            echoed_at=datetime.fromisoformat(data["echoed_at"])
        )
