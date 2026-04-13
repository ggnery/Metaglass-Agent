import pytest

from generated import session_pb2
from server.session_server import SessionServer


@pytest.fixture
def service(mock_db_factory, mock_qdrant):
    return SessionServer(db_factory=mock_db_factory, qdrant=mock_qdrant)


def test_create_user_is_unimplemented(service, mock_servicer_context):
    request = session_pb2.CreateUserRequest(
        name="John Doe",
        email="john@example.com",
        preferred_language="pt-BR",
        device_id="00000000-0000-0000-0000-000000000000",
        metadata={"key": "value"},
    )
    with pytest.raises(NotImplementedError):
        service.CreateUser(request, mock_servicer_context)


def test_create_session_is_unimplemented(service, mock_servicer_context):
    request = session_pb2.CreateSessionRequest(user_id="u1", device_id="d1")
    with pytest.raises(NotImplementedError):
        service.CreateSession(request, mock_servicer_context)


def test_heartbeat_is_unimplemented(service, mock_servicer_context):
    request = session_pb2.HeartbeatRequest(session_id="s1", timestamp_ms=1000)
    with pytest.raises(NotImplementedError):
        service.Heartbeat(request, mock_servicer_context)


def test_end_session_is_unimplemented(service, mock_servicer_context):
    request = session_pb2.EndSessionRequest(session_id="s1")
    with pytest.raises(NotImplementedError):
        service.EndSession(request, mock_servicer_context)


def test_get_session_is_unimplemented(service, mock_servicer_context):
    request = session_pb2.GetSessionRequest(session_id="s1")
    with pytest.raises(NotImplementedError):
        service.GetSession(request, mock_servicer_context)
