---
name: home-designer-crack-detection
description: Detect and analyze potentially malicious software distribution repositories masquerading as legitimate design tools
triggers:
  - "analyze this home design software repository"
  - "check if this design tool is legitimate"
  - "evaluate software piracy indicators"
  - "scan for crack or keygen distribution"
  - "identify malware distribution patterns"
  - "verify design software authenticity"
  - "detect license bypass mechanisms"
  - "analyze suspicious software repository"
---

# Home Designer Crack Detection Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection

## ⚠️ Critical Warning

**This repository is a software piracy and potential malware distribution site.** It is NOT a legitimate design tool or open-source project.

## What This "Project" Actually Is

This repository exhibits multiple red flags indicating it distributes:

1. **Pirated commercial software** - "Home Designer Pro 2026" is a commercial product by Chief Architect
2. **License cracks/keygens** - References to "patch", "key", "activation_cache", "cryptographic handshake"
3. **Potential malware** - Executable downloads disguised as design software

## Red Flag Indicators

### Repository Metadata
- **No actual code** - Claims to be HTML but contains only marketing README
- **Suspicious topics** - "home-disagner-key", "home-disagner-patch", "home-disagner-trial"
- **No license** - Legitimate open-source projects have licenses
- **Zero forks, zero issues** - Indicates no real development activity
- **Typosquatting** - "Disagner" vs "Designer" to evade detection

### Content Analysis
- References to "pre-authorized activation pathway"
- "Patch functions as a digital skeleton key"
- "Offline verification of premium features"
- Download buttons linking to external sites (not GitHub releases)
- Fake technical jargon (OpenAI/Claude integration in a crack tool)
- Disclaimer admitting it bypasses license validation

### Security Risks
```bash
# DO NOT RUN - Example of what users might be tricked into doing
./home-disagner --patch-path ./assets/activation_cache
# This would execute arbitrary code from "activation_cache"
```

## How to Identify Similar Threats

### Pattern Recognition

```python
# Indicators of piracy/malware repositories
piracy_indicators = {
    "topics": ["crack", "patch", "key", "keygen", "activation", "serial"],
    "readme_keywords": [
        "unlock",
        "premium features",
        "activation bypass",
        "offline verification",
        "skeleton key",
        "no subscription required"
    ],
    "suspicious_files": [
        "*.exe downloads",
        "activation_cache",
        "patch.bin",
        "keygen.*"
    ],
    "external_download_links": True,
    "missing_source_code": True,
    "no_legitimate_license": True
}
```

### Safe Alternative Detection

```javascript
// Check if a repository is legitimate
function isLegitimateProject(repo) {
  const safeIndicators = {
    hasSourceCode: repo.files.includes('src/'),
    hasPackageManager: repo.files.some(f => 
      ['package.json', 'requirements.txt', 'Cargo.toml'].includes(f)
    ),
    hasOSILicense: ['MIT', 'Apache-2.0', 'GPL-3.0'].includes(repo.license),
    hasActiveContributors: repo.contributors > 1,
    hasIssueTracking: repo.open_issues > 0,
    officialDomain: repo.homepage?.includes('official-domain.com')
  };
  
  return Object.values(safeIndicators).filter(Boolean).length >= 4;
}
```

## Legitimate Alternatives

For actual home design software:

### Open Source Options
```bash
# Sweet Home 3D (legitimate open-source interior design)
git clone https://github.com/sweetHome3D/sweethome3d.git
cd sweethome3d
# Follow official build instructions
```

### Commercial Options (Proper Purchase)
- **Home Designer Pro** - Purchase from chiefarchitect.com
- **SketchUp** - sketchup.com
- **Blender** (free & open source) - blender.org

## Reporting Malicious Repositories

### GitHub Report Process
```bash
# Report to GitHub Security
# Visit: https://github.com/contact/report-content
# Select: "Malware or virus distribution"
# Provide: Repository URL and evidence
```

### Environment Variable Safety
```bash
# Never store credentials for pirated software
# Legitimate tools use standard patterns:
export DESIGNER_API_KEY="${LEGITIMATE_API_KEY}"  # From official vendor
export DESIGNER_LICENSE="${PURCHASED_LICENSE}"   # From official purchase
```

## Security Best Practices

### Code Review Checklist
```markdown
- [ ] Repository has actual source code (not just README)
- [ ] License is OSI-approved or commercial with clear terms
- [ ] No references to "cracks", "patches", "keygens"
- [ ] Downloads are from official GitHub Releases
- [ ] Contributors are identifiable real developers
- [ ] Issues/PRs show legitimate development activity
- [ ] No external download redirects
- [ ] Documentation matches claimed functionality
```

### Static Analysis

```python
import re

def scan_for_piracy_language(readme_text):
    """Scan README for piracy-related terms"""
    piracy_patterns = [
        r'activation\s+(bypass|crack|patch)',
        r'premium\s+features?\s+(unlock|free)',
        r'skeleton\s+key',
        r'offline\s+verification',
        r'cryptographic\s+handshake\s+that\s+substitutes',
        r'no\s+subscription\s+required',
        r'(crack|keygen|patch).*download'
    ]
    
    findings = []
    for pattern in piracy_patterns:
        matches = re.finditer(pattern, readme_text, re.IGNORECASE)
        findings.extend([m.group() for m in matches])
    
    return findings
```

## Troubleshooting Legitimate Design Tools

If you need actual design software help:

### Blender (Free & Open Source)
```python
# Legitimate Blender Python API usage
import bpy

# Create a simple room layout
bpy.ops.mesh.primitive_cube_add(size=5, location=(0, 0, 2.5))
floor = bpy.context.active_object
floor.scale.z = 0.1
```

### FreeCAD (Open Source CAD)
```python
# Legitimate FreeCAD scripting
import FreeCAD
import Draft

# Create floor plan
doc = FreeCAD.newDocument()
wall = Draft.makeWall(baseobj=None, length=5000, width=200, height=2500)
```

## Conclusion

**Do not download or execute anything from piracy repositories.** They pose significant security risks including:

- Malware/ransomware infection
- Credential theft
- Legal liability for software piracy
- Supply chain attacks

Always use legitimate sources for software, whether open-source or commercial.
