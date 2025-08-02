from services.reddit_service import RedditService, RedditAPIError, RedditAuthenticationError, RedditRateLimitError, SubredditNotFound
from services.elasticsearch_service import ElasticsearchService
from fastapi import FastAPI, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models.post_model import PostListResponse
from cache.cache_handler import CacheHandler
from fastapi.responses import JSONResponse
from typing import List, Dict
from typing import Optional
import os
import logging
from loggers.log_handler import setup_logger  

logger = setup_logger()

REDDIT_ACCESS_TOKEN = os.getenv("REDDIT_ACCESS_TOKEN")

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
    logger.info("Rota '/' acessada com sucesso.")
    return JSONResponse(content={"message": "Teste prático nouslatam backend"}, status_code=status.HTTP_200_OK)

@app.get("/posts/{subreddit}", response_model=PostListResponse)
async def get_posts(
    subreddit: str,
    period: Optional[str] = Query("day", enum=["hour", "day", "week", "month", "year", "all"]),
    limit: Optional[int] = Query(10, ge=1, le=100), 
    sort_type: Optional[str] = Query("hot", enum=["hot", "new", "top", "rising"]) 
):
    logger.info(f"Rota '/posts/{subreddit}' acessada com params: period={period}, limit={limit}, sort_type={sort_type}")
    
    cache_key = f"reddit_posts_{subreddit}_{period}_{limit}_{sort_type}"
    logger.debug(f"Tentando recuperar cache com chave: {cache_key}")

    cached_posts = CacheHandler.get_cache(cache_key)
    
    if cached_posts:
        logger.info("Cache HIT - Dados encontrados no cache.")
        return {
            "posts": cached_posts,
            "origin": "cache",
            "cache_status": "hit"
        }

    logger.info("Cache MISS - Buscando dados no Reddit.")

    try:
        posts = await RedditService.fetch_posts(
            subreddit=subreddit, 
            token=REDDIT_ACCESS_TOKEN, 
            period=period, 
            limit=limit,
            sort_type=sort_type
        )
        logger.info(f"{len(posts)} posts obtidos da API do Reddit.")

        CacheHandler.set_cache(cache_key, posts)
        logger.debug("Dados armazenados no cache com sucesso.")

        return {
            "posts": posts,
            "origin": "api",
            "cache_status": "miss"
        }

    except SubredditNotFound as e:
        logger.warning(f"Subreddit '{subreddit}' não encontrado: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except RedditAuthenticationError as e:
        logger.error(f"Erro de autenticação com o Reddit: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    except RedditRateLimitError as e:
        logger.warning(f"Limite de requisições atingido no Reddit: {e}")
        raise HTTPException(status_code=429, detail=str(e))
    except RedditAPIError as e:
        logger.error(f"Erro genérico da API do Reddit: {e}")
        raise HTTPException(status_code=e.status_code or 500, detail=str(e))
    except Exception as e:
        logger.exception("Erro interno inesperado no endpoint '/posts/{subreddit}'.")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@app.get("/search/posts", response_model=List[Dict])
async def search_posts(
    field: str = Query(..., description="Campo onde a pesquisa será realizada (ex: title, author, etc.)", regex="^(title|author|url|score|created_utc)$"),
    query: str = Query(..., description="Termo de pesquisa para buscar nos posts")
):
    logger.info(f"Rota '/search/posts' chamada com field='{field}' e query='{query}'")

    try:
        results = ElasticsearchService.search_posts(field, query)
        logger.info(f"Número de resultados encontrados: {len(results)}")
        
        if not results:
            logger.warning("Nenhum post encontrado com os critérios de busca.")
            raise HTTPException(status_code=404, detail="Nenhum post encontrado.")
        
        return results
    
    except ValueError as e:
        logger.warning(f"Erro de validação no parâmetro 'field': {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Erro inesperado no endpoint '/search/posts'.")
        raise HTTPException(status_code=500, detail=str(e))
