from fastapi import APIRouter, Query, Depends, HTTPException
from app.services import get_data, get_csv_data
from app.auth import oauth2_scheme, verify_token

router = APIRouter()

# Rotas protegidas que requerem autenticação JWT
@router.get("/producao")
def producao(year: int = Query(None, ge=1970, le=2024), token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_data("producao", year)

@router.get("/processamento")
def processamento(year: int = Query(None, ge=1970, le=2024), token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_data("processamento", year)

@router.get("/comercializacao")
def comercializacao(year: int = Query(None, ge=1970, le=2024), token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_data("comercializacao", year)

@router.get("/importacao")
def importacao(year: int = Query(None, ge=1970, le=2024), token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_data("importacao", year)

@router.get("/exportacao")
def exportacao(year: int = Query(None, ge=1970, le=2024), token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_data("exportacao", year)

# Rotas para os arquivos CSV, também protegidas por autenticação JWT
@router.get("/csv/producao")
def producao_csv(token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_csv_data("producao")

@router.get("/csv/processamento")
def processamento_csv(token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_csv_data("processamento")

@router.get("/csv/comercializacao")
def comercializacao_csv(token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_csv_data("comercializacao")

@router.get("/csv/importacao")
def importacao_csv(token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_csv_data("importacao")

@router.get("/csv/exportacao")
def exportacao_csv(token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_csv_data("exportacao")