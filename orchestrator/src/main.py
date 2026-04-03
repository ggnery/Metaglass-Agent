import os
import sys
from concurrent import futures
from logging import INFO, basicConfig, getLogger

import grpc

# Ensure the project root is in the path so `generated` is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from generated import context_pb2_grpc, orchestrator_pb2_grpc, session_pb2_grpc

from db.postgres import SessionLocal, engine
from db.qdrant import qdrant_client
from services.context_service import ContextServiceServicer
from services.orchestrator_service import OrchestratorServiceServicer
from services.session_service import SessionServiceServicer

basicConfig(level=INFO)
logger = getLogger(__name__)

GRPC_PORT = os.getenv("GRPC_PORT", "50051")


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    orchestrator_pb2_grpc.add_OrchestratorServiceServicer_to_server(
        OrchestratorServiceServicer(db_factory=SessionLocal, qdrant=qdrant_client),
        server,
    )
    session_pb2_grpc.add_SessionServiceServicer_to_server(
        SessionServiceServicer(db_factory=SessionLocal, qdrant=qdrant_client),
        server,
    )
    context_pb2_grpc.add_ContextServiceServicer_to_server(
        ContextServiceServicer(db_factory=SessionLocal, qdrant=qdrant_client),
        server,
    )

    # Enable gRPC reflection so grpcurl can discover services
    from generated import context_pb2, orchestrator_pb2, session_pb2
    from grpc_reflection.v1alpha import reflection

    service_names = (
        orchestrator_pb2.DESCRIPTOR.services_by_name["OrchestratorService"].full_name,
        session_pb2.DESCRIPTOR.services_by_name["SessionService"].full_name,
        context_pb2.DESCRIPTOR.services_by_name["ContextService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    # Verify connectivity before accepting requests
    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1")
    logger.info("Database connection verified")

    qdrant_client.get_collections()
    logger.info("Qdrant connection verified")

    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    logger.info("gRPC server starting on port %s", GRPC_PORT)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
