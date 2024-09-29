# DataStreamX Architecture

DataStreamX is built following the **Clean Architecture** principles to ensure scalability, maintainability, and flexibility. The architecture separates the core business logic from the external systems like databases, caches, messaging queues, and search engines, allowing the system to be easily adaptable and testable.

## Clean Architecture Overview

The architecture is designed around the following key concepts:
- **Independence of Frameworks**: Business logic does not depend on frameworks or external systems.
- **Dependency Inversion**: The outer layers depend on the inner layers (use cases and domain), not vice versa.
- **Testability**: Each **part** of the system can be independently tested by mocking dependencies.
- **Separation of Concerns**: Business logic is separate from technical details like databases, APIs, and messaging queues.

Clean Architecture is divided into four key layers:

### 1. Domain Layer (Entities)
The **Domain Layer** contains the core business logic and entities, which are completely independent of external systems. This layer defines the primary data structures and the basic rules of the business domain.

- **Location**: `src/domain/`
- **Responsibility**: Defining business entities and core logic.

Example:
```python
class Article:
    def __init__(self, id: int, title: str, content: str):
        self.id = id
        self.title = title
        self.content = content
```

### 2. Use Case Layer (Application Layer)
The Use Case Layer contains the application-specific business logic. This layer handles the specific use cases of the application, such as creating or retrieving an article, interacting with the domain entities and coordinating between repositories.

- **Location**: src/usecases/
- **Responsibility**: Implementing application logic and orchestrating the flow of data between the domain and external systems.

Example:
```python
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
```

### 3. Interface Adapters Layer (Controllers & Repositories)
The Interface Adapters Layer acts as a bridge between the external systems (e.g., databases, web frameworks, and message queues) and the core application logic. It contains repositories and controllers that handle data translation and communication with the infrastructure.

- **Location**: src/adapters/
- **Responsibility**: Adapting external systems to interact with the use cases and domain.


Example (Database Repository):
```python
class ArticleRepository:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, article_id: int):
        return self.db.query(Article).filter(Article.id == article_id).first()

    def save(self, article: Article):
        self.db.add(article)
        self.db.commit()
```


Example (API Controller):
```python
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
```

### 4. Infrastructure Layer
The Infrastructure Layer is responsible for providing the actual implementations for databases, caches, search engines, and message queues. These services are used by the repositories to interact with the external world.

- **Location**: src/infrastructure/
- **Responsibility**: Configuring and managing connections to external services such as PostgreSQL, Redis, Elasticsearch, and RabbitMQ.


Example (Database Setup):

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "postgresql://user:password@localhost/mydb"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Summary of Layers
1. **Domain Layer (Entities)**: Contains business entities and core logic, independent of frameworks.
2. **Use Case Layer (Application)**: Coordinates application-specific business logic and orchestrates interaction between domain and infrastructure.
3. **Interface Adapters**: Provides the interface between external systems and core logic through controllers and repositories.
4. **Infrastructure Layer:** Handles the actual implementations for external systems like databases, caches, and queues.

By following this Clean Architecture structure, DataStreamX is designed to be flexible, testable, and maintainable, while allowing easy replacement or modification of external systems.