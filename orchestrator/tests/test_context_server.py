import pytest

from generated import common_pb2, context_pb2
from server.context_server import ContextServer


@pytest.fixture
def service(mock_db_factory, mock_qdrant):
    return ContextServer(db_factory=mock_db_factory, qdrant=mock_qdrant)


def test_semantic_search_is_unimplemented(service, mock_servicer_context):
    query = common_pb2.MediaPayload(data=b"test", mime_type="text/plain")
    request = context_pb2.SemanticSearchRequest(user_id="u1", query=query)
    with pytest.raises(NotImplementedError):
        service.SemanticSearch(request, mock_servicer_context)


def test_push_context_is_unimplemented(service, mock_servicer_context):
    payload = common_pb2.MediaPayload(
        data=b"supermarket",
        mime_type="text/plain",
        metadata={"context_hint": "location"},
    )
    request = context_pb2.PushContextRequest(
        session_id="s1", payload=payload, ttl=3600
    )
    with pytest.raises(NotImplementedError):
        service.PushContext(request, mock_servicer_context)


def test_get_session_context_is_unimplemented(service, mock_servicer_context):
    request = context_pb2.GetSessionContextRequest(session_id="s1", max_entries=10)
    with pytest.raises(NotImplementedError):
        service.GetSessionContext(request, mock_servicer_context)
