---
name: eve-esi-api
description: EVE Online ESI API patterns and zkillboard integration. Covers ESI endpoints, authentication, data models, zkillboard RedisQ listener, caching strategies, and EVE-specific IDs (characters, corporations, alliances, ships, systems, regions). Use when working with killmail data, fetching EVE universe info, or implementing ESI calls.
---

# EVE Online ESI API Guidelines

## Purpose

Patterns for interacting with the EVE Online ESI API and zkillboard data feeds in this project.

## When to Use

- Fetching data from ESI (characters, systems, ships, etc.)
- Processing killmail data from zkillboard
- Implementing ESI authentication (SSO)
- Caching EVE universe data
- Working with EVE-specific IDs and data structures

---

## Key URLs and Endpoints

| Service | Base URL | Purpose |
|---------|----------|---------|
| ESI | `https://esi.evetech.net/latest/` | Official EVE API |
| zkillboard RedisQ | `https://zkillredisq.stream/listen.php` | Real-time killmail feed |
| zkillboard | `https://zkillboard.com/` | Killmail browser |
| Fuzzwork | `https://www.fuzzwork.co.uk/api/` | Third-party celestial data |
| EVE SSO | `https://login.eveonline.com/` | OAuth authentication |
| EVE Images | `https://images.evetech.net/` | Character/ship/alliance icons |

---

## ESI Client Pattern

### Basic Structure

```rust
pub struct EsiClient {
    client: Client,  // reqwest::Client
}

impl EsiClient {
    pub fn new() -> Self {
        EsiClient {
            client: Client::new(),
        }
    }

    async fn fetch<T: for<'de> Deserialize<'de>>(
        &self,
        path: &str,
    ) -> Result<T, Box<dyn Error + Send + Sync>> {
        let url = format!("{}{}", ESI_URL, path);
        let response = self.client.get(&url).send().await?;
        if !response.status().is_success() {
            return Err(format!("ESI API returned status: {}", response.status()).into());
        }
        let data: T = response.json().await?;
        Ok(data)
    }
}
```

### Common ESI Endpoints

```rust
// Get system info
pub async fn get_system(&self, system_id: u32) -> Result<System, Error> {
    self.fetch(&format!("universe/systems/{}/", system_id)).await
}

// Get ship/item group
pub async fn get_ship_group_id(&self, type_id: u32) -> Result<u32, Error> {
    #[derive(Deserialize)]
    struct EsiType { group_id: u32 }
    let type_info: EsiType = self.fetch(&format!("universe/types/{}/", type_id)).await?;
    Ok(type_info.group_id)
}

// Get names (POST endpoint)
pub async fn get_name(&self, id: u64) -> Result<String, Error> {
    let names: Vec<EsiName> = self.client
        .post(format!("{}universe/names/", ESI_URL))
        .json(&[id])  // Array of IDs
        .send()
        .await?
        .json()
        .await?;
    Ok(names.into_iter().next()?.name)
}

// Get character affiliation (POST endpoint)
pub async fn get_character_affiliation(&self, character_id: u64)
    -> Result<(u64, Option<u64>), Error>  // (corp_id, alliance_id)
{
    let affiliations: Vec<Affiliation> = self.client
        .post(format!("{}characters/affiliation/", ESI_URL))
        .json(&[character_id])
        .send()
        .await?
        .json()
        .await?;
    let a = affiliations.into_iter().next()?;
    Ok((a.corporation_id, a.alliance_id))
}
```

---

## zkillboard RedisQ

### Listener Pattern

```rust
const REDISQ_URL: &str = "https://zkillredisq.stream/listen.php";

pub struct RedisQListener {
    client: Client,
    url: String,
}

impl RedisQListener {
    pub fn new(queue_id: &str) -> Self {
        // Each listener needs a unique queue ID
        let url = format!("{}?queueID={}", REDISQ_URL, queue_id);
        RedisQListener {
            client: Client::new(),
            url,
        }
    }

    pub async fn listen(&self) -> Result<Option<ZkData>, Error> {
        let response = self.client.get(&self.url)
            .timeout(Duration::from_secs(60))  // Long-polling
            .send()
            .await?;

        let wrapper: RedisQResponse = response.json().await?;
        Ok(wrapper.package)  // None if no new killmails
    }
}
```

### Main Loop Pattern

```rust
loop {
    match listener.listen().await {
        Ok(Some(zk_data)) => {
            info!("[Kill: {}] Received", zk_data.kill_id);
            process_killmail(&zk_data).await;
            sleep(Duration::from_secs(1)).await;
        }
        Ok(None) => {
            // No new data, RedisQ timed out
            sleep(Duration::from_secs(1)).await;
        }
        Err(e) => {
            error!("Error: {}", e);
            sleep(Duration::from_secs(5)).await;  // Backoff on error
        }
    }
}
```

---

## Data Models

### Killmail Structure

```rust
#[derive(Debug, Deserialize)]
pub struct ZkData {
    pub kill_id: u64,
    pub killmail: KillmailData,
    pub zkb: ZkbMeta,
}

#[derive(Debug, Deserialize)]
pub struct KillmailData {
    pub killmail_id: u64,
    pub killmail_time: String,  // RFC3339 format
    pub solar_system_id: u32,
    pub victim: Victim,
    pub attackers: Vec<Attacker>,
}

#[derive(Debug, Deserialize)]
pub struct Victim {
    pub ship_type_id: u32,
    pub character_id: Option<u64>,
    pub corporation_id: Option<u64>,
    pub alliance_id: Option<u64>,
    pub position: Option<Position>,
}

#[derive(Debug, Deserialize)]
pub struct Attacker {
    pub ship_type_id: Option<u32>,
    pub weapon_type_id: Option<u32>,
    pub character_id: Option<u64>,
    pub corporation_id: Option<u64>,
    pub alliance_id: Option<u64>,
    pub final_blow: bool,
}

#[derive(Debug, Deserialize)]
pub struct ZkbMeta {
    pub total_value: f64,
    pub location_id: Option<u64>,
    pub esi: String,  // URL to full ESI killmail
}
```

### System Data

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct System {
    pub id: u32,
    pub name: String,
    pub security_status: f64,
    pub region_id: u32,
    pub region: String,
    pub x: f64,
    pub y: f64,
    pub z: f64,
}
```

---

## Caching Strategy

### Cache ESI Data Locally

```rust
// Check cache first
{
    let systems = app_state.systems.read().unwrap();
    if let Some(system) = systems.get(&system_id) {
        return Some(system.clone());
    }
}

// Fetch and cache
match esi_client.get_system(system_id).await {
    Ok(system) => {
        let mut systems = app_state.systems.write().unwrap();
        systems.insert(system_id, system.clone());
        save_systems(&systems);  // Persist to disk
        Some(system)
    }
    Err(e) => {
        warn!("Failed to fetch system {}: {}", system_id, e);
        None
    }
}
```

### Using Moka for In-Memory Cache

```rust
use moka::future::Cache;

pub struct AppState {
    // Time-based expiry cache
    pub celestial_cache: Cache<u32, Arc<Celestial>>,
}

// Check cache
if let Some(celestial) = app_state.celestial_cache.get(&system_id) {
    return Some(celestial);
}

// Fetch and cache
let celestial = Arc::new(fetch_celestial().await?);
app_state.celestial_cache.insert(system_id, celestial.clone()).await;
```

---

## EVE-Specific Knowledge

### Important IDs

| Type | Example IDs | Notes |
|------|-------------|-------|
| Ship Groups | 485 (Dread), 659 (Super), 30 (Titan) | Used for filtering |
| Regions | 10000030 (Devoid), 10000012 (Curse) | Universe IDs |
| Systems | 30000142 (Jita), 30002086 (Turnur) | Solar system IDs |

### Ship Group Priorities

```rust
const SHIP_GROUP_PRIORITY: &[u32] = &[
    30,   // Titan
    659,  // Supercarrier
    4594, // Lancer
    485,  // Dreadnought
    1538, // FAX
    547,  // Carrier
    883,  // Capital Industrial Ship
    902,  // Jump Freighter
    513,  // Freighter
];
```

### Image URLs

```rust
// Alliance logo
fn alliance_icon(id: u64) -> String {
    format!("https://images.evetech.net/alliances/{}/logo?size=64", id)
}

// Corporation logo
fn corp_icon(id: u64) -> String {
    format!("https://images.evetech.net/corporations/{}/logo?size=64", id)
}

// Ship/item icon
fn ship_icon(id: u32) -> String {
    format!("https://images.evetech.net/types/{}/icon?size=64", id)
}

// Character portrait
fn character_portrait(id: u64) -> String {
    format!("https://images.evetech.net/characters/{}/portrait?size=64", id)
}
```

### External Links

```rust
// zkillboard
fn zkb_kill(id: u64) -> String {
    format!("https://zkillboard.com/kill/{}/", id)
}
fn zkb_character(id: u64) -> String {
    format!("https://zkillboard.com/character/{}/", id)
}
fn zkb_corp(id: u64) -> String {
    format!("https://zkillboard.com/corporation/{}/", id)
}

// Dotlan
fn dotlan_system(id: u32) -> String {
    format!("http://evemaps.dotlan.net/system/{}", id)
}
fn dotlan_region(id: u32) -> String {
    format!("http://evemaps.dotlan.net/region/{}", id)
}

// EVE Tools battle report
fn br_link(system_id: u32, timestamp: &str) -> String {
    format!("https://br.evetools.org/related/{}/{}", system_id, timestamp)
}
```

---

## SSO Authentication

### OAuth2 Flow

```rust
const ESI_AUTH_URL: &str = "https://login.eveonline.com/v2/oauth/token";
const ESI_VERIFY_URL: &str = "https://login.eveonline.com/oauth/verify";

pub async fn exchange_code_for_token(
    &self,
    code: &str,
    client_id: &str,
    client_secret: &str,
) -> Result<EveAuthToken, Error> {
    // 1. Exchange authorization code for tokens
    let params = [("grant_type", "authorization_code"), ("code", code)];
    let auth_response: Value = self.client
        .post(ESI_AUTH_URL)
        .basic_auth(client_id, Some(client_secret))
        .form(&params)
        .send()
        .await?
        .json()
        .await?;

    let access_token = auth_response["access_token"].as_str()?.to_string();
    let refresh_token = auth_response["refresh_token"].as_str()?.to_string();

    // 2. Verify token and get character info
    let verify_response: Value = self.client
        .get(ESI_VERIFY_URL)
        .bearer_auth(&access_token)
        .send()
        .await?
        .json()
        .await?;

    let character_id = verify_response["CharacterID"].as_u64()?;
    let character_name = verify_response["CharacterName"].as_str()?.to_string();

    Ok(EveAuthToken { character_id, character_name, access_token, refresh_token, ... })
}
```

### Authenticated Requests

```rust
pub async fn get_contacts(
    &self,
    entity_id: u64,
    token: &str,
    endpoint: &str,  // "characters", "corporations", or "alliances"
) -> Result<Vec<StandingContact>, Error> {
    let url = format!("{}{}/{}/contacts/", ESI_URL, endpoint, entity_id);
    let contacts: Vec<StandingContact> = self.client
        .get(&url)
        .bearer_auth(token)  // Include access token
        .send()
        .await?
        .json()
        .await?;
    Ok(contacts)
}
```

---

## Reference Files

- [resources/endpoints.md](resources/endpoints.md) - Complete ESI endpoint reference
- [resources/ids.md](resources/ids.md) - Common EVE IDs lookup table
