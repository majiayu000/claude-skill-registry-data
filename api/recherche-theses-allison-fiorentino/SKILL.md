---
name: "recherche-theses-allison-fiorentino"
description: "Recherche, cartographie et analyse des thèses de doctorat françaises via theses.fr (API ABES) et TEL (HAL). Spécialisée droit avec filtrage par sous-disciplines juridiques. Ouverte sur d'autres domaines universitaires. Capacités : (1) recherche multi-critères — sujet, directeur, jury, établissement, école doctorale, période, statut soutenue/en préparation, discipline ; (2) cartographie académique — qui dirige sur quel sujet, qui siège dans quels jurys, réseaux de co-direction, écoles doctorales productives ; (3) analyses temporelles — évolution d'un sujet, détection de saturation, calendrier des soutenances à venir ; (4) filtrage sous-discipline juridique — droit privé, public, social, affaires, international, etc. Déclencher dès que l'utilisateur mentionne thèse, doctorat, directeur de thèse, jury de thèse, école doctorale, soutenance, doctorant, ou demande une analyse d'écosystème doctoral. Pour articles ou ouvrages de doctrine, utiliser plutôt recherche-doctrine."
metadata:
  author: "Allison Fiorentino"
  license: "agpl-3.0"
  version: "2026-05-14"
---

# Recherche et Cartographie des Thèses de Doctorat — Droit

Skill spécialisée pour les enseignants-chercheurs, doctorants, jurys de recrutement et bibliothécaires juridiques. Couvre les thèses de doctorat françaises soutenues depuis 1985 et les thèses en préparation (depuis 2006).

> **Note de version (mai 2026)** : l'API publique theses.fr a été refondue (front Nuxt). Ce skill documente la **nouvelle structure** d'endpoints `/api/v1/theses/...` et `/api/v1/personnes/...`. Les anciennes routes `/api/v1/recherche/these` et `/api/v1/diffusion/...` ne fonctionnent plus. Voir § Procédure de récupération en cas de breakage.

## Sources et licences

| Source | Couverture | Endpoint racine | Licence |
|--------|-----------|-----------------|---------|
| **theses.fr API** (ABES) | Toutes thèses FR depuis 1985 + en préparation depuis 2006 | `https://theses.fr/api/v1/theses/recherche/` | Métadonnées sous Licence Ouverte Etalab 2.0 |
| **theses.fr — détail thèse** | Métadonnées complètes d'une thèse + champ `accessible` | `https://theses.fr/api/v1/theses/these/{NNT}` | Etalab 2.0 |
| **theses.fr — recherche personnes** | Recherche d'auteurs / directeurs / membres de jury | `https://theses.fr/api/v1/personnes/recherche/` | Etalab 2.0 |
| **theses.fr — profil personne** | **Rôles agrégés** (rapporteur, directeur, examinateur, président) + thèses + disciplines + établissements | `https://theses.fr/api/v1/personnes/personne/{PPN}` | Etalab 2.0 |
| **theses.fr — facets / completion / stats** | Facettes, autocomplétion, stats globales | `/api/v1/theses/facets/`, `/api/v1/theses/completion/`, `/api/v1/theses/statsTheses`, `/api/v1/theses/statsSujets` | Etalab 2.0 |
| **TEL (HAL)** | Texte intégral des thèses déposées | API HAL (`api.archives-ouvertes.fr/search/tel/`) | Variable, mention auteur obligatoire |
| **IdRef** | Référentiel d'autorités personnes/structures (PPN = IdRef) | `data.idref.fr` | Etalab 2.0 |
| **Sudoc** (optionnel) | Catalogue, thèses publiées en ouvrage | `www.sudoc.fr` | Etalab 2.0 |

**Périmètre :** thèses de doctorat uniquement. Les HDR, thèses d'exercice (médecine, pharmacie) et mémoires de master ne sont PAS dans theses.fr. Pour les HDR, signaler la limite à l'utilisateur.

## RÈGLES JURIDIQUES — À RESPECTER STRICTEMENT

**1. Métadonnées (titres, auteurs, jurys, dates, résumés, mots-clés)** — Réutilisation libre sous Etalab 2.0. Toujours ajouter en pied de réponse : *« Source : theses.fr / ABES — Licence Ouverte Etalab 2.0, données extraites le [date] ».*

**2. Texte intégral des thèses** — Le doctorant reste titulaire du droit d'auteur. Ne télécharger un PDF que si l'API confirme l'accès libre (champ `accessible:"oui"` sur l'endpoint détail). Ne JAMAIS tenter de contourner l'authentification CAS pour les thèses en accès restreint ESR.

**3. Citations dans les réponses** — Citations courtes uniquement (exception L.122-5, 3° CPI), entre guillemets, avec attribution. Pas de reproduction de paragraphes. Privilégier la paraphrase et le lien vers la thèse.

**4. Fouille de contenu (TDM)** — L'analyse automatisée est couverte par l'exception TDM recherche (L.122-5-3 II CPI) pour un enseignant-chercheur, à condition d'un accès licite. Donc : fouille uniquement sur thèses en accès libre.

**5. Données personnelles** — Les noms de directeurs, jurys et doctorants sont des données publiques au sens du RGPD (article 89 §1). Les utiliser pour cartographie académique est légitime. Ne pas extrapoler d'informations privées.

## ⚠️ PIÈGE PRINCIPAL — l'API ne renvoie pas d'erreur sur un champ Lucene inconnu

L'API renvoie **silencieusement `totalHits: 0`** quand un champ de la requête Lucene n'existe pas. Ce comportement masque des bugs de requête en faux négatifs. Toujours :

1. **Tester chaque champ** avec une requête sentinelle (un terme dont on sait qu'il existe) avant de conclure à l'absence de résultats.
2. **Privilégier les champs validés** ci-dessous.
3. Pour les champs imbriqués (directeurs, jury, école doctorale), passer par le **workflow PPN** (voir Capacité 2) plutôt que par une syntaxe `parent.enfant` qui ne fonctionne pas.

## Champs Lucene utilisables (validés mai 2026)

### Champs requêtables ✅

| Champ | Exemple | Notes |
|-------|---------|-------|
| `titrePrincipal` | `titrePrincipal:(blockchain)` | Titre français |
| `discipline` | `discipline:(droit*)` | ⚠️ pas `discipline.fr` |
| `dateSoutenance` | `dateSoutenance:[2020-01-01 TO 2025-12-31]` | Format `AAAA-MM-JJ` côté requête, mais retourné au format `JJ/MM/AAAA` |
| `status` | `status:soutenue` ou `status:enCours` | ⚠️ pas `enPreparation` |
| `accessible` | `accessible:oui` | String `"oui"` / `"non"` |
| `langues` | `langues:fr` | ⚠️ pluriel, pas `langue` |
| `etabSoutenanceN` | `etabSoutenanceN:(Lille)` | Établissement de soutenance |
| `sujetsLibelle` | `sujetsLibelle:(blockchain)` | Mots-clés libres saisis par l'auteur |

### Champs NON requêtables (renvoient 0 silencieusement) ❌

`directeursThese.nom`, `directeurs.nom`, `rapporteurs.nom`, `membresJury.nom`, `examinateurs.nom`, `presidentJury.nom`, `auteurs.nom`, `sujetsRameauLibelle`, `sujetsRameau.libelle`, `ecolesDoctorales.nom`, `partenairesRecherche.nom`, `etabCotutelleN`.

→ Pour ces critères, **deux contournements** :
- **Option A — workflow PPN (recommandé pour les personnes)** : interroger `/personnes/recherche/?q=Nom` pour trouver le PPN, puis `/personnes/personne/{PPN}` qui renvoie directement la liste des thèses associées et les rôles.
- **Option B — recherche full-text + filtrage client** : `?q=Loiseau` retourne tout document mentionnant ce nom, puis filtrer en Python sur le champ JSON pertinent.

## Structure JSON des réponses

⚠️ **Incohérence à connaître** : les deux endpoints n'utilisent PAS la même nomenclature pour les champs imbriqués.

### Endpoint `/theses/recherche/` (résultats de liste)

```
{
  "totalHits": 48613,
  "took": 53,
  "theses": [
    {
      "id": "...", "nnt": "...", "titrePrincipal": "...",
      "etabSoutenanceN": "...", "dateSoutenance": "JJ/MM/AAAA",
      "datePremiereInscriptionDoctorat": null,
      "auteurs":     [{"ppn", "nom", "prenom"}],
      "directeurs":  [{"ppn", "nom", "prenom"}],
      "rapporteurs": [{"ppn", "nom", "prenom"}],
      "examinateurs":[{"ppn", "nom", "prenom"}],
      "president":   {"ppn", "nom", "prenom"},      // singulier
      "discipline": "Droit",
      "status": "soutenue",
      "ecolesDoctorale":      [...],                 // singulier
      "partenairesDeRecherche":[...],                // 'De'
      "sujets": [...],
      "sujetsRameau": [{"ppn", "libelle"}]
    }
  ]
}
```

### Endpoint `/theses/these/{NNT}` (détail)

Champs supplémentaires et noms partiellement différents : `accessible`, `cas`, `codeEtab`, `doi`, `etabSoutenance` (sans `N`), `etabCotutelle`, `isSoutenue`, `langues`, `mapSujets`, `membresJury` (au lieu de `examinateurs`), `numSujet`, `partenairesRecherche` (sans `De`), `presidentJury` (au lieu de `president`), `resumes`, `source`, `titres` (multilingues), `ecolesDoctorales` (au pluriel).

→ Conséquence pratique : si on agrège des données issues des deux endpoints, **normaliser les noms côté client**.

### Endpoint `/personnes/personne/{PPN}` ⭐

Le plus utile pour la cartographie. Renvoie :

```
{
  "id": "035137576", "nom": "Loiseau", "prenom": "Grégoire", "has_idref": true,
  "roles": {
    "Rapporteur / Rapporteuse": 28,
    "Examinateur / Examinatrice": 70,
    "Directeur / Directrice": 79,
    "Président / Présidente du jury": 9,
    "Auteur / Autrice": 1
  },
  "theses": [...],
  "disciplines": ["Sciences juridiques", "Droit privé", "Droit"],
  "etablissements": ["Paris 1", "Paris 2", "Bordeaux"]
}
```

## Pagination et tri

- **Pagination** : `nombre=N&debut=K`. La limite testée fonctionne au moins jusqu'à `nombre=500` par requête. Pour de gros corpus, paginer par tranches de 100 reste prudent.
- **Tri** : ⚠️ **aucun paramètre `tri` ne semble appliqué côté serveur en mai 2026** (toutes les valeurs `dateSoutenance`, `dateSoutenanceDesc`, `dateSoutenanceAsc`, `-dateSoutenance`, `score` produisent le même ordre, qui n'est pas chronologique). **Trier côté client** après récupération.

## Capacités

### 1. Recherche d'objet thèse (multi-critères)

Combiner les filtres validés ci-dessus avec les opérateurs Lucene `AND`, `OR`, `NOT`, parenthèses. Exemple :

```
GET https://theses.fr/api/v1/theses/recherche/?q=
  titrePrincipal:(licenciement économique)
  AND discipline:(droit*)
  AND dateSoutenance:[2015-01-01 TO 2025-12-31]
  AND status:soutenue
&nombre=100&debut=0
```

Pour rechercher par sujet de manière plus large, combiner `titrePrincipal:(...)` avec une recherche full-text (sans préfixe de champ) qui interroge l'index complet : `?q=licenciement économique AND discipline:(droit*)`.

### 2. Cartographie académique — workflow PPN

**Pour identifier qui a rapporté/dirigé/jugé sur un sujet :**

```
1. Récupérer le corpus thématique via /theses/recherche/?q=...
2. Extraire les PPN uniques des champs directeurs/rapporteurs/examinateurs
3. (Optionnel) Pour chaque PPN, GET /personnes/personne/{PPN}
   → obtient les rôles agrégés sur l'ensemble du catalogue
   → utile pour distinguer un rapporteur "occasionnel" d'un "récurrent"
4. Agréger côté client (Counter Python sur PPN)
```

Désambiguïsation : le PPN de l'API theses.fr est l'identifiant Sudoc, qui est **identique** à l'IdRef. Une URL canonique vers la fiche personne : `https://www.idref.fr/{PPN}`.

**Pour cartographier une école doctorale ou un établissement :**

L'absence de champ Lucene utilisable pour `ecolesDoctorale` impose un workflow en deux temps :

```
1. /theses/recherche/?q=etabSoutenanceN:(NomEtab) AND status:soutenue
2. Côté client, regrouper sur les ecolesDoctorale[].nom retournées
```

### 3. Analyses temporelles

- **Courbe d'évolution** : récupérer toutes les thèses sur un sujet, agréger en Python par année (`dateSoutenance[-4:]` après split) → détection de saturation ou émergence
- **Calendrier prospectif** : `status:enCours` + `datePremiereInscriptionDoctorat` permet de prévoir les soutenances à venir (durée moyenne 3-6 ans en droit)
- **Délai de soutenance moyen** : différence `dateSoutenance` − `datePremiereInscriptionDoctorat`, utile pour comparer écoles doctorales

### 4. Filtrage par sous-discipline juridique

L'API expose la **discipline** déclarée par l'établissement (`discipline`, sans `.fr`), souvent libre, ce qui produit du bruit. Stratégie de filtrage :

- **Premier filtre grossier** : `discipline:(droit*)` capture la majorité des thèses juridiques
- **Affinage par mots-clés libres** : utiliser `sujetsLibelle:(...)` (plus précis qu'une recherche dans le titre) ; noter que `sujetsRameauLibelle` n'est PAS requêtable mais le champ `sujetsRameau[].libelle` est disponible **dans la réponse** pour filtrage côté client
- **Recherche full-text** : un `q=` sans préfixe interroge tout l'index, utile pour un thème transversal

Sous-disciplines principales gérées : droit privé, droit public, droit pénal, droit du travail / social, droit des affaires / sociétés / commercial, droit international (privé / public), droit européen, droit fiscal, histoire du droit, théorie / philosophie du droit, droit comparé, droit de la santé, droit du numérique, droit constitutionnel, droit administratif, procédure (civile / pénale / administrative).

## Workflow

### Étape 1 — Clarifier la demande

Avant toute recherche, identifier :
1. **Type de question** : objet thèse, cartographie, temporel, ou combiné ?
2. **Périmètre disciplinaire** : juridique général ou sous-discipline précise ?
3. **Période** : tout, dernières années, période historique ?
4. **Profondeur attendue** : liste rapide ou analyse complète avec graphiques ?

Si ambigu, demander avant de lancer une requête lourde.

### Étape 2 — Construction de la requête

Garder la requête initialement large pour éviter de manquer des résultats pertinents en raison d'une discipline mal renseignée. Rédiger un script Python plutôt que des curl pour faciliter l'agrégation.

```python
import urllib.request, urllib.parse, json
API = "https://theses.fr/api/v1/theses/recherche/"
q = ('titrePrincipal:(licenciement économique) '
     'AND discipline:(droit*) '
     'AND dateSoutenance:[2015-01-01 TO 2025-12-31] '
     'AND status:soutenue')
url = API + "?" + urllib.parse.urlencode({"q": q, "nombre": 100, "debut": 0})
data = json.loads(urllib.request.urlopen(url, timeout=30).read())
```

### Étape 3 — Affinage et croisement

- Si trop de résultats : ajouter contraintes (établissement, période plus serrée, mot-clé supplémentaire dans le titre)
- Si trop peu : retirer le filtre `discipline:(droit*)` (souvent trop strict si la thèse est mal classée), élargir aux résumés via une recherche full-text `q=...`
- **Test sentinelle systématique** : avant de conclure « pas de thèses sur ce sujet », faire une requête sans champ pour vérifier que le terme est indexé. Une requête `directeurs.nom:(Loiseau)` renvoie 0 alors que `Loiseau` en seul terme renvoie 655 hits.
- Désambiguïser les noms via le PPN avant agrégation sur les directeurs/jurys

### Étape 4 — Synthèse

Format de sortie selon la demande :
- **Liste de thèses** : tableau (auteur, titre, directeur, établissement, année, accessibilité, lien theses.fr)
- **Cartographie** : tableau ranking (personne, nombre de rôles, années, principaux sujets) ou graphe — privilégier le profil agrégé via `/personnes/personne/{PPN}` pour les figures principales
- **Analyse temporelle** : courbe ou tableau année / nombre de thèses, avec commentaire qualitatif
- **Analyse fine d'une thèse en accès libre** : récupérer la thèse via `/theses/these/{NNT}`, vérifier `accessible:"oui"`, puis chercher le PDF sur TEL/HAL si disponible

### Étape 5 — Citations et liens

Pour chaque thèse mentionnée :
- Lien canonique : `https://theses.fr/{NNT}` (ex : `https://theses.fr/2021NORMR098`)
- Lien personne : `https://www.idref.fr/{PPN}` ou `https://theses.fr/{PPN}`
- Mention de source Etalab obligatoire en pied de réponse
- Si une thèse n'est pas accessible en ligne, indiquer : *« Consultable en bibliothèque (Sudoc) »*

## Cas d'usage typiques en droit

**« Qui dirige des thèses sur le télétravail en France ? »**
→ Capacité 2. Recherche `titrePrincipal:(télétravail) AND discipline:(droit*) AND status:soutenue` + agrégation côté client sur `directeurs[].ppn` + tri par fréquence et récence.

**« Quelles thèses récentes sur la responsabilité algorithmique ? »**
→ Capacité 1 + 4. Recherche large `q=responsabilité algorithmique AND discipline:(droit*)` (full-text + filtre discipline) + tri date côté client.

**« Le sujet "discrimination à l'embauche" est-il saturé ? »**
→ Capacité 3. Récupération de toutes les thèses + agrégation annuelle Python + détection de pic.

**« Préparer un jury de thèse en droit du numérique : qui mobiliser ? »**
→ Capacité 2. Identifier les rapporteurs récurrents sur des thèses voisines (agrégation des PPN du champ `rapporteurs`) + désambiguïsation IdRef + consultation `/personnes/personne/{PPN}` pour confirmer le profil global.

**« Cette thèse a-t-elle été publiée en ouvrage ? »**
→ Croisement avec Sudoc par auteur ou titre.

**« Y a-t-il des thèses en cours sur la directive CSRD ? »**
→ Capacité 1 + 3. `status:enCours AND titrePrincipal:(CSRD)` + date prévisible de soutenance via `datePremiereInscriptionDoctorat`.

## Procédure de récupération en cas de breakage de l'API

Si une route renvoie 404 ou si tous les champs Lucene renvoient 0 :

```
1. curl -s "https://theses.fr/?q=test" -o /tmp/page.html
2. grep -o 'window.__NUXT__.config.*' /tmp/page.html
   → confirme la valeur courante de l'URL de l'API (clé `public.API`)
3. Identifier les chunks JS chargés :
   grep -oE '/_nuxt/[A-Za-z0-9_-]+\.js' /tmp/page.html
4. Télécharger les chunks et chercher les routes :
   curl -s "https://theses.fr/_nuxt/{chunk}.js" | grep -oE '"/[a-z]+/(recherche|completion|facets|stats)[^"]*"'
```

Cette procédure a permis (mai 2026) de retrouver les routes après leur refonte silencieuse.

## Limites à signaler à l'utilisateur

- **Délai de signalement** : entre soutenance et publication dans theses.fr, le délai moyen est de 250 jours. Les thèses des deux dernières années sont incomplètes.
- **Thèses en préparation** : le signalement n'est PAS obligatoire. Donc une absence dans theses.fr ne garantit pas qu'aucune thèse n'est en cours sur un sujet.
- **Champ `discipline`** : librement renseigné par les établissements, donc bruité. Compléter toujours par mots-clés libres (`sujetsLibelle`) ou recherche full-text.
- **Champs imbriqués non requêtables** : aucun filtre Lucene ne fonctionne sur `directeurs.*`, `rapporteurs.*`, `examinateurs.*`, `ecolesDoctorale.*`. L'API renvoie 0 hit sans erreur — risque élevé de faux négatifs si on ne le sait pas. Workflow PPN obligatoire.
- **Tri serveur inopérant** : aucun `tri=` ne semble appliqué — toujours trier côté client.
- **Jury et soutenance** : parfois absents pour les thèses anciennes (avant 2006).
- **HDR exclues** : signaler que les habilitations à diriger des recherches ne sont pas couvertes par theses.fr.
- **Thèses d'exercice exclues** : pour les thèses de médecine ou pharmacie, rediriger vers le Sudoc.
- **Incohérence des noms de champs JSON** entre `/theses/recherche/` et `/theses/these/{NNT}` : `examinateurs` vs `membresJury`, `president` vs `presidentJury`, `ecolesDoctorale` vs `ecolesDoctorales`, `partenairesDeRecherche` vs `partenairesRecherche`. Normaliser côté client.

## Mention de source obligatoire

À ajouter en pied de toute réponse utilisant ces données :

> *Sources : theses.fr / ABES — Licence Ouverte Etalab 2.0 ; le cas échéant, TEL (HAL) — données extraites le [JJ/MM/AAAA].*
