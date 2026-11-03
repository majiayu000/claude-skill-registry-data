---
name: surface-after-care
version: 1.6.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-24
aliases: [repo-after-care, repo-pflege, after-care, repo-nachpflege, repo-wartung]
description: >
  Regelmäßiger Pflegedurchlauf für ein bereits veröffentlichtes GitHub-Repository (Stufe 1,
  günstig und oft wiederholbar): zuerst alle Distributionsflächen des Projekts ermitteln
  (npm, PyPI, Registries, Marketplaces, Stores, Website) und Änderungen später dorthin spiegeln,
  dann Topics setzen, Privacy-Gate, Dokumente auf Veröffentlichungsabsicht prüfen und interne
  Planungsdateien nachträglich ignorieren, Banner ergänzen, Aussagen im README gegen den echten
  Code-Stand abgleichen, Darstellung verbessern, Sprachfassungen der README vervollständigen,
  Sichtbarkeitsmaßnahmen umsetzen, Eintrag auf der Organisationsseite prüfen sowie offene
  Issues und Pull Requests abarbeiten.
  Nutze diesen Skill, wenn ein bestehendes Repo gepflegt, aufgeräumt, aktualisiert, aufgehübscht
  oder "mal wieder durchgesehen" werden soll, wenn ein Repo veraltet oder unaufgeräumt wirkt,
  bei Formulierungen wie "Repo-Pflege", "after care", "Nachpflege", "Repo auf Stand bringen",
  "aufräumen und pushen" oder bei rotierenden Qualitätsrunden über mehrere Repos.
  Für die tiefe Runde inkl. Rechtscheck und orga-übergreifenden Querverweisen stattdessen
  full-after-care nutzen; für die Erstveröffentlichung github-repo-care.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, privacy, i18n, documentation, visibility, issues]
language: de
status: active
visibility: public

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="surface-after-care banner">
# Surface After Care — die regelmäßige Pflegerunde für ein veröffentlichtes Repo

## Wann dieser Skill greift

Nutze ihn für ein Repository, das **bereits öffentlich ist** und turnusmäßig durchgesehen werden soll. Er ist die günstige Stufe: alles, was sich am Repo selbst entscheiden lässt, ohne fremde Repos zu inventarisieren oder ein Rechtsgutachten anzustoßen.

Abgrenzung zu den Nachbarskills:

| Situation | Skill |
|---|---|
| Repo wird zum ersten Mal veröffentlicht | `github-repo-care` |
| Repo ist public, regelmäßige Pflegerunde | **dieser Skill** |
| Zusätzlich Rechtscheck + Querverweise über alle Orgas + App-i18n | `full-after-care` (Alias `deep-after-care`) |
| Reine Rechts-/Privacy-/Lizenzprüfung vor dem Public-Stellen | `repo-publish-check` |
| Sprachfassungen inhaltlich synchron halten | `bilingual-doc-sync` |
| Verteilung dieser Runde über viele Repos, fair rotierend | `rotation-check` |

## Kernidee

Ein veröffentlichtes Repo driftet in zwei Richtungen auseinander: **Die Doku beschreibt eine ältere Software als die, die im Repo liegt**, und **es sammeln sich Dateien an, die nie für fremde Augen gedacht waren**. Beides ist selten dramatisch, aber beides kostet genau die Nutzer, die man gewinnen will — der eine springt ab, weil die Installationsanleitung nicht mehr passt, der andere, weil er im Wurzelverzeichnis auf `AUFGABEN.txt` und `Plan.txt` stößt und den Eindruck bekommt, hier arbeite jemand nur für sich selbst.

Diese Runde räumt beides auf. Sie ist bewusst wiederholbar: lieber viermal im Jahr eine halbe Stunde als einmal ein Großputz.

## Ablauf

Die Reihenfolge ist nicht willkürlich. Schritt 0 steht am Anfang, weil er den Umfang aller folgenden Schritte bestimmt. Schritt 2 läuft vor allem, was Änderungen pusht — sonst schiebt man Verbesserungen über einen Stand, der erst noch bereinigt werden muss. Schritt 1 ist rein serverseitig und stört dabei nicht.

### 0. Distributionsflächen inventarisieren

**Bevor irgendetwas geändert wird: klären, wo dieses Projekt überall liegt.** Das GitHub-Repo ist selten die einzige Fläche. Eine korrigierte README nützt wenig, wenn die npm-Paketseite weiter die alte Fassung mit der falschen Installationsanweisung zeigt — und genau dort landen die meisten Nutzer, denn Paketregister ranken in Suchmaschinen oft besser als das Repo.

```bash
# Manifeste verraten die Kanäle
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Veröffentlichten Stand der Kanäle abfragen (nur was zutrifft)
npm view <paket> version description keywords 2>/dev/null
pip index versions <paket> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

Typische Flächen: npm, PyPI, Crates, Docker Hub, MCP-Registry, Plugin-/Skill-Verzeichnisse, VS-Code- oder Browser-Marketplaces, App-Stores, Zenodo/DOI, Projektwebsite, Organisationsprofil, `llms.txt`, Spiegel-Repos auf anderen Hosts.

Notiere die gefundene Liste im Laufprotokoll. Sie ist ab jetzt die **Zielmenge**: Jede Änderung aus den folgenden Schritten wird am Ende gegen diese Liste gespiegelt (siehe „Parität über alle Flächen"). Findest du eine Fläche, die niemand mehr pflegt und die auf einen toten Stand zeigt, ist das ein eigener Befund — entweder aktualisieren oder bewusst zurückziehen, aber nicht stehen lassen.

### 1. Topics setzen

Topics sind die wichtigste Suchfläche innerhalb von GitHub und kosten fast nichts.

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

Ziel sind ungefähr 5–12 Topics aus drei Richtungen: **was es ist** (`cli`, `mcp-server`, `python-library`), **worum es geht** (`file-management`, `tax`, `note-taking`) und **wie es arbeitet** (`local-first`, `offline`, `privacy`). Orientiere dich an Topics, die bei vergleichbaren Projekten tatsächlich verwendet werden — erfundene Topics finden keine Nutzer. Description und Homepage gleich mitprüfen, sie stehen in derselben Ansicht.

Topics haben auf den anderen Flächen aus Schritt 0 ein Pendant: `keywords` in `package.json`, `keywords`/`classifiers` in `pyproject.toml`, Kategorien und Tags in Marketplaces und Stores. Halte sie inhaltlich gleich — sie sind dieselbe Entscheidung, nur an mehreren Orten.

### 2a. Privacy-Gate — läuft immer

Dieser Schritt entfällt nie, auch nicht bei einer scheinbar harmlosen Runde. Gesucht wird im **getrackten** Set, nicht im sichtbaren Arbeitsbaum, denn genau das ist der Unterschied zwischen "sieht sauber aus" und "ist sauber".

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

Ergänze das Muster um die **Namen deiner eigenen internen Ablagen** — Pipeline-Ordner, Themenverzeichnisse, private Arbeitsbereiche:

```bash
rg -n "\.SOFTWARE|\.RESEARCH|_control-center|<weitere eigene Ordnernamen>" $(git ls-files)
```

Solche Verweise sind keine Secrets und lösen keinen Alarm aus, deshalb rutschen sie durch — aber sie sind für Leser **unauflösbar** („zurückübertragen aus der .SOFTWARE-Pipeline" sagt Fremden nichts) und geben die eigene Struktur preis. Sie werden ersetzt oder entfernt, nicht bloß toleriert. Eine Suche, die nur nach `C:\Users\…` und Token-Mustern fahndet, findet sie garantiert nicht.

Fündig geworden? Dann entscheidet die **Art** des Fundes über das Vorgehen — siehe Abschnitt „Force-Push-Regel". Ein Secret, das jemals committet wurde, ist verbrannt: Entfernen aus `HEAD` genügt nicht, es muss rotiert werden.

### 2b. Veröffentlichungsabsicht der Dokumente prüfen

Der eigentliche Kern dieser Runde. Gehe die getrackten `.md`, `.txt` und `.json` durch und frage bei jeder Datei: **War die je für Fremde gedacht?**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

Nicht anhand des Dateinamens raten — kurz hineinsehen. Ein `PLAN.md` kann eine öffentliche Roadmap sein, ein harmlos klingendes `notes.md` die interne Preisstrategie. Drei Kategorien:

**Gehört ins Repo** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, API-Referenzen, Beispiel-Configs, echte Roadmaps, Manifeste (`package.json`, `pyproject.toml`), Lockfiles, CI-Konfiguration.

**Gehört nicht ins Repo, ist aber unkritisch** — der Normalfall dieser Runde. Aufgaben- und Planungsdateien (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`), Session-Notizen und Übergaben (`HANDOFF`, `BRIEFING`, `_handoff/`), Statusdateien der eigenen Pipeline, Entwicklungstagebücher, `_archive/`, Registry- und Index-JSONs mit lokalen Pfaden, Zwischenstände und generierte Artefakte, Agenten-Arbeitsdateien. Solche Dateien sind nicht gefährlich, aber sie erzeugen Unübersichtlichkeit und den Eindruck einer fremden Baustelle. Behandlung: `.gitignore` ergänzen, `git rm --cached <datei>` und **ganz normal pushen**.

**Gehört nicht ins Repo und ist heikel** — Credentials, personenbezogene Daten, Kundendaten, interne Kalkulationen, Preis- und Verhandlungsstrategien, unveröffentlichte Geschäftspläne, Vertragsentwürfe, alles mit Wettbewerbswert. Hier reicht ein normaler Commit nicht, siehe Force-Push-Regel.

Bei `.json` lohnt ein zweiter Blick: Manifeste und Lockfiles bleiben, aber lokale Configs, Task-/Registry-Dateien, Export-Dumps und alles mit absoluten Pfaden oder Hostnamen sind typische blinde Passagiere.

Wenn du eine Datei entfernst, die jemand suchen könnte (eine Roadmap etwa), erwähne im Commit oder im README kurz, wo die Information jetzt lebt — sonst wirkt es wie ein Rückschritt.

### 3. Banner

Ein Banner entscheidet mit darüber, ob jemand überhaupt anfängt zu lesen. Prüfe, ob eines existiert und im README als erstes Element eingebunden ist.

Fehlt es, gibt es drei Wege — in dieser Reihenfolge sinnvoll:

1. **Bildgenerator eines Agenten** (z. B. agy; das Wort „generiere" ist dort der Trigger für echte PNG-Erzeugung), wenn ein Bildmotiv besser passt als Typografie.
2. **Codex**, wenn das Banner aus Code entstehen soll und ein Stilvorbild existiert, an dem es sich orientieren kann.
3. **Selbst als SVG**, wenn das Banner primär Wortmarke plus Formsprache ist — das ist oft die schnellste und am besten kontrollierbare Variante, und SVG bleibt später änderbar.

Halte die Familie ein, wenn das Projekt zu einer Gruppe gehört: gleiche Grundfarbe, gleiche Ästhetik, gleiche Wortmarken-Behandlung. Ein Banner, das aus der Reihe fällt, wirkt schlechter als keines. Übliche Größe 1200x300; als PNG ins Repo, das SVG als Quelle daneben.

### 4. Aussagen gegen den echten Stand abgleichen

Hier entsteht der meiste Wert. Das README behauptet Dinge — prüfe sie nach, statt sie zu glauben:

- **Version** im README/Badge gegen `pyproject.toml`/`package.json`/`__version__` und gegen den letzten Release-Tag. Bei mehreren Versionsträgern alle prüfen, nicht nur einen.
- **Installationsweg** wirklich durchspielen, zumindest lesend: Existiert das Paket unter dem genannten Namen? Stimmen Kommandos und Flags?
- **Feature-Liste** gegen den Code: Ist alles Genannte da, und fehlt Neues in der Liste?
- **Zahlen** (Anzahl Tools, unterstützte Formate, Testabdeckung) an der Quelle nachzählen statt fortzuschreiben. Zahlen im README veralten still.
- **Screenshots** gegen die aktuelle Oberfläche.
- **Requirements** (Python-/Node-Version, Abhängigkeiten) gegen die Manifeste.
- **Links** auf Nachbarprojekte, Doku und Registries: laufen sie noch?

**Eine Korrektur gilt für alle Flächen, nicht nur für die, auf der sie auffiel.** Wenn sich eine inhaltliche Aussage als falsch erweist — besonders wenn der Auftraggeber sie richtigstellt —, dann steht dieselbe Aussage mit hoher Wahrscheinlichkeit noch anderswo: im Organisationsprofil, in der `llms.txt`, in der zweiten Sprachfassung, im README eines Nachbarprojekts. Suche gezielt danach, bevor du den Punkt abhakst:

```bash
gh search code "<prägnante Formulierung>" --owner ORG
```

Sonst korrigierst du eine Stelle und lässt drei stehen — und der Widerspruch fällt erst auf, wenn das nächste Repo an die Reihe kommt. Das kostet nicht nur Zeit, es beschädigt auch das Vertrauen in die Doku: Wer zwei Beschreibungen derselben Sache findet, glaubt keiner mehr.

Anschließend die **Darstellung** verbessern, wo sie schwach ist: lange Aufzählungen von Optionen werden als Tabelle lesbarer; Codeblöcke brauchen Sprach-Tags; eine Struktur- oder Ablaufübersicht ist als Mermaid-Diagramm oder ASCII-Baum schneller erfasst als in Prosa; die erste Bildschirmhöhe sollte Zweck, Installation und ein Nutzungsbeispiel zeigen, nicht Badges und Vorgeschichte. Wenn das README über ~400 Zeilen geht, lagere Details nach `docs/` aus und verlinke.

**Sprachregel für READMEs:** Standard ist eine **englische `README.md`** plus **deutsche Zweitfassung**. Ausnahme: Der Gegenstandsbereich der Anwendung ist selbst deutsch (deutsches Recht, deutsches Steuer- oder Förderwesen, deutschsprachige Zielgruppe) oder es existiert bisher ausschließlich eine deutsche Fassung — dann bleibt Deutsch die Hauptsprache. Für jede weitere Sprache, die das Projekt bereits spricht, gehört eine eigene README-Fassung dazu. Halte dich an die im Repo schon verwendete Namenskonvention (`README_de.md`, `README.de.md`, `docs/README.de.md`) und erfinde keine zweite daneben. Verlinke die Fassungen gegenseitig in der Kopfzeile.

### 6. Fehlende Standardsprachen anlegen

Ergänze die READMEs, die von den **Standardsprachen** fehlen: Deutsch, Englisch, Spanisch, vereinfachtes Chinesisch, Japanisch, Russisch. Der Zweck ist Reichweite, deshalb gilt das vor allem für nutzernahe Projekte — bei einer entwicklernahen Bibliothek mit rein englischem Publikum ist eine russische README kein Gewinn, sondern nur weitere Pflegelast. Entscheide bewusst und halte die Entscheidung im Laufprotokoll fest, damit die nächste Runde sie nicht neu diskutiert.

Neue Fassungen werden **befüllt, nicht angelegt und leer gelassen** — ein Stub mit „TODO: translate" ist schlechter als gar keine Datei, weil er Vollständigkeit vortäuscht. Inhaltliche Parallelität und Rückangleichung regelt `bilingual-doc-sync`; bei mehr als zwei Fassungen lohnt es sich, diesen Skill für den Abgleich hinzuzuziehen.

### 7. Sichtbarkeit und Werbung

Ueberlege, welche Maßnahmen für **dieses** Projekt tatsächlich Nutzer bringen, und setze sie um:

- **Registries**, in die das Projekt technisch gehört: Paketregister (npm, PyPI), MCP-Registry, Plugin-/Skill-Verzeichnisse, Marketplaces.
- **Kuratierte Listen** (`awesome-*` und thematische Sammlungen), sofern die Aufnahmekriterien wirklich erfüllt sind. Ein PR an eine Liste, deren Kriterien das Projekt verfehlt, kostet Reputation.
- **Eigene Flächen**: Organisationsprofil, `llms.txt`, Projektwebsite, README des Oekosystems, Verweise aus verwandten eigenen Repos.
- **Release-Notes** als Anlass: Ein Release ohne erzählte Neuerung wird nicht wahrgenommen.

**Freigabe-Gate:** Alles, was nach außen geht — PRs an fremde Repos, Einträge in fremde Listen, Posts, Einreichungen — wird **vorgeschlagen und erst nach ausdrücklicher Freigabe ausgeführt**, sofern keine Dauerfreigabe für diesen Kanal existiert. Änderungen an eigenen Flächen brauchen dieses Gate nicht. Der Grund ist schlicht: Ein zurückgezogener PR an ein fremdes Repo ist öffentlich sichtbar und fällt auf das Projekt zurück.

### 8. Eintrag auf den Organisationsseiten

Zuerst die eigene Organisation: Ist das Repo im Profil-README (`ORG/.github` → `profile/README.md`) überhaupt aufgeführt, in der richtigen Rubrik, mit aktueller Beschreibung?

```bash
gh api user/orgs --jq '.[].login'
```

Dann durch **alle** Organisationen gehen und je Organisation eine einzige Frage beantworten: Würde ein Besucher dieser Organisationsseite von diesem Repo profitieren? Meist lautet die Antwort nein — dann ist „nicht verlinken" das richtige Ergebnis und keine Lücke. Wo die Antwort ja lautet (thematische Nähe, gemeinsame Nutzer, ein Werkzeug, das die dortigen Projekte ergänzt), setze den Verweis mit einer Zeile, die den Nutzen erklärt, nicht nur den Namen nennt.

Das Profil liegt in einem eigenen Repo (`ORG/.github`). Änderungen dort werden mitgepflegt und gepusht — nach der Dirty-Tree-Regel aus Schritt 11.

### 10. Issues und Pull Requests

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

Arbeite sie durch statt sie nur zu zählen:

- **Fixbare Bugs** direkt beheben — in dieser Runde ist der Kontext ohnehin geladen. Kleine, klar umrissene Fixes mit Test und Verweis auf die Issue-Nummer.
- **Bereits erledigte Issues** schließen, mit einem Satz, was sie gelöst hat.
- **Unklare Meldungen** brauchen eine gezielte Rückfrage (Version, Betriebssystem, Reproduktionsschritte).
- **PRs**: Diff wirklich lesen, Tests laufen lassen, dann mergen oder begründet zurückmelden. Ein PR, der monatelang unbeantwortet liegt, kostet mehr Wohlwollen als eine höfliche Ablehnung.
- **Stale-Fälle** auflösen statt weiterschleppen.

**Freigabe-Gate:** Öffentliche Kommentare, Schließungen mit Begründung und Merges fremder Beiträge sind Kommunikation nach außen — vor der Ausführung vorlegen, sofern keine Dauerfreigabe besteht. Reine Code-Fixes im eigenen Repo sind davon nicht betroffen.

### 11. Committen, pushen, verifizieren

Die Runde endet nicht mit den Änderungen, sondern damit, dass sie **draussen sind**. Ein Arbeitsbaum voller ungepushter Verbesserungen ist das schlechteste Ergebnis: Die nächste Session — möglicherweise ein anderer Agent oder ein anderes Gerät — muss sich erst in einen fremden, halbfertigen Stand einarbeiten, und auf den öffentlichen Flächen hat sich nichts verbessert.

Vor dem Push kurz absichern, was überprüfbar ist: Tests und Smokes laufen lassen, bei Doku-Änderungen die Links und die gerenderte Ansicht prüfen. Dann in **thematisch getrennten Commits** bündeln, statt alles in einen Sammel-Commit zu werfen — Aufräumen, Doku-Aktualisierung und Bugfixes sind drei verschiedene Dinge, und wer später einen davon zurückdrehen will, ist dankbar dafür:

```bash
git add .gitignore && git rm --cached <interne dateien>
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git commit -am "docs: README auf aktuellen Stand (Version, Toolzahl, Screenshots)"
git commit -am "fix: <Issue-Nummer> ..."

git pull --rebase        # bei divergiertem Branch, vor dem Push
git push
```

Danach verifizieren statt annehmen: Remote-README in der gerenderten Ansicht, CI-Lauf, Release- und Tag-Stand.

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

**Wenn die CI rot ist, obwohl dein Commit nur Doku anfasste**, liegt die Ursache fast nie an dir. Der mit Abstand häufigste Fall — bei dieser Repo-Familie an einem einzigen Tag **dreimal** getroffen — ist ein **ungepinnter Linter ohne festgeschriebenen Regelsatz**. Prüfe das **zuerst**, bevor du irgendetwas an deinem Commit vermutest.

Der Mechanismus: Läuft im Workflow `ruff check` (oder flake8, eslint …) gegen eine ungepinnte Dependency (`ruff>=0.12`, oder gar keine Version), und fehlt eine explizite Regel-Auswahl (`[tool.ruff.lint] select = [...]`, bei fehlendem `pyproject.toml` eine eigene `ruff.toml`), dann folgt der Lint dem Default der **jeweils frisch installierten** Version. Ein neues Linter-Release verschiebt diesen Default, und eine unveränderte Codebasis wird rot. Die Verräter:

- Regel-Codes, die das Projekt nie hatte (`UP045`, `UP006`, `BLE001`, `RUF100`, `DTZ005`, `N999` …), teils in dreistelliger Zahl.
- Der Bruch fällt oft **plattform-gespalten** aus: Runner mit gecachter älterer Version bleiben grün, frische werden rot.
- Manchmal beanstandet eine Regel etwas Unbehebbares (`N999` den Paketnamen selbst) — sicheres Zeichen, dass sie nie Standard war.

Fix: den Regelsatz festschreiben, der vorher grün war — `select = ["E4","E7","E9","F"]` sind die klassischen ruff-Defaults. Existiert kein `pyproject.toml`, lege eine `ruff.toml` an. Verifiziere gegen die **neue** Linter-Version selbst (installieren, ohne Config die Funde reproduzieren, mit Config „passed"). Die neuen Regeln kommen als **Aufgabe** ins Projekt — bewusst übernehmen ist eine Entscheidung, kein Nebeneffekt eines Tool-Updates. Das ist ein echter, wiederkehrender Befund: Ohne den Pin bricht die CI beim nächsten Linter-Release wieder, und zwar in **jedem** so konfigurierten Repo.

Zwei Fälle, in denen **nicht** gepusht wird: wenn für das Projekt eine Veröffentlichungs- oder Einreichungssperre gilt, oder wenn der Stand erklärtermaßen unfertig ist. Beides sind Ausnahmen, die man begründet — der Normalfall ist: committen und pushen.

Bei einer Veröffentlichungssperre wird die Runde nicht abgebrochen, sondern **umgeleitet**: auf einem eigenen Branch (`judging-hold/…`, `freeze/…`) lokal committen, den Hauptbranch unangetastet auf dem eingereichten Stand lassen, den Sperrgrund im Laufprotokoll vermerken und nach Aufhebung nachziehen. Wichtig ist dabei, konsequent zu sein: Gesperrt ist nicht nur `git push`, sondern **jede remote sichtbare Änderung** — Topics, Beschreibung, Homepage, Releases, Issue- und PR-Aktionen verändern das veröffentlichte Projekt genauso.

Existieren weitere Klone desselben Repos (zweites Gerät, Deploy-Kopie, Spiegel), ziehe sie unmittelbar nach dem Push nach. Ein Klon, der zehn Commits zurückliegt, produziert bei der nächsten Fehlersuche Diagnosen an einem Stand, den es nicht mehr gibt.

#### Änderungen an anderen Repos — Dirty-Tree-Ausnahme

Diese Runde erzeugt regelmäßig Änderungen **außerhalb** des gepflegten Repos: eine Zeile im Organisationsprofil (Schritt 8), später in der tiefen Runde ein Rückverweis in einem verwandten Repo. Solche Änderungen werden ebenfalls committet und gepusht — ein unveröffentlichter Rückverweis ist kein Rückverweis.

Vor dem Anfassen eines fremden Repos kurz dessen Zustand prüfen:

```bash
git -C <pfad> status --porcelain
```

**Sauberer Arbeitsbaum** → Änderung vornehmen, in einem **eigenen, thematisch klaren Commit** (`docs: link <projekt>`) committen und pushen. Nicht mit den Commits des gepflegten Repos vermischen: Es ist ein anderes Repo mit eigener Historie und eigenen Lesern.

**Dirty, aber die Fremdänderungen liegen in anderen Dateien** → die eigene Änderung ist trotzdem sauber machbar. Stage und committe **pfadgenau nur die eigene Datei**, damit fremde, ungeprüfte Arbeit nicht mitwandert:

```bash
git -C <pfad> add README.md
git -C <pfad> commit -m "docs: link <projekt>"     # nur der gestagte Pfad
```

Aber **nicht pushen**. Der Commit ist lokal harmlos; ein Push wäre es nicht unbedingt: Du weißt nicht, worauf der andere Arbeitsstand hinausläuft — vielleicht wird er gerade amendiert, rebased oder anders geschnitten, und dein Commit zwingt ihn dazu, sich damit auseinanderzusetzen. Der lokale Commit sichert die Arbeit, ohne jemandem etwas aufzuzwingen; der Lauf, der sich später jenem Repo zuwendet, findet ihn vor und nimmt ihn mit.

**Dirty in genau der Datei, die du ändern müsstest** → nicht anfassen. Hier müsstest du auf einem fremden Zwischenstand aufsetzen und ihn mit-committen; den erst zu verstehen kostet mehr, als dieser eine Verweis wert ist.

**Aktive Sperre (`LOCK*.txt`) im Ziel-Repo** → **zuerst den Lock lesen, statt ihn als pauschales Verbot zu behandeln.** Eine Sperre beschreibt ihren eigenen Umfang, und der ist oft enger als „gar nichts". Typische Fälle:

- **Bearbeitungssperre** („hier arbeitet gerade jemand") → nichts anfassen, auch keine Nebendatei.
- **Reine Veröffentlichungs-/Push-Sperre** (Einreichung, Judging, Freeze) → lokale Arbeit bleibt erlaubt, nur der Remote-Kontakt ist gesperrt. Dann auf einem eigenen Branch arbeiten und lokal committen; **remote-wirksame Schritte entfallen** — nicht nur der Push, sondern auch Topics, Beschreibung, Homepage, Releases und Issue-/PR-Aktionen, denn auch die verändern das veröffentlichte Projekt.

Ein Lock, der nur den Push sperrt, als Komplettverbot zu lesen, kostet den gesamten lokalen Teil der Runde ohne Sicherheitsgewinn. Umgekehrt reicht es nicht, nur den Push zu unterlassen und trotzdem Metadaten zu ändern. Im Zweifel den Lock zitieren und nachfragen.

#### Der Wunsch darf nicht verloren gehen

Wird die Änderung aus einem dieser Gründe **nicht** ausgeführt, wandert sie in die Aufgabenliste des Ziel-Repos — `AUFGABEN.txt`, `TODO.md` oder `TODO.txt`, je nachdem, was dort existiert. Ein Eintrag mit Datum, gewünschter Änderung und Grund:

```markdown
- [ ] [2026-07-24, after-care] Rückverweis auf <projekt> im README ergänzen
      (übersprungen: README hatte uncommittete Fremdänderungen)
```

Das ist der Unterschied zwischen „verschoben" und „vergessen": Die Aufgabenliste liegt dort, wo der nächste Bearbeiter dieses Repos ohnehin hineinsieht — verlässlicher als ein Vermerk im Protokoll eines fremden Laufs. Existiert keine Aufgabenliste, lege keine an; dann genügt der offene Punkt im eigenen Laufprotokoll.

Bei einer **aktiven Sperre gilt auch das nicht** — dann wird die Datei nicht angefasst und der Vermerk bleibt im eigenen Laufprotokoll. Notiere ihn in beiden Fällen auch dort, damit die Rotation den offenen Punkt kennt.

Zum Schluss die Flächen aus Schritt 0 bedienen — siehe nächster Abschnitt.

## Parität über alle Distributionsflächen

Zum Abschluss der Runde gegen die Liste aus Schritt 0 gehen: **Jede Änderung, die ein Nutzer sehen würde, muss auf jeder Fläche ankommen, auf der er sie sucht.** Ein Repo, dessen npm-Seite eine andere Geschichte erzählt, ist schlechter dran als eines mit nur einer Fläche.

Der entscheidende Mechanismus: **Paketregister zeigen die README des letzten Publish, nicht den aktuellen Repo-Stand.** Eine README-Korrektur wird auf npm oder PyPI erst mit einer neuen Version sichtbar. Wenn die Korrektur inhaltlich relevant ist (falsche Installation, falsche Version, veraltete Feature-Liste), gehört ein Patch-Release dazu — sonst bleibt der Fix wirkungslos.

| Fläche | Was dort gepflegt wird | Wie es ankommt |
|---|---|---|
| npm | README, `description`, `keywords`, Repository-Link | Nur per `npm publish` (Patch-Version); Metadaten kommen aus `package.json` |
| PyPI | README (`long_description`), Classifiers, Projekt-URLs | Nur per neuem Upload; Metadaten aus `pyproject.toml` |
| MCP-Registry / Plugin-Verzeichnisse | Beschreibung, Version, Toolliste, Einstiegsdoku | Je nach Registry Manifest-Update oder erneute Einreichung |
| Marketplace / Store | Beschreibung, Screenshots, Kategorien, Sprachfassungen | Über die jeweilige Verwaltungsoberfläche; Screenshots altern dort besonders schnell |
| Docker Hub / Container-Registry | Beschreibung, Tags, Nutzungsbeispiel | Repository-Beschreibung plus neuer Tag |
| Zenodo / DOI | Metadaten, Autoren, Version | In-Place-Edit für Metadaten, neue Version für Inhalte |
| Website / Org-Profil / `llms.txt` | Kurzbeschreibung, Link, Positionierung | Direkt editierbar — die günstigsten Flächen, deshalb nie vergessen |

Wenn eine Version angehoben wird, müssen **alle Versionsträger** gleichzeitig mitwandern: Manifest, Code-Konstante, README-Badge, Changelog, Release-Tag, `llms.txt`. Ein halb angehobener Versionsstand ist schwerer zu diagnostizieren als ein durchgängig alter.

Ist eine Aktualisierung auf einer Fläche gerade nicht möglich oder nicht sinnvoll (z. B. ein Release nur wegen eines Tippfehlers), halte das im Laufprotokoll fest, damit die nächste Runde die Abweichung nicht für ein Versehen hält.

## Force-Push-Regel

Der Standard ist **kein Force-Push**. Interne Planungsdateien nachträglich zu ignorieren rechtfertigt keine Historien-Umschreibung: Der Aufwand ist hoch, jeder Klon und jeder Fork bricht, offene PRs werden unbrauchbar — und der Gewinn ist gering, weil der Inhalt harmlos ist. Normaler Weg:

```bash
git rm --cached <datei>            # aus dem Tracking, bleibt lokal erhalten
# .gitignore ergänzen
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git push
```

Die Historie umschreiben (und damit `--force-with-lease` pushen) ist nur bei **echten Leaks** gerechtfertigt: Credentials und Keys, personenbezogene oder Kundendaten, sowie Dokumente mit echtem Wettbewerbswert — interne Kalkulationen, Preisstrategien, unveröffentlichte Pläne, Vertragsinterna. In diesem Fall:

1. Betroffene Secrets **zuerst rotieren** — die Historie ist zu diesem Zeitpunkt bereits kopiert, geforkt und in Caches. Rotation wirkt, Löschen nur kosmetisch.
2. Historie bereinigen (`git filter-repo` oder BFG), `--force-with-lease` pushen.
3. Forks und Caches prüfen; bei Bedarf GitHub-Support für verwaiste Objekte kontaktieren.
4. Vorgang im Laufprotokoll festhalten: was, wann, welche Rotation.

Im Zweifel zwischen „unkritisch" und „heikel": als heikel behandeln und vorlegen. Die Kosten sind asymmetrisch.

## Befunde werden Aufgaben, nicht nur Protokollzeilen

Eine Pflegerunde findet regelmäßig mehr, als sie in derselben Runde beheben kann oder soll: eine fehlende Sprachfassung, ein Modernisierungsrückstand, eine Veröffentlichung, die nie stattgefunden hat. **Solche Befunde werden im Moment der Entdeckung zu Aufgaben** — sonst hängen sie im Protokoll eines abgeschlossenen Laufs, wo der nächste Bearbeiter des Projekts nicht hinsieht.

Die Aufgabe gehört in das **ordnerlokale Aufgabensystem des Projekts** — dorthin, wo derjenige nachschaut, der als Nächstes an diesem Projekt arbeitet. Typischerweise ist das `AUFGABEN.txt` oder `TODO.md` im Projektordner, und der liegt oft **nicht im Git-Klon**, sondern in der Ablage, in der die Planung lebt. Der Klon enthält den Code, der Projektordner die Steuerung; ein Eintrag im Klon, der beim nächsten `git clean` verschwindet, ist keine Aufgabe.

Drei Dinge dabei beachten:

1. **Interne Aufgabenliste von öffentlicher Roadmap trennen.** Ein `TODO.md` kann eine gepflegte öffentliche Roadmap sein — dann ist es kein Ablageplatz für interne Nacharbeit. Sieh hinein, bevor du anhängst: Findet sich dort eine Überschrift wie „Public roadmap", schreib in die interne Datei daneben (`AUFGABEN.txt`) und markiere sie als intern.
2. **Bestehende Einträge prüfen, statt zu duplizieren.** Oft steht der Befund schon da. Dann wird er nicht neu angelegt, sondern **angereichert** — mit dem empirischen Beleg aus diesem Lauf („bestätigt: `--help` gibt vollständig deutsche Ausgaben aus"). Ein bekannter Punkt mit frischem Beweis ist wertvoller als ein zweiter Eintrag daneben.
3. **Erledigtes mitschreiben.** Was die Runde behoben hat, gehört als abgehakter Punkt mit Commit-Hash dazu. Das erklärt der nächsten Runde, warum ein Befund verschwunden ist, und verhindert, dass sie ihn erneut „entdeckt".

Formuliere die Aufgabe so, dass sie ohne den Kontext dieses Laufs verständlich ist: was gefunden wurde, warum es zählt, was der nächste Schritt wäre. „i18n unvollständig" ist keine Aufgabe; „Katalog enthält nur `status.title`, dort sind es/zh/ja/ru leer — erst CLI-Strings in den Katalog überführen, dann alle sechs Sprachen befüllen" ist eine.

## Laufprotokoll

Halte das Ergebnis in `_after-care/LOG.md` fest (der Ordner gehört in die `.gitignore` — er ist Pipeline-Material, kein Repo-Inhalt, genau nach der Regel aus Schritt 2b). Pro Lauf eine Zeile mit Datum, Stufe und den bewussten Entscheidungen:

```markdown
## 2026-07-24 — surface
- Flächen: GitHub, npm (<paket>), MCP-Registry, Org-Profil, llms.txt
- Topics: +local-first, +mcp-server; keywords in package.json angeglichen
- Entfernt: AUFGABEN.txt, _handoff/ (gitignored, kein Force-Push nötig)
- README: Version 0.9 -> 1.2 korrigiert, Toolzahl 23 -> 26 nachgezählt
- Sprachen: EN + DE gepflegt; ES/ZH/JA/RU bewusst nicht (entwicklernahes Publikum)
- Issues: #12 gefixt, #7 geschlossen (erledigt), #15 Rückfrage gestellt
- Push: 3 Commits, CI grün; npm-Republish 1.2.1 wegen README-Korrektur
- Offen: Store-Screenshots veraltet, brauchen neuen Build
```

Das Protokoll erspart der nächsten Runde, dieselben Entscheidungen neu zu treffen, und ist die Grundlage für rotierende Pflegeläufe über viele Repos (`rotation-check`).

## Häufige Fehler

| Fehler | Korrektur |
|---|---|
| Nur den Arbeitsbaum betrachtet, nicht `git ls-files` | Immer das getrackte Set prüfen — dort liegt das Problem |
| Privacy-Gate nur auf Pfade und Token gerichtet | Auch nach eigenen Pipeline-/Ordnernamen suchen — sie lösen keinen Alarm aus und rutschen durch |
| Interne Datei entfernt und dabei Historie umgeschrieben | Bei unkritischen Dateien reicht `git rm --cached` + normaler Push |
| Secret aus `HEAD` entfernt und Vorgang als erledigt betrachtet | Secret rotieren; alles andere ist Kosmetik |
| Dateien nach Namen klassifiziert | Kurz hineinsehen — Namen tragen die Absicht nicht zuverlässig |
| Zahlen im README fortgeschrieben statt nachgezählt | An der Quelle zählen (Tool-Liste, Testlauf, Manifest) |
| Neue Sprachfassung als leerer Stub angelegt | Befüllen oder weglassen — ein Stub täuscht Vollständigkeit vor |
| Zweite README-Namenskonvention neben der bestehenden eingeführt | Vorhandene Konvention übernehmen |
| PR an eine fremde Liste ohne Freigabe gestellt | Außenkommunikation vorlegen; nur eigene Flächen sind frei |
| Issues gezählt statt bearbeitet | Fixen, schließen oder gezielt nachfragen — jeder Fall bekommt einen Zustand |
| Banner im Alleingang in fremdem Stil erzeugt | Design-Familie des Oekosystems einhalten |
| README im Repo korrigiert, npm-/PyPI-Seite zeigt weiter die alte | Registry-Seiten stammen vom letzten Publish — Patch-Release nachziehen |
| Version nur im Manifest angehoben | Alle Versionsträger gleichzeitig: Manifest, Code, Badge, Changelog, Tag, `llms.txt` |
| Änderungen fertig, aber ungepusht liegen gelassen | Committen und pushen gehört zur Runde; nur Sperren rechtfertigen eine Ausnahme |
| Alles in einem Sammel-Commit | Aufräumen, Doku und Fixes trennen — sonst ist nichts einzeln zurückdrehbar |
| CI nach Doku-Commit rot, sich selbst verdächtigt | Ungepinnter Linter ohne `select` folgt dem Default der neuen Version — Regelsatz festschreiben |
| Falsche Aussage nur dort korrigiert, wo sie auffiel | Org-weit nach der Formulierung suchen — sie steht meist auch im Org-Profil, in `llms.txt` und in der zweiten Sprachfassung |
| Im dirty Fremd-Repo mit `commit -a` gearbeitet | Pfadgenau stagen und committen, nicht pushen — fremde Arbeit bleibt unberührt |
| Änderung im sauberen Org-Profil-Repo gemacht, aber nicht gepusht | Saubere Fremd-Repos bekommen einen eigenen Commit **und** einen eigenen Push |
| Übersprungene Änderung nur im eigenen Protokoll vermerkt | Zusätzlich in die Aufgabenliste des Ziel-Repos eintragen, sofern eine existiert |
| Befund nur ins Laufprotokoll geschrieben | Er wird zur Aufgabe im ordnerlokalen Aufgabensystem — ins Protokoll sieht später niemand |
| Interne Nacharbeit an eine öffentliche Roadmap gehängt | Erst hineinsehen; „Public roadmap" heißt: interne Datei daneben nutzen |
| Bekannten Befund als neuen Eintrag dupliziert | Bestehenden Punkt mit dem empirischen Beleg aus diesem Lauf anreichern |
| Bei einer Bearbeitungssperre eine TODO-Zeile ins gesperrte Repo geschrieben | Diese Sperre gilt für das ganze Projekt — dort gar nichts anfassen |
| Push-Sperre als Komplettverbot gelesen und das Repo ganz übersprungen | Lock lesen: sperrt er nur die Veröffentlichung, läuft die lokale Runde auf einem eigenen Branch weiter |
| Unter Push-Sperre zwar nicht gepusht, aber Topics oder Beschreibung geändert | Auch Metadaten sind remote sichtbar — unter einer Veröffentlichungssperre entfallen sie mit |

## Abschluss-Checkliste

- [ ] Distributionsflächen ermittelt und im Laufprotokoll notiert.
- [ ] Topics, Description und Homepage gesetzt und überprüft.
- [ ] Privacy-Gate über das getrackte Set gelaufen, Funde behandelt.
- [ ] `.md`/`.txt`/`.json` auf Veröffentlichungsabsicht geprüft, interne Dateien ignoriert.
- [ ] Kein Force-Push ohne echten Leak; bei Leak Rotation durchgeführt.
- [ ] Banner vorhanden und im README eingebunden.
- [ ] Version, Features, Zahlen, Screenshots, Links gegen den echten Stand geprüft.
- [ ] Darstellung verbessert (Tabellen, Diagramme, erste Bildschirmhöhe).
- [ ] README-Sprachmatrix vollständig; Entscheidungen zu weiteren Sprachen dokumentiert.
- [ ] Sichtbarkeitsmaßnahmen umgesetzt bzw. zur Freigabe vorgelegt.
- [ ] Eintrag im eigenen Org-Profil geprüft, sinnvolle Fremd-Orga-Verweise gesetzt.
- [ ] Änderungen an Fremd-Repos: sauber → committet und gepusht; dirty → lokal committet;
      nicht ausgeführt → in der Aufgabenliste des Ziel-Repos eingetragen.
- [ ] Issues und PRs in einen definierten Zustand gebracht.
- [ ] Getrennte Commits erstellt, gepusht, CI und Remote-Ansicht verifiziert.
- [ ] Alle Distributionsflächen auf denselben Stand gebracht (ggf. Patch-Release).
- [ ] Nicht behobene Befunde als Aufgaben im ordnerlokalen Aufgabensystem eingetragen.
- [ ] Laufprotokoll in `_after-care/LOG.md` geschrieben.

## Changelog

### 1.6.0 (2026-07-24)
- Regel ergänzt: Eine inhaltliche Korrektur gilt für alle Flächen. Empirisch gelernt — eine
  Nutzer-Klarstellung wurde in Durchlauf 1 im Hub korrigiert, stand aber unbemerkt noch fünfmal
  im Organisationsprofil (EN, DE, `llms.txt`) und fiel erst neun Durchläufe später auf.

### 1.5.0 (2026-07-24)
- Die Linter-Diagnose verschärft, nachdem das Muster an einem Tag dreimal auftrat
  (n8n-workflow-manager ruff 0.15, clirec + swarm-ai ruff 0.16): „zuerst prüfen", die konkreten
  Verräter-Regelcodes, der Plattform-Split, `ruff.toml` als Fix bei fehlendem `pyproject.toml`,
  Verifikation gegen die neue Linter-Version.

### 1.4.0 (2026-07-24)
- Diagnose ergänzt: Wenn die CI nach einem reinen Doku-Commit rot wird, ist die häufigste
  Ursache ein ungepinnter Linter ohne festgeschriebenen Regelsatz — ein neues Tool-Release
  verschiebt den Default und macht unveränderten Code rot. Fix: Regelsatz pinnen, neue Regeln
  als Aufgabe. Zweimal in Folge aufgetreten (n8n-workflow-manager mit ruff 0.15, clirec mit 0.16).

### 1.3.0 (2026-07-24)
- Neuer Abschnitt „Befunde werden Aufgaben": Was die Runde nicht selbst behebt, wird im Moment
  der Entdeckung ein Eintrag im ordnerlokalen Aufgabensystem des Projekts — dort, wo der nächste
  Bearbeiter hinsieht, nicht im Protokoll eines abgeschlossenen Laufs. Inklusive Trennung von
  interner Liste und öffentlicher Roadmap, Anreichern statt Duplizieren, Erledigtes mit Commit.

### 1.2.0 (2026-07-24)
- Privacy-Gate sucht zusätzlich nach den Namen der eigenen internen Ablagen. Sie sind keine
  Secrets, lösen daher keinen Alarm aus und überleben ein Gate, das nur auf Pfade und Token
  zielt — bleiben für Leser aber unauflösbar und geben die eigene Struktur preis.

### 1.1.0 (2026-07-24)
- Sperren werden gelesen statt pauschal als Verbot behandelt: eine reine Veröffentlichungs-/
  Push-Sperre leitet die Runde auf einen lokalen Branch um, statt sie abzubrechen. Zugleich
  klargestellt, dass unter einer solchen Sperre auch Metadaten, Releases und Issue-/PR-Aktionen
  entfallen — sie sind ebenso remote sichtbar wie ein Push.

### 1.0.0 (2026-07-24)
- Initiale Version. Stufe 1 der Repo-Nachpflege, abgeleitet aus `github-repo-care`.
