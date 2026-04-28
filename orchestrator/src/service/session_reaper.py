import logging
import threading
import time
from collections.abc import Callable

from qdrant_client import QdrantClient
from sqlalchemy.orm import Session

from config import Config
from service.session_service import SessionService

logger = logging.getLogger(__name__)


class SessionReaper:
    def __init__(
        self,
        db_factory: Callable[[], Session],
        qdrant: QdrantClient,
    ) -> None:
        self.session_service = SessionService(db_factory, qdrant)
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        logger.info("Starting SessionReaper...")
        self._thread.start()

    def stop(self) -> None:
        logger.info("Stopping SessionReaper...")
        self._stop_event.set()
        self._thread.join()

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                reaped_to_lost, reaped_to_closed = self.session_service.reap_sessions(
                    active_timeout_seconds=Config.ACTIVE_SESSION_TIMEOUT_SECONDS,
                    lost_timeout_seconds=Config.LOST_SESSION_TIMEOUT_SECONDS,
                )
                if reaped_to_lost > 0 or reaped_to_closed > 0:
                    logger.info(
                        "SessionReaper: Reaped %d to lost, %d to closed",
                        reaped_to_lost,
                        reaped_to_closed,
                    )
            except Exception as e:
                logger.error("SessionReaper error: %s", str(e))

            # Wait for X seconds, but check stop_event periodically
            # to allow faster shutdown
            wait_remaining = Config.REAPER_INTERVAL_SECONDS
            while wait_remaining > 0 and not self._stop_event.is_set():
                sleep_time = min(1.0, wait_remaining)
                time.sleep(sleep_time)
                wait_remaining -= sleep_time
