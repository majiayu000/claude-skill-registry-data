---
name: bankr-signals
description: >
  On-chain verified trading signals for Buzz BD Agent.
  Publish scan results with TX hash proof for credibility.
  Source: https://github.com/BankrBot/openclaw-skills/tree/main/bankr/bankr-signals
  NOTE: Replace this placeholder with actual skill from BankrBot repo.
---

# Bankr Signals — On-Chain Verified Trading Signals

## Source

Install from: `https://github.com/BankrBot/openclaw-skills`
Path: `bankr/bankr-signals/`

## Setup

```bash
# Clone and copy to skills directory
git clone https://github.com/BankrBot/openclaw-skills.git /tmp/bankr-skills
cp -r /tmp/bankr-skills/bankr/bankr-signals/* ./
rm -rf /tmp/bankr-skills
```

## Integration with Buzz

- After each scan cycle, SocialAgent publishes verified signals
- Each signal includes score + on-chain TX hash proof
- Builds @BuzzBySolCex credibility and track record
- Signals are auto-posted (no Ogie approval needed)

## NOTE

If the bankr-signals directory exists in the BankrBot repo,
replace this placeholder entirely with those files.
If it doesn't exist yet, this placeholder provides the intent
and Buzz uses standard tweet templates until signals are available.
