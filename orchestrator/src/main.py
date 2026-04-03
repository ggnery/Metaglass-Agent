import sys
import os
from concurrent import futures
from logging import basicConfig, getLogger, INFO

import grpc

# Ensure the project root is in the path so `generated` is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from generated import orchestrator_pb2_grpc, session_pb2_grpc, context_pb2_grpc
from services.orchestrator_service import OrchestratorServiceServicer
from services.session_service import SessionServiceServicer
from services.context_service import ContextServiceServicer

basicConfig(level=INFO)
logger = getLogger(__name__)

GRPC_PORT = os.getenv("GRPC_PORT", "50051")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    orchestrator_pb2_grpc.add_OrchestratorServiceServicer_to_server(
        OrchestratorServiceServicer(), server
    )
    session_pb2_grpc.add_SessionServiceServicer_to_server(
        SessionServiceServicer(), server
    )
    context_pb2_grpc.add_ContextServiceServicer_to_server(
        ContextServiceServicer(), server
    )

    # Enable gRPC reflection so grpcurl can discover services
    from grpc_reflection.v1alpha import reflection
    from generated import common_pb2, orchestrator_pb2, session_pb2, context_pb2

    service_names = (
        orchestrator_pb2.DESCRIPTOR.services_by_name["OrchestratorService"].full_name,
        session_pb2.DESCRIPTOR.services_by_name["SessionService"].full_name,
        context_pb2.DESCRIPTOR.services_by_name["ContextService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    logger.info("gRPC server starting on port %s", GRPC_PORT)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
