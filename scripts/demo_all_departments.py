"""Demo: Discoverer über alle relevanten Abteilungen.

Führt den UseCaseDiscoverer über Operations, Marketing, Engineering
und HR aus und speichert den Report als Markdown.

Ausführen:
    python -m scripts.demo_all_departments
"""

from pathlib import Path

from src.agents.discoverer import UseCaseDiscoverer

DEPARTMENTS = {
    "Operations": (
        "Wir bearbeiten täglich 50+ Kundenanfragen per E-Mail und Telefon. "
        "Jede muss kategorisiert, priorisiert und an den richtigen "
        "Mitarbeiter weitergeleitet werden. Das bindet 2 Vollzeitkräfte."
    ),
    "Marketing": (
        "Wir schreiben wöchentlich 3 Blogposts, 5 LinkedIn-Posts und "
        "2 Newsletter. Jeder Text muss für jeden Kanal neu angepasst werden."
    ),
    "Engineering": (
        "Wir reviewen täglich 20+ Pull Requests und dokumentieren "
        "Architekturentscheidungen. Beides kostet viel Zeit."
    ),
    "HR / People": (
        "Wir sichten 50+ Bewerbungen pro Woche und beantworten täglich "
        "wiederkehrende Fragen zu Benefits und Onboarding."
    ),
}


def main() -> None:
    discoverer = UseCaseDiscoverer()
    results = discoverer.discover_multi(
        DEPARTMENTS,
        team_size_default=5,
        company="Muster GmbH",  
    )

    report = discoverer.format_multi_as_markdown(results)

    output_path = Path("docs/use-cases-report.md")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    # Zusammenfassung
    total = sum(len(cases) for cases in results.values())
    print(f"\n✅ {total} Use-Cases über {len(results)} Abteilungen gefunden.")
    print(f"📄 Report gespeichert: {output_path}\n")
    for dept, cases in results.items():
        print(f"  {dept}: {len(cases)} Use-Cases")


if __name__ == "__main__":
    main()