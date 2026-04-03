from collections.abc import Callable

import grpc
from generated import context_pb2, context_pb2_grpc
from sqlalchemy.orm import Session


class ContextServiceServicer(context_pb2_grpc.ContextServiceServicer):
    def __init__(self, db_factory: Callable[[], Session]) -> None:
        self._db = db_factory

    def SemanticSearch(
        self,
        request: context_pb2.SemanticSearchRequest,
        context: grpc.ServicerContext,
    ) -> context_pb2.SemanticSearchResponse:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("SemanticSearch not implemented")
        raise NotImplementedError("SemanticSearch not implemented")

    def PushContext(
        self,
        request: context_pb2.PushContextRequest,
        context: grpc.ServicerContext,
    ) -> context_pb2.PushContextResponse:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("PushContext not implemented")
        raise NotImplementedError("PushContext not implemented")

    def GetSessionContext(
        self,
        request: context_pb2.GetSessionContextRequest,
        context: grpc.ServicerContext,
    ) -> context_pb2.GetSessionContextResponse:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("GetSessionContext not implemented")
        raise NotImplementedError("GetSessionContext not implemented")
