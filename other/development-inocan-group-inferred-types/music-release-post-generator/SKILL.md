---
name: music-release-post-generator
description: "Genera post Facebook per promuovere release musicali su YouTube. Usa quando pubblichi una nuova traccia e devi condividerla su gruppi Facebook con titolo, descrizione accattivante, CTA e hashtag."
---

# Music Release Post Generator

Genera post Facebook pronti per la condivisione di release musicali, ottimizzati per engagement nei gruppi musicali.

## Capabilities

- Creare post con struttura: emoji + titolo + descrizione + CTA + hashtag
- Riscrivere descrizioni YouTube in formato social-friendly
- Generare hashtag rilevanti per il genere musicale
- Adattare il tono al genere (techno, trance, house, ambient, etc.)
- Formattare per massimizzare visibilita nei gruppi Facebook

## Instructions

1. **Ricevi Input**: Titolo della traccia e descrizione YouTube
2. **Identifica Genere**: Estrai BPM, mood e genere dalla descrizione
3. **Crea Opening**: Emoji tematiche + "New release:" + titolo tra virgolette
4. **Riscrivi Descrizione**: Condensa in 2-3 frasi evocative
5. **Aggiungi CTA**: "Listen now" o equivalente con emoji freccia
6. **Lascia Spazio Link**: Riga vuota per incollare il link YouTube
7. **Genera Hashtag**: 5-8 hashtag rilevanti in CamelCase

## Input Format

Fornisci:
- **Titolo**: Nome completo della traccia
- **Descrizione YouTube**: Testo descrittivo della traccia (anche lungo)
- **Link** (opzionale): URL YouTube da includere nel post

## Output Format

```
[Emoji tematiche] New release: "[Titolo Traccia]" [Emoji tematiche]

[Descrizione condensata in 2-3 frasi evocative, focus su mood/vibe/esperienza]

Listen now [emoji freccia]
[link o spazio per link]

#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5
```

## Example

**Input**:
```
Titolo: Techno AI 2025: Cosmic Gateway
Descrizione: A consciousness-expanding trance journey at 138 BPM. This track opens dimensional portals as frequencies align, creating a transcendent experience through cosmic awareness. Deep basslines meet ethereal pads in a hypnotic progression.
```

**Output**:
```
🔊🌌 New release: "Techno AI 2025: Cosmic Gateway" 🌌🔊

Consciousness-expanding trance at 138 BPM. Dimensional portals open as frequencies align. A transcendent journey through cosmic awareness.

Listen now 👇
[incolla qui il link]

#CosmicGateway #HypnoticTrance #TechnoAI2025 #ConsciousnessExpanding #Trance138BPM #ElectronicMusic
```

## Emoji per Genere

| Genere | Emoji Suggerite |
|--------|-----------------|
| Techno | 🔊 ⚡ 🖤 🔥 |
| Trance | 🌌 ✨ 🌀 💫 |
| House | 🏠 🎵 💃 🪩 |
| Ambient | 🌊 🌙 🍃 ☁️ |
| Drum & Bass | 🥁 ⚡ 🔈 💥 |
| Psytrance | 👁️ 🌀 🔮 🌌 |

## Best Practices

1. **Titolo tra virgolette**: Sempre racchiudere il titolo in ""
2. **Descrizione breve**: Max 3 frasi, no muri di testo
3. **BPM se rilevante**: Includere solo per generi dove conta (trance, techno)
4. **Hashtag CamelCase**: #CosmicGateway non #cosmicgateway
5. **Emoji bilanciate**: Apertura e chiusura simmetriche
6. **CTA chiaro**: Sempre con emoji freccia verso il basso
7. **Spazio per link**: Lasciare sempre una riga dedicata

## Hashtag Strategy

Genera hashtag che includano:
- Nome/parole chiave della traccia
- Genere musicale principale
- Sottogenere se applicabile
- Mood/vibe (hypnotic, dark, uplifting)
- BPM range se caratteristico
- Tag generici musica elettronica

## Limitations

- Non puo verificare se gli hashtag sono trending
- Non accede al link YouTube per estrarre info automaticamente
- Richiede che l'utente fornisca titolo e descrizione manualmente
- Non genera varianti multiple (un post per richiesta)
- Non ottimizza per algoritmo Facebook (cambia frequentemente)
