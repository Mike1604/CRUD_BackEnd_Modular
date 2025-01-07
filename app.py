from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user_routes import router as users_routes;
from routes.health_routes import router as health_routes;
from util.tags_metadata import tags_metadata;

origins = [
    "http://localhost:5173",
]

app = FastAPI(
    title="CRUD Backend",
    description="This service is responsible for providing CRUD functionality to the main app",
    openapi_tags= tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(users_routes, prefix='/users', tags=["User operations"]); 
app.include_router(health_routes, prefix='/health', tags=["Health Check"])
