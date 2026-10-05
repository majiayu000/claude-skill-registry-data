---
name: doi2bib
description: Fetch a BibTeX entry for a given DOI from doi.org. Use when the user asks for a BibTeX citation, a `.bib` entry, or says something like "doi2bib <doi>".
argument-hint: <doi>
user-invocable: true
allowed-tools: Bash(curl:*)
---

# doi2bib

Resolve a DOI to its BibTeX entry using the doi.org content negotiation endpoint.

## Input

<doi>
$ARGUMENTS
</doi>

If no DOI is provided, ask the user for one. Accept either the bare DOI
(`10.1038/nature12373`) or a full URL (`https://doi.org/10.1038/nature12373`);
strip the URL prefix before making the request.

## How to Use

```bash
curl -s -L --max-time 10 -H "Accept: text/bibliography; style=bibtex" "https://doi.org/<DOI>"
```

- `-L` follows the redirect from doi.org to the publisher's Crossref/DataCite
  record.
- `--max-time 10` caps the request so a stalled publisher endpoint doesn't
  block the agent turn.
- The `Accept` header asks the resolver to return a BibTeX-formatted citation
  instead of the landing page.
- Quote the URL to protect any `&` or `;` characters in the DOI.

## Output

Return the raw BibTeX verbatim inside a ```bibtex code block so the user can
paste it straight into a `.bib` file. Do not reformat the entry or rename the
citation key unless the user asks.

## Error handling

If the response is empty, an HTML page, or a curl error, tell the user the DOI
could not be resolved and show what came back so they can diagnose (typo,
unregistered DOI, publisher not supporting BibTeX negotiation).
