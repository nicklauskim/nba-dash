from fastapi import FastAPI
from backend.api.routes import router


# Initialize FastAPI application and register the router for API endpoints
app = FastAPI()
# Register the route from routes.py under the /api path
app.include_router(router, prefix="/api")