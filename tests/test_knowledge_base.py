"""Tests für Knowledge Base und Documenter."""

from pathlib import Path

import pytest

from src.agents.documenter import Documenter
from src.core.knowledge_base import KnowledgeBase


@pytest.fixture
def temp_kb(tmp_path: Path) -> KnowledgeBase:
    db_path = tmp_path / "test_kb.db"
    return KnowledgeBase(database_url=f"sqlite:///{db_path}")


def test_add_and_search(temp_kb: KnowledgeBase) -> None:
    temp_kb.add(
        title="Claude für Meeting-Zusammenfassungen",
        category="tool",
        content="Nutze die Anthropic API, um Transkripte zusammenzufassen.",
        tags=["claude", "meeting"],
    )
    temp_kb.add(
        title="Prompt-Tipps für Einsteiger",
        category="best_practice",
        content="Sei konkret, gib Kontext, nutze Beispiele.",
        tags=["prompting"],
    )

    assert temp_kb.count() == 2
    results = temp_kb.search("Claude")
    assert len(results) == 1
    assert "Meeting" in results[0].title


def test_list_by_category(temp_kb: KnowledgeBase) -> None:
    temp_kb.add("A", "tool", "Inhalt A")
    temp_kb.add("B", "tool", "Inhalt B")
    temp_kb.add("C", "use_case", "Inhalt C")

    assert len(temp_kb.list_by_category("tool")) == 2
    assert len(temp_kb.list_by_category("use_case")) == 1


@pytest.mark.slow
def test_documenter_creates_entry() -> None:
    doc = Documenter()
    before = doc.kb.count()

    text = doc.document_tool(
        tool_name="Meeting-Summarizer",
        use_case="Meeting-Transkripte in Action Items umwandeln",
        steps=[
            "Transkript aus Zoom oder Teams exportieren",
            "Datei in das Streamlit-Tool hochladen",
            "Auf 'Zusammenfassen' klicken",
            "Ergebnis prüfen und in Notion einfügen",
        ],
        tags=["meeting", "claude", "automation"],
    )

    assert len(text) > 200
    assert doc.kb.count() == before + 1