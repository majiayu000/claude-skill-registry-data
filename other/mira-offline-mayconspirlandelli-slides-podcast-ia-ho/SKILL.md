---
name: mira-offline
description: >-
  Converte um deck do Mira já criado para modo OFFLINE (self-contained, sem CDN
  em runtime), para abrir por file:// mesmo atrás do firewall corporativo que
  bloqueia as CDNs (Tailwind, AOS, Lucide, D3, fonte Inter e Three.js dos slides
  3D). Use SEMPRE que o usuário disser /mira-offline, deixa o deck offline, deixa
  o slide self-contained, o firewall da empresa está bloqueando o slide, funciona
  sem internet, tira as CDN, baixa as bibliotecas pro deck, ou o aluno não
  consegue abrir o slide na empresa. Rode por último, depois do deck pronto.
---

# Skill: deck do Mira em modo offline (à prova de firewall)

Torna um deck já montado **100% self-contained**: nenhuma lib que ele puxa de CDN
é buscada em runtime. Passa a abrir por `file://` mesmo numa rede corporativa que
bloqueia `unpkg.com`, `cdn.tailwindcss.com` ou `fonts.googleapis.com`.

> **Copia, não baixa.** As libs já vieram no pacote npm (`mira-templates/vendor/`,
> que a empresa costuma liberar) e são apenas copiadas. É de propósito: o aluno pode
> estar atrás do firewall *enquanto* constrói o deck, e baixar das CDNs falharia
> justamente quando é mais necessário.

## O que é localizado

Copiado de `mira-templates/vendor/` para `<deck>/assets/vendor/` e religado nos HTMLs:

| De (CDN, bloqueável) | Para (local, relativo) |
|---|---|
| `cdn.tailwindcss.com` | `assets/vendor/tailwind.js` |
| `unpkg.com/aos@2.3.1/...` | `assets/vendor/aos.css` · `aos.js` |
| `unpkg.com/lucide@...` | `assets/vendor/lucide.js` |
| `d3js.org/d3.v7.min.js` | `assets/vendor/d3.v7.min.js` |
| `fonts.googleapis.com/...Inter...` | `assets/vendor/inter.css` (+ `fonts/*.woff2`) |
| `unpkg.com/three@.../build/...` + `examples/jsm/` | `assets/vendor/three/` (só em decks 3D) |

Os `<link rel="preconnect">` para `fonts.googleapis.com`/`fonts.gstatic.com` são
removidos (externos e inúteis offline). **Todos** os HTMLs do deck são reescritos,
não só o `index.html`.

**Three.js (mira-3d):** o importmap é reescrito para caminhos locais e a pasta
`three/` (core + `OrbitControls` + `GLTFLoader` + dep transitiva) é copiada para
`assets/vendor/three/`, **só quando** o deck usa 3D (são ~1,4 MB; decks sem 3D não
levam esse peso). Os `import 'three'` / `import 'three/addons/...'` seguem como bare
specifiers, resolvidos pelo importmap local. Se um deck 3D usar um addon **além** de
OrbitControls/GLTFLoader, ele não estará no bundle: a skill avisa.

## O que NÃO é localizado (e por quê)

- **GSAP** (skills de morph): já é vendorado por-deck em `assets/gsap/`. A skill só
  confere e avisa se achar GSAP por CDN.

## Como rodar

O trabalho é determinístico. Rode na raiz do projeto apontando para a pasta do deck:

```bash
node mira-templates/vendor/apply-offline.mjs decks/<nome-do-deck>
```

É **idempotente**: rodar de novo não duplica nem estraga (URLs já locais não casam
com os padrões de CDN). Se o deck reintroduzir uma CDN após edição, rode de novo.

## Passos

1. **Identificar o deck.** Confirme a pasta em `decks/<nome>/`. Se o usuário não disse
   qual, liste os decks e pergunte. Deck novo: monte pelo pipeline primeiro e rode esta
   skill **por último**.
2. **Conferir o bundle.** Garanta que `mira-templates/vendor/` existe (veio na
   instalação). Se faltar, o projeto foi instalado por versão antiga do Mira — peça
   `npx mira-animator update` antes.
3. **Rodar o script** `node mira-templates/vendor/apply-offline.mjs decks/<nome>`.
4. **Ler o relatório.** Diz, por HTML, quantos recursos foram localizados e lista
   avisos (Three.js, GSAP ou URL externa remanescente).
5. **Tratar os avisos.** Se avisar Three.js, explique que o 3D não fica offline por
   aqui (opções acima). Se sobrar outra URL externa, mostre-a.
6. **Reportar.** Caminhos reescritos, que o deck agora abre por `file://` sem rede, e
   o tamanho aproximado adicionado (~1,3 MB de libs em `assets/vendor/`).

## Verificação (faça, não presuma)

- Abra o `index.html` e confirme no `<head>` que **nenhuma** `src`/`href` começa com
  `http://` ou `https://` (exceto Three.js avisado, se houver).
- Ideal: abrir por `file://` **com a rede desligada** (ou DevTools > Network > Offline)
  e ver tudo carregar — fonte Inter aplicada, ícones Lucide renderizados, animações
  AOS/D3 rodando.

## Checklist

- [ ] Rodou o script; não editou HTML na mão (a reescrita é determinística).
- [ ] `assets/vendor/` populado (tailwind, aos css+js, lucide, d3, inter.css, fonts/).
- [ ] **Todos** os HTMLs do deck reescritos (index + variantes 1x1/9x16/thirds/dissolve).
- [ ] Nenhuma `src`/`href` http(s) remanescente nos HTMLs conhecidos.
- [ ] `preconnect` de fonts removidos.
- [ ] Three.js (se deck 3D): importmap reescrito e `assets/vendor/three/` copiado; addon fora do par OrbitControls/GLTFLoader é avisado, não dado como offline.
- [ ] GSAP de morph: confirmado já local em `assets/gsap/` (não duplicado).
- [ ] Nada foi baixado da internet durante a operação (à prova de firewall).
- [ ] Nenhum travessão (—); acentuação UTF-8 correta (segue `agents/_shared/idioma.md`).
