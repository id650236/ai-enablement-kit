"""Knowledge Base für KI-Tools und Best Practices."""

import logging
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import get_settings

logger = logging.getLogger(__name__)

Base = declarative_base()


class KnowledgeEntry(Base):
    """Ein Eintrag in der Wissensbasis."""

    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    def __repr__(self) -> str:
        return f"<KnowledgeEntry id={self.id} title={self.title!r}>"


class KnowledgeBase:
    """Verwaltet die interne Wissensbasis."""

    def __init__(self, database_url: str | None = None) -> None:
        settings = get_settings()
        url = database_url or settings.database_url
        self.engine = create_engine(url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("KnowledgeBase initialisiert: %s", url)

    def add(
            self,
            title: str,
            category: str,
            content: str,
            tags: list[str] | None = None,
    ) -> int:
        with self.Session() as session:
            entry = KnowledgeEntry(
                title=title,
                category=category,
                content=content,
                tags=",".join(tags or []),
            )
            session.add(entry)
            session.commit()
            session.refresh(entry)
            return entry.id

    def search(
            self,
            query: str,
            category: str | None = None,
            limit: int = 20,
    ) -> list[KnowledgeEntry]:
        with self.Session() as session:
            q = session.query(KnowledgeEntry)
            if category:
                q = q.filter(KnowledgeEntry.category == category)
            like = f"%{query}%"
            q = q.filter(
                (KnowledgeEntry.title.ilike(like))
                | (KnowledgeEntry.content.ilike(like))
                | (KnowledgeEntry.tags.ilike(like))
            )
            return q.limit(limit).all()

    def list_by_category(self, category: str) -> list[KnowledgeEntry]:
        with self.Session() as session:
            return (
                session.query(KnowledgeEntry)
                .filter(KnowledgeEntry.category == category)
                .all()
            )

    def count(self) -> int:
        with self.Session() as session:
            return session.query(KnowledgeEntry).count()