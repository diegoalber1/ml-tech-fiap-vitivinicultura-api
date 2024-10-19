# Vitivinicultura API

Bem-vindo à **Vitivinicultura API**. Esta API fornece acesso a dados relacionados à produção, processamento, comercialização, importação e exportação de vinhos. É uma ferramenta útil para profissionais da indústria vitivinícola, pesquisadores e entusiastas que desejam obter informações detalhadas sobre o setor.

## **Índice**
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Autenticação](#autenticação)
- [Endpoints](#endpoints)
- [Testes](#testes)
- [Deploy](#deploy)
- [Monitoramento](#monitoramento)
- [Arquitetura](#Arquitetura)
- [Licença](#licença)

---

## **Funcionalidades**
- Consultar dados históricos e em tempo real sobre vitivinicultura.
- Monitorar a produção de vinhos no Brasil.
- Utilizar dados para alimentar modelos de previsão de demanda.
- Acessar informações detalhadas sobre a comercialização e exportação de vinhos.

---

## **Tecnologias Utilizadas**
- **FastAPI**: Framework de alto desempenho para construção de APIs em Python.
- **JWT (JSON Web Tokens)**: Utilizado para autenticação segura.
- **Heroku**: Plataforma de deploy em nuvem.
- **Python 3.12+**: Linguagem de programação utilizada no desenvolvimento da API.

---

## **Pré-requisitos**
Antes de começar, certifique-se de ter os seguintes pré-requisitos instalados em sua máquina:

- **Python 3.12+**: [Instalar Python](https://www.python.org/downloads/)
- **Git**: [Instalar Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- **Heroku CLI** (caso deseje realizar o deploy no Heroku): [Instalar Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

---

## **Instalação**

### **Passo a passo para Instalação Local**
1. Clone o repositório:
```bash
   git clone https://github.com/diegoalber1/vitivinicultura-api.git
   cd vitivinicultura-api
```
2. Crie e ative um ambiente virtual:
```bash
   python3 -m venv venv
   source venv/bin/activate
```   
3. Instale as dependências:
```bash
   pip install -r requirements.txt
```   
4. Configure as variáveis de ambiente:
```bash
   cp .env.example .env
```   
5. Execute a aplicação localmente:
```bash
   uvicorn main:app --reload
```   
Agora, a API estará rodando localmente no endereço http://127.0.0.1:8000.

## **Configuração**

### **Variáveis de Ambiente**
Certifique-se de configurar as seguintes variáveis de ambiente no arquivo `.env`:


- `SECRET_KEY`: Chave secreta para geração de tokens JWT.
- `ALGORITHM`: Algoritmo utilizado para assinar os tokens JWT (ex: HS256).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tempo de expiração do token de acesso.
- `DEBUG`: Define se o modo de depuração está ativado (True/False).

Exemplo de arquivo `.env`:

```bash
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

## **Uso**

### **Autenticação**
A API utiliza **JWT (JSON Web Tokens)** para autenticação. Para acessar os endpoints protegidos, você precisa obter um token de acesso.

1. **Obter o Token de Acesso (Login)**:
```bash
   curl -X 'POST' \
   'http://localhost:8000/token' \
   -H 'Content-Type: application/x-www-form-urlencoded' \
   -d 'username=seu_usuario&password=sua_senha'
```

2. **Acessar o Endpoint Protegido**:

```bash
   curl -X 'GET' \
   'http://localhost:8000/users/me' \
   -H 'Authorization: Bearer seu_token_jwt_aqui'
```
Substitua seu_token_jwt_aqui pelo token JWT que você obteve no passo anterior.

**Fluxo de Autenticação**:

. O cliente envia uma requisição de login com as credenciais para o endpoint `/token`.\
. A API valida as credenciais e, se forem válidas, gera um token JWT.\
. O cliente usa o token JWT para acessar os endpoints protegidos.\ 
. A API valida o token JWT em cada requisição protegida.\
. Se o token for válido, a API permite o acesso ao recurso solicitado. Caso contrário, retorna um erro de autenticação.

## **Endpoints**

GET /dados/producao: Retorna dados de produção de vitivinicultura.\
GET /dados/processamento: Retorna dados de processamento de vitivinicultura.\
GET /dados/comercializacao: Retorna dados de comercialização de vitivinicultura.\
GET /dados/importacao: Retorna dados de importação de vitivinicultura.\
GET /dados/exportacao: Retorna dados de exportação de vitivinicultura.

## **Testes**

### **Executar Testes**
Para garantir que tudo está funcionando corretamente, você pode executar os testes automatizados:

1. **Instale as dependências de teste:**:
```bash
   pip install -r requirements-test.txt
```

2. **Execute os testes:**:

```bash
   pytest
```

## **Deploy**

### **Deploy no Heroku**
1. **Crie uma conta no Heroku (se ainda não tiver) e instale o Heroku CLI.**:

2. **Faça login no Heroku:**:
```bash
   heroku login
```
3. **Crie um novo app no Heroku:**:

```bash
   heroku create vitivinicultura-api   
```
4. **Configure as variáveis de ambiente no Heroku:**:

```bash
   heroku config:set SECRET_KEY=<sua_secret_key>
```
5. **Faça o deploy da aplicação:**:

```bash
   git push heroku main 
```
6. **Escale a aplicação:**:

```bash
   heroku ps:scale web=1  
```
7. **Acesse a aplicação:**:

```bash
   heroku open
```

## **Monitoramento**

### **Heroku Metrics**

O Heroku oferece métricas integradas para monitorar o desempenho da aplicação, como uso de CPU, memória e tempo de resposta. Essas métricas podem ser acessadas diretamente no painel do Heroku.

### **Heroku Logs**

Para visualizar os logs da aplicação, utilize o seguinte comando:

```bash
   heroku logs --tail
```

## Arquitetura
### Diagrama de Arquitetura
```plaintext
+-------------------+        +-------------------+        +-------------------+
|                   |        |                   |        |                   |
|   Ingestão de     |        |   API Backend     |        |   Banco de Dados  |
|   Dados (Embrapa) | -----> |   (FastAPI)       | -----> |   (PostgreSQL)    |
|                   |        |                   |        |                   |
+-------------------+        +-------------------+        +-------------------+
        |                           |
        v                           v
+-------------------+        +-------------------+
|                   |        |                   |
|   Pipeline de     |        |   Monitoramento   |
|   Machine Learning|        |   (Prometheus,    |
|   (Previsão de    |        |   Grafana)        |
|   Demanda)        |        |                   |
|                   |        |                   |
+-------------------+        +-------------------+

```

## Licença 

Este projeto está licenciado sob a Licença MIT. Isso significa que você pode usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do software, desde que mantenha o aviso de copyright original. Leia o arquivo [LICENSE](./LICENSE) para mais detalhes. --- MIT License Copyright (c) [2024] [Diego Alberone Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.