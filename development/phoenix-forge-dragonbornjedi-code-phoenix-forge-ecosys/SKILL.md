---
name: phoenix-forge
description: Build and manage Phoenix Forge ecosystem - Ezra Quest, Smart Home, Digital Empire. Use when working on quests, automations, Home Assistant, sales, or any Phoenix project.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Phoenix Forge Ecosystem Skill

## Quick Context
- **Ezra's Quest**: Gamified learning for 6-year-old Ezra
- **Smart Home**: Home Assistant + emotion engine + LED automations
- **Digital Empire**: Gumroad/Etsy/Shopify product sales
- **Hardware**: ESP32, Wii, IoT buttons, motion sensors

## Key Locations
- Main repo: ~/repos/phoenix-forge-ecosystem/
- Quest data: data/200_core_quests_COMPLETE.csv
- Emotion rules: 9_Documentation/emotion_engine_rules.yaml
- AI personas: ai/

## 20 Quest Categories
L(Literacy), M(Math), S(Science), T(Tech), H(History), LC(Language)
PF(Fitness), YM(Yoga), GM(Gross Motor), FM(Fine Motor)
ER(Emotional), SS(Social), SC(Self-Care), MM(Meditation)
HS(Household), SA(Safety), MR(Money), TM(Time)
VA(Visual Arts), MP(Music)

## APIs Available
- GROQ_API_KEY - Fast LLM
- GUMROAD_ACCESS_TOKEN - Sales
- GITHUB_TOKEN - Repos
- Check ~/.env for all keys

## Infrastructure
- DragonSnest: 100.71.190.76 (this laptop)
- Phone: 100.76.93.63
- Home Assistant: http://192.168.12.207:8123
