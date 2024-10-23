from fastapi import FastAPI
from app.routes import router as api_router
from app.auth import router as auth_router

app = FastAPI(
    title="Vitivinicultura API",
    description="API para consulta de dados de vitivinicultura da Embrapa",
    version="1.0.0"
)

# Inclui as rotas da API
app.include_router(api_router)
app.include_router(auth_router)

# Endpoint básico para verificar se a API está funcionando
@app.get("/")
async def root():
    return {"message": "Bem-vindo à RM358672-fiap-vitivinicultura-api- TECH CHALLENGE!"}