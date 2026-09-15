from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import DATABASE_PATH
from src.database.seed_data import seed_database
from src.api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure database is seeded if running for the first time."""
    if not DATABASE_PATH.exists():
        print(f"[*] Database not found at {DATABASE_PATH}. Seeding fresh database...")
        seed_database()
    else:
        print(f"[+] Connected to existing database at {DATABASE_PATH}")
    yield

app = FastAPI(
    title="Enterprise AI Workflow Agent API",
    description=(
        "Production backend for the Enterprise AI Workflow Agent. "
        "Provides structured endpoints for Products, Orders, Returns, and a direct Database Tool interface."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Enable CORS for cross-origin orchestration (e.g. n8n, frontend dashboards)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 router
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["System"])
def root():
    return {
        "service": "Enterprise AI Workflow Agent API",
        "status": "running",
        "documentation": "/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "products": "/api/v1/products",
            "orders": "/api/v1/orders/{order_id}",
            "returns_summary": "/api/v1/returns/summary",
            "database_query": "/api/v1/database/query",
            "database_schema": "/api/v1/database/schema",
        }
    }
