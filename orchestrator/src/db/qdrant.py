import os

from qdrant_client import QdrantClient

QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_GRPC_PORT: int = int(os.getenv("QDRANT_GRPC_PORT", "6334"))

qdrant_client: QdrantClient = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
    grpc_port=QDRANT_GRPC_PORT,
    prefer_grpc=True,
)
