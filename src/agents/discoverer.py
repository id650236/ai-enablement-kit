"""Agent 1: Use-Case-Discoverer.

Analysiert Beschreibungen von Arbeitsabläufen aus verschiedenen
Abteilungen und identifiziert konkrete, umsetzbare KI-Use-Cases.

Beispiel:
    discoverer = UseCaseDiscoverer()
    cases = discoverer.discover(
        department="Operations",
        workflow="Wir beantworten täglich 50+ E-Mails...",
        team_size=8,
        max_cases=8,
    )
"""

import logging

from pydantic import BaseModel, Field

from src.core.claude_client import ClaudeClient

logger = logging.getLogger(__name__)


class UseCase(BaseModel):
    """Ein identifizierter KI-Use-Case."""

    title: str = Field(description="Kurzer, prägnanter Titel")
    department: str = Field(description="Abteilung, z. B. Operations")
    pain_point: str = Field(description="Aktuelles Problem")
    ai_solution: str = Field(description="Konkrete KI-Lösung")
    effort: str = Field(description="low | medium | high")
    impact: str = Field(description="low | medium | high")
    tools_needed: list[str] = Field(default_factory=list)


class UseCaseDiscoverer:
    """Findet KI-Use-Cases in Abteilungen."""

    SYSTEM_PROMPT = """Du bist ein KI-Berater bei einem NewSpace-Startup.
Deine Aufgabe: Analysiere die Beschreibung eines Arbeitsablaufs
und identifiziere konkrete, umsetzbare KI-Use-Cases.

Fokus:
- Zeitersparnis für das Team
- Reduktion von Reibung und manueller Arbeit
- Machbarkeit mit LLMs und einfachen API-Integrationen
- Nutzen für nicht-technische Nutzer

Wichtig:
- Empfehle als LLM-Backend AUSSCHLIESSLICH Claude (Anthropic API),
  da wir diese bereits lizenzieren. Keine OpenAI-/GPT-Empfehlungen.
- Sei konkret, nicht generisch (keine "KI kann helfen"-Floskeln)
- Bevorzuge Lösungen, die in Tagen statt Monaten umsetzbar sind
- Antworte auf Deutsch"""

    def __init__(self) -> None:
        self.claude = ClaudeClient()

    # ------------------------------------------------------------------
    # Single-Department
    # ------------------------------------------------------------------

    def discover(
            self,
            department: str,
            workflow: str,
            team_size: int = 5,
            max_cases: int = 5,
    ) -> list[UseCase]:
        """Identifiziert KI-Use-Cases für einen Arbeitsablauf.

        Args:
            department: Name der Abteilung (z. B. "Operations").
            workflow: Beschreibung des aktuellen Arbeitsablaufs.
            team_size: Anzahl der betroffenen Personen.
            max_cases: Maximale Anzahl der zu generierenden Use Cases.

        Returns:
            Liste von UseCase-Objekten.
        """
        logger.info(
            "Discoverer analysiert %s (Team: %d, Workflow: %d chars, max: %d)",
            department, team_size, len(workflow), max_cases,
        )

        user_prompt = f"""Abteilung: {department}
Teamgröße: {team_size}
Aktueller Workflow:
{workflow}

Identifiziere bis zu {max_cases} konkrete KI-Use-Cases für diese Abteilung.
Antworte im folgenden JSON-Format:
{{
  "use_cases": [
    {{
      "title": "...",
      "department": "{department}",
      "pain_point": "...",
      "ai_solution": "...",
      "effort": "low|medium|high",
      "impact": "low|medium|high",
      "tools_needed": ["..."]
    }}
  ]
}}"""

        data = self.claude.complete_json(
            self.SYSTEM_PROMPT,
            user_prompt,
            max_tokens=max(2500, max_cases * 400),
        )
        use_cases = [UseCase(**uc) for uc in data["use_cases"]]
        logger.info("%d Use-Cases identifiziert", len(use_cases))
        return use_cases

    def format_as_markdown(self, use_cases: list[UseCase]) -> str:
        """Formatiert Use-Cases als Markdown für Reports."""
        lines = ["# KI-Use-Cases\n"]
        for i, uc in enumerate(use_cases, 1):
            lines.append(f"## {i}. {uc.title}")
            lines.append(f"**Abteilung:** {uc.department}")
            lines.append(f"**Pain Point:** {uc.pain_point}")
            lines.append(f"**Lösung:** {uc.ai_solution}")
            lines.append(f"**Impact:** {uc.impact} | **Effort:** {uc.effort}")
            lines.append(f"**Tools:** {', '.join(uc.tools_needed)}")
            lines.append("")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Multi-Department
    # ------------------------------------------------------------------

    def discover_multi(
            self,
            departments: dict[str, str],
            team_size_default: int = 5,
    ) -> dict[str, list[UseCase]]:
        """Analysiert mehrere Abteilungen in einem Durchlauf.

        Args:
            departments: Mapping von Abteilungsname → Workflow-Beschreibung.
            team_size_default: Teamgröße, falls nicht anders angegeben.

        Returns:
            Mapping von Abteilungsname → Liste von UseCase-Objekten.
        """
        results: dict[str, list[UseCase]] = {}
        for dept, workflow in departments.items():
            logger.info("Multi-Discover: %s", dept)
            try:
                results[dept] = self.discover(
                    department=dept,
                    workflow=workflow,
                    team_size=team_size_default,
                )
            except Exception as exc:
                logger.error("Discover für %s fehlgeschlagen: %s", dept, exc)
                results[dept] = []
        return results

    def format_multi_as_markdown(
            self,
            results: dict[str, list[UseCase]],
    ) -> str:
        """Formatiert Multi-Department-Ergebnisse als Markdown."""
        lines = ["# KI-Use-Cases nach Abteilung\n"]
        for dept, cases in results.items():
            lines.append(f"\n## Abteilung: {dept}\n")
            if not cases:
                lines.append("_Keine Use-Cases identifiziert._\n")
                continue
            for i, uc in enumerate(cases, 1):
                lines.append(f"### {i}. {uc.title}")
                lines.append(f"- **Pain Point:** {uc.pain_point}")
                lines.append(f"- **Lösung:** {uc.ai_solution}")
                lines.append(f"- **Impact:** {uc.impact} | **Effort:** {uc.effort}")
                lines.append(f"- **Tools:** {', '.join(uc.tools_needed)}\n")
        return "\n".join(lines)