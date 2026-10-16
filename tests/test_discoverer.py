"""Tests für den UseCaseDiscoverer."""

import pytest

from src.agents.discoverer import UseCaseDiscoverer


@pytest.fixture(scope="module")
def discoverer() -> UseCaseDiscoverer:
    return UseCaseDiscoverer()


def test_discover_operations(discoverer: UseCaseDiscoverer) -> None:
    """Findet Use-Cases für ein Operations-Team."""
    cases = discoverer.discover(
        department="Operations",
        workflow=(
            "Wir erhalten täglich 50+ E-Mails von Satellitenbetreibern. "
            "Jede muss gelesen, kategorisiert und an die richtige Person "
            "weitergeleitet werden. Das dauert ca. 3 Stunden pro Tag."
        ),
        team_size=8,
    )

    assert len(cases) >= 3
    for c in cases:
        assert c.title
        assert c.department == "Operations"
        assert c.effort in ("low", "medium", "high")
        assert c.impact in ("low", "medium", "high")
        print(f"  ✅ {c.title} | Impact: {c.impact} | Effort: {c.effort}")


def test_markdown_format(discoverer: UseCaseDiscoverer) -> None:
    """Markdown-Report enthält alle wichtigen Felder."""
    cases = discoverer.discover(
        department="Marketing",
        workflow=(
            "Wir schreiben Blogposts, LinkedIn-Posts und Newsletter. "
            "Jeder Text muss für jeden Kanal neu angepasst werden."
        ),
        team_size=3,
    )
    md = discoverer.format_as_markdown(cases)

    assert "# KI-Use-Cases" in md
    assert "Marketing" in md
    assert all(c.title in md for c in cases)