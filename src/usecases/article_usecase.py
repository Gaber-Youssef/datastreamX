# src/usecases/article_usecase.py
from domain.models import Article


class ArticleUseCase:
    def __init__(self, article_repo, cache_repo):
        self.article_repo = article_repo
        self.cache_repo = cache_repo

    def get_article(self, article_id: int):
        cached_article = self.cache_repo.get(f"article:{article_id}")
        if cached_article:
            return cached_article

        article = self.article_repo.get_by_id(article_id)
        if article:
            self.cache_repo.set(f"article:{article_id}", article)
        return article

    def create_article(self, title: str, content: str):
        article = Article(id=None, title=title, content=content)
        self.article_repo.save(article)
        return article
