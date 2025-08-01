from fastapi import FastAPI, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from services.reddit_service import RedditService, RedditAPIError, RedditAuthenticationError, RedditRateLimitError, SubredditNotFound
from models.post_model import PostListResponse
from cache.cache_handler import CacheHandler
from fastapi.responses import JSONResponse
from typing import Optional
import os

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
    return JSONResponse(content={"message": "Teste prático nouslatam backend"}, status_code=status.HTTP_200_OK)


@app.get("/posts/{subreddit}", response_model=PostListResponse)
async def get_posts(
    subreddit: str,
    period: Optional[str] = Query("day", enum=["hour", "day", "week", "month", "year", "all"]),
    limit: Optional[int] = Query(10, ge=1, le=100), 
    sort_type: Optional[str] = Query("hot", enum=["hot", "new", "top", "rising"]) 
):
    """
    Busca posts populares de um subreddit específico.
    
    - **subreddit**: Nome do subreddit (ex: python, django)
    - **period**: Período de tempo para filtrar posts
    - **limit**: Número máximo de posts a retornar (1-100)
    - **sort_type**: Tipo de ordenação dos posts
    """
    cache_key = f"reddit_posts_{subreddit}_{period}_{limit}_{sort_type}"
    
    cached_posts = CacheHandler.get_cache(cache_key)
    if cached_posts:
        return {"posts": cached_posts}

    try:
        posts = await RedditService.fetch_posts(
            subreddit=subreddit, 
            token=REDDIT_ACCESS_TOKEN, 
            period=period, 
            limit=limit,
            sort_type=sort_type
        )
        
        CacheHandler.set_cache(cache_key, posts)
        
        return {"posts": posts}
        
    except SubredditNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RedditAuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except RedditRateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except RedditAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
