"""Tests für die Builder-Agenten."""

import pytest

from src.agents.builder import ContentAdapter, MeetingSummarizer


@pytest.fixture(scope="module")
def summarizer() -> MeetingSummarizer:
    return MeetingSummarizer()


@pytest.fixture(scope="module")
def adapter() -> ContentAdapter:
    return ContentAdapter()


SAMPLE_TRANSCRIPT = """
Anna: Wir müssen die Kollisionswarnung für Satellit XR-42 priorisieren.
Ben: Ja, ich schaue mir die Bahndaten heute Nachmittag an.
Anna: Gut. Wer informiert den Kunden?
Ben: Das kann ich übernehmen, bis morgen Vormittag.
Anna: Perfekt. Übrigens, die neue Software-Version müssen wir nächste Woche ausrollen.
Ben: Wann genau?
Anna: Sagen wir Mittwoch. Ich erstelle den Deployment-Plan.
Ben: Noch eine Frage: Brauchen wir ein Update für die Dokumentation?
Anna: Gute Frage, das ist noch offen.
"""


def test_meeting_summarizer(summarizer: MeetingSummarizer) -> None:
    """Meeting wird strukturiert zusammengefasst."""
    result = summarizer.summarize(
        SAMPLE_TRANSCRIPT, meeting_title="Kollisionswarnung XR-42"
    )

    assert result.summary
    assert len(result.summary) > 20
    assert len(result.action_items) >= 2
    assert any(
        "XR-42" in item.task or "Kollision" in item.task
        for item in result.action_items
    )


def test_content_adapter_linkedin(adapter: ContentAdapter) -> None:
    """Text wird für LinkedIn angepasst."""
    original = (
        "Wir haben eine neue Version unseres Kollisionsvermeidungssystems "
        "veröffentlicht. Sie reduziert die Reaktionszeit um 40%."
    )
    result = adapter.adapt(original, channel="linkedin")

    assert len(result) > 50
    assert "#" in result  # Hashtags


def test_content_adapter_invalid_channel(adapter: ContentAdapter) -> None:
    """Unbekannter Kanal wirft Fehler."""
    with pytest.raises(ValueError, match="Unbekannter Kanal"):
        adapter.adapt("Test", channel="tiktok")