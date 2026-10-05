---
name: vikingo-stilus
description: Vikingo house style for all Hungarian user-facing text. MUST be applied whenever writing ANY Hungarian text a user will see in a Vikingo product — WordPress plugin admin screens, buttons, error/success messages, emails, frontend copy, form labels, documentation. Covers tone (informal "tegező" voice), Hungarian typography and orthography rules (quotes, dashes, dates, numbers, currency), a terminology glossary for consistent wording, message patterns (success, error, confirmation, empty state), and the i18n code technique (Hungarian source strings wrapped in translation functions). Companion of vikingo-szabvany (structure); this skill governs language and tone. Triggers on Vikingo, vikingokft, vk- plugins, Fegyvertár, Hungarian UI copy, hibaüzenet, admin szöveg, e-mail szöveg.
---

# Vikingo stílus – magyar szöveg és hangnem

Ez a Vikingo Studio házi stílusa minden felhasználónak látszó magyar szöveghez: plugin admin felületek, gombok, üzenetek, e-mailek, űrlapok, frontend szövegek, dokumentáció. A párja a `vikingo-szabvany` skill: az a szerkezetről szól (mappák, nevek, fejléc), ez a nyelvről és a hangnemről.

## 0. Alapelv

A szöveg is termék. Ugyanolyan következetesnek kell lennie, mint a kódnak: ugyanazt a fogalmat mindig ugyanaz a szó jelöli, ugyanaz a helyzet mindig ugyanolyan szerkezetű üzenetet kap. Tömören, magyarul, helyesen.

Elsőbbség: ha egy általános skill angol forrás-szövegeket vagy más hangnemet feltételez, Vikingo projektben ez a skill nyer. A forrás-szöveg magyar, a hangnem tegező.

## 1. Hangnem

- **Tegező, közvetlen, tömör.** Úgy beszélünk a felhasználóval, mint egy hozzáértő kollégával: "Elmentettük a beállításaidat." Nem bratyizós és nem hivataloskodó.
- **Gombokon és menüpontokon tömör főnévi forma:** "Mentés", "Beállítások mentése", "Új kupon". Nem "Mentsd el!" és nem "Save".
- **Üzenetekben tegező mondatok:** "Nem sikerült csatlakozni a Stripe-hoz. Ellenőrizd az API kulcsot a Beállítások fülön."
- **Nincs bocsánatkérés, nincs köntörfalazás, nincs felkiáltójel-halmozás.** "Sajnáljuk, valami hiba történt! :(" helyett: "A mentés nem sikerült, mert a szerver nem válaszolt. Próbáld újra egy perc múlva."
- **Kerüljük a gépies formulákat:** "Kérjük, adja meg..." tiltva (magázó és hivataloskodó). Helyette: "Add meg az e-mail címed."

## 2. Helyesírás és tipográfia

| Mi | Szabály | Példa |
|---|---|---|
| Idézőjel | magyar „lenti-fenti" pár | „Fegyvertár" csomag |
| Gondolatjel | nagykötőjel (–) szóközökkel; em-dash (—) TILOS | A mentés kész – folytathatod. |
| Tartomány | nagykötőjel szóköz nélkül | 8–10 munkanap |
| Dátum | év. hónapnév nap. | 2026. július 10. |
| Idő | kettősponttal | 14:30 |
| Szám | ezresek nem törő szóközzel | 10 000 |
| Pénz | összeg + szóköz + Ft | 12 500 Ft |
| Százalék | szóköz nélkül | 25% |
| Ellipszis | egyetlen … karakter | Betöltés… |
| E-mail szó | kötőjellel | e-mail cím |
| Weboldal szó | egybe | weboldal |
| Címek, címkék | mondatkezdő nagybetű, nem Title Case | "Fizetési beállítások", nem "Fizetési Beállítások" |

## 3. Terminológia-szótár

Ugyanarra a fogalomra mindig ugyanazt a szót használjuk. A felhasználónak látszó szövegben a bal oszlop érvényes; a belső dokumentációban és kódban az angol szakszó (plugin, hook) rendben van.

| Ezt használd | Ezt ne | Mikor |
|---|---|---|
| bővítmény | plugin | felhasználói szöveg |
| beállítások | opciók, konfiguráció | menü, oldal címe |
| mentés | elmentés, tárolás | gomb |
| mégse | mégsem, visszavonás | elvetés gomb |
| törlés | eltávolítás | végleges törlés gomb |
| bejelentkezés / kijelentkezés | belépés / kilépés | auth |
| fiók | profil, account | felhasználói fiók |
| e-mail cím | email, e-mail-cím | űrlapmező |
| hozzáférés | jogosultság, access | Fegyvertár kontextusban |
| előfizetés | tagság, subscription | fizetős csomag |
| rendelés | megrendelés | WooCommerce |
| pénztár | fizetés oldal, checkout | WooCommerce |
| kosár | bevásárlókosár | WooCommerce |
| frissítés | update, aktualizálás | szoftver és adat |
| feltöltés / letöltés | upload / download | fájlok |
| keresés | search | mező, gomb |

Ha új, gyakran visszatérő fogalom kerül elő, vedd fel ebbe a táblázatba, ne dönts ad hoc.

## 4. Üzenet-minták

- **Siker:** rövid, múlt idejű, tegező többes. "Elmentettük." / "A kupon létrejött." Nem kell megismételni, mit csinált a felhasználó.
- **Hiba:** két rész, mindig ebben a sorrendben: mi történt + mit tegyen. "Nem sikerült elmenteni, mert a Stripe kulcs érvénytelen. Másold be újra a kulcsot a Stripe fiókodból." Soha nem csak "Hiba történt".
- **Megerősítés (visszafordíthatatlan műveletnél):** nevezd meg, mi vész el. "Biztosan törlöd a(z) „Nyári kampány" kupont? Ez nem vonható vissza." Gombok: "Törlés" és "Mégse".
- **Üres állapot:** mondd meg, mit lát majd itt, és hogyan hozhatja létre az elsőt. "Még nincs egy kuponod sem. Az „Új kupon" gombbal hozhatod létre az elsőt."
- **Betöltés:** "Betöltés…" vagy konkrétabb: "Rendelések lekérése…"

## 5. Kód-technika (i18n)

A forrás-szövegeket **magyarul írjuk, de mindig fordítható függvényben**, így a plugin bármikor fordíthatóvá válik anélkül, hogy a kódhoz nyúlni kellene.

- Minden felhasználónak látszó string `__()`, `esc_html__()`, `esc_attr__()` hívásban, a plugin text domainjével: `esc_html__( 'Elmentettük.', 'vk-fegyvertar-access' )`.
- Behelyettesítésnél `sprintf` + fordítói komment, a mondatot SOHA nem daraboljuk össze konkatenációval:

```php
/* translators: %s: a kupon neve */
sprintf( esc_html__( 'A(z) „%s" kupon létrejött.', 'vk-fegyvertar-access' ), $coupon_name );
```

- Többes szám `_n()`-nel, mert a magyar egyes/többes alak eltér: `_n( '%s rendelés', '%s rendelés', $count, ... )` helyett valódi eltérő alakok, pl. "1 új rendelés" / "%s új rendelés".
- Dátum kiírása `wp_date()`-tel a WordPress beállított formátumában, szám kiírása `number_format_i18n()`-nel. Kézzel formázott dátum és szám tilos.
- A helyesírási szabályok (2. pont) a kódban lévő magyar stringekre is érvényesek: magyar idézőjel, nagykötőjel, nem törő szóköz (`&nbsp;` vagy `\u{00A0}`) az ezresek és a Ft előtt.

## 6. E-mailek

- Tárgy: tömör, konkrét, nagybetű-halmozás nélkül. "A rendelésed úton van", nem "FONTOS: Rendelési Értesítés!!!".
- Törzs: tegező, rövid bekezdések, egy e-mail egy célra. A lényeg (link, kód, összeg) vizuálisan kiemelve.
- Aláírás egységesen: "Üdv, a Vikingo csapata".

## 7. Ne csináld

- Ne keverj angol szót magyar mondatba, ha van bevett magyar szó ("checkout oldal" helyett "pénztár oldal").
- Ne írj Title Case Címeket Magyar Szövegben.
- Ne használj em-dash-t (—) sehol.
- Ne szólítsd meg a felhasználót magázva, és ne váltogass tegezés-magázás között.
- Ne tegyél felkiáltójelet hibaüzenetbe.
- Ne fűzz össze mondatot változókból és fél mondatokból, mert fordíthatatlan és magyartalan lesz.
- Ne írd ki nyers gépi értékeket (true, null, error code) felhasználói üzenetben; fordítsd le emberi nyelvre, a technikai részlet mehet a naplóba.
