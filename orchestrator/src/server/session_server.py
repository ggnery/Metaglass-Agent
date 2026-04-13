from collections.abc import Callable
from typing import cast

import grpc
from generated import common_pb2, session_pb2, session_pb2_grpc
from qdrant_client import QdrantClient
from sqlalchemy.orm import Session

from db import models
from service.session_service import SessionService

# Map database enum to gRPC enum
_STATE_MAP = {
    models.SessionState.active: common_pb2.SessionState.SESSION_STATE_ACTIVE,
    models.SessionState.lost: common_pb2.SessionState.SESSION_STATE_LOST,
    models.SessionState.closed: common_pb2.SessionState.SESSION_STATE_CLOSED,
}


class SessionServer(session_pb2_grpc.SessionServicer):
    def __init__(
        self,
        db_factory: Callable[[], Session],
        qdrant: QdrantClient,
    ) -> None:
        self.session_service = SessionService(db_factory, qdrant)

    def RegisterDevice(
        self,
        request: session_pb2.RegisterDeviceRequest,
        context: grpc.ServicerContext,
    ) -> session_pb2.RegisterDeviceResponse:
        try:
            device = self.session_service.register_device(
                device_name=request.device_name or None,
                device_model=request.device_model or None,
                metadata=dict(request.metadata),
            )

            return session_pb2.RegisterDeviceResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_OK,
                    message="Device registered successfully",
                ),
                device_id=str(device.id),
            )
        except Exception as e:
            return session_pb2.RegisterDeviceResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_ERROR,
                    message=f"Error registering device: {str(e)}",
                )
            )

    def CreateUser(
        self,
        request: session_pb2.CreateUserRequest,
        context: grpc.ServicerContext,
    ) -> session_pb2.CreateUserResponse:
        try:
            user = self.session_service.create_user(
                name=request.name or None,
                email=request.email or None,
                preferred_language=request.preferred_language or "pt-BR",
                device_id=request.device_id or None,
                metadata=dict(request.metadata),
            )

            return session_pb2.CreateUserResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_OK,
                    message="User created successfully",
                ),
                user_id=str(user.id),
            )
        except Exception as e:
            return session_pb2.CreateUserResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_ERROR,
                    message=f"Error creating user: {str(e)}",
                )
            )

    def CreateSession(
        self,
        request: session_pb2.CreateSessionRequest,
        context: grpc.ServicerContext,
    ) -> session_pb2.CreateSessionResponse:
        try:
            session = self.session_service.create_session(
                user_id=request.user_id,
                device_id=request.device_id or None,
                initial_metadata=dict(request.initial_metadata),
            )

            return session_pb2.CreateSessionResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_OK,
                    message="Session created successfully",
                ),
                session_id=str(session.id),
            )
        except Exception as e:
            return session_pb2.CreateSessionResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_ERROR,
                    message=f"Error creating session: {str(e)}",
                )
            )

    def Heartbeat(
        self,
        request: session_pb2.HeartbeatRequest,
        context: grpc.ServicerContext,
    ) -> session_pb2.HeartbeatResponse:
        try:
            success = self.session_service.heartbeat(request.session_id)
            if not success:
                return session_pb2.HeartbeatResponse(
                    status=common_pb2.Status(
                        code=common_pb2.StatusCode.STATUS_CODE_ERROR,
                        message=f"Session not found or closed: {request.session_id}",
                    )
                )

            return session_pb2.HeartbeatResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_OK,
                    message="Heartbeat received",
                )
            )
        except Exception as e:
            return session_pb2.HeartbeatResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_ERROR,
                    message=f"Error processing heartbeat: {str(e)}",
                )
            )

    def EndSession(
        self,
        request: session_pb2.EndSessionRequest,
        context: grpc.ServicerContext,
    ) -> session_pb2.EndSessionResponse:
        try:
            success = self.session_service.end_session(request.session_id)
            if not success:
                return session_pb2.EndSessionResponse(
                    status=common_pb2.Status(
                        code=common_pb2.StatusCode.STATUS_CODE_ERROR,
                        message=f"Session closed or not found: {request.session_id}",
                    )
                )

            return session_pb2.EndSessionResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_OK,
                    message="Session ended successfully",
                )
            )
        except Exception as e:
            return session_pb2.EndSessionResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_ERROR,
                    message=f"Error ending session: {str(e)}",
                )
            )

    def GetSession(
        self,
        request: session_pb2.GetSessionRequest,
        context: grpc.ServicerContext,
    ) -> session_pb2.GetSessionResponse:
        try:
            session = self.session_service.get_session(request.session_id)
            if not session:
                return session_pb2.GetSessionResponse(
                    status=common_pb2.Status(
                        code=common_pb2.StatusCode.STATUS_CODE_ERROR,
                        message=f"Session not found: {request.session_id}",
                    )
                )

            # Explicitly cast session.state to satisfy type checker
            state_enum = cast(models.SessionState, session.state)
            grpc_state = _STATE_MAP.get(
                state_enum, common_pb2.SessionState.SESSION_STATE_UNSPECIFIED
            )

            return session_pb2.GetSessionResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_OK,
                    message="Session retrieved successfully",
                ),
                session_id=str(session.id),
                user_id=str(session.user_id),
                state=grpc_state,
            )
        except Exception as e:
            return session_pb2.GetSessionResponse(
                status=common_pb2.Status(
                    code=common_pb2.StatusCode.STATUS_CODE_ERROR,
                    message=f"Error retrieving session: {str(e)}",
                )
            )
