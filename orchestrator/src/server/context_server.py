from collections.abc import Callable

import grpc
from generated import context_pb2, context_pb2_grpc
from qdrant_client import QdrantClient
from sqlalchemy.orm import Session


class ContextServer(context_pb2_grpc.ContextServicer):
    def __init__(
        self,
        db_factory: Callable[[], Session],
        qdrant: QdrantClient,
    ) -> None:
        self._db = db_factory
        self._qdrant = qdrant

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
