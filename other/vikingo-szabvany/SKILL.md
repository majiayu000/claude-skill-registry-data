---
name: vikingo-szabvany
description: Vikingo Studio plugin and repo standard. MUST be applied whenever creating, naming, reviewing, or releasing anything for Vikingo Studio / vikingokft — WordPress plugins, themes, GitHub repos, apps, or tools. Covers repo naming taxonomy (wp-plugin-, app-, tool-, site- prefixes), plugin naming conventions (vk- prefixes for slugs, hooks, options, meta, CPTs, REST routes), the mandatory plugin header, folder structure, versioning and release flow, the private plugin update channel via the vikingoauth.hu proxy (Update URI header, no per-site token, server-side PLUGINS whitelist and GitHub PAT setup), admin UI rules (native-first, no brand webfonts in wp-admin), security baseline, and the pre-release checklist. Triggers on Vikingo, vikingokft, vk- prefix, Fegyvertár, plugin update or auto-update, vikingoauth.hu, vikingo.hu / vikingo.studio / vikingoapp.hu / vikingodev.hu, or any new plugin/repo scaffolding for this organization.
---

# Vikingo Studio – Plugin és repo szabvány

Ez a dokumentum minden Vikingo Studio által fejlesztett WordPress bővítmény és GitHub repo közös alapja. Kliens oldalakra, a Fegyvertárra, a nyilvános appokra és a belső eszközökre egyaránt érvényes. A cél, hogy minden projekt belül ugyanúgy nézzen ki, előre kiszámítható legyen, ne ütközzön más pluginekkel, és a lehető legkisebb erőforrásköltséggel fusson.

## 0. Alapelvek

- A márkanév **Vikingo**, az ügynökség a **Vikingo Studio**.
- Minden általunk fejlesztett plugin szerzője **Vikingo Studio**, függetlenül attól, hogy melyik kliensnek készül.
- Kevesebb kód, kevesebb asset, kevesebb hibalehetőség. A natív WordPress megoldás mindig előrébb való a sajátnál, ha a natív elég jó.

## 0.1. Elsőbbség: ütközésnél ez a szabvány nyer

Az általános WordPress skillek (plugin-scaffold, wordpress, woocommerce készletek) technikai tudását HASZNÁLD (hookok, cron, életciklus, biztonság, teljesítmény), de ahol a példáik vagy konvencióik ellentmondanak ennek a szabványnak, ott MINDIG ez a szabvány érvényes. Az általános skill csak ott ad döntést, ahol ez a dokumentum hallgat.

A tipikus ütközések és a Vikingo döntés:

| Általános skill mondja | Vikingo szabvány szerint |
|---|---|
| `includes/` mappa a PHP osztályoknak | `src/` mappa, PSR-4 autoload, `Vikingo\{PluginNév}` namespace |
| generikus `yourprefix_`, `my_plugin_` prefixek | `vk_{plugin}_` a 3. pont táblázata szerint |
| angol forrás-stringek + fordítási fájl | magyar forrás-stringek fordítható függvényben (10. pont, vikingo-stilus skill) |
| tetszőleges plugin header | a 4. pont kötelező fejléce (Author: Vikingo Studio, GPL-2.0-or-later) |
| saját admin design | natív-first admin a 7. pont szerint |

Egy kivétel jogos az i18n-nél: a WP 6.7+ betöltés előtti (bootstrap-fázisú) hibaüzenetek nem mehetnek fordítási függvénybe; ezek nálunk nyers magyar stringek, nem angolok.

## 1. Domainek és szerepük

| Domain | Szerep |
|---|---|
| `vikingo.hu` | Oktatás, itt él a Fegyvertár |
| `vikingo.studio` | Ügynökség, a pluginek hivatalos szerzői és support háttere |
| `vikingoapp.hu` | Nyilvános, másoknak is elérhető appok és eszközök |
| `vikingodev.hu` | Kizárólag belső használatú eszközök |

A domain besorolási tengelyként is működik. Egy nyilvános app a `vikingoapp.hu` alá települ, egy belső eszköz a `vikingodev.hu` alá. Ez a döntés a repo típusát is meghatározza.

## 2. Repo elnevezési taxonómia

A repo neve mindig két dolgot mond meg: a prefix azt, hogy **mi az artefakt**, a slug pedig azt, hogy **konkrétan melyik**. A cél domain a típusból következik.

| Repo prefix | Mi az | Cél domain |
|---|---|---|
| `wp-plugin-{slug}` | WordPress bővítmény | kliens oldal vagy Fegyvertár |
| `wp-mu-{slug}` | must-use plugin, snippet-fix | eseti |
| `wp-theme-{slug}` | egyedi téma vagy child theme | kliens oldal |
| `tool-{slug}` | belső eszköz, automatizmus | `*.vikingodev.hu` |
| `site-{domain}` | élő weboldal vagy webapp, a slug maga a domain | a névben szereplő domain |
| `skill-{slug}` | Claude Code skill | repo, nem deploy |
| `chrome-ext-{slug}` | Chrome bővítmény | Chrome Web Store |
| `edu-{slug}` | oktatási segédanyag, kurzus tartalom, mintamegoldás | repo vagy GitHub Pages |
| `archive-{slug}` | lezárt, már nem használt repo | nincs, archiválva |

Slug szabály: kisbetű, kebab-case, ékezet nélkül, tömör és beszédes. Pont és egyéb írásjel nem szerepelhet a repo nevében. Példa: "Fegyvertár hozzáférés" lesz `fegyvertar-access`.

Archiválási szabály: ha egy repo lezárult és már nem használjuk, átnevezéskor `archive-` előtagot kap (`archive-{régi-név}`), majd a GitHubon archiválva lesz. Így a listában ránézésre elkülönül az élő állománytól.

Site szabály: minden élő weboldal és webapp repója `site-{domain}` nevű, ahol a domain kötőjelesen írva szerepel: `site-onlinesorsolas-hu` az onlinesorsolas.hu-hoz, `site-elcs-wpkurzus-hu` az elcs.wpkurzus.hu-hoz. Így a repo nevéből azonnal látszik, hol él az oldal. Külön `app-` kategória nincs.

Termék-névtér: ha egy repo egy konkrét termékhez tartozik (például a Fegyvertárhoz), a slug a termék nevével kezdődik a típus-előtag után: `tool-fegyvertar-{funkció}`, `skill-fegyvertar-{funkció}`. Így típuson belül a termék repói egymás mellé rendeződnek. Emellett a repo megkapja a termék GitHub topicját (`fegyvertar`), így az org repólistája egy kattintással szűrhető a teljes termék-családra, típustól függetlenül.

Láthatóság: `tool-` repo mindig privát. `edu-` és `skill-` lehet publikus, kliens- és termék-repo (`wp-plugin-`, `site-`) alapból privát.

Kód-könyvtárak (npm csomagok), sablonok és tudásbázis repók besorolása még nyitott döntés, addig a meglévő, beszédes nevük marad.

## 3. Plugin elnevezési konvenciók

Két szintet használunk. Rövid vizuális prefixet a frontend rétegen, és plugin-nevesített prefixet mindenhol, ahol az adat globális térbe kerül. Ez utóbbi azért kell, mert a csupasz `vk_` az adatbázisban vagy egy hookon ütközhetne két Vikingo plugin között. A plugin nevét ezért mindig bele kell tenni.

| Terület | Konvenció | Példa |
|---|---|---|
| CSS osztály és id | `vk-` | `.vk-panel`, `#vk-settings` |
| GitHub repo | `wp-plugin-{slug}` | `wp-plugin-fegyvertar-access` |
| Plugin slug, mappa, text domain | `vk-{funkció}` | `vk-fegyvertar-access` |
| PHP namespace (PSR-4) | `Vikingo\{PluginNév}` | `Vikingo\FegyvertarAccess` |
| Globális PHP függvény, ha muszáj | `vk_{plugin}_` | `vk_fegyvertar_render()` |
| Konstans | `VK_{PLUGINRÖVID}_` | `VK_FGV_VERSION` |
| Action és filter hook | `vk_{plugin}_` | `vk_fegyvertar_access_granted` |
| Option kulcs | `vk_{plugin}_` | `vk_fegyvertar_settings` |
| Post meta (privát) | `_vk_{plugin}_` | `_vk_fegyvertar_expiry` |
| Transient | `vk_{plugin}_` | `vk_fegyvertar_cache` |
| User meta (privát) | `_vk_{plugin}_` | `_vk_fegyvertar_level` |
| Custom post type | `vk_{rövid}`, max 20 karakter | `vk_lesson` |
| Taxonomy | `vk_{rövid}` | `vk_lesson_cat` |
| AJAX action | `vk_{plugin}_{művelet}` | `wp_ajax_vk_fegyvertar_sync` |
| Nonce action | `vk_{plugin}_{művelet}` | `vk_fegyvertar_save_settings` |
| Cron esemény | `vk_{plugin}_{művelet}` | `vk_fegyvertar_daily_sync` |
| Shortcode | `vk_{plugin}` vagy `vk_{plugin}_{funkció}` | `[vk_fegyvertar_panel]` |
| Adatbázis tábla | `{$wpdb->prefix}vk_{plugin}_{entitás}` | `wp_vk_fegyvertar_logs` |
| Capability, ha saját kell | `vk_{plugin}_{jog}` | `vk_fegyvertar_manage` |
| Cookie | `vk_{plugin}_` | `vk_fegyvertar_token` |
| REST namespace | `vikingo/v1`, a route a pluginnal kezdődik | `vikingo/v1/fegyvertar/access` |
| Gutenberg blokk | `vikingo/{blokk}` | `vikingo/lesson-list` |
| Enqueue handle | `vk-{plugin}-{context}` | `vk-fegyvertar-admin` |
| Localize JS objektum | `vk{Plugin}` camelCase | `vkFegyvertar` |
| Composer csomagnév | `vikingo/{plugin-slug}` | `vikingo/vk-fegyvertar-access` |

- A custom post type kulcs maximum 20 karakter lehet, ezt a WordPress core kényszeríti, ezért ott rövid nevet használunk plugin-nevesítés nélkül. A rövid CPT és taxonomy neveket érdemes egy közös listában nyilvántartani, hogy két plugin ne foglalja le ugyanazt.
- A REST namespace közös `vikingo/v1`, de a route első szegmense mindig a plugin neve, így két plugin sosem ütközik ugyanazon az útvonalon.

## 4. Plugin header

Minden plugin fő fájlának ez a fejléce, kitöltve. Em-dash sehol, a leírásban sem.

```php
<?php
/**
 * Plugin Name:       Vikingo Fegyvertár Access
 * Plugin URI:        https://vikingo.studio
 * Description:       Fegyvertár hozzáférés-kezelés Circle és Stripe alapon.
 * Version:           1.0.0
 * Requires at least: 6.4
 * Requires PHP:      8.0
 * Author:            Vikingo Studio
 * Author URI:        https://vikingo.studio
 * License:           GPL-2.0-or-later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       vk-fegyvertar-access
 * Domain Path:       /languages
 * Update URI:        https://vikingoauth.hu/plugin/vk-fegyvertar-access
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
```

- Az **Author** mindig `Vikingo Studio`, az **Author URI** és a **Plugin URI** mindig `https://vikingo.studio`, aloldal nélkül.
- A **License** GPL-2.0-or-later, ez nem opció, privát pluginnél is így csináljuk.
- A **Text Domain** kötelezően azonos a plugin sluggal és a mappanévvel.
- Az **Update URI** a frissítési proxyra mutat: `https://vikingoauth.hu/plugin/{plugin-slug}`. Ez egyszerre két dolgot ad: a wp.org frissítő sosem tol rá azonos slugú publikus plugint, és a WP a `update_plugins_vikingoauth.hu` filteren keresztül tőlünk kéri a frissítést (lásd 6. pont).
- A **Requires PHP** minimum 8.0, a támogatott WP verzió az aktuális és az azt megelőző fő verzió.

## 5. Mappa- és fájlstruktúra

Egységes váz, csak azzal, amire tényleg szükség van.

```
wp-plugin-fegyvertar-access/
├── vk-fegyvertar-access.php      # fő fájl, csak bootstrap
├── uninstall.php                 # takarítás eltávolításkor
├── composer.json                 # PSR-4 autoload, dev függőségek
├── readme.md
├── CHANGELOG.md
├── .editorconfig
├── .gitignore
├── languages/
│   └── vk-fegyvertar-access.pot
├── src/                          # PHP osztályok, Vikingo\FegyvertarAccess namespace
│   ├── Plugin.php
│   ├── Admin/
│   ├── Frontend/
│   └── Rest/
└── assets/
    ├── css/                      # csak ha muszáj, minimalizálva
    ├── js/
    └── img/
```

A fő fájl csak betölt és indít. A logika a `src/` alatt van PSR-4 autoloaddal. A `node_modules` és a build köztes fájljai soha nem kerülnek a repóba, csak a release zipbe.

## 6. Tárolás, verziózás, megosztás, frissítés

- Minden plugin külön privát GitHub repo a Vikingo org alatt, `wp-plugin-{slug}` néven.
- A `main` mindig telepíthető állapotban van, a fejlesztés feature branchen.
- Szemantikus verziózás, `MAJOR.MINOR.PATCH`. Minden kiadás egy git tag `v1.0.0` formában. A header `Version` és a tag mindig egyezik.
- A `CHANGELOG.md` a Keep a Changelog formátumot követi, magyarul.
- Release-enként tiszta, build utáni zipet töltünk fel release asset-ként, dev függőség és `node_modules` nélkül. A build GitHub Actionben fut, kézzel nem rakunk össze zipet.
- Ha egy plugin később a Fegyvertár tagoknak megy ki, opcionálisan bekerülhet egy egyszerű licenc- vagy token-ellenőrzés. Ezt csak tényleges fizetős terjesztésnél építjük be.

## 6.1. Frissítési csatorna: a vikingoauth.hu proxy

A privát pluginek frissítése **egységesen a vikingoauth.hu proxyn** keresztül megy, nem közvetlenül a GitHubról. Ez a kötelező minta minden Vikingo pluginnál.

**Miért így:** privát repóból a GitHub API csak tokennel ad vissza release-t. Ha ezt a tokent kliensenként kellene beírni (pl. `wp-config.php` konstansként), az sok tucat oldalon nem skálázódik, és a token szétszóródik. A proxynál a GitHub token **egyetlen központi helyen** (Cloudflare secret) él, a kliens oldalakra **semmilyen titkot nem kell beállítani**. Ez egyben megszünteti a korábbi plugin-update-checker (YahnisElsts) könyvtár igényét is: nincs vendorolt függőség, kevesebb kód, kisebb zip.

**Kliens oldal (a pluginban).** Natív WP frissítés, nincs külső könyvtár:

1. A plugin header `Update URI: https://vikingoauth.hu/plugin/{slug}` (4. pont). Ebből a WP a `update_plugins_vikingoauth.hu` filtert származtatja.
2. Egy kis `src/Update/UpdateChecker.php` osztály (kb. 200 sor, könyvtár nélkül) rákötődik erre a filterre és a `plugins_api` filterre, lekéri a proxy `/plugin/update` endpointjának metadatáját (`version`, `package`, `changelog`, …), és 6 órás transientben cache-eli (hibánál 1 órás negatív cache).
3. A közös bearer kulcs a pluginba van égetve az osztály konstansaként. **Nem per-oldal titok:** csak azt védi ki, hogy kívülálló letölthesse a zipet, azt a zipet, amit a telepített oldal amúgy is birtokol. Ugyanaz a kulcs minden Vikingo pluginban.
4. A zipet a WP core tölti a `/plugin/download` endpointról; a bearer fejlécet a `http_request_args` filter injektálja (csak a `vikingoauth.hu` `/plugin/` útra), így a kulcs URL-be és logba sem kerül.

Referencia-implementáció, amiből másolni kell: `vikingo-backup` és `wp-plugin-vikingo-woocommerce` `src/Update/UpdateChecker.php`. Új pluginnál ezt az osztályt kell átemelni, a `SLUG`, `HOST`, `ENDPOINT` és a szöveges nevek átírásával; a bearer kulcs változatlan.

**„Frissítés keresése" gomb (ajánlott).** A plugin saját beállítási oldalán (pl. Eszközök fül) legyen egy gomb, ami azonnal lekérdezi a csatornát, hogy friss kiadás után ne kelljen a WP frissítési cron/cache lejártát (6–12 óra) kivárni. A minta: az `UpdateChecker` egy `force_check()` metódusa üríti a saját metaadat-transientet, meghívja a `wp_update_plugins()`-t (hogy a Bővítmények oldal is frissüljön), és visszaadja az aktuális + legfrissebb verziót; a beállítási oldal egy nonce-olt `admin-post` művelettel hívja, majd értesítésben jelzi az eredményt (új verzió elérhető / naprakész / a csatorna nem válaszolt). A gomb az `UpdateChecker`-t használja, nem duplikálja a proxy-hívást; a tényleges telepítés marad a Bővítmények oldalon. Referencia: `wp-plugin-vikingo-woocommerce` (`UpdateChecker::force_check()` + a beállítási oldal Eszközök füle).

**Szerver oldal (vikingo-auth-server, Cloudflare Worker a `vikingoauth.hu`-n).** A `/plugin/update` és `/plugin/download` endpoint a `src/routes/plugin.ts` `PLUGINS` whitelistjéből dolgozik. Új plugin bekötése két lépés:

1. Egy bejegyzés a `PLUGINS` konstansba: `'{slug}': { repo: 'vikingokft/wp-plugin-{slug}', requires, requiresPhp, tested }`.
2. `npx wrangler deploy`.

A GitHub tokennel (`GITHUB_TOKEN` Cloudflare secret, a `vikingoauth-plugin-updates` fine-grained PAT) **nem kell külön semmit csinálni**: a token **Repository access = All repositories**, Contents: Read-only hatókörű, így az org minden mostani és jövőbeli repóját automatikusan látja. Új plugin repónál tehát nincs GitHub-oldali teendő.

**Hibakeresés (ha a `/plugin/update` mégis 502 `release_unavailable`-t ad):** az auditban `github_http_404` a GitHub token gondja — mert privát repónál jogosultsághiányra is 404-et küld, nem 403-at. Okok: a token elveszett/lejárt, vagy valaki visszaszűkítette „Only select repositories"-ra és kimaradt a repo, vagy rossz a resource owner (nem `vikingokft`). A tünet független a release helyességétől. Új token feltöltése: `npx wrangler secret put GITHUB_TOKEN`.

Teszt kiadás után (cache-buster kell, mert a Cloudflare edge cache-elheti a korábbi választ):

```bash
KEY=<a pluginba égetett bearer kulcs>
curl -s -H "Authorization: Bearer $KEY" \
  "https://vikingoauth.hu/plugin/update?slug={slug}&cb=$RANDOM"
# Vár: HTTP 200 + JSON a legfrissebb verzióval. 502 = PAT-scope hiányzik.
```

**Migrációs következmény:** a proxy-csatorna egy oldalon csak azután él, hogy az azt tartalmazó verzió **egyszer felkerült** rá (új telepítés vagy egyszeri kézi frissítés). A régebbi verziót futtató oldalak a korábbi csatornájukon maradnak, amíg egyszer kézzel frissülnek. Onnantól minden további frissítés automatikus, token nélkül.

## 7. Arculat és admin felület

Az arculat itt szándékosan minimális. Egy erősen brandelt admin oldal jól mutat, de minden extra CSS és font fájl letöltési költség plusz hibafelület. A szabály natív-first.

Amit használunk:

- WordPress natív admin komponensek: `.button`, `.button-primary`, `.notice`, `postbox`, Settings API mezők.
- A saját arculat maximum néhány CSS custom property a saját admin oldal gyökerén, semmi globális felülírás.
- A logó inline SVG, nem külön képfájl, nem külön kérés.

Amit nem csinálunk:

- A Clash Display vagy bármilyen brand webfont soha nem töltődik be a wp-adminba. Az adminban a WP alapértelmezett rendszer-fontstackje megy. A brand fontok a frontendre valók, ott is csak indokolt esetben.
- Nincs globális admin CSS. A plugin admin stílusa csak a saját képernyőin töltődik, feltételesen:

```php
add_action( 'admin_enqueue_scripts', function ( $hook ) {
	// Miért: csak a saját beállítási oldalon töltjük be, hogy ne lassítsuk a teljes admint.
	if ( 'settings_page_vk-fegyvertar-access' !== $hook ) {
		return;
	}
	wp_enqueue_style(
		'vk-fegyvertar-admin',
		VK_FGV_URL . 'assets/css/admin.css',
		array(),
		VK_FGV_VERSION
	);
} );
```

Az arculat forrása a **Vikingo Design System** (Claude Designnal épített rendszer, `colors_and_type.css`), az az egyetlen igazság-forrás. A WordPress pluginekbe ebből CSAK az alábbi, származtatott token-részhalmaz kerül át, bemásolva a plugin admin CSS-ébe (nincs külső kérés, nincs npm függőség, kb. fél kilobájt). A React és web-component réteg, az illusztrációs színpaletta és a brand fontok (Clash Display, DM Mono) NEM jönnek át; a komponensek a natív WP admin elemek, csak a színüket és a rádiuszt kapják a tokenekből.

```css
/* Vikingo admin tokenek. Származtatva: Vikingo Design System,
   colors_and_type.css. Arculatváltásnál ott a teljes készlet,
   itt ez a részhalmaz frissül. */
:root .vk-admin {
	--vk-color-primary:       #FF544D; /* korall */
	--vk-color-primary-hover: #E83D36;
	--vk-color-accent:        #3E2E45; /* padlizsán (ink) */
	--vk-color-bg:            #F3EEEB; /* meleg krém (paper) */
	--vk-color-surface:       #FFFFFF;
	--vk-color-border:        #DCD0C3; /* sand */
	--vk-color-text-muted:    #7A687F; /* mauve */
	--vk-radius-sm:           8px;     /* mezők, kis elemek */
	--vk-radius:              12px;    /* gombok, panelek */
	--vk-radius-lg:           16px;    /* kártyák, nagy dobozok */
}
```

Ennél több token pluginbe nem kerül. Ha egy plugin frontend felülete (felhasználónak látszó widget) többet igényel, ott is a design system tokenjeit használjuk, de csak a ténylegesen használt sorokat másoljuk át, buildelt CSS-ként.

Az arculati elemek egységesek minden pluginben, ugyanaz a logó (a design system repo `vikingo-emblema-*.svg` fájljai inline SVG-ként), ugyanaz a színvilág, ugyanaz a szerzői link. A plugin listában a support és dokumentáció linket a `plugin_row_meta` szűrővel adjuk hozzá, mindig a `vikingo.studio` alá mutatva.

## 8. Biztonsági alapkövetelmények

- `ABSPATH` guard minden PHP fájl tetején.
- Jogosultság-ellenőrzés minden művelet előtt: `current_user_can()`.
- Nonce minden űrlapnál és AJAX hívásnál.
- Bemenet tisztítása, kimenet escapelése: `sanitize_*`, `esc_html`, `esc_attr`, `esc_url`, összetett HTML-nél `wp_kses`.
- Adatbázis lekérdezés mindig `$wpdb->prepare()`.
- Debug adat csak `WP_DEBUG` mögött.

## 9. Teljesítmény

- Nem futtatunk kódot minden kérésnél, amit nem kell. Adminban csak adminra, frontendben csak frontendre.
- Nagy option értékeknél az `autoload` legyen `no`.
- Asset verziózás a plugin verzió konstanssal a cache-buster miatt, fejlesztés alatt `filemtime`.
- Külső PHP könyvtárat composerrel prefixelve szállítunk (PHP-Scoper vagy Mozart), hogy két plugin ne ütközzön ugyanazon a verzión.

## 10. Fordíthatóság és szövegek

- A forrás-szövegeket magyarul írjuk, de minden felhasználónak látható szöveg fordítható függvényben áll: `__()`, `esc_html__()`. Így a plugin bármikor fordíthatóvá válik a kód átírása nélkül.
- A text domain mindig a plugin slug, a betöltés az `init` hookon.
- POT fájl a `languages/` mappában.
- A szövegek hangneme, helyesírása és terminológiája a **vikingo-stilus** skillben van szabályozva (tegező hangnem, magyar tipográfia, egységes szótár, üzenet-minták). Minden felületi szöveg aszerint készül.

## 11. Kód-konvenciók

- WordPress Coding Standards PHPCS-sel ellenőrizve, dev függőségként.
- `.editorconfig` minden repóban.
- Nincs em-dash sehol, se kódban, se leírásban.
- A kommentek magyarul, a miért és nem a mit elv szerint. A kód megmutatja mit csinál, a komment megmagyarázza miért van rá szükség.
- OOP alapú felépítés namespace-szel, globális függvény csak indokolt esetben.

## 12. Aktiválás, deaktiválás, eltávolítás

- `register_activation_hook`: kezdeti option-ök, adatbázis tábla, jogosultságok.
- `register_deactivation_hook`: ütemezett feladatok törlése, cache ürítés.
- `uninstall.php`: az adatok végleges takarítása. Alapból legyen egy beállítás, ami eldönti, hogy eltávolításkor törlődjenek-e az adatok.

## 13. Kiadás előtti ellenőrzőlista

- [ ] Header teljesen kitöltve, Author és Author URI a Vikingo Studio.
- [ ] Text domain azonos a sluggal és a mappanévvel.
- [ ] Verzió a headerben és a git tagen egyezik.
- [ ] Nincs csupasz `vk_` az adatbázisban, hookon, AJAX actionben, cron eseményen vagy cookie-ban, mindenhol plugin-nevesített.
- [ ] REST route a plugin nevével kezdődik a `vikingo/v1` namespace alatt.
- [ ] Admin CSS és JS csak a saját képernyőkön töltődik.
- [ ] Nincs brand webfont az adminban.
- [ ] Minden bemenet tisztítva, minden kimenet escapelve, nonce és capability minden műveletnél.
- [ ] Nincs em-dash sehol.
- [ ] Release zip tiszta, dev függőség és node_modules nélkül.
- [ ] `Update URI` a proxyra mutat (`https://vikingoauth.hu/plugin/{slug}`), a plugin `src/Update/UpdateChecker.php`-t tartalmazza (6.1 pont).
- [ ] A plugin fel van véve a vikingo-auth-server `PLUGINS` whitelistjébe és a worker deployolva. (A GitHub PAT „All repositories" hatókörű, így új repót nem kell külön felvenni.)
- [ ] Kiadás után a `/plugin/update?slug={slug}` HTTP 200-at ad (curl-teszt a 6.1 pont szerint).
