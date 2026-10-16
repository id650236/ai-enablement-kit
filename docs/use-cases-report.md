# KI-Use-Cases nach Abteilung


## Abteilung: Operations

### 1. Automatische Kollisionswarnung-Triage
- **Pain Point:** Ingenieure verbringen Stunden damit, jede Kollisionswarnung manuell zu sichten und nach Dringlichkeit zu sortieren, obwohl viele Warnungen nach ähnlichen Kriterien bewertet werden können.
- **Lösung:** Claude analysiert eingehende Kollisionswarnungen (TCA, Pc-Wert, Objekttyp, Bahnparameter) automatisch via API, klassifiziert sie in Prioritätsstufen (kritisch/beobachten/ignorieren) und liefert eine strukturierte Begründung. Nur kritische Fälle landen sofort beim Ingenieur, der Rest wird gebündelt im Tagesreport.
- **Impact:** high | **Effort:** medium
- **Tools:** Anthropic Claude API, Space-Track.org API oder internes CDM-Feed, Python-Skript als Middleware, Slack oder E-Mail für Alert-Routing

### 2. Automatische Dokumentationserstellung für Conjunction Events
- **Pain Point:** Nach jeder geprüften Kollisionswarnung muss manuell ein Bericht erstellt werden: Bewertung, Entscheidung, Begründung. Das kostet pro Event 20-45 Minuten reine Schreibarbeit.
- **Lösung:** Claude generiert auf Basis strukturierter Eingaben (Pc-Wert, Satellit, Entscheidung des Ingenieurs, Manöver ja/nein) automatisch einen vollständigen Conjunction-Report im internen Format. Der Ingenieur gibt nur die Kerndaten ein und bestätigt den Entwurf – Schreibaufwand sinkt auf unter 5 Minuten.
- **Impact:** high | **Effort:** low
- **Tools:** Anthropic Claude API, Einfaches Web-Formular oder Notion/Confluence-Integration, Dokumentenvorlage als Prompt-Template

### 3. Täglicher KI-generierter Lagebericht für alle 40+ Satelliten
- **Pain Point:** Das Team muss täglich den Status aller Satelliten überblicken und intern kommunizieren. Die Zusammenfassung wird manuell erstellt und kostet täglich 1-2 Stunden.
- **Lösung:** Ein nächtlicher Cronjob zieht alle relevanten Telemetrie- und Warndaten, Claude fasst sie zu einem priorisierten Tagesbriefing zusammen: Welche Satelliten brauchen heute Aufmerksamkeit, welche Warnungen sind neu, was wurde gestern entschieden. Automatischer Versand morgens per Slack oder E-Mail an das gesamte Team.
- **Impact:** medium | **Effort:** low
- **Tools:** Anthropic Claude API, Python-Cronjob, Internes Telemetrie-API oder CSV-Export, Slack Webhook oder SMTP

### 4. KI-Assistent für Manöverentscheidungs-Support
- **Pain Point:** Bei kritischen Warnungen müssen Ingenieure schnell entscheiden, ob ein Ausweichmanöver sinnvoll ist. Die Abwägung (Treibstoffkosten, Bahnänderung, Risiko) erfolgt manuell und unter Zeitdruck.
- **Lösung:** Claude fungiert als strukturierter Sparringspartner: Der Ingenieur gibt die Warndaten ein, Claude listet systematisch Pro/Contra eines Manövers auf, berechnet qualitative Risikoabwägungen und verweist auf vergleichbare historische Ereignisse aus einer internen Wissensbasis. Keine autonome Entscheidung – aber schnellere, besser dokumentierte Entscheidungsfindung.
- **Impact:** high | **Effort:** medium
- **Tools:** Anthropic Claude API, Interne Datenbank vergangener Conjunction Events als Kontext, Einfaches Chat-Interface (z.B. Streamlit), Optionale RAG-Integration für historische Manöverdaten

### 5. Automatische Eskalations- und Benachrichtigungslogik
- **Pain Point:** Wenn eine Warnung kritisch wird, muss manuell entschieden werden, wer informiert werden muss (Führungsebene, Kunde, Behörde). Diese Kommunikation kostet Zeit und ist fehleranfällig.
- **Lösung:** Claude wertet die Schwere einer Kollisionswarnung aus und generiert automatisch passende Benachrichtigungsentwürfe für verschiedene Empfängergruppen (technisch für interne Teams, nicht-technisch für Management, formal für Behörden). Der Ingenieur prüft und sendet mit einem Klick – kein Formulieren unter Stress.
- **Impact:** medium | **Effort:** low
- **Tools:** Anthropic Claude API, E-Mail-Integration (SMTP oder SendGrid), Empfänger-Regelwerk als Konfigurationsdatei, Slack für interne Eskalation


## Abteilung: Marketing

### 1. Multi-Kanal Content-Transformation
- **Pain Point:** Ein Blogpost muss manuell in LinkedIn-Post, Newsletter-Abschnitt und weitere Formate umgeschrieben werden – das kostet pro Stück 1-2 Stunden zusätzliche Redaktionszeit.
- **Lösung:** Ein einfaches Web-Tool (z.B. Streamlit oder Notion-Integration), in das man den Rohtext einfügt und per Klick kanalspezifische Versionen generiert. Claude erhält für jeden Kanal einen festen System-Prompt mit Tonalität, Zeichenlimit und Format (z.B. LinkedIn: Hook + 3 Bullets + CTA, max. 1300 Zeichen). Output: alle Varianten auf einmal, kopierbereit.
- **Impact:** high | **Effort:** low
- **Tools:** Anthropic Claude API, Streamlit oder Make.com, Notion oder Google Docs als Ausgabe

### 2. Automatisierte Wettbewerbsanalyse mit Zusammenfassung
- **Pain Point:** Wöchentliche Wettbewerbsanalysen werden manuell recherchiert und zusammengefasst – repetitiv, zeitintensiv und oft inkonsistent in Struktur und Tiefe.
- **Lösung:** Ein automatisierter Workflow (z.B. via Make.com): Webseiten und Blogposts der Wettbewerber werden per RSS-Feed oder Scraper gesammelt, die Rohdaten an Claude übergeben, der daraus ein strukturiertes Briefing erstellt (Neue Produkte, Messaging-Änderungen, Kampagnen, Bewertung der Relevanz). Wöchentlicher Versand als E-Mail oder Slack-Nachricht.
- **Impact:** high | **Effort:** medium
- **Tools:** Anthropic Claude API, Make.com oder n8n, RSS-Feeds / Firecrawl oder Apify zum Scraping, Slack oder E-Mail für Ausgabe

### 3. Case Study Drafting aus Interview-Notizen
- **Pain Point:** Case Studies entstehen aus Kunden-Interviews, deren Notizen oder Transkripte erst mühsam in eine strukturierte Story umgewandelt werden müssen – oft dauert das mehrere Tage.
- **Lösung:** Rohe Interview-Notizen oder ein Transkript werden in Claude eingefügt. Claude erstellt daraus einen vollständigen Case-Study-Entwurf nach einem festen Template (Ausgangssituation, Herausforderung, Lösung, Ergebnis, Zitat). Der Entwurf ist direkt redigierbar und reduziert die Schreibzeit von Tagen auf Stunden.
- **Impact:** high | **Effort:** low
- **Tools:** Anthropic Claude API, Notion oder Google Docs Integration, Optional: Whisper API für Transkription von Audio-Interviews

### 4. SEO-optimierte Blogpost-Briefings auf Knopfdruck
- **Pain Point:** Vor dem Schreiben eines Blogposts fehlt oft ein strukturiertes Briefing mit Keyword-Fokus, Gliederung und Argumentationslogik – das kostet Recherche- und Planungszeit.
- **Lösung:** Eingabe: Thema + Zielgruppe + 2-3 Keywords. Claude generiert ein vollständiges Briefing: SEO-Titel-Optionen, Meta-Description, vorgeschlagene H2/H3-Struktur, Key Messages pro Abschnitt und interne Verlinkungshinweise. Das Briefing kann direkt als Schreibvorlage genutzt werden.
- **Impact:** medium | **Effort:** low
- **Tools:** Anthropic Claude API, Streamlit-Frontend oder Notion-Button-Integration

### 5. Newsletter-Personalisierung nach Segment
- **Pain Point:** Der Newsletter wird in einer Einheitsversion verschickt, obwohl die Empfänger unterschiedliche Rollen haben (z.B. Investoren, Kunden, Partner) – Relevanz und Öffnungsraten leiden darunter.
- **Lösung:** Aus einem Master-Newsletter-Text erstellt Claude automatisch 2-3 segmentspezifische Varianten mit angepasster Einleitung, priorisierten Inhalten und passendem CTA je Zielgruppe. Integration in bestehende Newsletter-Tools (z.B. Mailchimp) via API oder manueller Copy-Paste aus einem einfachen Tool.
- **Impact:** medium | **Effort:** medium
- **Tools:** Anthropic Claude API, Make.com oder Zapier, Mailchimp oder HubSpot


## Abteilung: Engineering

### 1. Automatisiertes PR-Review mit Claude
- **Pain Point:** Tägliche Pull-Request-Reviews kosten viel Zeit und blockieren den Flow anderer Entwickler, während sie auf Feedback warten.
- **Lösung:** GitHub Action, die bei jedem PR automatisch Claude aufruft, um Code auf häufige Probleme zu prüfen: Logikfehler, fehlende Fehlerbehandlung, Sicherheitslücken, Stil-Inkonsistenzen. Claude postet einen strukturierten Review-Kommentar direkt im PR, bevor ein Mensch schaut. Das Team reviewt dann nur noch den Claude-Kommentar und den Code gemeinsam – spart die erste Durchsicht.
- **Impact:** high | **Effort:** low
- **Tools:** Anthropic API (Claude), GitHub Actions, GitHub REST API

### 2. Test-Generierung aus bestehendem Code
- **Pain Point:** Tests schreiben ist zeitaufwendig und wird oft aufgeschoben, weil es repetitiv ist – besonders für Edge Cases und Boilerplate.
- **Lösung:** CLI-Tool oder VS-Code-Extension, die eine Funktion oder ein Modul an Claude schickt und Unit-Tests im verwendeten Framework (z.B. pytest, Jest) zurückbekommt. Claude analysiert die Signatur, Seiteneffekte und Kommentare und generiert Tests inklusive Edge Cases. Entwickler prüfen und ergänzen nur noch – statt von Null zu schreiben.
- **Impact:** high | **Effort:** low
- **Tools:** Anthropic API (Claude), VS Code Extension API oder einfaches CLI-Skript (Python/Node)

### 3. ADR-Generator für Architekturentscheidungen
- **Pain Point:** Architecture Decision Records (ADRs) werden oft nicht oder zu spät geschrieben, weil das Formulieren zeitaufwendig ist und der Kontext nach dem Meeting verloren geht.
- **Lösung:** Entwickler fügen nach einer Entscheidung stichpunktartig Kontext, Optionen und Ergebnis in ein einfaches Formular (Slack-Shortcut oder Web-UI) ein. Claude generiert daraus einen vollständigen, strukturierten ADR im Markdown-Format (Titel, Status, Kontext, Entscheidung, Konsequenzen) und legt ihn per API direkt im Git-Repo oder Confluence ab.
- **Impact:** high | **Effort:** medium
- **Tools:** Anthropic API (Claude), Slack API oder einfaches Web-Formular, GitHub API oder Confluence REST API

### 4. Semantische Suche in der internen Wissensbasis
- **Pain Point:** Die Suche in der internen Wissensbasis (Confluence, Notion, Docs) liefert schlechte Ergebnisse bei natürlichsprachigen Fragen – Entwickler finden relevante Infos oft erst nach langem Suchen oder fragen Kollegen.
- **Lösung:** Dokumente der Wissensbasis werden einmalig in Chunks aufgeteilt und als Embeddings in einer Vektordatenbank gespeichert. Bei einer Frage werden die relevantesten Chunks abgerufen und zusammen mit der Frage an Claude geschickt (RAG-Pattern). Claude antwortet präzise mit Quellenangabe. Zugang über Slack-Bot (/ask-kb) oder einfaches Web-Interface.
- **Impact:** high | **Effort:** medium
- **Tools:** Anthropic API (Claude), Vektordatenbank (z.B. Chroma oder Supabase pgvector), Confluence/Notion API, Slack API (optional)

### 5. Commit-Message- und Changelog-Generator
- **Pain Point:** Commit-Messages und Changelogs sind oft unvollständig oder inkonsistent, was späteres Debugging und Release-Kommunikation erschwert.
- **Lösung:** Git-Hook (pre-commit oder post-commit), der den aktuellen Diff an Claude schickt und eine strukturierte Commit-Message im Conventional-Commits-Format vorschlägt. Für Releases aggregiert ein Skript alle Commits seit dem letzten Tag und lässt Claude daraus einen lesbaren Changelog generieren – gegliedert nach Features, Fixes und Breaking Changes.
- **Impact:** medium | **Effort:** low
- **Tools:** Anthropic API (Claude), Git Hooks (Shell-Skript), einfaches Python- oder Node-Skript


## Abteilung: HR / People

### 1. Automatisches Bewerbungs-Screening mit Bewertungsmatrix
- **Pain Point:** Das manuelle Sichten von Bewerbungen kostet täglich mehrere Stunden und ist inkonsistent, da verschiedene Teammitglieder unterschiedliche Kriterien anlegen.
- **Lösung:** Claude analysiert eingehende Bewerbungen (PDF/Text) anhand einer vordefinierten Kriterienmatrix (Skills, Erfahrung, kultureller Fit) und erstellt pro Bewerbung eine strukturierte Zusammenfassung mit Scoring und Empfehlung (Einladen / Ablehnen / Warteliste). Das HR-Team sieht nur noch das aufbereitete Ergebnis und trifft die finale Entscheidung.
- **Impact:** high | **Effort:** low
- **Tools:** Anthropic Claude API, Make.com oder n8n (Automatisierung), E-Mail-Eingang oder ATS-Webhook (z.B. Personio)

### 2. KI-gestützter Interview-Leitfaden-Generator
- **Pain Point:** Vor jedem Erstinterview müssen passende Fragen vorbereitet werden – das kostet Zeit und die Qualität variiert je nach Interviewer.
- **Lösung:** Claude generiert auf Basis der Stellenbeschreibung und des Lebenslaufs des Kandidaten einen maßgeschneiderten Interviewleitfaden mit Einstiegsfragen, Tiefenfragen und Red-Flag-Indikatoren. Der Output wird als ausfüllbares Dokument bereitgestellt, das direkt im Interview genutzt werden kann.
- **Impact:** medium | **Effort:** low
- **Tools:** Anthropic Claude API, Notion oder Google Docs API, Einfaches Web-Formular (z.B. Typeform oder internes Tool)

### 3. Interner HR-Chatbot für Benefits- und Prozessfragen
- **Pain Point:** Das HR-Team beantwortet täglich dieselben Fragen zu Urlaubsregelungen, Benefits, Onboarding-Prozessen und internen Richtlinien – das bindet wertvolle Kapazität.
- **Lösung:** Ein Slack-Bot (oder Web-Widget) auf Basis von Claude, der auf eine kuratierte Wissensdatenbank (HR-Wiki, FAQ-Dokumente) zugreift und Mitarbeiterfragen sofort beantwortet. Unbekannte Fragen werden automatisch an das HR-Team eskaliert und gleichzeitig als Lücke im Wissensdokument markiert.
- **Impact:** high | **Effort:** medium
- **Tools:** Anthropic Claude API, Slack API, Notion oder Confluence als Wissensbasis, n8n oder Make.com

### 4. Automatisierte Onboarding-Dokumenten-Personalisierung
- **Pain Point:** Onboarding-Unterlagen müssen für jede neue Person manuell angepasst werden (Name, Rolle, Team, Startdatum, Ansprechpartner) – fehleranfällig und zeitintensiv.
- **Lösung:** Claude befüllt automatisch Onboarding-Templates mit den relevanten Daten der neuen Person und passt Texte kontextuell an (z.B. rollenspezifische Hinweise für Engineering vs. Sales). Die fertigen Dokumente werden direkt per E-Mail oder in Notion/Google Drive bereitgestellt.
- **Impact:** medium | **Effort:** low
- **Tools:** Anthropic Claude API, Google Docs API oder Notion API, Personio oder HR-System als Datenquelle, Make.com

### 5. Strukturierte Interview-Nachbereitung und Entscheidungsvorlage
- **Pain Point:** Nach Interviews werden Notizen unstrukturiert festgehalten, Feedbacks verschiedener Interviewer sind schwer vergleichbar und die Entscheidungsfindung zieht sich unnötig in die Länge.
- **Lösung:** Interviewer tippen oder diktieren ihr rohes Feedback nach dem Gespräch. Claude strukturiert es automatisch nach vordefinierten Kategorien (fachliche Eignung, Kommunikation, Motivation, Bedenken), fasst mehrere Interviewer-Feedbacks zusammen und erstellt eine Entscheidungsvorlage mit Pro/Contra-Übersicht für den Hiring Manager.
- **Impact:** medium | **Effort:** low
- **Tools:** Anthropic Claude API, Slack oder E-Mail als Input-Kanal, Notion oder Google Docs für Output, Optional: Whisper API für Sprach-zu-Text
