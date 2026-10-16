"""Zentraler Client für alle Claude-Interaktionen.

Kapselt die Anthropic-API und bietet Hilfsmethoden für
strukturierte Ausgaben (JSON) und einfache Completion.
"""

import json
import logging
from typing import Any

import anthropic

from src.core.config import get_settings

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Wrapper um den Anthropic-Client.

    Bietet:
    - complete(): einfache Text-Generierung
    - complete_json(): erzwungene JSON-Antwort mit robustem Parsing
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name
        logger.info("ClaudeClient initialisiert mit Modell %s", self.model)

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ) -> str:
        """Einfache Text-Completion."""
        logger.debug("Claude complete() – system=%d chars, user=%d chars",
                     len(system), len(user))

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return response.content[0].text

    def complete_json(
        self,
        system: str,
        user: str,
        max_tokens: int = 2000,
    ) -> dict[str, Any]:
        """Erzwingt eine JSON-Antwort und parst sie robust."""
        system_json = (
            system
            + "\n\nWICHTIG: Antworte AUSSCHLIESSLICH mit validem JSON. "
            + "Keine Erklärungen, kein Markdown, keine Code-Fences."
        )

        raw = self.complete(system_json, user, max_tokens, temperature=0.2)
        logger.debug("Claude raw JSON response: %s", raw[:200])

        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            cleaned = cleaned[start : end + 1]

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            logger.error("JSON-Parsing fehlgeschlagen: %s", cleaned[:500])
            raise ValueError(
                f"Claude-Antwort ist kein valides JSON: {exc}"
            ) from exc