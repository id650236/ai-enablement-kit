"""Streamlit-UI für das AI Enablement Kit (Standalone, ohne FastAPI)."""

import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Projekt-Root zum Suchpfad hinzufügen
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
from md2pdf import convert

# --- WICHTIG: set_page_config muss die erste Streamlit-Funktion sein ---
st.set_page_config(
    page_title="AI Enablement Kit",
    page_icon="🚀",
    layout="wide",
)

# --- Secrets / Env laden ---
def get_api_key() -> str:
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    from dotenv import load_dotenv
    load_dotenv()
    return os.getenv("ANTHROPIC_API_KEY", "")

os.environ["ANTHROPIC_API_KEY"] = get_api_key()

# --- Agenten importieren und instanziieren (erst NACH set_page_config) ---
from src.agents import (  # noqa: E402
    ContentAdapter,
    Documenter,
    MeetingSummarizer,
    UseCaseDiscoverer,
)

@st.cache_resource
def get_agents():
    return {
        "discoverer": UseCaseDiscoverer(),
        "summarizer": MeetingSummarizer(),
        "adapter": ContentAdapter(),
        "documenter": Documenter(),
    }

agents = get_agents()

# --- Ab hier UI ---
st.title("🚀 AI Enablement Kit")
st.caption(
    "Interne KI-Tools für OKAPI:Orbits – "
    "Use Cases entdecken, Meetings zusammenfassen, Content adaptieren."
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["🔍 Use Cases", "📝 Meeting", "✍️ Content", "📚 Wissensbasis"]
)


def markdown_to_pdf(markdown_text: str) -> bytes:
    with tempfile.NamedTemporaryFile(
        suffix=".md", delete=False, mode="w", encoding="utf-8"
    ) as f:
        f.write(markdown_text)
        md_path = f.name
    pdf_path = md_path.replace(".md", ".pdf")
    try:
        convert(md_path, pdf_path)
        with open(pdf_path, "rb") as f:
            return f.read()
    finally:
        for p in (md_path, pdf_path):
            if os.path.exists(p):
                os.unlink(p)


def render_pdf_download(markdown_text: str, filename: str, key: str) -> None:
    try:
        pdf_bytes = markdown_to_pdf(markdown_text)
        st.download_button(
            label="📥 Als PDF herunterladen",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            key=key,
        )
    except Exception as e:
        st.error(f"PDF-Fehler: {e}")


# ---------------------------------------------------------------------------
# Tab 1
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("KI-Use-Cases entdecken")
    st.write("Beschreibe den Arbeitsablauf einer Abteilung – die KI findet Potenziale.")

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        department = st.text_input("Abteilung", value="Operations")
    with col2:
        team_size = st.number_input("Teamgröße", 1, 100, 5)
    with col3:
        max_cases = st.number_input("Max. Use Cases", 3, 15, 5)

    workflow = st.text_area(
        "Beschreibe den aktuellen Workflow",
        height=150,
        placeholder="z. B. Wir überwachen 40+ Satelliten ...",
    )

    if st.button("🔍 Use Cases finden", type="primary"):
        if not workflow.strip():
            st.warning("Bitte einen Workflow beschreiben.")
        else:
            with st.spinner("Claude analysiert den Workflow..."):
                try:
                    cases = agents["discoverer"].discover(
                        department=department,
                        workflow=workflow,
                        team_size=int(team_size),
                        max_cases=int(max_cases),
                    )
                    st.success(f"✅ {len(cases)} Use Cases gefunden")

                    for uc in cases:
                        with st.expander(f"**{uc.title}**"):
                            st.markdown(f"**Pain Point:** {uc.pain_point}")
                            st.markdown(f"**Lösung:** {uc.ai_solution}")
                            col_a, col_b = st.columns(2)
                            col_a.metric("Impact", uc.impact)
                            col_b.metric("Effort", uc.effort)
                            st.markdown(f"**Tools:** {', '.join(uc.tools_needed)}")

                    markdown_report = agents["discoverer"].format_as_markdown(cases)
                    with st.expander("📄 Markdown-Report"):
                        st.markdown(markdown_report)

                    date_str = datetime.now().strftime("%Y-%m-%d")
                    filename = f"use_cases_{department.lower()}_{date_str}.pdf"
                    render_pdf_download(markdown_report, filename, key="pdf_tab1")
                except Exception as e:
                    st.error(f"Fehler: {e}")

# ---------------------------------------------------------------------------
# Tab 2
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Meeting zusammenfassen")
    st.write("Füge ein Transkript ein – du bekommst Action Items, Entscheidungen und offene Fragen.")

    meeting_title = st.text_input("Meeting-Titel", value="Ops Weekly")
    transcript = st.text_area("Transkript", height=250)

    if st.button("📝 Zusammenfassen", type="primary"):
        if len(transcript.strip()) < 20:
            st.warning("Bitte ein Transkript einfügen (min. 20 Zeichen).")
        else:
            with st.spinner("Claude fasst zusammen..."):
                try:
                    summary = agents["summarizer"].summarize(transcript, meeting_title)

                    st.markdown("### 📋 Zusammenfassung")
                    st.write(summary.summary)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"### ✅ Action Items ({len(summary.action_items)})")
                        for item in summary.action_items:
                            owner = item.owner or "—"
                            deadline = item.deadline or "—"
                            st.markdown(
                                f"- **{item.task}**  \n"
                                f"  _Owner:_ {owner} · _Deadline:_ {deadline}"
                            )
                    with col2:
                        st.markdown(f"### 🎯 Entscheidungen ({len(summary.decisions)})")
                        for d in summary.decisions:
                            st.markdown(f"- {d}")
                        st.markdown(f"### ❓ Offene Fragen ({len(summary.open_questions)})")
                        for q in summary.open_questions:
                            st.markdown(f"- {q}")

                    md_lines = [
                        f"# Meeting: {meeting_title}\n",
                        f"## Zusammenfassung\n{summary.summary}\n",
                        "## Action Items",
                    ]
                    for item in summary.action_items:
                        md_lines.append(f"- {item.task} (Owner: {item.owner or '—'})")
                    md_lines.append("\n## Entscheidungen")
                    for d in summary.decisions:
                        md_lines.append(f"- {d}")
                    md_lines.append("\n## Offene Fragen")
                    for q in summary.open_questions:
                        md_lines.append(f"- {q}")

                    safe_title = meeting_title.lower().replace(" ", "_")
                    filename = f"meeting_{safe_title}.pdf"
                    render_pdf_download("\n".join(md_lines), filename, key="pdf_tab2")
                except Exception as e:
                    st.error(f"Fehler: {e}")

# ---------------------------------------------------------------------------
# Tab 3
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Content für verschiedene Kanäle adaptieren")
    st.write("Ein Originaltext – angepasst an LinkedIn, Newsletter, Slack oder interne Doku.")

    text = st.text_area("Originaltext", height=150)
    channel = st.selectbox(
        "Zielkanal",
        ["linkedin", "newsletter", "slack", "internal_doc"],
    )

    if st.button("✍️ Adaptieren", type="primary"):
        if len(text.strip()) < 10:
            st.warning("Bitte einen Text einfügen.")
        else:
            with st.spinner(f"Claude adaptiert für {channel}..."):
                try:
                    adapted = agents["adapter"].adapt(text, channel)

                    st.markdown(f"### Ergebnis für **{channel}**")
                    st.markdown(adapted)
                    st.code(adapted, language="markdown")

                    filename = f"content_{channel}.pdf"
                    render_pdf_download(adapted, filename, key="pdf_tab3")
                except Exception as e:
                    st.error(f"Fehler: {e}")

# ---------------------------------------------------------------------------
# Tab 4
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("Wissensbasis durchsuchen")
    st.write("Finde Anleitungen, Use Cases und Best Practices.")

    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Suchbegriff", value="")
    with col2:
        category = st.selectbox("Kategorie", ["alle", "tool", "use_case", "best_practice"])

    if query.strip():
        try:
            cat = None if category == "alle" else category
            entries = agents["documenter"].kb.search(query, category=cat)

            st.info(f"{len(entries)} Treffer für '{query}'")

            for entry in entries:
                st.markdown(f"**{entry.title}** — _{entry.category}_")
                if entry.tags:
                    st.caption(f"Tags: {entry.tags}")

            if entries:
                md_lines = [f"# Suchergebnisse für '{query}'\n"]
                for entry in entries:
                    md_lines.append(f"## {entry.title} ({entry.category})")
                safe_query = query.lower().replace(" ", "_")
                filename = f"wissen_{safe_query}.pdf"
                render_pdf_download("\n".join(md_lines), filename, key="pdf_tab4")
        except Exception as e:
            st.error(f"Fehler: {e}")