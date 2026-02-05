---
name: vendure
description: Assiste au développement avec le framework e-commerce Vendure pour Node.js. Gère le commerce headless, les APIs GraphQL, la gestion des commandes, les catalogues produits, l'intégration des paiements et le développement TypeScript e-commerce. Utiliser lors du travail sur des projets Vendure, la création de plugins, ou l'intégration de storefronts.
---

# Vendure E-Commerce Framework Skill

Assistance complète pour le développement Vendure, générée à partir de la documentation officielle (docs.vendure.io).

## Quand utiliser ce Skill

Déclencher ce skill pour :

- **Construction d'applications e-commerce headless** avec Node.js/TypeScript
- **Travail avec les APIs GraphQL** pour produits, commandes ou gestion clients
- **Implémentation d'intégrations de paiement** (Stripe, handlers personnalisés)
- **Création de plugins personnalisés** ou extension des fonctionnalités Vendure
- **Configuration de workflows de commande** et machines à états
- **Développement d'extensions Dashboard** avec React
- **Configuration de boutiques multi-devises** ou multi-canaux
- **Débogage de code Vendure** ou résolution de problèmes e-commerce
- **Apprentissage des bonnes pratiques Vendure** pour le développement TypeScript

## Concepts Clés

Concepts fondamentaux de l'architecture Vendure :

- **Order State Machine** - Workflow personnalisable (AddingItems → Delivered) via OrderProcess avec interceptors
- **Custom Fields** - Ajouter des propriétés aux entités via VendureConfig, extension automatique du schema GraphQL, support des relations et 10+ types de champs
- **Plugins** - Extensibilité via décorateur @VendurePlugin, hooks de cycle de vie, pattern InjectableStrategy pour comportement pluggable

## Guide de Navigation

Ce skill est organisé en **3 sections principales** pour une navigation optimale :

### 📚 references/Guides/ - Guides Pratiques (~16,000 lignes)

| Fichier                      | Lignes | Contenu                                        | Quand consulter               |
| ---------------------------- | ------ | ---------------------------------------------- | ----------------------------- |
| `getting-started.md`         | 619    | Installation, création projet, premiers pas    | **Démarrer un projet**        |
| `developer-guide.md`         | 5,247  | Architecture, API Layer, Middleware, NestJS    | **Comprendre l'architecture** |
| `core-concepts.md`           | 1,502  | Collections, Money, Assets, Taxes, Payment     | **Concepts fondamentaux**     |
| `extending-the-dashboard.md` | 2,362  | Extensions React, routes, pages personnalisées | **Personnaliser l'admin**     |
| `how-to.md`                  | 2,880  | Custom fields, paiements, shipping calculators | **Tutoriels spécifiques**     |
| `storefront.md`              | 1,618  | Next.js, Remix, connexion API, starters        | **Créer un storefront**       |
| `deployment.md`              | 1,145  | Docker, production, sécurité, HardenPlugin     | **Déployer en production**    |
| `user-guide.md`              | 473    | Utilisation Dashboard pour administrateurs     | **Former les utilisateurs**   |
| `migrating-from-v1.md`       | 302    | Breaking changes, guide de migration v1→v2     | **Migration de version**      |

**Commandes grep utiles :**

```bash
grep -n "OrderProcess" references/Guides/developer-guide.md
grep -n "Custom Fields" references/Guides/how-to.md
grep -n "Collections" references/Guides/core-concepts.md
```

---

### 📖 references/reference/ - Documentation API (~39,000 lignes)

| Fichier             | Lignes | Contenu                                              | Quand consulter                  |
| ------------------- | ------ | ---------------------------------------------------- | -------------------------------- |
| `typescript-api.md` | 21,561 | **TOUT** : Classes, interfaces, strategies, services | **Recherche API TypeScript**     |
| `admin-ui-api.md`   | 5,712  | API Angular (deprecated), composants legacy          | **Maintenir code Angular**       |
| `core-plugins.md`   | 4,527  | EmailPlugin, AssetServerPlugin, HardenPlugin, etc.   | **Configurer plugins officiels** |
| `dashboard.md`      | 3,585  | React hooks, composants Dashboard, extensions        | **Développer extensions React**  |
| `graphql-api.md`    | 4,078  | Shop API, Admin API, queries, mutations              | **Requêtes GraphQL**             |
| `reference.md`      | 35     | Index/overview de la section                         | Vue d'ensemble                   |

**Fichier clé : `typescript-api.md`** - Contient TOUTES les interfaces et classes Vendure.

**Commandes grep utiles :**

```bash
grep -n "^# " references/reference/typescript-api.md | head -50  # Liste des sections
grep -n "PaymentMethodHandler" references/reference/typescript-api.md
grep -n "OrderService" references/reference/typescript-api.md
grep -n "useDetailPage" references/reference/dashboard.md
```

---

### 🎨 references/UI/ - Composants Dashboard React (~4,500 lignes)

**NOUVELLE SECTION** - Composants UI pour extensions Dashboard

| Fichier                         | Lignes | Composants                                                           | Quand consulter          |
| ------------------------------- | ------ | -------------------------------------------------------------------- | ------------------------ |
| `ui.md`                         | 1,315  | 42 composants : Button, Dialog, Card, Badge, Popover, Tabs...        | **Éléments UI de base**  |
| `form-inputs.md`                | 1,082  | 11 composants : TextInput, SelectInput, CheckboxInput, DatePicker... | **Formulaires**          |
| `layout.md`                     | 862    | DetailPage, ListPage, PageLayout, TabsLayout                         | **Structure de pages**   |
| `framework.md`                  | 516    | DataTable, AssetGallery, PaginationControls                          | **Affichage de données** |
| `VENDURE_UI_COMPONENTS_BASE.md` | 724    | Documentation de base des composants                                 | **Référence rapide**     |

**Import standard :**

```tsx
import { Button, Card, Dialog, Badge } from "@vendure/dashboard";
import { TextInput, SelectInput } from "@vendure/dashboard";
import { DetailPage, ListPage } from "@vendure/dashboard";
```

**Commandes grep utiles :**

```bash
grep -A 20 "^## Button" references/UI/ui.md
grep -A 30 "TextInput" references/UI/form-inputs.md
grep -n "DetailPage" references/UI/layout.md
```

## Workflows par Niveau

### 🟢 Débutant - Premier projet

1. **Démarrer** → `references/Guides/getting-started.md`
2. **Comprendre** → `references/Guides/core-concepts.md` (Money, Collections)
3. **Construire** → `references/Guides/how-to.md`
4. **Explorer** → GraphQL Playground à `/shop-api`

### 🟡 Intermédiaire - Fonctionnalités personnalisées

1. **Rechercher API** → `references/reference/typescript-api.md`
2. **Créer plugins** → `references/Guides/developer-guide.md`
3. **Paiements** → `references/reference/core-plugins.md` (StripePlugin)
4. **Emails** → `references/reference/core-plugins.md` (EmailPlugin)

### 🔴 Avancé - Architecture & Production

1. **Architecture** → `references/Guides/developer-guide.md` (API Layer, Middleware)
2. **Dashboard custom** → `references/UI/` + `references/Guides/extending-the-dashboard.md`
3. **Sécurité** → `references/Guides/deployment.md` (HardenPlugin, OWASP)
4. **Performance** → State machines, caching, optimisations

## Liens Rapides par Tâche

| Tâche                  | Fichier de référence                                 |
| ---------------------- | ---------------------------------------------------- |
| Démarrer un projet     | `Guides/getting-started.md`                          |
| Afficher des prix      | `Guides/core-concepts.md`                            |
| Accepter des paiements | `reference/core-plugins.md`                          |
| Envoyer des emails     | `reference/core-plugins.md`                          |
| Créer un plugin        | `Guides/developer-guide.md`                          |
| Upload de fichiers     | `Guides/developer-guide.md`                          |
| Valider commandes      | `reference/typescript-api.md`                        |
| Requêtes GraphQL       | `reference/graphql-api.md`                           |
| Stocker des prix       | `Guides/core-concepts.md`                            |
| Installer Dashboard    | `Guides/getting-started.md`                          |
| Créer page Dashboard   | `UI/layout.md` + `Guides/extending-the-dashboard.md` |
| Composants formulaire  | `UI/form-inputs.md`                                  |
| DataTable              | `UI/framework.md`                                    |

## Conseils de Navigation

### Rechercher dans les fichiers

```bash
# Trouver une classe/interface
grep -rn "PaymentMethodHandler" references/

# Trouver un hook React
grep -rn "useDetailPage" references/reference/

# Trouver un composant UI
grep -n "Button" references/UI/ui.md

# Lister les sections d'un fichier
grep -n "^## " references/reference/typescript-api.md | head -30
```

### Structure des chemins

```
references/
├── Guides/              # Tutoriels et guides pratiques
│   ├── getting-started.md
│   ├── developer-guide.md
│   ├── core-concepts.md
│   ├── extending-the-dashboard.md
│   ├── how-to.md
│   ├── storefront.md
│   ├── deployment.md
│   ├── user-guide.md
│   └── migrating-from-v1.md
├── reference/           # Documentation API technique
│   ├── typescript-api.md    # ⭐ Le plus important (21k lignes)
│   ├── core-plugins.md
│   ├── dashboard.md
│   ├── graphql-api.md
│   ├── admin-ui-api.md
│   └── reference.md
└── UI/                  # Composants Dashboard React
    ├── ui.md               # 42 composants UI
    ├── form-inputs.md      # 11 composants formulaire
    ├── layout.md           # Pages et layouts
    ├── framework.md        # DataTable, etc.
    └── VENDURE_UI_COMPONENTS_BASE.md
```

## Ressources Additionnelles

### scripts/

Scripts utilitaires pour interagir avec les APIs GraphQL de Vendure.

#### Prérequis

- `curl` - Requêtes HTTP
- `jq` - Manipulation JSON
- `bash` 5+ - Requis pour tableaux associatifs (macOS: `brew install bash`)

#### Scripts disponibles

| Script     | Description                                |
| ---------- | ------------------------------------------ |
| `login.sh` | Authentification et aide aux requêtes curl |
| `query.sh` | Exécution simplifiée de requêtes GraphQL   |

#### `login.sh` - Authentification et aide curl

Script d'authentification pour obtenir un token JWT et faciliter les requêtes curl.

| Option           | Alias | Description               |
| ---------------- | ----- | ------------------------- |
| `--from-last`    | `-l`  | Utilise last-account.json |
| `--superadmin`   | `-s`  | Mode superadmin           |
| `--email`        | `-e`  | Email de connexion        |
| `--password`     | `-p`  | Mot de passe              |
| `--env`          | `-E`  | Chemin .env               |
| `--export`       | `-x`  | Affiche exports shell     |
| `--curl-example` | `-c`  | Exemple curl complet      |
| `--quiet`        | `-q`  | Mode silencieux           |
| `--verbose`      | `-v`  | Mode verbeux              |

```bash
./login.sh -l                 # Login avec last-account.json
./login.sh -l -c              # Affiche exemple curl complet
./login.sh -l -x              # Affiche exports shell
./login.sh -s -E /path/.env   # Login superadmin
./login.sh -e x@y.com -p z    # Login manuel
./login.sh -l -q              # Mode silencieux (scripts)
```

**`query.sh`** - Requêtes GraphQL simplifiées

| Option          | Alias | Description                                                     |
| --------------- | ----- | --------------------------------------------------------------- |
| `--vars`        | `-V`  | Variables GraphQL JSON (remplace tout)                          |
| `--set`         | -     | Modifier une variable (merge jq)                                |
| `--file`        | `-f`  | Fichier .graphql                                                |
| `--superadmin`  | `-s`  | Mode superadmin                                                 |
| `--env`         | `-e`  | Chemin .env                                                     |
| `--raw`         | `-r`  | Sortie JSON brute                                               |
| `--data`        | `-d`  | Affiche seulement .data                                         |
| `--clear-cache` | `-c`  | Force reconnexion                                               |
| `--timeout`     | `-t`  | Timeout en secondes                                             |
| `--history`     | `-H`  | Affiche les 10 dernières requêtes                               |
| `--last`        | `-L`  | Ré-exécute la dernière requête                                  |
| `--replay N`    | `-R`  | Ré-exécute la requête #N de l'historique                        |
| `--inspect N`   | `-I`  | Affiche query #N + variables (sans exécuter)                    |
| `--save NAME`   | `-S`  | Sauvegarde dans `queries/NAME.graphql`                          |
| `--shop`        | `-p`  | Utilise `/shop-api` au lieu de `/admin-api`                     |
| `--time`        | `-T`  | Affiche le temps d'exécution                                    |
| `--diff "OPTS"` | -     | Compare 2 exécutions (avant/après OPTS)                         |
| `--diff-only`   | -     | Avec --diff: affiche uniquement les valeurs changées            |
| `--no-fail`     | -     | Ne pas exit 1 sur erreur GraphQL (continuer malgré les erreurs) |
| `--dry-run`     | -     | Affiche la requête sans l'exécuter (pas d'auth)                 |
| `--curl`        | -     | Génère la commande curl équivalente (copier-coller)             |
| `--jq FILTER`   | `-j`  | Appliquer un filtre jq sur le résultat                          |
| `--assert EXPR` | `-a`  | Valider une condition jq (exit 1 si fausse)                     |
| `--quiet`       | `-q`  | Mode silencieux (supprime tous les logs stderr)                 |
| `--output FILE` | `-o`  | Écrire le résultat dans un fichier                              |
| `--verbose`     | `-v`  | Mode verbeux                                                    |

```bash
./query.sh '{ me { id } }'            # Requête simple
./query.sh -d '{ me { id } }'         # Affiche seulement .data
./query.sh -s -e /path/.env '{ administrators { totalItems } }'
./query.sh -c '{ me { id } }'         # Force reconnexion
./query.sh -t 60 '{ me { id } }'      # Timeout 60s (défaut: 30s)
./query.sh -s -c -d '{ me { id } }'   # Combinaison d'alias

# Historique et Replay (50 requêtes max, style Burp Repeater)
./query.sh -H                         # Affiche les 10 dernières
./query.sh -I 3                       # Inspecte query #3 + variables (sans exécuter)
./query.sh -L                         # Ré-exécute la dernière
./query.sh -L -s                      # Dernière requête en superadmin
./query.sh -R 3                       # Ré-exécute la requête #3
./query.sh -R 3 -s                    # Requête #3 en superadmin
./query.sh -R 3 --vars '{"take": 5}'  # Requête #3 avec variables remplacées
./query.sh -R 3 --shop                # Requête #3 sur shop-api
./query.sh -R 3 -T                    # Requête #3 avec timing

# Modifier des variables avec --set (merge intelligent)
./query.sh -R 3 --set '.take=10'                    # Modifier une variable
./query.sh -R 3 --set '.take=10 | .skip=20'         # Modifier plusieurs (pipe jq)
./query.sh -R 3 --set '.filter.status="active"'     # Objet imbriqué
./query.sh -R 3 --set '.take=10' --set '.id="99"'   # Multiples --set

# Comparer deux exécutions avec --diff
./query.sh '{ me { id } }' --diff "--superadmin"    # vendor vs superadmin
./query.sh -R 3 --diff "--set '.take=20'"           # take=10 vs take=20
./query.sh '{ products { totalItems } }' --diff "--shop"  # admin vs shop

# Mode compact avec --diff-only (affiche uniquement les chemins JSON modifiés)
./query.sh -R 3 --diff "--set '.take=1'" --diff-only
# Affiche: A .data.products.items[1].name = "Courgette"
#          B .data.products.items[1].name = (absent)

# Prévisualiser sans exécuter avec --dry-run (pas d'authentification)
./query.sh '{ products { items { id } } }' --dry-run
./query.sh -R 3 --set '.take=10' --superadmin --dry-run
./query.sh --file queries/get-product.graphql --vars '{"id":"42"}' --shop --dry-run
# Affiche: 📝 Query, 📦 Variables, 🔑 Auth, 🌐 Endpoint + "(non exécuté)"

# Générer une commande curl équivalente (copier-coller)
./query.sh '{ me { id } }' --curl
./query.sh '{ products { items { id } } }' --superadmin --curl
./query.sh -R 3 --vars '{"take": 5}' --shop --curl
# Affiche:
# curl -X POST 'http://localhost:3000/admin-api' \
#   -H 'Content-Type: application/json' \
#   -H 'Authorization: Bearer eyJ...' \
#   -d '{"query":"{ me { id } }","variables":{}}'

# Filtrer les résultats avec --jq
./query.sh '{ products { totalItems } }' --jq '.data.products.totalItems'
# → 42
./query.sh '{ products { items { name } } }' --jq '.data.products.items[].name'
# → Orange Sanguine
# → Courgette Longue verte
./query.sh '{ products { items { id name enabled } } }' \
  --jq '.data.products.items[] | select(.enabled == true) | .name'
./query.sh '{ products { items { id } } }' -j '.data.products.items | length'
# → 5

# Valider avec --assert (exit 1 si condition fausse)
./query.sh '{ products { totalItems } }' --assert '.data.products.totalItems > 0'
./query.sh '{ product(id: "1") { id } }' -a '.data.product | type == "object"'

# Workflows conditionnels avec && / ||
./query.sh '{ products { totalItems } }' --assert '.data.products.totalItems > 0' \
  && echo "Catalogue OK" || echo "Catalogue vide!"

# Combiner --assert et --jq (valider puis extraire)
./query.sh '{ products { totalItems } }' \
  --assert '.data.products.totalItems > 0' \
  --jq '.data.products.totalItems'

# Mode silencieux avec --quiet (capture propre)
TOTAL=$(./query.sh -q '{ products { totalItems } }' -j '.data.products.totalItems')
echo "Total: $TOTAL"

# Écrire dans un fichier avec --output
./query.sh '{ products { items { id name } } }' --output /tmp/products.json
./query.sh '{ orders { items { id } } }' -o /tmp/orders.json

# Automatisation totale : --quiet + --output + --assert + --jq
./query.sh -q '{ products { totalItems } }' \
  --assert '.data.products.totalItems > 0' \
  --jq '.data.products.totalItems' \
  -o /tmp/count.txt

# Sauvegarde
./query.sh -S get-me '{ me { id } }'  # Sauvegarde dans queries/get-me.graphql
./query.sh -f queries/get-me.graphql  # Charge et exécute

# Requête multi-lignes (guillemets simples)
./query.sh '
query {
  products(options: { take: 5 }) {
    items { id name }
  }
}
'

# Avec variables (utiliser heredoc si la requête contient !)
./query.sh --vars '{"id": "42"}' <<'EOF'
query GetProduct($id: ID!) {
  product(id: $id) { name }
}
EOF

# Depuis stdin
echo '{ me { id } }' | ./query.sh

# Shop API (storefront)
./query.sh --shop '{ products { items { id name } } }'
./query.sh --shop '{ activeCustomer { id emailAddress } }'

# Mesure du temps d'exécution
./query.sh -T '{ me { id } }'             # Affiche "⏱ 74ms"
./query.sh -s -T '{ administrators { totalItems } }'
./query.sh --shop -T '{ products { items { id } } }'
```

> **⚠️ Limitation** : Le caractère `!` (ex: `ID!`) pose problème en inline à cause
> du history expansion bash. Si erreur "Unexpected character", utiliser **heredoc**
> (`<<'EOF'`) ou **fichier** (`--file query.graphql`) à la place des guillemets simples.

#### Workflow de débogage (style Burp Repeater)

Le système d'historique et replay permet de déboguer efficacement les requêtes GraphQL :

```bash
# 1. Exécuter une requête qui échoue ou retourne des résultats inattendus
./query.sh '{ products(options: { take: 5 }) { items { id name } } }'

# 2. Consulter l'historique pour voir les requêtes récentes
./query.sh -H
# Affiche:
# [1] 14:23:01 { me { id } }...
# [2] 14:25:33 query GetProducts($take: Int)...
# [3] 14:28:45 { collections { items { id }...

# 3. Inspecter une requête AVANT de la rejouer (voir query + variables)
./query.sh -I 2
# ═══════════════════════════════════════════════════════════
# Query #2 (2025-12-30 14:25:33)
# ═══════════════════════════════════════════════════════════
# query GetProducts($take: Int) { products(options: { take: $take }) { ... } }
# ───────────────────────────────────────────────────────────
# Variables: {"take": 5}
# ═══════════════════════════════════════════════════════════

# 4. Rejouer une requête avec modifications
./query.sh -R 2                       # Identique
./query.sh -R 2 -s                    # En superadmin (voir plus de données)
./query.sh -R 2 --vars '{"take": 10}' # Remplacer toutes les variables
./query.sh -R 2 --shop                # Sur shop-api au lieu d'admin-api

# 5. Modifier des variables spécifiques avec --set (merge)
./query.sh -R 2 --set '.take=10'                  # Modifier une seule variable
./query.sh -R 2 --set '.filter.status="pending"'  # Modifier un objet imbriqué
./query.sh -R 2 --set '.take=10' --set '.skip=5'  # Modifier plusieurs variables

# 6. Comparer les résultats avec --diff
./query.sh -R 2 --diff "--superadmin"             # vendor vs superadmin (diff coloré)
./query.sh -R 2 --diff "--set '.take=10'"         # take=5 vs take=10
./query.sh -R 2 --diff "--shop"                   # admin-api vs shop-api
./query.sh -R 2 --diff "--set '.take=1'" --diff-only  # Mode compact (chemins JSON)
```

**Cas d'usage typiques :**

- **Inspecter avant de rejouer** : voir la query complète et ses variables avec `-I`
- **Prévisualiser sans exécuter** : utiliser `--dry-run` pour voir query/variables/auth/endpoint sans connexion
- **Générer curl** : utiliser `--curl` pour obtenir une commande curl copier-coller (Postman, CI/CD, partage)
- **Modifier chirurgicalement** : utiliser `--set` pour changer une variable sans tout retaper
- **Comparer rapidement** : utiliser `--diff` pour voir les différences, `--diff-only` pour le format compact
- **Valider avant d'agir** : utiliser `--assert` pour vérifier des conditions (workflows conditionnels)
- **Continuer malgré les erreurs** : utiliser `--no-fail` pour enchaîner plusieurs requêtes sans interruption
- **Extraire et filtrer** : utiliser `--jq` pour extraire des valeurs spécifiques
- **Capturer proprement** : utiliser `--quiet` pour supprimer les logs et capturer uniquement le résultat
- **Sauvegarder les résultats** : utiliser `--output` pour écrire dans un fichier (JSON propre sans couleurs)
- Modifier des objets imbriqués facilement avec la syntaxe jq
- Basculer entre admin-api et shop-api pour comparer les comportements
- Analyser les erreurs de permission en comparant vendor vs superadmin

#### Fichiers générés

- `last-account.json` : Credentials du dernier compte créé (email, password, vendorId)
- `.token-cache.vendor` : Cache des tokens vendeur (30 min)
- `.token-cache.superadmin` : Cache des tokens superadmin (30 min)
- `.query-history` : Historique des 50 dernières requêtes GraphQL
- `queries/` : Requêtes GraphQL sauvegardées avec `--save`

## Notes

- Ce skill est généré à partir de la documentation officielle Vendure (docs.vendure.io)
- Les exemples de code incluent la détection de langage pour le highlighting
- Toutes les valeurs monétaires sont représentées en entiers (diviser par 100 pour l'affichage)
- GraphQL est l'interface API principale (Shop API pour storefront, Admin API pour gestion)
- Le Dashboard utilise React et TailwindCSS - toujours importer depuis `@vendure/dashboard`

## Mise à jour

Pour rafraîchir ce skill avec une documentation mise à jour :

1. Re-scraper la documentation officielle docs.vendure.io
2. Réorganiser les fichiers dans la structure Guides/reference/UI
3. Mettre à jour les compteurs de lignes dans ce SKILL.md
