import pytest

from generated import session_pb2
from server.session_server import SessionServer


@pytest.fixture
def service(mock_db_factory, mock_qdrant):
    return SessionServer(db_factory=mock_db_factory, qdrant=mock_qdrant)


def test_register_device(service, mock_servicer_context):
    request = session_pb2.RegisterDeviceRequest(
        device_name="Ray-Ban Meta",
        device_model="V1",
        metadata={"firmware": "1.0.0"},
    )
    response = service.RegisterDevice(request, mock_servicer_context)
    assert response.status.code == 1  # STATUS_CODE_OK
    assert response.status.message == "Device registered successfully"
    assert response.device_id is not None


def test_create_user(service, mock_servicer_context):
    request = session_pb2.CreateUserRequest(
        name="John Doe",
        email="john@example.com",
        preferred_language="pt-BR",
        device_id="00000000-0000-0000-0000-000000000000",
        metadata={"key": "value"},
    )
    # The method should now return a success response
    response = service.CreateUser(request, mock_servicer_context)
    assert response.status.code == 1  # STATUS_CODE_OK
    assert response.status.message == "User created successfully"
    assert response.user_id is not None


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
