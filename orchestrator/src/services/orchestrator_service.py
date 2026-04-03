from collections.abc import Callable, Iterator

import grpc
from generated import orchestrator_pb2, orchestrator_pb2_grpc
from qdrant_client import QdrantClient
from sqlalchemy.orm import Session


class OrchestratorServiceServicer(
    orchestrator_pb2_grpc.OrchestratorServiceServicer,
):
    def __init__(
        self,
        db_factory: Callable[[], Session],
        qdrant: QdrantClient,
    ) -> None:
        self._db = db_factory
        self._qdrant = qdrant

    def Query(
        self,
        request: orchestrator_pb2.QueryRequest,
        context: grpc.ServicerContext,
    ) -> orchestrator_pb2.QueryResponse:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Query not implemented")
        raise NotImplementedError("Query not implemented")

    def QueryStream(
        self,
        request: orchestrator_pb2.QueryRequest,
        context: grpc.ServicerContext,
    ) -> Iterator[orchestrator_pb2.QueryResponse]:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("QueryStream not implemented")
        raise NotImplementedError("QueryStream not implemented")

    def StreamQuery(
        self,
        request_iterator: Iterator[orchestrator_pb2.QueryRequest],
        context: grpc.ServicerContext,
    ) -> Iterator[orchestrator_pb2.QueryResponse]:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("StreamQuery not implemented")
        raise NotImplementedError("StreamQuery not implemented")
