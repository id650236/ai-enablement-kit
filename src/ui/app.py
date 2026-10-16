"""Streamlit-UI für das AI Enablement Kit.

Vier Tabs für die vier Kernaufgaben:
1. Use Cases entdecken
2. Meeting zusammenfassen
3. Content adaptieren
4. Wissensbasis durchsuchen
"""

import httpx
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Enablement Kit",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 AI Enablement Kit")
st.caption(
    "Interne KI-Tools für OKAPI:Orbits – "
    "Use Cases entdecken, Meetings zusammenfassen, Content adaptieren."
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["🔍 Use Cases", "📝 Meeting", "✍️ Content", "📚 Wissensbasis"]
)

# ---------------------------------------------------------------------------
# Tab 1: Use Cases entdecken
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("KI-Use-Cases entdecken")
    st.write("Beschreibe den Arbeitsablauf einer Abteilung – die KI findet Potenziale.")

    col1, col2 = st.columns([3, 1])
    with col1:
        department = st.text_input("Abteilung", value="Operations")
    with col2:
        team_size = st.number_input("Teamgröße", 1, 100, 5)

    workflow = st.text_area(
        "Beschreibe den aktuellen Workflow",
        height=150,
        placeholder=(
            "z. B. Wir überwachen 40+ Satelliten und erhalten täglich "
            "mehrere Kollisionswarnungen. Jede muss manuell geprüft, "
            "priorisiert und dokumentiert werden..."
        ),
    )

    if st.button("🔍 Use Cases finden", type="primary"):
        if not workflow.strip():
            st.warning("Bitte einen Workflow beschreiben.")
        else:
            with st.spinner("Claude analysiert den Workflow..."):
                try:
                    r = httpx.post(
                        f"{API_URL}/discover",
                        json={
                            "department": department,
                            "workflow": workflow,
                            "team_size": int(team_size),
                        },
                        timeout=120.0,
                    )
                    r.raise_for_status()
                    data = r.json()

                    st.success(f"✅ {data['count']} Use Cases gefunden")

                    for uc in data["use_cases"]:
                        with st.expander(f"**{uc['title']}**"):
                            st.markdown(f"**Pain Point:** {uc['pain_point']}")
                            st.markdown(f"**Lösung:** {uc['ai_solution']}")
                            col_a, col_b = st.columns(2)
                            col_a.metric("Impact", uc["impact"])
                            col_b.metric("Effort", uc["effort"])
                            st.markdown(
                                f"**Tools:** {', '.join(uc['tools_needed'])}"
                            )

                    with st.expander("📄 Markdown-Report"):
                        st.markdown(data["markdown"])
                except httpx.HTTPError as e:
                    st.error(f"Fehler: {e}")

# ---------------------------------------------------------------------------
# Tab 2: Meeting zusammenfassen
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Meeting zusammenfassen")
    st.write(
        "Füge ein Transkript ein – du bekommst Action Items, "
        "Entscheidungen und offene Fragen."
    )

    meeting_title = st.text_input("Meeting-Titel", value="Ops Weekly")
    transcript = st.text_area("Transkript", height=250)

    if st.button("📝 Zusammenfassen", type="primary"):
        if len(transcript.strip()) < 20:
            st.warning("Bitte ein Transkript einfügen (min. 20 Zeichen).")
        else:
            with st.spinner("Claude fasst zusammen..."):
                try:
                    r = httpx.post(
                        f"{API_URL}/summarize",
                        json={
                            "transcript": transcript,
                            "meeting_title": meeting_title,
                        },
                        timeout=120.0,
                    )
                    r.raise_for_status()
                    data = r.json()

                    st.markdown("### 📋 Zusammenfassung")
                    st.write(data["summary"])

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(
                            f"### ✅ Action Items ({len(data['action_items'])})"
                        )
                        for item in data["action_items"]:
                            owner = item.get("owner") or "—"
                            deadline = item.get("deadline") or "—"
                            st.markdown(
                                f"- **{item['task']}**  \n"
                                f"  _Owner:_ {owner} · _Deadline:_ {deadline}"
                            )
                    with col2:
                        st.markdown(
                            f"### 🎯 Entscheidungen ({len(data['decisions'])})"
                        )
                        for d in data["decisions"]:
                            st.markdown(f"- {d}")

                        st.markdown(
                            f"### ❓ Offene Fragen ({len(data['open_questions'])})"
                        )
                        for q in data["open_questions"]:
                            st.markdown(f"- {q}")
                except httpx.HTTPError as e:
                    st.error(f"Fehler: {e}")

# ---------------------------------------------------------------------------
# Tab 3: Content adaptieren
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Content für verschiedene Kanäle adaptieren")
    st.write(
        "Ein Originaltext – angepasst an LinkedIn, Newsletter, "
        "Slack oder interne Doku."
    )

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
                    r = httpx.post(
                        f"{API_URL}/adapt",
                        json={"text": text, "channel": channel},
                        timeout=120.0,
                    )
                    r.raise_for_status()
                    data = r.json()

                    st.markdown(f"### Ergebnis für **{data['channel']}**")
                    st.markdown(data["adapted"])
                    st.code(data["adapted"], language="markdown")
                except httpx.HTTPError as e:
                    st.error(f"Fehler: {e}")

# ---------------------------------------------------------------------------
# Tab 4: Wissensbasis
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("Wissensbasis durchsuchen")
    st.write("Finde Anleitungen, Use Cases und Best Practices.")

    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Suchbegriff", value="")
    with col2:
        category = st.selectbox(
            "Kategorie",
            ["alle", "tool", "use_case", "best_practice"],
        )

    if query.strip():
        try:
            params = {"q": query}
            if category != "alle":
                params["category"] = category
            r = httpx.get(
                f"{API_URL}/knowledge/search",
                params=params,
                timeout=30.0,
            )
            r.raise_for_status()
            data = r.json()

            st.info(f"{data['count']} Treffer für '{query}'")

            for entry in data["results"]:
                st.markdown(
                    f"**{entry['title']}** — _{entry['category']}_"
                )
                if entry.get("tags"):
                    st.caption(f"Tags: {entry['tags']}")
        except httpx.HTTPError as e:
            st.error(f"Fehler: {e}")