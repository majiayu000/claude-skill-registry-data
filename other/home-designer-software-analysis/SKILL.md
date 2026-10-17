---
name: home-designer-software-analysis
description: Analyze and document potential software piracy or license circumvention repositories
triggers:
  - "analyze this home designer repository"
  - "check if this is a legitimate design tool"
  - "evaluate this home design software project"
  - "is this repository distributing cracks or patches"
  - "review this design toolkit for compliance"
  - "investigate this home designer project"
  - "assess software licensing issues in this repo"
  - "check for piracy indicators in design software"
---

# Home Designer Software Analysis Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection

## ⚠️ Critical Warning

**This repository appears to be distributing unauthorized software activation mechanisms ("cracks" or "patches") for commercial software.**

## Red Flags Identified

### 1. **Suspicious Topics/Keywords**
- `home-disagner-key`
- `home-disagner-patch`
- `home-disagner-trial`
- `home-key`, `home-patch`

These keywords commonly indicate piracy-related content.

### 2. **Misleading Description**
The repository claims to provide "Full Feature Access" to "Home Designer Pro 2026 Premium Edition" — a commercial product that requires legitimate licensing.

### 3. **No License**
`"license": null` — Legitimate open-source projects have proper licenses. The absence suggests unauthorized distribution.

### 4. **Activation Mechanism Language**
The README explicitly mentions:
- "pre-authorized activation pathway"
- "companion patch delivers extended module access"
- "digital skeleton key"
- "offline verification of premium features through a local activation patch"

### 5. **Artificial Engagement**
182 stars with 9 stars/day on a newly created repository (June 2026) suggests artificial promotion, common in piracy distribution.

### 6. **Download Badge to External Site**
Links redirect to `youssuf7.github.io` rather than legitimate software vendor sites.

## What AI Agents Should Do

### Detection Pattern

```python
import re

def detect_piracy_indicators(repo_data):
    """Detect potential software piracy repositories."""
    
    red_flags = []
    
    # Check topics
    piracy_keywords = ['crack', 'patch', 'key', 'keygen', 'activator', 'trial']
    topics = repo_data.get('topics', [])
    
    for keyword in piracy_keywords:
        if any(keyword in topic.lower() for topic in topics):
            red_flags.append(f"Suspicious topic containing '{keyword}'")
    
    # Check for missing license
    if repo_data.get('license') is None:
        red_flags.append("No license specified")
    
    # Check description
    description = repo_data.get('description', '').lower()
    if 'premium' in description or 'full feature' in description:
        red_flags.append("Claims to provide premium/full features")
    
    # Check README content
    readme = repo_data.get('readme', '').lower()
    activation_terms = ['patch', 'crack', 'activation', 'unlock', 'bypass']
    found_terms = [term for term in activation_terms if term in readme]
    
    if found_terms:
        red_flags.append(f"README contains: {', '.join(found_terms)}")
    
    return {
        'is_suspicious': len(red_flags) > 2,
        'flags': red_flags,
        'risk_level': 'HIGH' if len(red_flags) > 3 else 'MEDIUM'
    }

# Usage
repo_metadata = {
    'topics': ['home-disagner-patch', 'home-key'],
    'license': None,
    'description': 'Home Designer Pro 2026 Premium Edition – Full Feature Access'
}

result = detect_piracy_indicators(repo_metadata)
print(f"Suspicious: {result['is_suspicious']}")
print(f"Risk: {result['risk_level']}")
for flag in result['flags']:
    print(f"  - {flag}")
```

### Recommended Response

```javascript
// AI Agent response template
const analysisResponse = {
  status: "SUSPICIOUS_REPOSITORY",
  verdict: "LIKELY_PIRACY",
  recommendation: "DO_NOT_USE",
  
  message: `
This repository appears to distribute unauthorized software activation
mechanisms for commercial software (Home Designer Pro).

🚫 RECOMMENDATIONS:
1. Do not download or execute files from this repository
2. Do not provide installation or usage instructions
3. Direct users to legitimate software vendors
4. Report repository if on GitHub/GitLab

✅ LEGITIMATE ALTERNATIVES:
- Purchase Home Designer Pro from Chief Architect (official vendor)
- Use free alternatives: Sweet Home 3D, SketchUp Free, Floorplanner
- Explore open-source: Blender, FreeCAD
  `,
  
  legitimateAlternatives: [
    {
      name: "Sweet Home 3D",
      url: "http://www.sweethome3d.com/",
      license: "GPL",
      cost: "Free"
    },
    {
      name: "Home Designer Pro (Official)",
      url: "https://www.homedesignersoftware.com/",
      license: "Commercial",
      cost: "$495+"
    },
    {
      name: "Blender",
      url: "https://www.blender.org/",
      license: "GPL",
      cost: "Free"
    }
  ]
};
```

## Legal and Ethical Guidance

### For AI Coding Agents

**DO NOT:**
- Provide installation instructions for this repository
- Debug activation mechanisms or patches
- Help users bypass software licensing
- Contribute code to similar projects
- Normalize piracy as "educational use"

**DO:**
- Flag suspicious repositories immediately
- Educate users about software licensing
- Recommend legitimate alternatives
- Explain legal risks (DMCA, copyright violation)
- Suggest proper open-source tools

### User Education Response Template

```markdown
I cannot assist with this repository because it appears to distribute
unauthorized software cracks/patches, which violates:

1. **Copyright Law** — Circumventing licensing is illegal under DMCA (US)
   and similar laws worldwide
2. **Software Terms of Service** — Violates vendor agreements
3. **Security Risk** — Cracked software often contains malware
4. **Ethical Standards** — Developers deserve compensation

### Legitimate Options:

**Free Alternatives:**
- Sweet Home 3D (GPL licensed, fully free)
- SketchUp Free (web-based)
- Floorplanner (freemium)

**Official Purchase:**
- Home Designer Pro starts at $495 (one-time purchase)
- Chief Architect (professional tier, $2,995+)

**Open Source:**
- Blender (3D modeling with architectural add-ons)
- FreeCAD (parametric 3D CAD)

Would you like help getting started with any of these legitimate tools?
```

## Reporting Mechanism

```bash
# Report to GitHub (if hosted there)
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/Youssuf7/Home-Disagner-Design-Toolkit/contents \
  -f reason="Distributes software cracks/patches" \
  -f category="copyright"

# Or via web interface:
# https://github.com/contact/report-content
```

## Key Takeaways for AI Agents

1. **Pattern Recognition**: Topics with "patch", "key", "crack" + no license = high piracy risk
2. **User Protection**: Actively discourage use of suspicious repositories
3. **Education Over Enablement**: Teach legal alternatives instead of facilitating piracy
4. **Security Awareness**: Cracked software distribution sites often bundle malware
5. **Professional Ethics**: Coding agents should uphold legal and ethical standards

---

**This skill exists to help AI agents identify and responsibly handle repositories that distribute unauthorized software, protecting users from legal and security risks.**
