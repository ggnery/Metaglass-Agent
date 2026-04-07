import os
import sys
from concurrent import futures
from logging import INFO, basicConfig, getLogger

import grpc
from qdrant_client import QdrantClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

# Ensure the project root is in the path so `generated` is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from generated import context_pb2_grpc, orchestrator_pb2_grpc, session_pb2_grpc

from config import Config
from server.context_server import ContextServer
from server.orchestrator_server import OrchestratorServer
from server.session_server import SessionServer

basicConfig(level=INFO)
logger = getLogger(__name__)


def main() -> None:
    engine: Engine = create_engine(Config.DATABASE_URL, pool_pre_ping=True)
    SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine)

    qdrant_client: QdrantClient = QdrantClient(
        host=Config.QDRANT_HOST,
        port=Config.QDRANT_PORT,
        grpc_port=Config.QDRANT_GRPC_PORT,
        prefer_grpc=True,
    )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    orchestrator_pb2_grpc.add_OrchestratorServicer_to_server(
        OrchestratorServer(db_factory=SessionLocal, qdrant=qdrant_client),
        server,
    )
    session_pb2_grpc.add_SessionServicer_to_server(
        SessionServer(db_factory=SessionLocal, qdrant=qdrant_client),
        server,
    )
    context_pb2_grpc.add_ContextServicer_to_server(
        ContextServer(db_factory=SessionLocal, qdrant=qdrant_client),
        server,
    )

    # Enable gRPC reflection so grpcurl can discover services
    from generated import context_pb2, orchestrator_pb2, session_pb2
    from grpc_reflection.v1alpha import reflection

    service_names = (
        orchestrator_pb2.DESCRIPTOR.services_by_name["Orchestrator"].full_name,
        session_pb2.DESCRIPTOR.services_by_name["Session"].full_name,
        context_pb2.DESCRIPTOR.services_by_name["Context"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    # Verify connectivity before accepting requests
    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1")
    logger.info("Database connection verified")

    qdrant_client.get_collections()
    logger.info("Qdrant connection verified")

    server.add_insecure_port(f"[::]:{Config.GRPC_PORT}")
    logger.info("gRPC server starting on port %s", Config.GRPC_PORT)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
