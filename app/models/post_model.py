from pydantic import BaseModel
from typing import List

class Post(BaseModel):
    title: str
    author: str
    url: str
    created_utc: int  # Timestamp de criação do post
    score: int

class PostListResponse(BaseModel):
    posts: List[Post]
