from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import status

app = FastAPI(
    title="API de Trending Topics",
    description="API para consulta de tópicos populares, com cache e filtros",
    version="1.0.0",
)

origins = [
    "http://localhost",  
    "http://localhost:3000",  
    "https://meuapp.com",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.get("/", summary="Rota principal de teste")
async def root():
    return JSONResponse(content={"message": "Teste prático nouslatam backend"}, status_code=status.HTTP_200_OK)
