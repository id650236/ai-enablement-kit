# KI-Use-Case-Analyse für OKAPI:Orbits

**Durchgeführt von:** Arnaud Fotsa
**Datum:** 16.10.2026
**Methodik:** KI-gestützte Workflow-Analyse (Claude Agent)
**Umfang:** 4 Abteilungen × 5 Use-Cases = 20 identifizierte Potenziale

## Executive Summary

Die Analyse identifiziert **20 konkrete KI-Use-Cases** über Operations,
Marketing, Engineering und HR. Davon sind:

- **8 Quick Wins** (Impact high/medium, Effort low) → in Tagen umsetzbar
- **7 mittelfristige Projekte** (Effort medium) → in Wochen umsetzbar
- **5 strategische Initiativen** (Impact high, Effort medium)

## Top-3-Empfehlungen für den Start

### 1. Automatische Dokumentationserstellung (Operations)
- **Effort:** low | **Impact:** high
- **Nutzen:** 20–45 Min Schreibarbeit pro Conjunction Event → unter 5 Min
- **Umsetzung:** Claude API + einfaches Web-Formular

### 2. Multi-Kanal Content-Transformation (Marketing)
- **Effort:** low | **Impact:** high
- **Nutzen:** 1–2 Stunden Redaktionszeit pro Blogpost → Minuten
- **Umsetzung:** Claude API + Streamlit-Tool

### 3. Automatisiertes PR-Review (Engineering)
- **Effort:** low | **Impact:** high
- **Nutzen:** Erste Review-Runde automatisiert, Team reviewt nur noch den Output
- **Umsetzung:** Claude API + GitHub Action

## Nächste Schritte

1. **Woche 1–2:** Quick Wins umsetzen (3 Use Cases, je 1–2 Tage)
2. **Woche 3–4:** Pilotierung mit einem Team, Feedback einholen
3. **Woche 5–8:** Rollout der mittelfristigen Projekte
4. **Laufend:** Wissensbasis aufbauen, Enablement-Sessions

## Methodik (Transparenz)

- Workflow-Beschreibungen aus 4 Abteilungen als Input
- Claude-basierter `UseCaseDiscoverer`-Agent mit Pydantic-Validierung
- Strukturierte Outputs (Impact/Effort-Matrix, Tool-Empfehlungen)
- Reproduzierbar: jedes Ergebnis ist mit einem Befehl neu generierbar

## Anhang

Vollständiger Report: `docs/use-cases-report.md`
Agent-Code: `src/agents/discoverer.py`