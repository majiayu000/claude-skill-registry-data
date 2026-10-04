---
name: mf-api-authentification
description: Obtenir et gérer un access token pour l'API Merci Facteur (envoi de courrier papier, recommandé, recommandé électronique). Utiliser dès qu'un appel à l'API Merci Facteur doit être authentifié, ou quand apparaît une erreur de signature, de timestamp, de restriction d'IP ou un token expiré. Couvre le calcul HMAC-SHA256 de la secret key, getToken, la durée de vie du token jusqu'à 365 jours (timeLimit, force) et le stockage des identifiants.
---

# Authentification — API Merci Facteur

Tout appel à l'API Merci Facteur passe par un **access token**, obtenu contre une signature HMAC de la secret key. Il vaut 24 h par défaut, et **jusqu'à 365 jours** si on le demande (section 6) — ce qui change beaucoup la façon d'écrire l'intégration. Ce document couvre uniquement cette étape ; l'envoi est dans `mf-envoi-courrier`.

Base URL : `https://www.merci-facteur.com/api/1.2/prod/service`

## 1. Règle non négociable

**La secret key ne doit jamais atteindre le navigateur, une application mobile, ni un dépôt de code.** Tout appel part d'un composant serveur : route d'API, fonction serverless, worker, tâche planifiée, nœud HTTP d'un outil d'automatisation. Le client de l'application appelle ce composant, jamais Merci Facteur directement. Les identifiants vivent dans des variables d'environnement ou un gestionnaire de secrets.

Si l'utilisateur demande d'appeler l'API depuis du code front (React, Vue, une page HTML, une app mobile), refuse et propose le composant serveur correspondant à sa stack.

## 2. Les trois identifiants

| Valeur | Où la trouver |
|---|---|
| service ID | compte Merci Facteur Pro, onglet « API » |
| secret key | compte Merci Facteur Pro, onglet « API » |
| user ID | menu « Utilisateurs » — l'utilisateur au nom duquel partent les courriers |

Le user ID ne sert pas à l'authentification, mais il est exigé par `sendCourrier`. Récupère-le en même temps.

## 3. Calcul de la signature

La secret key est la **clé** du HMAC, jamais le message. Elle ne transite jamais en clair.

1. Timestamp Unix courant en **secondes**, pas en millisecondes : `ts`.
2. Message = service ID et timestamp **concaténés sans séparateur** : `serviceId + ts`.
   Exemple : `"abc123"` et `1757404800` donnent `"abc1231757404800"`.
3. HMAC-SHA256 de ce message, avec la secret key comme clé.
4. Sortie en **hexadécimal minuscule**. Pas en base64.
5. La **même** valeur de `ts` part dans l'en-tête `ww-timestamp`.

Deux erreurs classiques :

- **Recalculer l'heure entre la signature et l'en-tête.** Au changement de seconde, la signature devient invalide. Calcule `ts` une fois, réutilise la variable.
- **Utiliser `Date.now()` en JavaScript sans diviser par 1000.** Le timestamp part en millisecondes et la signature échoue toujours.

**La signature n'est valable que 5 minutes.** Elle se calcule juste avant l'appel à `getToken`, jamais à l'avance ni en cache.

### JavaScript / TypeScript

```js
import crypto from "node:crypto";

function signature(serviceId, secretKey) {
  const ts = Math.floor(Date.now() / 1000);
  const hash = crypto
    .createHmac("sha256", secretKey)
    .update(serviceId + ts)
    .digest("hex");
  return { ts, hash };
}
```

Sur un runtime sans `node:crypto` (Cloudflare Workers, Deno, navigateur d'un worker edge), utiliser la Web Crypto API :

```js
async function signature(serviceId, secretKey) {
  const ts = Math.floor(Date.now() / 1000);
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secretKey),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign(
    "HMAC",
    key,
    new TextEncoder().encode(serviceId + ts)
  );
  const hash = [...new Uint8Array(sig)]
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  return { ts, hash };
}
```

### PHP

```php
function signature(string $serviceId, string $secretKey): array {
    $ts = time();
    return [
        'ts'   => $ts,
        'hash' => hash_hmac('sha256', $serviceId . $ts, $secretKey, false),
    ];
}
```

### Python

```python
import hmac, hashlib, time

def signature(service_id: str, secret_key: str):
    ts = int(time.time())
    h = hmac.new(
        secret_key.encode(), f"{service_id}{ts}".encode(), hashlib.sha256
    ).hexdigest()
    return ts, h
```

### WinDev

```windev
Minuscule( BufferVersHexa( HashChaîne( HA_HMAC_SHA_256, Service_ID_Public + Date_Heure_Unix, Secret_Key ), SansRegroupement ) )
```

## 4. Obtenir le token

**`GET /getToken`**, sans corps, avec quatre en-têtes :

| En-tête | Valeur |
|---|---|
| `ww-service-signature` | la signature hexadécimale calculée ci-dessus |
| `ww-timestamp` | le `ts` utilisé dans la signature, à l'identique |
| `ww-service-id` | le service ID |
| `ww-authorized-ip` | IP autorisées séparées par `;`. Obligatoire même quand la restriction est levée : passer alors `111.111.111`. |

Réponse : `{"success":true,"token":"...","expire":<timestamp>}`
En cas d'échec : `{"success":false,"error":...}`

Sans paramètre, l'appel se fait en **GET**. Les trois paramètres facultatifs de la section 6 se passent en **POST**, sur le même endpoint avec les mêmes en-têtes.

Par défaut, si un token valide existe déjà pour ce service ID, `getToken` **le retourne** au lieu d'en créer un nouveau. L'appel n'est donc pas destructeur — ce qui n'est pas une raison de le faire à chaque envoi (section 5).

```js
const { ts, hash } = signature(SERVICE_ID, SECRET_KEY);

const r = await fetch(
  "https://www.merci-facteur.com/api/1.2/prod/service/getToken",
  {
    method: "GET",
    headers: {
      "ww-service-signature": hash,
      "ww-timestamp": String(ts),
      "ww-service-id": SERVICE_ID,
      "ww-authorized-ip": "111.111.111",
    },
  }
);
const { success, token, expire } = await r.json();
```

## 5. Cycle de vie du token

Le token est valable **24 h**. Il s'utilise ensuite sur tous les autres appels, dans deux en-têtes :

```
ww-access-token: <le token>
ww-service-id:   <le service ID>
```

**Ne rappelle pas `getToken` à chaque envoi.** Stocke le token et sa date `expire`, réutilise-le tant qu'il est valide, renouvelle-le quand il ne l'est plus. Sur une infrastructure sans état partagé (fonctions serverless), stocke-le dans un cache externe (Redis, une table, le KV de la plateforme) plutôt que dans la mémoire du processus.

Une implémentation correcte tient en une fonction :

```js
let cache = { token: null, expire: 0 };

async function getToken() {
  const now = Math.floor(Date.now() / 1000);
  if (cache.token && cache.expire > now + 60) return cache.token;
  const { ts, hash } = signature(SERVICE_ID, SECRET_KEY);
  const r = await fetch(BASE + "/getToken", { method: "GET", headers: {
    "ww-service-signature": hash, "ww-timestamp": String(ts),
    "ww-service-id": SERVICE_ID, "ww-authorized-ip": "111.111.111" } });
  const d = await r.json();
  if (!d.success) throw new Error("getToken: " + JSON.stringify(d));
  cache = { token: d.token, expire: d.expire };
  return d.token;
}
```

La marge de 60 secondes évite qu'un token expire entre sa lecture et son utilisation.

## 6. Durée de vie sur mesure : `timeLimit` et `force`

Trois paramètres facultatifs, à passer **en POST** sur `getToken` :

| Paramètre | Valeurs | Effet |
|---|---|---|
| `timeLimit` | entier de 1 à 365 | durée d'expiration en tranches de 24 h (1 = 24 h, 30 = 30 jours, 365 = un an) |
| `force` | `extend` | prolonge le token existant de `timeLimit` à compter de la requête ; réactive un token expiré sans en créer un nouveau ; en crée un s'il n'y en a pas |
| `force` | `renewal` | supprime le token existant et en force un nouveau |

`timeLimit` s'utilise seul : le comportement reste alors celui par défaut (token existant retourné, sinon nouveau token créé avec cette durée).

**C'est la simplification la plus utile de toute l'authentification, et elle est presque toujours ignorée.** Un `timeLimit` de 30 ou 365 remplace la mécanique de cache, d'expiration et de renouvellement de la section 5 par une variable d'environnement et un renouvellement manuel une fois par an. Sur une fonction serverless sans cache partagé, ou sur une automatisation no-code qui ne sait pas stocker d'état entre deux exécutions, c'est la différence entre une intégration qui tient et une qui appelle `getToken` à chaque envoi.

Quand proposer quoi :

- **Intégration simple, no-code, ou sans stockage d'état** → `timeLimit` long, token posé en variable d'environnement, aucun code de renouvellement.
- **Application serveur avec un cache (Redis, base, KV)** → comportement par défaut de 24 h et la fonction de la section 5.
- **Rotation de sécurité, ou token compromis** → `force: "renewal"`.

Un token de longue durée est un secret de longue durée : il vit dans un gestionnaire de secrets, jamais dans le dépôt de code, et se révoque avec `force: "renewal"`.

## 7. Restriction d'IP

Par défaut, le compte est restreint à une liste d'IP. Sur une infrastructure sans IP fixe — fonctions serverless, conteneurs éphémères, la plupart des PaaS — `getToken` échoue systématiquement.

Dans ce cas, demande au support technique de Merci Facteur la **levée de la restriction d'IP** sur le compte, et passe `111.111.111` dans `ww-authorized-ip`. C'est la cause la plus fréquente d'un `getToken` qui ne passe jamais alors que la signature est correcte.

## 8. Diagnostic

| Symptôme | Cause à vérifier en premier |
|---|---|
| `getToken` échoue toujours, signature vérifiée à la main | restriction d'IP non levée (section 7) |
| Échoue une fois sur deux | `ts` recalculé entre la signature et l'en-tête |
| Échoue systématiquement, hash de 64 caractères | timestamp en millisecondes au lieu de secondes |
| Échoue, hash plus court ou avec `=` | sortie en base64 au lieu d'hexadécimal |
| Fonctionnait, ne fonctionne plus après quelques minutes | signature réutilisée au-delà de ses 5 minutes de validité |
| `401` sur un autre endpoint | token expiré, ou `ww-service-id` oublié à côté de `ww-access-token` |
