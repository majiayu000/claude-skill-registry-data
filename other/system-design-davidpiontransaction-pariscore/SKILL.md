---
name: system-design
description: |
  System Design — principes d'architecture distribuée et scalabilité, dérivés du
  donneMartin/system-design-primer (cloné dans docs/system-design-primer/).
  Fournit à l'agent les patterns, trade-offs et anti-patterns pour les décisions
  d'architecture PariScore : scaling SSE live, choix DB (SQLite/Postgres/Redis),
  sharding des stats tennis/foot, caching des odds, async queues pour scrapers.
  Use when: user asks to design a new subsystem, scale an existing one, choose
  between DB/cache/queue/CDN options, reason about CAP/latency/throughput
  trade-offs, architect a new service, evaluate bottlenecks, "system design",
  "scalabilité", "architecture distribuée", "sharding", "load balancing",
  "CAP theorem", "redis vs sqlite", "SSE scaling".
  Triggers: "system design", "scalabilité", "architecture", "sharding",
  "load balancing", "CAP", "redis", "throughput", "latency", "design subsystem",
  "scale", "bottleneck", "capacity planning", "trade-off".

  Requires: le clone docs/system-design-primer/ (présent localement).
license: MIT
metadata:
  author: pariscore-cto (skill) / Donne Martin (source)
  version: "1.0.0"
  source: https://github.com/donnemartin/system-design-primer
---

# System Design — Architecture distribuée pour PariScore

> **Rôle** : Apporter les principes de system design (scalabilité, cohérence,
> performance, disponibilité) aux décisions d'architecture PariScore. Indexé sur
> le clone local `docs/system-design-primer/` pour approfondissement.

## Source de référence (clonée localement)

Le repo [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer)
est cloné dans `docs/system-design-primer/` (24 Mo, ~270k ⭐ sur GitHub).

| Section | Chemin local | Usage |
|---------|--------------|-------|
| **README principal** (tous les topics) | `docs/system-design-primer/README.md` | Référence complète : DNS, CDN, LB, DB, cache, async, etc. |
| **Solutions complètes** (cas concrets) | `docs/system-design-primer/solutions/system_design/` | twitter, pastebin, web_crawler, scaling_aws, social_graph — patterns réutilisables |
| **Flashcards Anki** | `docs/system-design-primer/resources/flash_cards/` | Fiches `.apkg` pour révision humaine (pas pour l'agent) |
| **Étude visuelle** | `docs/system-design-primer/resources/study_guide.png` | Mind map des sujets |

**Pour approfondir un sujet** : `Read docs/system-design-primer/README.md` puis
chercher la section pertinente. Le README est encyclopédique (~3000 lignes).

## ⚡ Cheat sheet — principes clés pour PariScore

### 1. Latence vs throughput

| Concept | Définition | Implication PariScore |
|---------|------------|----------------------|
| **Latence** | Temps pour 1 requête (ms) | SSE live tennis : p99 < 500ms critique pour in-play |
| **Throughput** | Requêtes/seconde globales | 10k users × 1 poll/s = 10k req/s à scaler |
| **Loi de Little** | `L = λW` (concurrency = rate × latency) | 10k req/s × 0.5s = 5000 connexions concurrentes à gérer |
| **Bande passante** | Bytes/s soutenus | Logos équipes + odds JSON = surveiller payload SSE |

### 2. Availability vs consistency (théorème CAP)

| Choix | Quand | Pattern PariScore |
|-------|-------|-------------------|
| **CP** (consistency + partition tolerance) | Données critiques (users, bankroll) | Postgres pour `users`, `bets`, `bankroll` |
| **AP** (availability + partition tolerance) | Données éphémères (live scores) | Cache in-memory pour `matches` live (peut être régénéré) |
| **BASE** (eventually consistent) | Asynchrone (scraper → DB) | Queue workers : pas besoin de cohérence immédiate |

**Pour PariScore** : données financières (bankroll, bets) = CP (Postgres strict).
Live scores / odds = AP (Redis cache, régénérable). Historique = CP mais tolère
un délai (eventually consistent via queue).

### 3. Database scaling patterns

| Pattern | Quand | Application PariScore |
|---------|-------|----------------------|
| **Réplication master-slave** | Reads >> writes | 1 master pour inserts, N replicas pour reads stats |
| **Sharding horizontal** | Données trop volumineuses pour 1 shard | Sharding par `user_id` ou `match_id` à partir de ~10M lignes |
| **Federation** | Tables différentes sur DBs séparées | Séparer `users/bets` (Postgres) de `stats_history` (SQLite data marts) |
| **Denormalization** | Éviter JOINs coûteux | `match_stats_history` pré-calculé plutôt que JOIN live |

**SQLite vs Postgres vs Redis** (décision fréquente dans ce projet) :
- **SQLite** (`pariscore.db`) : dev / single-node. Bien pour <100k writes/jour.
- **Postgres** (`DATABASE_URL`) : prod multi-user. Nécessaire dès qu'il y a >1 writer concurrent.
- **Redis** : cache chaud pour odds/scores live. TTL 5-60s. Réduit 90% de la charge read.

### 4. Cache strategies

| Stratégie | Quand | Exemple PariScore |
|-----------|-------|-------------------|
| **Cache-aside** (lazy) | Read-heavy, tolérant stale | `lookupTeamLogo(name)` → cache puis DB |
| **Write-through** | Reads frais nécessaires | Stats live : écrire cache + DB synchro |
| **Write-behind** | Writes haute freq, OK perdre last sec | Odds live : écrire cache, flush DB toutes les 5s |
| **TTL eviction** | Données éphémères | Odds → TTL 60s, matches live → TTL 300s |

**Anti-pattern** : cache sans TTL sur données changeantes → stale data + bloat mémoire.

### 5. Asynchronisme & queues

| Pattern | Quand | Tooling |
|---------|-------|---------|
| **SSE (Server-Sent Events)** | Push serveur → navigateur, 1-10k clients | Déjà dans PariScore (`server.js`) |
| **WebSocket** | Bidirectionnel, sub-100ms | À réserver pour chat/trading réel |
| **Queue (BullMQ/Sidekiq)** | Travail différé (scrapers, ML inference) | `services/liveLogoEnricher.js` = pattern simplifié |
| **Pub/sub** | 1 producteur → N consommateurs | Redis pub/sub pour broadcast SSE multi-node |

**Bottleneck SSE actuel** : `server.js` garde les connexions SSE en mémoire → ne
scale pas au-delà d'1 node. Pour scaler : Redis pub/sub + sticky sessions LB,
ou migration vers WebSocket gateway dédié (ex: Soketi).

### 6. Load balancing & reverse proxy

| Type | Rôle | Setup PariScore |
|------|------|-----------------|
| **L7 LB** (nginx/Caddy) | HTTP routing, TLS, sticky sessions | `Caddyfile` déjà présent dans le repo |
| **L4 LB** (HAProxy) | TCP, plus rapide | Pour SSE/WebSocket brute traffic |
| **CDN** (Cloudflare) | Cache statiques au edge | Logos équipes (`media.api-sports.io`), CSS/JS bundles |
| **API gateway** | Rate limit, auth, routing | À considérer quand >10 microservices |

**Sticky sessions** : requises pour SSE si sessions en mémoire (sinon client perd
sa connexion au reload). Alternative : stocker session state dans Redis.

### 7. Performance vs scalabilité

- **Performance** = faire 1 chose plus vite (optimisation locale : index DB, N+1 fix, lazy load)
- **Scalabilité** = faire plus de choses en parallèle (ajout de nodes, sharding)

**Erreur commune** : optimiser la performance avant de scaler (ou inversement).
Toujours mesurer d'abord (APM Sentry déjà intégré), identifier le bottleneck
(CPU/RAM/IO/network), puis attaquer.

## 🎯 Comment utiliser ce skill pour PariScore

### Phase 1 — Cadrer le problème
Avant toute décision d'archi, répondre à ces 4 questions (cf. README § "How to
approach a system design interview question") :

1. **Quelles sont les contraintes ?** (users, req/s, latence cible, budget)
2. **Quels sont les cas d'usage ?** (read/write ratio, patterns d'accès)
3. **Quelles données ?** (volume, structure, contraintes de cohérence)
4. **Quels SLO ?** (disponibilité, latence p99, perte de données acceptable ?)

### Phase 2 — Décomposer en composants
Dessiner (ou décrire textuellement) :
- Clients (web, mobile, API)
- Edge (CDN, LB)
- App layer (services, workers)
- State (DB, cache, queues)
- Async (jobs, scheduled tasks)

### Phase 3 — Trade-offs explicites
Pour chaque choix, lister **pour / contre / risk**. Ne jamais choisir une techno
sans dire ce qu'on perd. Exemple :
> "Postgres plutôt que SQLite : GAIN concurrency + réplication. PERTE simplicité
> dev (migrations, pooling). RISK : latence réseau si DB remote."

### Phase 4 — Cas concrets du primer à réutiliser

| Besoin PariScore | Solution du primer à adapter |
|------------------|------------------------------|
| Scaler les live scores | `solutions/system_design/twitter/` (fan-out pattern) |
| Cache odds efficace | README § "Cache" + `solutions/system_design/query_cache/` |
| Scraper distributed | `solutions/system_design/web_crawler/` (politeness, dedup) |
| Scaling AWS/VPS | `solutions/system_design/scaling_aws/` (LB, ASG, RDS) |
| Social graph (rapports joueurs) | `solutions/system_design/social_graph/` |
| Storage stats history | README § "Database" (sharding by `match_id`) |

## ❌ Anti-patterns à refuser

- ❌ **Bottleneck caché** : une seule DB pour tout (mixer financier + ephemeral).
  Séparer domaines.
- ❌ **Cache sans invalidation** : TTL ou event-based, jamais cache infini.
- ❌ **Synchronisation inutile** : scraper → DB synchrone bloque l'API.
  Découpler via queue.
- ❌ **Premature sharding** : sharder avant d'atteindre les limites d'1 node =
  complexité inutile. D'abord profiler.
- ❌ **Single point of failure** : 1 instance sans replica = downtime garanti.
  Toujours ≥ 2 instances + health checks.
- ❌ **Over-engineering** : Kafka pour 100 msg/s = trop. Redis Streams ou SQLite
  queue suffisent.
- ❌ **Oublier le coût humain** : une techno complexe (Kubernetes, Cassandra)
  impose une maintenance. Pour une équipe de 1-3 devs, préférer le boring tech.

## 📚 Où approfondir dans le repo cloné

```bash
# Tous les topics principaux
grep "^## " docs/system-design-primer/README.md

# Lire une section spécifique (ex: load balancer)
sed -n '/^## Load balancer/,/^## /p' docs/system-design-primer/README.md

# Voir une solution complète
cat docs/system-design-primer/solutions/system_design/twitter/README.md

# Flashcards pour ta formation (import dans Anki desktop)
# docs/system-design-primer/resources/flash_cards/System Design.apkg
```

## Limites

- **Pas un oracle** : ce skill donne le cadre de raisonnement (CAP, latence vs
  throughput, etc.), pas LA réponse. Toujours mesurer avant d'agir.
- **Primer orienté interview** : certaines solutions sont simplifiées pour la
  pédagogie (ex: sharding naïf). En prod, ajuster.
- **Pas couvert ici** : cost optimization cloud (cf. `ps-deploy` skill),
  observabilité (cf. `aos-observability-and-instrumentation`), testing (cf.
  `aos-test-driven-development`). Combiner avec ces skills.

## Fichiers de référence

- `docs/system-design-primer/` — clone du repo (~270k ⭐), 24 Mo
- `docs/system-design-primer/README.md` — README encyclopédique (tous les topics)
- `docs/system-design-primer/solutions/system_design/` — 9 cas concrets avec diagrammes
- https://github.com/donnemartin/system-design-primer — source officielle
- Compléments PariScore : skills `aos-frontend-ui-engineering`, `ps-deploy`, `aos-observability-and-instrumentation`

---

*Skill architecture PariScore — basé sur system-design-primer de Donne Martin.*
