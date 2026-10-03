---
name: net-dns-dnstwist
description: "Net Dns Dnstwist."
domain: cybersecurity
---

")
        for entry in high_risk[:10]:
            print(f"  {entry['domain']} (score: {entry['risk_score']})")
            for factor in entry['risk_factors']:
                print(f"    - {factor}")

    return {"high": high_risk, "medium": medium_risk, "low": low_risk}

analysis = analyze_results(results, legitimate_ips={"93.184.216.34"})
```

### Step 3: Continuous Monitoring Pipeline

```python
import time
import hashlib

class TyposquatMonitor:
    def __init__(self, domains, known_domains_file="known_typosquats.json"):
        self.domains = domains
        self.known_file = known_domains_file
        self.known_domains = self._load_known()

    def _load_known(self):
        try:
            with open(self.known_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_known(self):
        with open(self.known_file, "w") as f:
            json.dump(self.known_domains, f, indent=2)

    def scan_all_domains(self):
        """Scan all monitored domains for new typosquats."""
        new_findings = []
        for domain in self.domains:
            results = run_dnstwist_scan(domain)
            for entry in results:
                domain_key = entry.get("domain", "")
                if domain_key not in self.known_domains:
                    entry["first_seen"] = datetime.now().isoformat()
                    entry["monitored_domain"] = domain
                    self.known_domains[domain_key] = entry
                    new_findings.append(entry)
                    print(f"  [NEW] {domain_key} ({entry.get('fuzzer', '')})")

        self._save_known()
        print(f"\n[+] New typosquatting domains found: {len(new_findings)}")
        return new_findings

    def generate_alert(self, findings):
        """Generate alert for new high-risk typosquatting domains."""
        analysis = analyze_results(findings)
        alerts = []
        for entry in analysis["high"]:
            alerts.append({
                "severity": "HIGH",
                "domain": entry["domain"],
                "target": entry.get("monitored_domain", ""),
                "risk_score": entry["risk_score"],
                "risk_factors": entry["risk_factors"],
                "dns_a": entry.get("dns_a", []),
                "dns_mx": entry.get("dns_mx", []),
                "timestamp": datetime.now().isoformat(),
            })
        return alerts

monitor = TyposquatMonitor(["mycompany.com", "mycompany.org"])
new_findings = monitor.scan_all_domains()
alerts = monitor.generate_alert(new_findings)
```

### Step 4: Export for Blocklist and Takedown

```python
def export_blocklist(analysis, output_file="blocklist.txt"):
    """Export high-risk domains as blocklist for firewall/proxy."""
    domains = []
    for entry in analysis["high"] + analysis["medium"]:
        domain = entry.get("domain", "")
        if domain:
            domains.append(domain)

    with open(output_file, "w") as f:
        f.write(f"# Typosquatting blocklist generated {datetime.now().isoformat()}\n")
        for d in sorted(set(domains)):
            f.write(f"{d}\n")

    print(f"[+] Blocklist saved: {len(domains)} domains -> {output_file}")
    return domains

def generate_takedown_report(high_risk_domains):
    """Generate takedown request report."""
    report = f"""# Domain Takedown Request
Generated: {datetime.now().isoformat()}

## Summary
{len(high_risk_domains)} domains identified as potential typosquatting/phishing.

## Domains Requiring Takedown
"""
    for entry in high_risk_domains:
        report += f"""
### {entry['domain']}
- **Permutation Type**: {entry.get('fuzzer', 'unknown')}
- **IP Address**: {', '.join(entry.get('dns_a', ['N/A']))}
- **MX Records**: {', '.join(entry.get('dns_mx', ['N/A']))}
- **Risk Score**: {entry.get('risk_score', 0)}
- **Risk Factors**: {'; '.join(entry.get('risk_factors', []))}
- **Web Similarity**: {entry.get('ssdeep_score', 'N/A')}%
"""
    with open("takedown_report.md", "w") as f:
        f.write(report)
    print("[+] Takedown report generated: takedown_report.md")

export_blocklist(analysis)
generate_takedown_report(analysis["high"])
```

## Validation Criteria

- DNSTwist generates domain permutations for target domain
- DNS resolution identifies registered lookalike domains
- Web similarity scoring detects cloned phishing pages
- Risk scoring prioritizes domains by threat level
- Continuous monitoring detects newly registered typosquats
- Blocklist and takedown reports generated correctly

## References

- [dnstwist GitHub Repository](https://github.com/elceef/dnstwist)
- [dnstwister Online Service](https://dnstwister.report/)
- [HawkEye: Detect Typosquatting with DNSTwist](https://hawk-eye.io/2022/11/how-to-detect-typosquatting-using-dnstwist/)
- [Darktrace: Monitoring Typosquatting Domains](https://www.darktrace.com/blog/vigilance-in-action-monitoring-typosquatting-domains)
- [Security Risk Advisors: Domain Monitoring](https://sra.io/blog/domain-monitoring-fast-and-cheap/)
- [Conscia: How to Detect Typosquatting](https://conscia.com/blog/diving-deep-how-to-detect-typosquatting/)
