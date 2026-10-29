"""Agent 2 und 3: Builder – konkrete KI-Automatisierungen und Content Adapter

Enthält zwei spezialisierte Sub-Agenten:

- MeetingSummarizer: Fasst Meeting-Transkripte zusammen und
  extrahiert Action Items, Entscheidungen und offene Fragen.
- ContentAdapter: Passt Inhalte an verschiedene Kanäle an
  (LinkedIn, Newsletter, Slack, interne Doku).
"""

import logging
from typing import Optional

from pydantic import BaseModel, Field

from src.core.claude_client import ClaudeClient

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Meeting Summarizer
# ---------------------------------------------------------------------------

class ActionItem(BaseModel):
    """Eine Aufgabe aus einem Meeting."""

    task: str = Field(description="Was zu tun ist")
    owner: Optional[str] = Field(default=None, description="Wer es macht")
    deadline: Optional[str] = Field(default=None, description="Bis wann")


class MeetingSummary(BaseModel):
    """Strukturierte Zusammenfassung eines Meetings."""

    summary: str
    action_items: list[ActionItem] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)


class MeetingSummarizer:
    """Fasst Meeting-Transkripte strukturiert zusammen."""

    SYSTEM_PROMPT = """Du bist ein präziser Meeting-Assistent bei {company}.
Deine Aufgabe: Extrahiere strukturierte Informationen aus Transkripten.

Regeln:
- Zusammenfassung: max. 5 Sätze, Fokus auf Ergebnisse (nicht Diskussion)
- Action Items: konkret, mit Owner und Deadline, falls genannt
- Offene Fragen: nur echte, ungeklärte Punkte
- Entscheidungen: nur final getroffene Entscheidungen
- Antworte auf Deutsch"""

    def __init__(self) -> None:
        self.claude = ClaudeClient()

    def summarize(
        self,
        transcript: str,
        meeting_title: str = "Meeting",
        company: str = "Ihrem Unternehmen",
    ) -> MeetingSummary:
        logger.info("Summarize: %s @ %s (%d chars)", meeting_title, company, len(transcript))

        user_prompt = f"""Meeting: {meeting_title}

Transkript:
{transcript}

Erstelle eine strukturierte Zusammenfassung im folgenden JSON-Format:
{{
  "summary": "...",
  "action_items": [
    {{"task": "...", "owner": "...", "deadline": "..."}}
  ],
  "open_questions": ["..."],
  "decisions": ["..."]
}}"""

        system_prompt = self.SYSTEM_PROMPT.format(company=company)
        data = self.claude.complete_json(
            system_prompt, user_prompt, max_tokens=2000
        )
        return MeetingSummary(**data)


# ---------------------------------------------------------------------------
# Content Adapter
# ---------------------------------------------------------------------------

class ContentAdapter:
    """Passt Inhalte an verschiedene Zielkanäle an."""

    CHANNEL_STYLES = {
        "linkedin": "Professionell, nahbar, max. 200 Wörter, 3-5 Hashtags am Ende",
        "newsletter": "Informativ, strukturiert mit Zwischenüberschriften, klarer Call-to-Action",
        "slack": "Kurz und locker, Emojis erlaubt, max. 150 Wörter",
        "internal_doc": "Sachlich, vollständig, mit Beispielen und Kontext",
    }

    SYSTEM_PROMPT = """Du bist ein Kommunikations-Experte bei einem NewSpace-Startup.
Deine Aufgabe: Passe Inhalte präzise an den Zielkanal an.

Regeln:
- Behalte die Kernbotschaft bei
- Ändere Ton, Länge und Struktur passend zum Kanal
- Keine Floskeln, keine Übertreibungen
- Antworte auf Deutsch"""

    def __init__(self) -> None:
        self.claude = ClaudeClient()

    def adapt(self, text: str, channel: str) -> str:
        """Passt Text an einen Kanal an."""
        if channel not in self.CHANNEL_STYLES:
            raise ValueError(
                f"Unbekannter Kanal: {channel}. "
                f"Erlaubt: {list(self.CHANNEL_STYLES.keys())}"
            )

        logger.info("Adapt: %d chars → %s", len(text), channel)

        user_prompt = f"""Zielkanal: {channel}
Stil: {self.CHANNEL_STYLES[channel]}

Originaltext:
{text}

Schreibe den Text für den Kanal um."""

        return self.claude.complete(
            self.SYSTEM_PROMPT, user_prompt, max_tokens=1200
        )

    def adapt_multi(self, text: str, channels: list[str]) -> dict[str, str]:
        """Passt Text an mehrere Kanäle gleichzeitig an."""
        return {ch: self.adapt(text, ch) for ch in channels}