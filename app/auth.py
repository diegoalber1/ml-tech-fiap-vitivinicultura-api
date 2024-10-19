from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt

# Chave secreta para assinar os tokens JWT
SECRET_KEY = "e9b1f8a9c8f4e2b7a1d9f8e7c6b5a4d3e2f1c0b9a8d7e6f5c4b3a2f1e0d9c8b7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer é o esquema de autenticação que espera um token JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def create_access_token(data: dict):
    """Função para criar um token JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Função para verificar e decodificar o token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint para login e geração de token"""
    # Aqui você pode validar o usuário e senha (exemplo simples)
    if form_data.username == "fiap" and form_data.password == "mltech":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    """Endpoint protegido que requer um token JWT válido"""
    payload = verify_token(token)
    return {"username": payload.get("sub")}