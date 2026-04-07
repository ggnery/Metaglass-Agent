import pytest

from generated import orchestrator_pb2
from server.orchestrator_server import OrchestratorServer


@pytest.fixture
def service(mock_db_factory, mock_qdrant):
    return OrchestratorServer(db_factory=mock_db_factory, qdrant=mock_qdrant)


def test_query_is_unimplemented(service, mock_servicer_context):
    request = orchestrator_pb2.QueryRequest(session_id="s1", text_query="hello")
    with pytest.raises(NotImplementedError):
        service.Query(request, mock_servicer_context)


def test_query_stream_is_unimplemented(service, mock_servicer_context):
    request = orchestrator_pb2.QueryRequest(session_id="s1", text_query="hello")
    with pytest.raises(NotImplementedError):
        service.QueryStream(request, mock_servicer_context)


def test_stream_query_is_unimplemented(service, mock_servicer_context):
    with pytest.raises(NotImplementedError):
        service.StreamQuery(iter([]), mock_servicer_context)
