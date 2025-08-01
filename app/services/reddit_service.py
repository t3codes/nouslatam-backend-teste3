import httpx
import asyncio
from typing import List, Dict, Optional

class RedditAPIError(Exception):
    """Exceção base para erros relacionados à API do Reddit."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)

class SubredditNotFound(RedditAPIError):
    """Lançada quando um subreddit não é encontrado."""
    def __init__(self, subreddit: str):
        message = f"O subreddit '{subreddit}' não foi encontrado ou é privado."
        super().__init__(message, status_code=404)

class RedditAuthenticationError(RedditAPIError):
    """Lançada para erros de autenticação (token inválido)."""
    def __init__(self):
        message = "Erro de autenticação. Verifique se o token de acesso é válido."
        super().__init__(message, status_code=401)

class RedditRateLimitError(RedditAPIError):
    """Lançada quando o limite de requisições da API do Reddit é atingido."""
    def __init__(self):
        message = "Limite de requisições da API do Reddit atingido. Tente novamente mais tarde."
        super().__init__(message, status_code=429)

class RedditService:
    """
    Service para interagir com a API do Reddit e buscar posts populares.
    """
    @staticmethod
    async def fetch_posts(
        subreddit: str,
        token: str,
        period: str = "day",
        limit: int = 10,
        sort_type: str = "hot"
    ) -> List[Dict]:
        """
        Busca os posts de um determinado subreddit com filtros de período, limite e ordenação.

        Args:
            subreddit (str): O nome do subreddit (ex: 'python', 'django').
            token (str): O token de acesso OAuth2 para autenticação.
            period (str): O período de tempo para os posts ('hour', 'day', 'week', 'month', 'year', 'all').
            limit (int): O número máximo de posts a serem retornados.
            sort_type (str): O tipo de ordenação ('hot', 'new', 'top', 'rising').

        Returns:
            List[Dict]: Uma lista de dicionários formatados com os campos necessários para o modelo Post.

        Raises:
            SubredditNotFound: Se o subreddit não for encontrado.
            RedditAuthenticationError: Se o token for inválido ou expirado.
            RedditRateLimitError: Se o limite de requisições for atingido.
            RedditAPIError: Para outros erros da API (erros de servidor, etc.).
        """
        # URL correta baseada na documentação da API do Reddit
        if sort_type in ["top", "controversial"]:
            url = f"https://oauth.reddit.com/r/{subreddit}/{sort_type}"
        else:
            url = f"https://oauth.reddit.com/r/{subreddit}/{sort_type}"
        
        params = {
            "limit": limit,
            "raw_json": 1  
        }
        
        if sort_type in ["top", "controversial"]:
            params["t"] = period

        headers = {
            
            "User-Agent": "Teste2:1zpdmvBmF0a8gaWmixdTsA:v1.0.0 (by /u/Fun-Weight-2423)",
            "Authorization": f"Bearer {token}"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)

           
            if response.status_code == 401:
                raise RedditAuthenticationError()
           
            elif response.status_code == 429:
                raise RedditRateLimitError()

            
            response.raise_for_status()
            
            data = response.json()
            if not data.get('data', {}).get('children'):
                 is_real_subreddit = await RedditService.check_subreddit_exists(subreddit, token)
                 if not is_real_subreddit:
                    raise SubredditNotFound(subreddit)

            # Extrai e formata os dados dos posts para o formato esperado pelo modelo Post
            formatted_posts = []
            for child in data['data']['children']:
                post_data = child['data']
                formatted_post = {
                    "title": post_data.get('title', ''),
                    "author": post_data.get('author', ''),
                    "url": post_data.get('url', ''),
                    "created_utc": int(post_data.get('created_utc', 0)),
                    "score": post_data.get('score', 0)
                }
                formatted_posts.append(formatted_post)

            return formatted_posts

        except httpx.HTTPStatusError as e:
            raise RedditAPIError(
                f"Erro na API do Reddit: {e.response.status_code} - {e.response.text}",
                status_code=e.response.status_code
             )
        except httpx.RequestError as e:
            raise RedditAPIError(f"Erro de conexão com o Reddit: {str(e)}")

    @staticmethod
    async def check_subreddit_exists(subreddit: str, token: str) -> bool:
        """
        Verifica se um subreddit existe usando um endpoint diferente.
        """
        url = f"https://oauth.reddit.com/r/{subreddit}/about"
        headers = {
            "User-Agent": "Teste2:1zpdmvBmF0a8gaWmixdTsA:v1.0.0 (by /u/Fun-Weight-2423)",
            "Authorization": f"Bearer {token}"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
            return response.status_code == 200
        except httpx.RequestError:
            return False
