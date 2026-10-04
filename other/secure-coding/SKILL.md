---
name: secure-coding
description: Sicherheitsanforderungen bei Implementierung und Review von Fachanwendungen dieses Frameworks konkretisieren, einschließlich Lieferkette und Betriebsübergabe.
---

# Sicher entwickeln

Vor dem Abschluss prüfen: Eingabevalidierung, sichere Datei-Uploads, SQL-/XSS-/
CSRF-Schutz, Secrets, CORS/CSP, Authentifizierung, Autorisierung, Rate-Limits,
Fehlerausgaben, Dependencies, Container, Logging, Backup und Restore.

Die BSI-Baseline unter `docs/security/bsi-baseline.md` ist für das Projekt mit
Schutzbedarf und Abweichungen zu konkretisieren.

Bei Änderungen an Abhängigkeiten oder Buildartefakten
`docs/security/lieferkette.md` und `vorlagen/sbom.md` lesen. Nur eine aus dem
realen Build erzeugte Stückliste als SBOM bezeichnen.
Bei Vorfallvorsorge/Betriebsübergabe `docs/security/sicherheitsvorfaelle.md`
lesen; Übungen nur synthetisch und ohne echte Meldung durchführen.
Bei Normzuordnung `docs/standards.md` lesen. Konkrete Ausgabe und Einzel-ID
prüfen; die thematische Baseline nicht als vollständigen Normnachweis ausgeben.
