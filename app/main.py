import logging
import logging.handlers
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import engine, Base
from .routers import addresses
from .config import settings

# ── Logging setup ────────────────────────────────────────────────
LOG_DIR  = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

# Formatter — same format for both handlers
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Handler 1 — Terminal (console)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Handler 2 — Rotating log file (max 5MB, keeps last 3 files)
file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)

# Root logger
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    handlers=[console_handler, file_handler]
)

logger = logging.getLogger(__name__)
# ── End logging setup ─────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up.")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created / verified.")
    yield
    logger.info("Application shutdown.")


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.include_router(addresses.router)
