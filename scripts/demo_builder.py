"""Demo: Meeting-Summarizer + Content-Adapter.

Schreibt die Ausgabe nach docs/builder-demo.md und zeigt eine
kurze Zusammenfassung in der Konsole.
"""

from pathlib import Path

from src.agents.builder import ContentAdapter, MeetingSummarizer

TRANSCRIPT = """
Anna (Ops Lead): Danke, dass ihr alle da seid. Wir müssen über die
Kollisionswarnung für XR-42 sprechen. Die aktuelle Pc liegt bei 1.2e-3.

Ben (Flight Dynamics): Ich habe die Bahndaten heute Morgen analysiert.
Das Risiko ist real, aber nicht akut. TCA ist in 36 Stunden.

Anna: Gut. Was schlägst du vor?

Ben: Ich würde ein Manöver vorbereiten, aber erst in 12 Stunden zünden,
wenn wir die nächsten Tracking-Daten haben. Bis dahin beobachten.

Anna: Einverstanden. Wer informiert den Kunden?

Clara (Customer Success): Ich übernehme das. Bis heute 18 Uhr habe ich
eine erste Einschätzung raus.

Anna: Perfekt. Eine Sache noch: Das Software-Update für die neue
Kollisions-API muss diese Woche raus. Können wir Mittwoch deployen?

Ben: Mittwoch ist sportlich, aber machbar wenn die Tests heute laufen.

Anna: Dann machen wir Mittwoch. Clara, kannst du die Release-Notes
vorbereiten?

Clara: Ja, bis Dienstag.

Anna: Und brauchen wir ein Update für die interne Dokumentation?

Ben: Gute Frage, das ist noch offen. Ich kläre das mit dem Tech Writer.

Anna: Okay, dann sind wir durch. Danke euch.
"""

ORIGINAL_CONTENT = (
    "OKAPI:Orbits hat heute ein neues Modul zur automatischen "
    "Kollisionsvermeidung vorgestellt. Es reduziert die manuelle "
    "Prüfzeit um 70% und wird ab Q1 2026 für alle Kunden verfügbar sein."
)


def main() -> None:
    print("=" * 70)
    print("BUILDER-DEMO")
    print("=" * 70)

    # --- Meeting-Summarizer ---
    print("\n[1/2] Meeting-Summarizer läuft...")
    summarizer = MeetingSummarizer()
    result = summarizer.summarize(
        TRANSCRIPT, meeting_title="Ops Weekly – Kollisionswarnung XR-42"
    )
    print(f"      → {len(result.action_items)} Action Items extrahiert")
    print(f"      → {len(result.decisions)} Entscheidungen erkannt")

    # --- Content-Adapter ---
    print("\n[2/2] Content-Adapter läuft (linkedin + slack)...")
    adapter = ContentAdapter()
    linkedin = adapter.adapt(ORIGINAL_CONTENT, channel="linkedin")
    slack = adapter.adapt(ORIGINAL_CONTENT, channel="slack")
    print(f"      → LinkedIn: {len(linkedin)} Zeichen")
    print(f"      → Slack: {len(slack)} Zeichen")

    # --- Markdown-Report schreiben ---
    lines = [
        "# Builder-Demo\n",
        "## Meeting-Zusammenfassung\n",
        "**Meeting:** Ops Weekly – Kollisionswarnung XR-42\n",
        f"\n{result.summary}\n",
        "\n## Action Items\n",
    ]
    for i, item in enumerate(result.action_items, 1):
        owner = item.owner or "—"
        deadline = item.deadline or "—"
        lines.append(f"{i}. **{item.task}**  ")
        lines.append(f"   _Owner:_ {owner} · _Deadline:_ {deadline}\n")

    lines.append("\n## Offene Fragen\n")
    for q in result.open_questions:
        lines.append(f"- {q}")

    lines.append("\n## Entscheidungen\n")
    for d in result.decisions:
        lines.append(f"- {d}")

    lines.append("\n---\n")
    lines.append("## Content-Adapter\n")
    lines.append(f"\n**Original:**\n\n> {ORIGINAL_CONTENT}\n")
    lines.append("\n### LinkedIn\n")
    lines.append(linkedin)
    lines.append("\n### Slack\n")
    lines.append(slack)

    output = Path("docs/builder-demo.md")
    output.parent.mkdir(exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")

    print(f"\n📄 Markdown gespeichert: {output}")



if __name__ == "__main__":
    main()