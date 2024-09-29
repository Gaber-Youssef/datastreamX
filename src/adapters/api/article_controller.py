# src/adapters/api/article_controller.py
from fastapi import APIRouter, Depends
from usecases.article_usecase import ArticleUseCase
from adapters.persistence.article_repo import ArticleRepository
from adapters.cache.cache_repo import CacheRepository
from infrastructure.database import get_db
from infrastructure.cache import get_cache

router = APIRouter()


@router.get("/articles/{id}")
def get_article(id: int, db=Depends(get_db), cache=Depends(get_cache)):
    article_repo = ArticleRepository(db)
    cache_repo = CacheRepository(cache)
    article_usecase = ArticleUseCase(article_repo, cache_repo)

    article = article_usecase.get_article(id)
    if article:
        return {"data": article}
    return {"error": "Article not found"}, 404
