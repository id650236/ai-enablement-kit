"""FastAPI-Backend für das AI Enablement Kit.

Stellt die Agenten als REST-Endpoints bereit, damit sowohl
Streamlit-UI als auch andere Tools sie nutzen können.
"""

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.agents import (
    ContentAdapter,
    Documenter,
    MeetingSummarizer,
    UseCaseDiscoverer,
)
from src.core.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Interne KI-Tools für OKAPI:Orbits",
)

# Agenten einmalig instanziieren
discoverer = UseCaseDiscoverer()
summarizer = MeetingSummarizer()
adapter = ContentAdapter()
documenter = Documenter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class DiscoverRequest(BaseModel):
    department: str = Field(..., description="Abteilung, z. B. Operations")
    workflow: str = Field(..., description="Beschreibung des Arbeitsablaufs")
    team_size: int = Field(5, ge=1, le=100)


class SummarizeRequest(BaseModel):
    transcript: str = Field(..., min_length=20)
    meeting_title: str = Field("Meeting")


class AdaptRequest(BaseModel):
    text: str = Field(..., min_length=10)
    channel: str = Field(
        ...,
        description="linkedin | newsletter | slack | internal_doc",
    )


class DocumentRequest(BaseModel):
    tool_name: str
    use_case: str
    steps: list[str]
    tags: list[str] | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def root() -> dict:
    """Health-Check und Übersicht."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "endpoints": [
            "POST /discover",
            "POST /summarize",
            "POST /adapt",
            "POST /document",
            "GET  /knowledge/search",
        ],
    }


@app.post("/discover")
def discover(req: DiscoverRequest) -> dict:
    """Findet KI-Use-Cases für eine Abteilung."""
    try:
        cases = discoverer.discover(
            department=req.department,
            workflow=req.workflow,
            team_size=req.team_size,
        )
        return {
            "department": req.department,
            "count": len(cases),
            "use_cases": [uc.model_dump() for uc in cases],
            "markdown": discoverer.format_as_markdown(cases),
        }
    except Exception as exc:
        logger.exception("Discover fehlgeschlagen")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/summarize")
def summarize(req: SummarizeRequest) -> dict:
    """Fasst ein Meeting-Transkript zusammen."""
    try:
        summary = summarizer.summarize(req.transcript, req.meeting_title)
        return summary.model_dump()
    except Exception as exc:
        logger.exception("Summarize fehlgeschlagen")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/adapt")
def adapt(req: AdaptRequest) -> dict:
    """Passt Text an einen Kanal an."""
    try:
        return {
            "channel": req.channel,
            "adapted": adapter.adapt(req.text, req.channel),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Adapt fehlgeschlagen")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/document")
def document(req: DocumentRequest) -> dict:
    """Erstellt eine Tool-Anleitung und speichert sie in der Wissensbasis."""
    try:
        text = documenter.document_tool(
            tool_name=req.tool_name,
            use_case=req.use_case,
            steps=req.steps,
            tags=req.tags,
        )
        return {"tool_name": req.tool_name, "documentation": text}
    except Exception as exc:
        logger.exception("Document fehlgeschlagen")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/knowledge/search")
def search_knowledge(q: str, category: str | None = None) -> dict:
    """Durchsucht die Wissensbasis."""
    entries = documenter.kb.search(q, category=category)
    return {
        "query": q,
        "count": len(entries),
        "results": [
            {
                "id": e.id,
                "title": e.title,
                "category": e.category,
                "tags": e.tags,
            }
            for e in entries
        ],
    }