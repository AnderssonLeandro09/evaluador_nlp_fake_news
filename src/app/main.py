from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .api.routes import router as api_router
from .db.models import init_db
from .core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Iniciar base de datos al arrancar
@app.on_event("startup")
async def startup_event():
    init_db()

# Incluir rutas de la API
app.include_router(api_router, prefix="/api/v1")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="src/app/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("src/app/static/index.html")

@app.get("/health")
async def health_check():
    from datetime import datetime
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
