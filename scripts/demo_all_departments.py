"""Demo: Discoverer über alle relevanten Abteilungen.

Führt den UseCaseDiscoverer über Operations, Marketing, Engineering
und HR aus und speichert den Report als Markdown.

Ausführen:
    python docs/demo_all_departments.py
"""

from pathlib import Path

from src.agents.discoverer import UseCaseDiscoverer

DEPARTMENTS = {
    "Operations": (
        "Wir überwachen 40+ Satelliten und erhalten täglich mehrere "
        "Kollisionswarnungen. Jede muss manuell geprüft, priorisiert und "
        "dokumentiert werden. Das bindet 2 Ingenieure fast vollzeit."
    ),
    "Marketing": (
        "Wir schreiben Blogposts, LinkedIn-Posts, Newsletter und "
        "Case Studies. Jeder Text muss für jeden Kanal neu angepasst "
        "werden. Außerdem erstellen wir wöchentlich Wettbewerbsanalysen."
    ),
    "Engineering": (
        "Wir reviewen täglich Pull Requests, schreiben Tests und "
        "dokumentieren Architekturentscheidungen. Außerdem verbringen "
        "wir viel Zeit mit der Suche nach relevanten Informationen in "
        "unserer internen Wissensbasis."
    ),
    "HR / People": (
        "Wir sichten Bewerbungen, führen Erstinterviews und pflegen "
        "Onboarding-Unterlagen. Außerdem beantworten wir täglich "
        "wiederkehrende Fragen zu Benefits und Prozessen."
    ),
}


def main() -> None:
    discoverer = UseCaseDiscoverer()
    results = discoverer.discover_multi(DEPARTMENTS, team_size_default=5)

    report = discoverer.format_multi_as_markdown(results)

    output_path = Path("docs/use-cases-report.md")
    output_path.write_text(report, encoding="utf-8")

    # Zusammenfassung
    total = sum(len(cases) for cases in results.values())
    print(f"\n✅ {total} Use-Cases über {len(results)} Abteilungen gefunden.")
    print(f"📄 Report gespeichert: {output_path}\n")
    for dept, cases in results.items():
        print(f"  {dept}: {len(cases)} Use-Cases")


if __name__ == "__main__":
    main()