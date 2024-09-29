# src/adapters/persistence/article_repo.py
from domain.models import Article
from sqlalchemy.orm import Session


class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, article_id: int) -> Article:
        return self.db.query(Article).filter(Article.id == article_id).first()

    def save(self, article: Article):
        self.db.add(article)
        self.db.commit()
