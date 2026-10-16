"""Agent 3: Documenter – schreibt Anleitungen und pflegt die Wissensbasis."""

import logging

from src.agents.builder import ContentAdapter
from src.core.claude_client import ClaudeClient
from src.core.knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)


class Documenter:
    """Schreibt Anleitungen und pflegt die Wissensbasis."""

    SYSTEM_PROMPT = """Du bist ein technischer Redakteur bei einem NewSpace-Startup.
Deine Aufgabe: Schreibe verständliche Anleitungen für KI-Tools
und interne Prozesse.

Zielgruppe: Kolleg:innen ohne technischen Hintergrund.

Struktur jeder Anleitung:
1. **Wann nutzen?** – Konkrete Situationen
2. **Schritt-für-Schritt** – Nummerierte Anleitung
3. **Beispiele** – 1-2 konkrete Beispiele aus dem Arbeitsalltag
4. **Typische Fehler** – Was schiefgehen kann
5. **Datenschutz** – Was zu beachten ist

Regeln:
- Keine Fachbegriffe ohne Erklärung
- Immer konkrete Beispiele
- Antworte auf Deutsch"""

    def __init__(self) -> None:
        self.claude = ClaudeClient()
        self.kb = KnowledgeBase()
        self.adapter = ContentAdapter()

    def document_tool(
            self,
            tool_name: str,
            use_case: str,
            steps: list[str],
            tags: list[str] | None = None,
    ) -> str:
        logger.info("Documenter: %s (%d Schritte)", tool_name, len(steps))

        user_prompt = f"""Tool: {tool_name}
Use Case: {use_case}
Schritte:
{chr(10).join(f'{i}. {s}' for i, s in enumerate(steps, 1))}

Schreibe eine vollständige Anleitung nach der vorgegebenen Struktur."""

        doc = self.claude.complete(self.SYSTEM_PROMPT, user_prompt, max_tokens=2000)

        self.kb.add(
            title=f"Anleitung: {tool_name}",
            category="tool",
            content=doc,
            tags=tags or [tool_name.lower(), "anleitung"],
        )
        return doc

    def search(self, query: str) -> list[str]:
        entries = self.kb.search(query)
        return [f"{e.title} ({e.category})" for e in entries]