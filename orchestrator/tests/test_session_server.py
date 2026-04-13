import pytest
from unittest.mock import MagicMock

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


def test_create_session(service, mock_servicer_context):
    request = session_pb2.CreateSessionRequest(
        user_id="00000000-0000-0000-0000-000000000000",
        device_id="00000000-0000-0000-0000-000000000000",
        initial_metadata={"lang": "en"},
    )
    
    # Mocking create_session
    mock_session = MagicMock()
    mock_session.id = "11111111-1111-1111-1111-111111111111"
    service.session_service.create_session = MagicMock(return_value=mock_session)
    
    response = service.CreateSession(request, mock_servicer_context)
    assert response.status.code == 1  # STATUS_CODE_OK
    assert response.session_id == str(mock_session.id)


def test_heartbeat(service, mock_servicer_context):
    request = session_pb2.HeartbeatRequest(
        session_id="00000000-0000-0000-0000-000000000000",
        timestamp_ms=1000,
    )

    # Test success (covers active and lost -> active resurrection)
    service.session_service.heartbeat = lambda sid: True
    response = service.Heartbeat(request, mock_servicer_context)
    assert response.status.code == 1  # STATUS_CODE_OK
    assert response.status.message == "Heartbeat received"

    # Test failure (not found or closed)
    service.session_service.heartbeat = lambda sid: False
    response = service.Heartbeat(request, mock_servicer_context)
    assert response.status.code == 2  # STATUS_CODE_ERROR
    assert "Session not found or closed" in response.status.message


def test_end_session(service, mock_servicer_context):
    request = session_pb2.EndSessionRequest(
        session_id="00000000-0000-0000-0000-000000000000"
    )

    # Test success
    service.session_service.end_session = lambda sid: True
    response = service.EndSession(request, mock_servicer_context)
    assert response.status.code == 1  # STATUS_CODE_OK
    assert response.status.message == "Session ended successfully"

    # Test failure
    service.session_service.end_session = lambda sid: False
    response = service.EndSession(request, mock_servicer_context)
    assert response.status.code == 2  # STATUS_CODE_ERROR
    assert "Session closed or not found" in response.status.message


def test_get_session(service, mock_servicer_context):
    request = session_pb2.GetSessionRequest(
        session_id="00000000-0000-0000-0000-000000000000"
    )

    # Mock success
    mock_session = MagicMock()
    mock_session.id = "00000000-0000-0000-0000-000000000000"
    mock_session.user_id = "11111111-1111-1111-1111-111111111111"
    from db.models import SessionState
    mock_session.state = SessionState.active
    service.session_service.get_session = lambda sid: mock_session

    response = service.GetSession(request, mock_servicer_context)
    assert response.status.code == 1  # STATUS_CODE_OK
    assert response.session_id == str(mock_session.id)
    assert response.user_id == str(mock_session.user_id)
    assert response.state == 1  # SESSION_STATE_ACTIVE

    # Test failure
    service.session_service.get_session = lambda sid: None
    response = service.GetSession(request, mock_servicer_context)
    assert response.status.code == 2  # STATUS_CODE_ERROR
    assert "Session not found" in response.status.message
