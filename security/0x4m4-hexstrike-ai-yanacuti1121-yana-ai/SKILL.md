---
name: 0x4m4--hexstrike-ai
description: "HexStrike AI — MCP server cho 150+ cybersecurity tools: Nmap, SQLMap, Nuclei, Ghidra, Prowler... AI agent tự chọn tool, chạy pentest, bug bounty automation. Cần authorization."
allowed-tools: Bash, Read
user-invocable: true
---

HexStrike AI: MCP server expose 150+ cybersec tools cho AI agent — Claude/GPT/Copilot tự chọn tool phù hợp, chạy automated pentesting và vulnerability discovery.

**QUAN TRỌNG**: Chỉ dùng cho authorized targets. Unauthorized testing = illegal.

## Install & Start

```bash
git clone https://github.com/0x4m4/hexstrike-ai
cd hexstrike-ai
pip install -r requirements.txt
# Install required tools: nmap, nuclei, sqlmap, etc.
python3 hexstrike_server.py
```

## MCP Config (Claude Desktop)

```json
{
  "mcpServers": {
    "hexstrike-ai": {
      "command": "python3",
      "args": ["/path/to/hexstrike_mcp.py", "--server", "http://localhost:8888"],
      "timeout": 300
    }
  }
}
```

## 150+ Tools — 6 Categories

```
Network & Recon (25+)
  Nmap, Rustscan, Masscan, Amass, Subfinder, TheHarvester, Enum4linux

Web Application (40+)
  Gobuster, Feroxbuster, FFuf, Nuclei, SQLMap, WPScan, Dalfox, OWASP ZAP

Auth & Passwords (12+)
  Hydra, Hashcat, John the Ripper, Medusa, Evil-WinRM

Binary Analysis (25+)
  GDB, Radare2, Ghidra, Binwalk, Pwntools, Volatility, Angr

Cloud Security (20+)
  Prowler, Scout Suite, Trivy, Kube-Hunter, Docker Bench

CTF & Forensics (20+)
  Foremost, Steghide, ExifTool, CyberChef
```

## Key MCP Tools

```python
nmap_scan(target, flags)
nuclei_scan(target, templates)
sqlmap_scan(url, options)
ghidra_analyze(binary_path)
prowler_assess(cloud_provider)
# POST /api/intelligence/select-tools — AI chọn tool tự động
# POST /api/intelligence/analyze-target — target analysis
```

## 12 Specialized Agents

```
Intelligent tool selection + parameter optimization
Bug bounty workflow automation
CTF challenge solving
CVE intelligence gathering
Exploit code generation
Attack chain discovery
```

## Speed Claims

```
Subdomain enumeration: 2-4h → 5-10min (24x faster)
Vuln scanning:         4-8h → 15-30min
Web app testing:       6-12h → 20-45min
```

## Source

https://github.com/0x4m4/hexstrike-ai · MIT
