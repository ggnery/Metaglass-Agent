from collections.abc import Callable

import grpc
from generated import common_pb2, session_pb2, session_pb2_grpc
from qdrant_client import QdrantClient
from sqlalchemy.orm import Session

from service.session_service import SessionService


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
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("CreateSession not implemented")
        raise NotImplementedError("CreateSession not implemented")

    def Heartbeat(
        self,
        request: session_pb2.HeartbeatRequest,
        context: grpc.ServicerContext,
    ) -> session_pb2.HeartbeatResponse:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Heartbeat not implemented")
        raise NotImplementedError("Heartbeat not implemented")

    def EndSession(
        self,
        request: session_pb2.EndSessionRequest,
        context: grpc.ServicerContext,
    ) -> session_pb2.EndSessionResponse:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("EndSession not implemented")
        raise NotImplementedError("EndSession not implemented")

    def GetSession(
        self,
        request: session_pb2.GetSessionRequest,
        context: grpc.ServicerContext,
    ) -> session_pb2.GetSessionResponse:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("GetSession not implemented")
        raise NotImplementedError("GetSession not implemented")
