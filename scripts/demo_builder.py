"""Demo: Meeting-Summarizer + Content-Adapter.

Schreibt die Ausgabe nach docs/builder-demo.md und zeigt eine
kurze Zusammenfassung in der Konsole.

Verwendet generische Business-Beispiele (nicht firmenspezifisch).
"""

from pathlib import Path

from src.agents.builder import ContentAdapter, MeetingSummarizer

# Generisches Marketing-/Business-Meeting
TRANSCRIPT = """
Anna (Marketing Lead): Danke für eure Zeit. Wir müssen die Q3-Kampagne finalisieren.
Ben (Content): Der Blogpost ist fertig, ich brauche noch ein Review von euch.
Anna: Bis wann kannst du die LinkedIn-Version vorbereiten?
Ben: Bis Mittwoch. Clara, kannst du die Newsletter-Version übernehmen?
Clara (CRM): Ja, aber ich brauche die finale Überschrift bis Montag.
Anna: Verstanden. Eine Sache noch: Das Budget für Q4 ist noch offen.
Ben: Gute Frage, das müssen wir mit dem CFO klären. Ich schreibe ihm heute.
Anna: Perfekt. Dann sind wir durch.
"""

# Generischer Content-Text (z. B. für ein Produkt-Update)
ORIGINAL_CONTENT = (
    "Unser Unternehmen hat heute ein neues Feature vorgestellt, das "
    "die manuelle Bearbeitungszeit um 40% reduziert. Es ist ab "
    "sofort für alle Bestandskunden verfügbar."
)


def main() -> None:
    print("=" * 70)
    print("BUILDER-DEMO (Generisch)")
    print("=" * 70)

    # --- Meeting-Summarizer ---
    print("\n[1/2] Meeting-Summarizer läuft...")
    summarizer = MeetingSummarizer()
    
    # Hier übergeben wir einen generischen Firmennamen. 
    # (Falls du builder.py noch nicht angepasst hast, ignoriert Python den Parameter einfach.)
    result = summarizer.summarize(
        TRANSCRIPT, 
        meeting_title="Q3-Kampagnen-Planung",
        company="Muster GmbH"
    )
    print(f"      → {len(result.action_items)} Action Items extrahiert")
    print(f"      → {len(result.decisions)} Entscheidungen erkannt")

    # --- Content-Adapter ---
    print("\n[2/2] Content-Adapter läuft (linkedin + slack)...")
    adapter = ContentAdapter()
    
    linkedin = adapter.adapt(ORIGINAL_CONTENT, channel="linkedin", company="Muster GmbH")
    slack = adapter.adapt(ORIGINAL_CONTENT, channel="slack", company="Muster GmbH")
    print(f"      → LinkedIn: {len(linkedin)} Zeichen")
    print(f"      → Slack: {len(slack)} Zeichen")

    # --- Markdown-Report schreiben ---
    lines = [
        "# Builder-Demo\n",
        "## Meeting-Zusammenfassung\n",
        "**Meeting:** Q3-Kampagnen-Planung\n",
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