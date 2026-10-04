---
name: target-recon
description: "Target discovery methodology for finding high-quality npm/PyPI/GitHub packages to audit for vulnerabilities, with evaluation criteria and search strategies."
metadata:
  filePattern:
    - "**/package.json"
    - "**/requirements.txt"
    - "**/go.mod"
  bashPattern:
    - "npm search"
    - "gh search repos"
    - "pip search"
  priority: 70
---

# Target Recon -- Finding High-Quality Audit Targets

## When to Use

Starting a new research cycle. Need fresh targets with high CVE potential but low existing researcher attention.

## Target Sweet Spot

The ideal target is a package that:
- Is widely used (>100K weekly downloads on npm)
- Handles untrusted input (parsing, validation, file processing)
- Is small enough to audit in a day (< 10K lines of code)
- Has few existing CVEs (< 5)
- Is actively maintained (last commit within 6 months)
- Has 500-15K GitHub stars

## Avoid

- **Mega-packages** (lodash, axios, moment, express, django, rails) -- too many researchers
- **Full frameworks** (Next.js, Nuxt, Laravel) -- too large, too audited
- **>20K stars AND >10 prior CVEs** -- over-audited territory
- **Abandoned packages** (no commits in 2+ years) -- CVE may not be assigned
- **Alpha/beta packages** -- maintainer may not issue CVE

## Search Strategies

### npm Search
```bash
# Search by category
npm search xml parser
npm search csv parse
npm search template engine
npm search file upload
npm search schema validator

# Check weekly downloads on npmjs.com
# Look for packages with 100K-10M weekly downloads
```

### GitHub Search
```bash
# Search repos by language and star count
gh search repos "xml parser" --language javascript --stars 500..15000
gh search repos "yaml" --language python --stars 500..10000
gh search repos "template engine" --language javascript --stars 500..15000
gh search repos "archive extract" --language go --stars 500..10000
```

### grep.app (Cross-Repo Code Search)
Search for vulnerable patterns across many repos:
```
https://grep.app/search?q=new%20Function&regexp=false&filter[lang][0]=JavaScript
https://grep.app/search?q=eval%28&regexp=false&filter[lang][0]=JavaScript
```

### Libraries.io
Check dependency counts -- packages depended on by many other packages have higher impact.

## Category-Based Targeting

### Highest Yield Categories

| Category | Vulnerability Classes | Example Packages |
|----------|----------------------|------------------|
| Parsing (XML/CSV/YAML) | Entity expansion, ReDoS, clobbering | fast-xml-parser, csv-parse, js-yaml |
| Validation/Schema | Code injection, ReDoS, proto pollution | ajv, joi, fastest-validator |
| Template Engines | SSTI, code injection | ejs, nunjucks, handlebars, pug |
| Archive/Compression | Zip Slip, decompression bomb, path traversal | adm-zip, decompress, fflate |
| File Handling | Path traversal, symlink attacks | express-fileupload, formidable |
| Deep Merge/Clone | Proto pollution, recursion DoS | deepmerge, rfdc, klona |
| Expression Evaluators | Sandbox escape, code injection | simpleeval, expr-eval, filtrex |
| HTTP Clients | SSRF, header injection, auth leak | got, superagent, needle |
| Serialization | Clobbering, code injection, recursion | flatted, superjson, msgpackr |
| URL/Path Utilities | SSRF bypass, path traversal | url-parse, normalize-url |

## Evaluation Process

For each candidate:

1. **Check Registry**: Is it already in REGISTRY.md?
2. **Check NVD**: Search for existing CVEs
3. **Check GitHub Advisories**: Look at security tab
4. **Read README**: Does it warn about untrusted input?
5. **Check SECURITY.md**: Does the project accept security reports?
6. **Read recent CHANGELOG**: Any "security fix" entries? (incomplete patches are goldmines)
7. **Check HackerOne/bug bounty**: Bonus, not required
8. **Estimate attack surface**: What untrusted input does it process?
9. **Match to vuln classes**: Which skills apply?

## Brief Template

Write a brief for each approved target:

```markdown
# Target Brief: [package-name]

- **GitHub**: [URL]
- **Stars**: [count]
- **Weekly Downloads**: [count]
- **Last Commit**: [date]
- **Language**: [JS/Python/Go/etc.]

## Attack Surface
- [What untrusted input does it process?]

## Existing CVEs
- [none / list with CVE IDs]

## Bug Bounty
- [yes/no + link]

## Top 3 Vectors
1. [Most likely vulnerability class + why]
2. [Second most likely]
3. [Third most likely]

## Why Promising
[1-2 sentences on why this target is worth investigating]
```

## References

- [Parallel Scanning](references/parallel-scanning.md) -- Batch evaluation methodology
- [Search Queries](references/search-queries.md) -- Pre-built search queries by category
