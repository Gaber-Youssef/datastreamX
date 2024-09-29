# src/domain/models.py
class Article:
    def __init__(self, id: int, title: str, content: str):
        self.id = id
        self.title = title
        self.content = content
