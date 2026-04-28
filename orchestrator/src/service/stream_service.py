from collections.abc import Callable

from qdrant_client import QdrantClient
from sqlalchemy.orm import Session


class StreamService:
    def __init__(self, db_factory: Callable[[], Session], qdrant: QdrantClient) -> None:
        self.db_factory = db_factory
        self.qdrant = qdrant
