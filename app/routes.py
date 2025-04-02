from fastapi import APIRouter, Query, Depends, HTTPException
from app.services import get_data, get_csv_data
from app.auth import oauth2_scheme, verify_token
from app.services import fetch_and_save_producao, fetch_and_save_exportacao, exportacao_predict_wrapper

router = APIRouter()

# Rotas protegidas que requerem autenticação JWT
@router.get("/producao")
def producao(year: int = Query(None, ge=1970, le=2024), token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    # return get_data("producao", year)
    return fetch_and_save_producao(year)

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
    return fetch_and_save_exportacao(year)



@router.get("/exportacao/predict")
def exportacao_predict(
    year: int = Query(..., ge=2024, le=2100),  # O parâmetro `year` agora é obrigatório
    country: str = Query(...),  # O parâmetro `country` também é obrigatório
    token: str = Depends(oauth2_scheme)  # Token JWT para autenticação
):
    # Verifica o token JWT
    verify_token(token)
    
    # Chama a lógica de previsão
    return exportacao_predict_wrapper(year, country)

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
    
@router.get("/csv/exportacao")
def exportacao_csv(token: str = Depends(oauth2_scheme)):
    # Verifica o token JWT
    verify_token(token)
    return get_csv_data("exportacao")