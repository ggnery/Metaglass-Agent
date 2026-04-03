from collections.abc import Callable

import grpc
from generated import session_pb2, session_pb2_grpc
from sqlalchemy.orm import Session


class SessionServiceServicer(session_pb2_grpc.SessionServiceServicer):
    def __init__(self, db_factory: Callable[[], Session]) -> None:
        self._db = db_factory

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
