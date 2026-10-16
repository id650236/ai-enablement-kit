"""Tests für den ClaudeClient.

Achtung: Diese Tests rufen die echte Anthropic-API auf.
Sie benötigen einen gültigen ANTHROPIC_API_KEY in .env.
"""

import pytest

from src.core.claude_client import ClaudeClient


@pytest.fixture(scope="module")
def client() -> ClaudeClient:
    return ClaudeClient()


def test_simple_completion(client: ClaudeClient) -> None:
    """Einfache Text-Completion auf Deutsch."""
    result = client.complete(
        system="Du bist ein hilfsbereiter Assistent. Antworte knapp.",
        user="Sag 'Hallo' auf Deutsch.",
        max_tokens=50,
    )
    assert "Hallo" in result
    assert len(result) > 0


def test_json_completion(client: ClaudeClient) -> None:
    """Strukturierte JSON-Antwort."""
    result = client.complete_json(
        system="Du bist ein Daten-Extraktor.",
        user=(
            "Gib mir eine Liste von 3 KI-Use-Cases für ein Space-Startup. "
            'Format: {"use_cases": [{"title": "...", "impact": "low|medium|high"}]}'
        ),
        max_tokens=500,
    )
    assert isinstance(result, dict)
    assert "use_cases" in result
    assert len(result["use_cases"]) == 3
    for uc in result["use_cases"]:
        assert "title" in uc
        assert uc["impact"] in ("low", "medium", "high")