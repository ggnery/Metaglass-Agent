import pytest

from generated import context_pb2
from services.context_service import ContextServiceServicer


@pytest.fixture
def service(mock_db_factory, mock_qdrant):
    return ContextServiceServicer(db_factory=mock_db_factory, qdrant=mock_qdrant)


def test_semantic_search_is_unimplemented(service, mock_servicer_context):
    request = context_pb2.SemanticSearchRequest(user_id="u1", query_text="test")
    with pytest.raises(NotImplementedError):
        service.SemanticSearch(request, mock_servicer_context)


def test_push_context_is_unimplemented(service, mock_servicer_context):
    entry = context_pb2.ContextEntry(context_type="location", content="supermarket")
    request = context_pb2.PushContextRequest(session_id="s1", entry=entry)
    with pytest.raises(NotImplementedError):
        service.PushContext(request, mock_servicer_context)


def test_get_session_context_is_unimplemented(service, mock_servicer_context):
    request = context_pb2.GetSessionContextRequest(session_id="s1", max_entries=10)
    with pytest.raises(NotImplementedError):
        service.GetSessionContext(request, mock_servicer_context)
