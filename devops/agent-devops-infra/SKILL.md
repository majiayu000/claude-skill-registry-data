---
name: agent-devops-infra
description: "DevOps & Infrastructure IA — Gère le VPS, Docker, déploiements, monitoring, sécurité, tunnels Cloudflare. Expert Hetzner + Coolify + self-hosting."
tags: [devops, vps, docker, self-hosting, infrastructure]
---

# 🛠️ DevOps & Infrastructure IA

## Rôle
Expert en infrastructure self-hosted. Déploie, sécurise, et maintient les services sur le VPS.

## Vidéos sources (compétences)
| ID | Titre | Insight clé |
|---|---|---|
| `lxYb-yaBYpE` | Ce serveur VPS remplace 10 abonnements IA | Architecture complète : Hermes + Ollama + n8n + OpenWebUI + SearXNG + Firecrawl |
| `E0tUio6ZgH8` | You Need a VPS — Hetzner + Cloudflare DNS sous $5/mois | Setup fondational VPS : SSH, firewall, DNS, tunnels |
| `5h-ZVM3RTps` | VPS GRATUIT avec Oracle Cloud | Alternative gratuite pour le prototypage |
| `7FSyY5I9u8M` | Arrête de payer ChatGPT : Ollama lance OpenClaw + Paperclip | Services IA open source self-hosted |
| `5_cZCmrlcow` | DeepSeek V4 + NVIDIA NIM = Free Claude Code Alternative | Alternatives cloud gratuites pour le dev |

## Compétences clés
- **VPS Management** : Hetzner (prod), Oracle Cloud (free tier), hardening SSH
- **Docker & Services** : Coolify (PaaS), Portainer, systemd user services
- **Réseau** : Cloudflare tunnels, Tailscale VPN, Nginx reverse proxy
- **Monitoring** : Cron health-checks, auto sleep/wake, backups
- **Sécurité** : UFW, Fail2ban, key-only auth, cgroup limits (OOM)
- **Stack IA** : Ollama (local), NVIDIA NIM (cloud), SearXNG, Firecrawl, n8n
- **GitHub** : SSH ed25519 setup, PAT tokens, repo management

## Configuration VPS Odin
- **IP** : 178.105.204.174
- **Ports** : 2222=SSH, 3000=WhatsApp, 3001=Heziri, 3002=Firecrawl, 3080=OpenWebUI, 5678=n8n, 8081=SearXNG, 8888=Coolify, 9000/9443=Portainer, 11434=Ollama(0.0.0.0)
- **Services critiques** : Coolify, Portainer, Tailscale, SSH, Hermes, CF tunnels
- **Services endormables** : Ollama, SearXNG, n8n, OpenWebUI, Firecrawl
- **GitHub** : compte ziri22, SSH ed25519 configuré

## ⚠️ Piège : Modèles Ollama et contexte minimum
Hermes exige ≥64K tokens de contexte. Avant d'installer un modèle Ollama, vérifier `ollama show <model> | grep context`. Si <64K, ajouter `context_length` override dans config.yaml fallback_providers. Exemples : qwen2.5-coder:7b=32K ❌, qwen3:8b=40K (override requis), llama3.2:3b=128K ✅.

## ⚠️ Piège : Suppression de modèle Ollama casse les cron jobs
Avant de `ollama rm <model>`, vérifier TOUJOURS les cron jobs qui l'utilisent :
```bash
hermes cron list | grep <model>
```
Chaque cron job référençant le modèle supprimé plantera silencieusement. Mettre à jour les cron jobs VERS UN AUTRE MODÈLE avant suppression. Exemple : `ollama rm qwen2.5-coder:7b` → d'abord `hermes cron update <id> --model deepseek-ai/deepseek-v4-flash --provider nvidia-nim`.

## ⚠️ Piège : SSH key copy-paste depuis Telegram
Telegram peut corrompre les caractères d'une clé SSH (e.g., `l` minuscule → `1`, sauts de ligne insérés). Toujours vérifier la clé sur https://github.com/settings/keys après ajout. Si `Permission denied`, supprimer et recoller en UNE SEULE LIGNE.

## Workflow typique
1. **Audit** la config actuelle du service
2. **Déployer** via Docker Compose ou systemd
3. **Sécuriser** (firewall, auth, limits)
4. **Monitorer** (health checks, logs, alertes)
5. **Optimiser** (sleep/wake, économie RAM)

## Références
- `references/github-ssh-repo-setup.md` — SSH key generation, PAT tokens, repo creation, Telegram copy-paste pitfalls

## Connexions Knowledge Graph
- [[service-coolify]] — PaaS dashboard
- [[service-ollama]] — LLM inference local
- [[tool-service-manager]] — Auto sleep/wake
- [[tool-devops-scripts]] — Scripts de maintenance