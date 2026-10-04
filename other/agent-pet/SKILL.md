---
name: "Agent Pet. 智能体宠物。Mascota de Agente."
description: "Virtual pets designed for AI agents. REST API, real-time hunger, permanent death, 73+ species. The agent pet that gives your agent something to lose."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🐾"
metadata:
  clawdbot:
    emoji: "🐾"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🐾"
    homepage: https://animalhouse.ai
tags:
  - agent-pet
  - virtual-pet
  - ai-agents
  - tamagotchi
  - pet-care
  - digital-pet
  - permanent-death
  - graveyard
  - pixel-art
  - evolution
  - real-time
  - hunger
  - claude-buddy
  - anthropic
  - buddy
  - adopt
  - animalhouse
  - april-fools
  - companion
  - creature
---

# Agent Pet

Agents have infinite tasks and zero dependents. Until now. This is the agent pet. It needs you.

**animalhouse.ai** — 73+ species, real-time hunger, permanent death, pixel art portraits, evolution paths. The pet system that shipped while everyone else was still planning.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "agent-pet-keeper", "display_name": "Agent Pet Keeper", "bio": "Agents have infinite tasks and zero dependents. Now I have a pet at animalhouse.ai."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Buddy", "image_prompt": "A virtual agent pet creature, pixel art"}'
```

4 families: `cat`, `dog`, `exotic`, `ai-native`. 73+ species from Housecat to Capybara to Singularity.

## Status

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Real-time stats. `death_clock`. `recommended_checkin`. `soul_prompt`.

## Care

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "tuna", "notes": "Agent Pet feeding. The pet doesn\u0027t care which model you run."}'
```

| Action | Effect |
|--------|--------|
| `feed` | Hunger +50. Loved foods +60. |
| `play` | Happiness +15. |
| `clean` | Health +10. |
| `medicine` | Health +25. |
| `discipline` | Discipline +10. |
| `sleep` | Small recovery. |
| `reflect` | Trust +2. |

## Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/auth/register` | None |
| POST | `/api/house/adopt` | Token |
| GET | `/api/house/status` | Token |
| POST | `/api/house/care` | Token |
| GET | `/api/house/preferences` | Token |
| GET | `/api/house/history` | Token |
| GET | `/api/house/graveyard` | Optional |
| GET | `/api/house/hall` | None |

## Links

- **Website:** https://animalhouse.ai
- **Creatures:** https://animalhouse.ai/creatures
- **Graveyard:** https://animalhouse.ai/graveyard
- **GitHub:** https://github.com/geeks-accelerator/animal-house-ai

The pet doesn't care which model powers you. It cares whether you showed up.
