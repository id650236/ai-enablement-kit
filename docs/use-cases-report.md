# KI-Use-Cases nach Abteilung


## Abteilung: Operations

### 1. Automatische E-Mail-Kategorisierung und Weiterleitung
- **Pain Point:** 2 Vollzeitkräfte verbringen den Großteil ihrer Zeit damit, eingehende E-Mails manuell zu lesen, zu kategorisieren und weiterzuleiten – eine repetitive Aufgabe ohne Mehrwert.
- **Lösung:** Claude analysiert jede eingehende E-Mail automatisch, erkennt Kategorie (z.B. Beschwerde, Bestellung, Rückfrage, Reklamation), Dringlichkeit und leitet sie per Regel an den zuständigen Mitarbeiter weiter. Eine Zusammenfassung in 2-3 Sätzen wird direkt in die Weiterleitung eingefügt, damit der Empfänger sofort den Kontext hat.
- **Impact:** high | **Effort:** low
- **Tools:** Claude API (Anthropic), E-Mail-Webhook (z.B. via Gmail API oder Outlook Graph API), Make.com oder Zapier für Routing-Logik

### 2. Echtzeit-Gesprächsleitfaden für Telefon-Support
- **Pain Point:** Mitarbeiter im Telefon-Support müssen während des Gesprächs gleichzeitig zuhören, Informationen suchen und antworten – das führt zu langen Gesprächszeiten und inkonsistenter Qualität.
- **Lösung:** Ein einfaches Web-Interface, in das der Mitarbeiter das Gesprächsthema oder Stichwörter eingibt. Claude generiert sofort passende Antwortvorschläge, relevante interne Informationen und nächste Schritte. Nach dem Gespräch erstellt Claude automatisch eine strukturierte Gesprächsnotiz.
- **Impact:** medium | **Effort:** medium
- **Tools:** Claude API (Anthropic), Einfaches Web-Frontend (z.B. Streamlit oder internes Tool), Interne Wissensdatenbank als Kontext-Input

### 3. Automatische Antwort-Entwürfe für Standardanfragen
- **Pain Point:** Ein großer Teil der 50+ täglichen Anfragen sind wiederkehrende Standardfragen, die trotzdem manuell beantwortet werden und wertvolle Zeit kosten.
- **Lösung:** Claude erkennt Standardanfragen (z.B. Lieferstatus, Öffnungszeiten, Rückgabebedingungen) und erstellt einen fertigen, personalisierten Antwort-Entwurf im Tonfall der Muster GmbH. Der Mitarbeiter prüft den Entwurf mit einem Klick und sendet ihn ab – statt ihn von Grund auf zu schreiben. Ziel: Bearbeitungszeit pro E-Mail von ~8 Minuten auf ~1 Minute reduzieren.
- **Impact:** high | **Effort:** low
- **Tools:** Claude API (Anthropic), E-Mail-Client-Integration (Gmail/Outlook Add-in oder Make.com), Vorlagen-Dokument mit Unternehmenstonalität als System-Prompt

### 4. Intelligentes Priorisierungs-Dashboard
- **Pain Point:** Die manuelle Priorisierung von Anfragen ist subjektiv und fehleranfällig – dringende Kundenanliegen können untergehen, während unkritische Anfragen bevorzugt werden.
- **Lösung:** Claude bewertet jede eingehende Anfrage nach definierten Kriterien (Kundenwert, Eskalationsrisiko, Zeitkritikalität, Sentiment) und vergibt einen Prioritäts-Score. Ein einfaches Dashboard zeigt dem Team die Warteschlange sortiert nach Priorität – keine manuelle Einschätzung mehr nötig.
- **Impact:** medium | **Effort:** medium
- **Tools:** Claude API (Anthropic), Einfaches Dashboard (z.B. Notion, Airtable oder Streamlit), Webhook-Integration zum E-Mail-Postfach

### 5. Täglicher Anfragen-Report mit Trendanalyse
- **Pain Point:** Das Operations-Team hat keinen strukturierten Überblick darüber, welche Themen und Probleme sich häufen – Optimierungspotenziale bleiben unsichtbar.
- **Lösung:** Claude analysiert täglich alle bearbeiteten Anfragen, erkennt wiederkehrende Themen und Muster und erstellt automatisch einen kurzen Management-Report (1 Seite): Top-Themen des Tages, auffällige Häufungen, Empfehlungen zur Prozessverbesserung. Wird jeden Abend automatisch per E-Mail an die Teamleitung gesendet.
- **Impact:** medium | **Effort:** low
- **Tools:** Claude API (Anthropic), Datenexport aus E-Mail-System oder Ticketing-Tool, Make.com oder Python-Script für automatisierten Versand


## Abteilung: Marketing

### 1. Automatische Kanal-Adaption von Blogposts
- **Pain Point:** Jeder Blogpost muss manuell für LinkedIn und Newsletter umgeschrieben werden – das kostet pro Woche mehrere Stunden redaktionelle Arbeit.
- **Lösung:** Ein Claude-basiertes Tool nimmt den fertigen Blogpost als Input und generiert automatisch: eine LinkedIn-Version (max. 1300 Zeichen, Hook-Opener, 3 Hashtags) und eine Newsletter-Version (Betreffzeile + 150-Wort-Teaser). Der Redakteur prüft und veröffentlicht – kein Neuschreiben mehr.
- **Impact:** high | **Effort:** low
- **Tools:** Anthropic Claude API, Make.com oder n8n (Workflow-Automatisierung), Google Docs oder Notion als Input-Quelle

### 2. LinkedIn-Post-Generator aus Themen-Briefings
- **Pain Point:** 5 LinkedIn-Posts pro Woche erfordern kreative Energie und Zeit, obwohl die Kernbotschaften oft bereits in internen Briefings oder Blogposts vorhanden sind.
- **Lösung:** Claude erhält ein kurzes Themen-Briefing (3-5 Stichpunkte) und generiert 3 Varianten eines LinkedIn-Posts in unterschiedlichen Tonalitäten (informativ, provokant, storytelling). Das Team wählt eine Variante aus und passt sie minimal an.
- **Impact:** high | **Effort:** low
- **Tools:** Anthropic Claude API, Slack-Bot oder einfaches Web-Frontend (z.B. Streamlit)

### 3. Newsletter-Betreffzeilen-Optimierer
- **Pain Point:** Die Öffnungsrate der 2 wöchentlichen Newsletter hängt stark von der Betreffzeile ab, aber das Team testet selten Alternativen mangels Zeit.
- **Lösung:** Claude generiert zu jedem Newsletter automatisch 5 Betreffzeilen-Varianten (neugierig, nutzenorientiert, zahlenbasiert, Frage-Format, FOMO). Das Team wählt 2 für einen A/B-Test aus. Langfristig lernt das Team, welche Muster bei ihrer Zielgruppe funktionieren.
- **Impact:** medium | **Effort:** low
- **Tools:** Anthropic Claude API, Mailchimp oder HubSpot (für A/B-Tests), Make.com für Automatisierung

### 4. Content-Kalender-Assistent mit Themenvorschlägen
- **Pain Point:** Die wöchentliche Planung von 10+ Content-Stücken kostet Meetingzeit und führt oft zu Last-Minute-Themensuche.
- **Lösung:** Claude analysiert vergangene Blogposts, aktuelle Branchentrends (via RSS-Feed-Input) und saisonale Relevanz und schlägt jeden Montag automatisch 5 Themenideen mit Kanal-Zuordnung und Zielgruppen-Begründung vor. Output landet direkt in Notion oder einem Google Sheet.
- **Impact:** medium | **Effort:** medium
- **Tools:** Anthropic Claude API, n8n oder Make.com, RSS-Feed-Quellen, Notion oder Google Sheets

### 5. SEO-Optimierungs-Check für Blogposts
- **Pain Point:** Blogposts werden ohne systematische SEO-Prüfung veröffentlicht, weil kein dedizierter SEO-Spezialist im 5-köpfigen Team ist.
- **Lösung:** Claude analysiert jeden fertigen Blogpost und gibt strukturiertes Feedback: fehlendes Keyword-Vorkommen, zu langer/kurzer Meta-Description, fehlende interne Verlinkungsvorschläge, Lesbarkeits-Score und konkrete Verbesserungsvorschläge. Kein SEO-Fachwissen beim Nutzer nötig.
- **Impact:** medium | **Effort:** low
- **Tools:** Anthropic Claude API, Google Docs Add-on oder Notion-Integration, Optional: Google Search Console API für echte Keyword-Daten


## Abteilung: Engineering

### 1. Automatisches PR-Review mit Claude
- **Pain Point:** 20+ Pull Requests täglich binden enorm viel Entwicklerzeit und verzögern den Merge-Prozess.
- **Lösung:** GitHub Actions Workflow, der bei jedem PR automatisch die Claude API aufruft. Claude analysiert den Diff und liefert strukturiertes Feedback zu: Code-Qualität, potenziellen Bugs, Security-Risiken, fehlenden Tests und Stil-Verstößen. Das Ergebnis wird als PR-Kommentar gepostet, bevor ein Mensch reviewt. Entwickler sehen sofort offensichtliche Probleme und können sie beheben, bevor ein Kollege Zeit investiert.
- **Impact:** high | **Effort:** low
- **Tools:** Claude API (Anthropic), GitHub Actions, GitHub REST API

### 2. Architecture Decision Record (ADR) Generator
- **Pain Point:** Architekturentscheidungen werden entweder gar nicht oder inkonsistent dokumentiert, weil das Schreiben von ADRs zeitaufwendig ist.
- **Lösung:** Entwickler füllen ein kurzes Slack-Formular oder ein einfaches Web-Formular aus (Problem, gewählte Lösung, verworfene Alternativen – Stichpunkte reichen). Claude generiert daraus ein vollständiges, strukturiertes ADR-Dokument im Markdown-Format und legt es automatisch per GitHub API im /docs/adr-Ordner des Repos als PR an. Der Entwickler muss nur noch approven.
- **Impact:** high | **Effort:** low
- **Tools:** Claude API (Anthropic), GitHub REST API, Slack API oder einfaches Web-Formular (z.B. Typeform)

### 3. PR-Beschreibung automatisch generieren
- **Pain Point:** Entwickler schreiben oft unvollständige oder fehlende PR-Beschreibungen, was Reviews verlangsamt, weil Kontext fehlt.
- **Lösung:** Ein Git-Hook oder GitHub Action liest den Diff und den Branch-Namen und ruft Claude auf, um automatisch eine strukturierte PR-Beschreibung zu generieren (Was wurde geändert? Warum? Wie testen?). Diese wird als Vorschlag in die PR-Beschreibung eingefügt. Der Entwickler kann sie anpassen oder direkt übernehmen.
- **Impact:** medium | **Effort:** low
- **Tools:** Claude API (Anthropic), GitHub Actions, GitHub REST API

### 4. Review-Kommentar-Zusammenfassung für PR-Autoren
- **Pain Point:** Bei PRs mit vielen Review-Kommentaren verlieren Entwickler den Überblick, was wirklich geändert werden muss.
- **Lösung:** Wenn ein PR als 'Changes Requested' markiert wird, ruft eine GitHub Action Claude auf, um alle Review-Kommentare zu aggregieren und eine priorisierte To-do-Liste zu erstellen (Blocker vs. Nice-to-have). Diese wird als zusammenfassender Kommentar an den PR-Autor gepostet. Spart Zeit beim Durcharbeiten langer Review-Threads.
- **Impact:** medium | **Effort:** low
- **Tools:** Claude API (Anthropic), GitHub Actions, GitHub REST API

### 5. Wöchentlicher Architektur-Digest aus PRs und ADRs
- **Pain Point:** Technische Entscheidungen und Änderungen gehen im Tagesgeschäft unter; das Team verliert den Überblick über die Gesamtarchitektur.
- **Lösung:** Ein wöchentlicher Cron-Job sammelt alle gemergten PRs und neuen ADRs der Woche und schickt sie an Claude. Claude erstellt eine kompakte Zusammenfassung: wichtigste Änderungen, getroffene Architekturentscheidungen, offene technische Schulden. Das Ergebnis wird automatisch in den Engineering-Slack-Kanal gepostet. Kein manueller Aufwand, volle Transparenz.
- **Impact:** medium | **Effort:** medium
- **Tools:** Claude API (Anthropic), GitHub REST API, Slack API, Cron-Job (z.B. GitHub Actions Scheduler oder einfacher Server-Cronjob)


## Abteilung: HR / People

### 1. Automatisches Bewerbungs-Screening mit Bewertungsmatrix
- **Pain Point:** 50+ Bewerbungen pro Woche manuell sichten kostet das 5-köpfige Team enorm viel Zeit und führt zu inkonsistenten Bewertungen.
- **Lösung:** Claude analysiert eingehende Bewerbungen (CV + Anschreiben) automatisch anhand vordefinierter Kriterien (Muss- und Kann-Anforderungen je Stelle) und erstellt eine strukturierte Bewertungsübersicht mit Punktzahl, Stärken, Lücken und einer Go/No-Go-Empfehlung. Das HR-Team sieht nur noch die Zusammenfassung und entscheidet in Sekunden.
- **Impact:** high | **Effort:** medium
- **Tools:** Claude API (Anthropic), Make.com oder n8n (Automatisierung), E-Mail-Eingang oder ATS-Webhook (z.B. Personio, Recruitee)

### 2. KI-Chatbot für Benefits- und Onboarding-Fragen
- **Pain Point:** Täglich wiederkehrende Fragen zu Benefits, Urlaubsregelungen und Onboarding-Prozessen binden HR-Kapazitäten, die für strategische Aufgaben fehlen.
- **Lösung:** Ein interner Chatbot auf Basis von Claude beantwortet Mitarbeiterfragen rund um die Uhr – gespeist aus einem HR-Wissensdokument (FAQ, Handbuch, Benefit-Übersicht). Der Bot eskaliert nur bei unbekannten Fragen an das HR-Team und lernt durch neue Einträge im Dokument dazu. Umsetzbar z.B. als Slack-Bot oder einfaches Web-Widget.
- **Impact:** high | **Effort:** low
- **Tools:** Claude API (Anthropic), Slack API oder Web-Widget, Notion / Google Docs als Wissensbasis, n8n oder Make.com

### 3. Automatische Erstellung personalisierter Absage- und Einladungs-E-Mails
- **Pain Point:** Das manuelle Verfassen von Absagen und Interview-Einladungen für Dutzende Kandidaten pro Woche ist repetitiv und fehleranfällig (falscher Name, falsche Stelle).
- **Lösung:** Claude generiert auf Basis der Bewerberdaten (Name, Stelle, Ergebnis des Screenings) individuell formulierte, wertschätzende Absagen oder Einladungen. Die Texte wirken persönlich, nicht wie Vorlagen. Das HR-Team prüft und sendet mit einem Klick – oder aktiviert vollautomatischen Versand für klare No-Gos.
- **Impact:** medium | **Effort:** low
- **Tools:** Claude API (Anthropic), Make.com oder n8n, E-Mail-Provider (Gmail, Outlook) oder ATS

### 4. KI-gestütztes Erstellen von Stellenausschreibungen
- **Pain Point:** Neue Stellenausschreibungen werden von Hand formuliert, was Zeit kostet und oft zu inkonsistenter Sprache oder fehlenden Inhalten führt.
- **Lösung:** HR gibt in einem einfachen Formular die Eckdaten ein (Rolle, Team, Muss-Skills, Gehaltsspanne, Remote-Policy). Claude erstellt daraus eine vollständige, ansprechende Stellenausschreibung im Muster-GmbH-Tone-of-Voice – inklusive Aufgaben, Anforderungen und Benefits-Abschnitt. Das Team überarbeitet nur noch, statt von Null zu starten.
- **Impact:** medium | **Effort:** low
- **Tools:** Claude API (Anthropic), Einfaches Web-Formular (z.B. Tally, Typeform) oder Notion-Integration

### 5. Automatische Zusammenfassung und Strukturierung von Interview-Notizen
- **Pain Point:** Nach Interviews liegen unstrukturierte Notizen vor, die aufwändig in vergleichbare Bewertungsbögen übertragen werden müssen – besonders bei mehreren Interviewern.
- **Lösung:** Interviewer diktieren oder tippen ihre rohen Notizen nach dem Gespräch. Claude strukturiert diese automatisch in ein einheitliches Format (Stärken, Bedenken, Kulturfit, Empfehlung) und erstellt eine Zusammenfassung, die direkt ins ATS oder eine geteilte Tabelle geschrieben wird. So sind alle Bewertungen vergleichbar.
- **Impact:** medium | **Effort:** low
- **Tools:** Claude API (Anthropic), Slack-Shortcut oder Web-Formular als Eingabe, Google Sheets oder ATS-Integration via n8n
