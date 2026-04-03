import grpc
import pytest
from unittest.mock import MagicMock

from qdrant_client import QdrantClient


@pytest.fixture
def mock_servicer_context():
    ctx = MagicMock(spec=grpc.ServicerContext)
    return ctx


@pytest.fixture
def mock_db_factory():
    return MagicMock()


@pytest.fixture
def mock_qdrant():
    return MagicMock(spec=QdrantClient)
