---
name: stix2-generator
description: Generate STIX 2.1 objects and bundles for threat intelligence sharing. Create indicators, malware descriptions, attack patterns, threat actors, and complete bundles from various input formats including IOC lists, MITRE ATT&CK IDs, and threat reports.
---

# STIX 2.1 Generator

Generate valid STIX 2.1 objects and bundles for threat intelligence sharing. This skill helps create properly formatted STIX content from various sources including IOC lists, threat descriptions, and MITRE ATT&CK mappings.

## Requirements

Install the STIX library before use:

```bash
pip install stix2
```

## Usage

### Generate from IOC List

```bash
python scripts/generate_stix.py --iocs examples/ioc_list.txt --output bundle.json
```

### Generate from Threat Description

```bash
python scripts/generate_stix.py --threat examples/threat_description.json --output bundle.json
```

### Generate from MITRE ATT&CK

```bash
python scripts/generate_stix.py --attack-pattern T1055 --output bundle.json
```

### Interactive Mode

```bash
python scripts/generate_stix.py --interactive
```

### Batch Processing

```bash
python scripts/generate_stix.py --batch examples/batch_input.json --output-dir ./output/
```

## Options

| Option | Description |
|--------|-------------|
| `--iocs FILE` | Generate indicators from IOC list file |
| `--threat FILE` | Generate threat actor and campaign from description |
| `--attack-pattern ID` | Generate attack pattern from MITRE ATT&CK ID |
| `--malware FILE` | Generate malware object from description |
| `--campaign FILE` | Generate campaign with related objects |
| `--identity NAME` | Specify identity for created_by_ref |
| `--labels LIST` | Add labels to indicators (comma-separated) |
| `--pattern-type TYPE` | Specify pattern type (stix, snort, yara) |
| `--valid-from DATE` | Valid from timestamp (ISO format) |
| `--valid-until DATE` | Valid until timestamp (ISO format) |
| `--confidence LEVEL` | Confidence level (0-100) |
| `--output FILE` | Output file (default: stdout) |
| `--format FORMAT` | Output format (json, yaml) |
| `--validate` | Validate generated STIX |
| `--bundle` | Wrap objects in a bundle |
| `--relationships` | Generate relationships between objects |
| `--interactive` | Interactive mode for guided creation |
| `--batch FILE` | Batch process multiple objects |

## Object Types

### Indicators

Generate indicators from various sources:

```bash
# From IP addresses
python scripts/generate_stix.py --iocs ips.txt --labels malicious-activity

# From domain list
python scripts/generate_stix.py --iocs domains.txt --labels phishing

# From file hashes
python scripts/generate_stix.py --iocs hashes.txt --labels malware

# Mixed IOCs with auto-detection
python scripts/generate_stix.py --iocs mixed_iocs.txt --auto-detect
```

### Malware

Create malware objects:

```bash
python scripts/generate_stix.py --malware examples/emotet.json
```

Input format:
```json
{
  "name": "Emotet",
  "malware_types": ["trojan", "downloader"],
  "is_family": true,
  "description": "Emotet is a modular banking trojan",
  "capabilities": ["captures-credentials", "exfiltrates-data"],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "initial-access"
    }
  ]
}
```

### Attack Patterns

Generate from MITRE ATT&CK:

```bash
# Single technique
python scripts/generate_stix.py --attack-pattern T1055

# Multiple techniques
python scripts/generate_stix.py --attack-pattern T1055,T1003,T1021.001

# With custom description
python scripts/generate_stix.py --attack-pattern T1055 --description "Custom process injection implementation"
```

### Threat Actors

Create threat actor profiles:

```bash
python scripts/generate_stix.py --threat examples/apt28.json
```

Input format:
```json
{
  "name": "APT28",
  "threat_actor_types": ["nation-state"],
  "description": "Russian threat actor group",
  "aliases": ["Fancy Bear", "Sofacy"],
  "roles": ["agent"],
  "sophistication": "expert",
  "resource_level": "government",
  "primary_motivation": "organizational-gain",
  "goals": ["espionage", "disruption"],
  "observed_ttps": ["T1055", "T1003"]
}
```

### Campaigns

Generate complete campaigns:

```bash
python scripts/generate_stix.py --campaign examples/campaign.json --relationships
```

## Output Examples

### Simple Indicator Bundle

```json
{
  "type": "bundle",
  "id": "bundle--uuid",
  "objects": [
    {
      "type": "indicator",
      "spec_version": "2.1",
      "id": "indicator--uuid",
      "created": "2024-01-01T00:00:00.000Z",
      "modified": "2024-01-01T00:00:00.000Z",
      "name": "Malicious IP: 192.0.2.1",
      "pattern": "[network-traffic:dst_ref.type = 'ipv4-addr' AND network-traffic:dst_ref.value = '192.0.2.1']",
      "pattern_type": "stix",
      "valid_from": "2024-01-01T00:00:00.000Z",
      "labels": ["malicious-activity"],
      "confidence": 90
    }
  ]
}
```

### Complex Bundle with Relationships

```json
{
  "type": "bundle",
  "id": "bundle--uuid",
  "objects": [
    {
      "type": "threat-actor",
      "id": "threat-actor--uuid",
      "name": "APT28",
      "threat_actor_types": ["nation-state"]
    },
    {
      "type": "attack-pattern",
      "id": "attack-pattern--uuid",
      "name": "Process Injection",
      "external_references": [
        {
          "source_name": "mitre-attack",
          "external_id": "T1055"
        }
      ]
    },
    {
      "type": "relationship",
      "id": "relationship--uuid",
      "relationship_type": "uses",
      "source_ref": "threat-actor--uuid",
      "target_ref": "attack-pattern--uuid"
    }
  ]
}
```

## Batch Processing

Process multiple objects at once:

```json
{
  "identity": {
    "name": "ACME Security",
    "identity_class": "organization"
  },
  "objects": [
    {
      "type": "indicator",
      "iocs": ["192.0.2.1", "192.0.2.2"],
      "labels": ["malicious-activity"]
    },
    {
      "type": "malware",
      "name": "BadMalware",
      "malware_types": ["remote-access-trojan"]
    },
    {
      "type": "attack-pattern",
      "mitre_id": "T1055"
    }
  ],
  "relationships": [
    {
      "source": "malware/BadMalware",
      "relationship": "uses",
      "target": "attack-pattern/T1055"
    }
  ]
}
```

## Integration

### With STIX Validator

Generate and validate in one command:

```bash
python scripts/generate_stix.py --iocs iocs.txt --output bundle.json --validate
```

### With MISP

Export to MISP format:

```bash
python scripts/generate_stix.py --iocs iocs.txt --format misp --output event.json
```

### With TAXII

Prepare for TAXII upload:

```bash
python scripts/generate_stix.py --iocs iocs.txt --taxii-collection indicators --output bundle.json
```

## Pattern Types

### STIX Patterns

Default pattern type for indicators:

```
[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']
[domain-name:value = 'evil.com']
[ipv4-addr:value = '192.0.2.1']
```

### SNORT Rules

Generate SNORT-compatible patterns:

```bash
python scripts/generate_stix.py --iocs ips.txt --pattern-type snort
```

### YARA Rules

Generate YARA-compatible patterns:

```bash
python scripts/generate_stix.py --iocs hashes.txt --pattern-type yara
```

## Best Practices

1. **Always validate** generated STIX using the validator skill
2. **Use meaningful labels** for indicators (malicious-activity, phishing, etc.)
3. **Include confidence scores** when known
4. **Set appropriate valid_from and valid_until** timestamps
5. **Generate relationships** to show connections between objects
6. **Include external references** for MITRE ATT&CK techniques
7. **Use consistent identities** for created_by_ref
8. **Batch process** related objects together
9. **Document custom extensions** if used

## Error Handling

The generator validates input and provides clear error messages:

- Invalid IOC format
- Missing required fields
- Invalid MITRE ATT&CK IDs
- Relationship reference errors
- Pattern syntax errors

## Security Considerations

- Generated STIX should be validated before sharing
- Sensitive information should be reviewed before distribution
- Use TLP markings when appropriate
- Consider privacy implications of shared indicators
- Validate source authenticity before generating STIX from external data

## Performance

- Batch processing is more efficient than individual generation
- Large IOC lists are processed in chunks
- Relationship generation uses efficient graph algorithms
- Memory-efficient for large bundles