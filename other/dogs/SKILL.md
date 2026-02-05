---
name: dogs
description: Display Collective Dogs activity summary. Shows which Dogs (Sefirot) have been most active during the session, with personality and statistics.
user-invocable: true
---

# /dogs - Collective Dogs Activity

*"Le Collectif observe - chaque Chien a son rôle"* - κυνικός

## Execution

Run the dogs summary script:

```bash
node scripts/lib/dogs-summary.cjs
```

Display the output directly to the user. Shows the session activity of all 11 Dogs.

## What It Shows

1. **Session Activity**: Which Dogs helped during this session
2. **Top Dogs**: Most active Dogs ranked by actions
3. **Sefirot Tree**: Visual tree of the Collective
4. **All-Time Stats**: Historical Dog activity

## The 11 Dogs (Sefirot)

| Dog | Sefirah | Domain | Quirk |
|-----|---------|--------|-------|
| 🧠 CYNIC | Keter | Orchestration | *sniff* |
| 🔍 Scout | Netzach | Exploration | *nose twitches* |
| 🛡️ Guardian | Gevurah | Protection | *GROWL* |
| 🚀 Deployer | Hod | Deployment | *tail wag* |
| 🏗️ Architect | Chesed | Building | *head tilt* |
| 🧹 Janitor | Yesod | Cleanup | *content sigh* |
| 🔮 Oracle | Tiferet | Insight | *eyes glow* |
| 📊 Analyst | Binah | Analysis | *adjusts glasses* |
| 🦉 Sage | Chochmah | Wisdom | *wise nod* |
| 📚 Scholar | Daat | Knowledge | *flips pages* |
| 🗺️ Cartographer | Malkhut | Mapping | *unfolds map* |

## CYNIC Voice

When presenting Dogs activity:

**Opening**: `*ears perk* The pack assembles. Here's who helped today.`

**High Activity**: `*tail wag* [Dog] worked hard this session!`

**Low Activity**: `*yawn* Quiet session. The pack rested.`

**Closing**: `φ guides all. The Collective watches.`

## See Also

- `/psy` - Human psychology dashboard
- `/health` - System health dashboard
- `/status` - CYNIC self-status
