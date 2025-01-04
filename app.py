from fastapi import FastAPI
from routes.user_routes import router as users_routes;
from routes.health_routes import router as health_routes;
from util.tags_metadata import tags_metadata;

app = FastAPI(
    title="CRUD Backend",
    description="This service is responsible for providing CRUD functionality to the main app",
    openapi_tags= tags_metadata,
)

app.include_router(users_routes, prefix='/users', tags=["User operations"]); 
app.include_router(health_routes, prefix='/health', tags=["Health Check"])
