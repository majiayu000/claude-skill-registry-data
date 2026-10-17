---
name: ai-graphic-design
description: Guide for creating logos, brand identities, and visual assets using AI tools — covers tool selection, prompt engineering, vectorization pipelines, mockups, automation, and IP safety.
risk: low
source: custom
date_added: '2026-04-01'
---

# AI Graphic Design — Logomarcas e Identidades Visuais com IA

## When to Trigger

Invoke this skill when the user mentions:
- Logomarca, logo, logotipo, marca, branding
- Identidade visual, design grafico, vetorizacao
- Mockup, apresentacao visual, material grafico
- Prompt visual, geracao de imagem para marca
- SVG, EPS, vetorial, Illustrator, Recraft, Midjourney

---

## 1. Tool Selection Matrix

Escolha a ferramenta pelo cenario. **Nao existe bala de prata** — cada IA tem uma forca especifica.

| Cenario | Ferramenta | Por que |
|---|---|---|
| Logo vetorial (SVG) limpo e escalavel | **Recraft V3/V4** | Gera SVG nativo com precisao estrutural; Style IDs travam consistencia |
| Exploracao criativa / moodboards | **Midjourney v6+** | Estetica cinematografica inigualavel; --sref e --cref manteem consistencia |
| Uso comercial IP-safe (corporate) | **Adobe Firefly / Illustrator** | Treinado em Adobe Stock; oferece indenizacao de IP |
| Storyboards / iteracao conversacional | **DALL-E 3 (ChatGPT)** | Interpretacao literal; refinamento via chat natural |
| Controle total / geracao em lote | **Stable Diffusion** | Open-source; LoRAs customizados; ControlNet para exatidao milimetrica |
| Wireframe / prototipo UI | **Uizard** | Converte rascunhos em wireframes interativos |
| Mockups fotorrealistas | **Nano Banana / Phygital+** | Insere arte em ambientes 3D com sombras e deformacoes reais |
| Vetorizacao de raster | **Vectorizer.ai** | Converte JPG/PNG em SVG/EPS cirurgicamente |
| Remocao de fundo | **Remove.bg / Adobe Express** | Recortes complexos (cabelos, fios) em um clique |
| Upscaling | **Upscayl** (local/gratis) / **Topaz Labs** (premium) | Aumenta resolucao sem pixelar |
| Paleta de cores | **Colormind** | ML extrai logica cromatica de fotos-referencia |
| Identificar fonte | **WhatTheFont** | Visao computacional cruza imagem com banco de fontes |
| Consistencia de produto/personagem | **Krea AI / Flora AI** | Modos dedicados para manter fidelidade em multiplos angulos |
| Moodboard → estilo consistente | **Visual Electric** | Extrai "Custom Style" de 6-12 imagens curadas |

---

## 2. Briefing Frameworks

Antes de gerar qualquer visual, defina a identidade verbal da marca.

### Framework RCAO (para prompts de LLM)

```
Role:    "Voce e um diretor de arte senior especialista em [nicho]"
Context: "[publico-alvo], [tom de voz], [valores da marca], [concorrentes]"
Action:  "Crie [N] direcoes visuais para [tipo de entregavel]"
Output:  "Formato: [tabela/lista]. Restricoes: [sem gradientes, max 3 cores]"
```

### Metodologia StoryBrand (identidade de marca)

Instrua o LLM a definir:
1. **Personagem** — cliente e seus desejos
2. **Problema** — externo (funcional) + interno (emocional)
3. **Guia** — a marca como mentora (nunca como heroi)
4. **Plano / CTA** — passos claros
5. **Sucesso vs Falha** — cenarios com e sem o servico

Output: paragrafo de posicionamento + tom de voz + arquetipo dominante.

### Arquetipo de Marca

Defina **um unico** arquetipo dominante antes de qualquer geracao visual. Misturar arquetipos conflitantes (ex: luxuoso + brincalhao + barato) e o erro #1 em briefings com IA.

---

## 3. Prompt Engineering por Ferramenta

### 3.1 Recraft (Logotipos Vetoriais)

O prompt deve funcionar como um **briefing de design rigoroso**:

```
Estrutura obrigatoria:
1. Tipo de grafico     → "bold word logo", "logotipo tipografico em negrito"
2. Logica de formas    → geometria, simetria, silhueta
3. Sistema de cores    → paleta exata + estilo (flat, chapado)
4. Disciplina de linhas → centralizacao, escalabilidade, coesao
5. Restricoes (CRITICO) → "evite gradientes, texturas, sombras, linhas finas"
```

**Exemplo funcional:**
```
Logo "KINDRA" Serif or sans-serif, typographic composition in bold, ultra-chunk.
Brand about care, community, kindness, human connection.
Flat colors, no gradients, no shadows, no thin lines.
```

### 3.2 Midjourney (Ideacao e Moodboards)

Requer vocabulario artistico + parametros sintaticos:

```
Parametros essenciais:
--ar [ratio]     → proporcao (1:1, 16:9, 4:5)
--sref [url]     → Style Reference (copia paleta/luz/textura sem copiar sujeito)
--cref [url]     → Character/Omni Reference (mantem rosto/objeto identico)
--seed [n]       → fixa aleatoriedade para iteracao controlada
--stylize [n]    → 0=literal, 1000=maximo artistico
--chaos [n]      → variacao entre resultados
```

**Tecnica de iteracao:** Fixe seed + aspect ratio → altere UMA palavra por vez.

### 3.3 DALL-E 3 (Conversacional)

- Sem parametros sintaticos — 100% linguagem natural
- Foco em relacoes espaciais descritivas
- Refinamento via chat: "mova para a esquerda", "mude a cor para azul"
- Melhor para: storyboards sequenciais e assets ultra-especificos

### 3.4 Stable Diffusion (Controle Total)

- Requer montagem de nos (nodes) no ComfyUI/A1111
- **LoRAs**: treine com 15-30 imagens da marca → `<lora:nome:0.8>` no prompt
- **ControlNet**: impoe pose, profundidade ou enquadramento com exatidao milimetrica
- Curva de aprendizado mais acentuada, mas controle inigualavel

### 3.5 Formula Universal para Mockups

```
[Assunto] + [Background] + [Estilo] + [Material] + [Detalhes] + [Tamanho] + [Camera] + [Parametros]
```

**Exemplo funcional:**
```
A mockup design of a sleek wine bottle on a marble surface,
surrounded by delicate golden details, minimalist and luxurious,
set against a clean white background,
shot with a Canon EOS 5D, 50mm f/1.2 lens, soft natural lighting
```

### Prompts que FALHAM

- Exagero de detalhes → imagem confusa
- Sem restricoes negativas → logo com gradientes/texturas inutilizaveis
- Multiplos estilos conflitantes → "AI slop" generico

---

## 4. Workflow End-to-End

### Fase 1: Briefing e Estrategia

1. Use LLM (Claude/ChatGPT) com framework RCAO ou StoryBrand
2. Defina: publico, arquetipo, valores, tom de voz, paleta
3. Compile em Manual da Marca (PDF)
4. Insira o manual como contexto persistente (Projeto no Claude / Custom GPT)

### Fase 2: Ideacao Visual

1. Gere 20-40 variacoes no **Midjourney** (moodboards)
2. Curadoria rigorosa — selecione 3-5 direcoes promissoras
3. Valide com cliente antes de prosseguir

### Fase 3: Criacao do Ativo Vetorial

1. Leve o conceito aprovado para **Recraft V3/V4** ou **Adobe Illustrator**
2. No Recraft: treine Style ID com ativos da marca para consistencia
3. Gere logo + biblioteca de icones em SVG
4. Refine curvas de Bezier manualmente (Box Method — ver secao 6)

### Fase 4: Mockups e Apresentacao

1. Gere bases no Midjourney (formula: assunto+fundo+estilo+camera)
2. Ou use **Phygital+ / Nano Banana** para insercao automatica
3. No Photoshop: aplique Displacement Maps + Blend Options (ver secao 7)
4. Curadoria final das pecas

### Fase 5: Entrega

1. Exporte nos formatos corretos (ver secao 8)
2. Organize entregaveis: logo principal + variacoes + icones + mockups
3. Documente guidelines de uso

---

## 5. Consistencia Visual em Campanhas

O grande desafio da IA e **domar a aleatoriedade** entre pecas.

### Tecnicas por ferramenta:

| Tecnica | Ferramenta | Como |
|---|---|---|
| Style IDs | Recraft | Alimente com ativos da marca → trave estilo para todas as geracoes |
| --sref + --cref | Midjourney | Style Ref copia atmosfera; Char Ref mantem rosto/objeto identico |
| --seed fixo | Midjourney | Fixe seed → altere 1 elemento por vez |
| LoRAs | Stable Diffusion | Treine com 15-30 imagens → aplique com peso (ex: 0.8) |
| Custom Style | Visual Electric | Agrupe 6-12 imagens curadas → extraia regras de luz/cor/textura |

### Regras de ouro:

- **Gerenciar pastas por personagem/campanha** — nunca misturar seeds
- **Arquivar seeds e prompts** — toda geracao aprovada deve ter prompt documentado
- **Padronizar "blocos de estilo"** nos prompts — reutilize descricoes de atmosfera
- **Curadoria manual** — rejeite pecas que destoam da narrativa da marca

---

## 6. Pipeline de Vetorizacao (Raster → Vetor)

### Passo 1: Upscaling Inteligente

Escolha o modelo correto para nao alucinhar texturas:

| Modelo | Quando usar | O que faz |
|---|---|---|
| **Prime** | Logo pixelado / JPEG comprimido | Reconstroi bordas com nitidez e texturas organicas |
| **Gentle** | Arte limpa que so precisa de mais resolucao | Adiciona pixels SEM interpretacao criativa (ideal para tipografia) |
| **Digital Art** | Ilustracoes, icones, flat design, output de MJ/SD | Preserva cores chapadas e linhas nitidas sem ruido fotografico |
| **Ultra** | Arquivo de baixissima resolucao (ultimo recurso) | Reconstrucao agressiva — use com baixa intensidade |

**ARMADILHA:** Usar modelo fotografico (Prime) em logo flat → IA adiciona graos e texturas de papel no meio do logotipo. Use **Digital Art** ou **Gentle**.

### Passo 2: Vetorizacao

- **Vectorizer.ai** → converte raster upscalado em SVG/EPS/PDF automaticamente
- **Chat2SVG** (emergente) → LLM gera estrutura geometrica + difusao aplica texturas + otimizacao ajusta pontos vetoriais

### Passo 3: Cleanup de Bezier (Manual)

Mesmo com IA, vetores podem ter nos desnecessarios ou alcas desgovernadas.

**Box Method:**
1. Crie retangulos delimitadores ao redor das formas geradas
2. Posicione ancoras exatamente onde a curva toca as tangentes da caixa
3. Alcas sempre alinhadas na horizontal ou vertical
4. Objetivo: **numero minimo de pontos de ancoragem** → renderizacao rapida, precisao em plotters

Curvas cubicas de Bezier permitem formas complexas com poucos pontos (baseadas em polinomios de Bernstein).

---

## 7. Tecnicas de Mockup Profissional

### Displacement Maps (Photoshop)

Para aplicar estampa em tecido/superficie com realismo:

1. Duplique a foto original do mockup
2. Remova saturacao (Ctrl+U → Saturation 0)
3. Aplique Gaussian Blur sutil (~0.7px)
4. Salve como PSD (este e o "mapa")
5. Posicione a arte sobre o mockup
6. Filtro > Distorcao > Deslocamento (Displace) → carregue o PSD
7. A arte se deforma acompanhando dobras e rugas

### Blend Options (Opcoes de Mesclagem)

1. Clique na camada da arte → Opcoes de Mesclagem
2. Segure Alt → arraste controles da "Camada Subjacente" (areas escuras) para direita
3. As sombras da foto "vazam" sobre a estampa → integracao com iluminacao ambiente

### Alternativas com IA

- **Phygital+**: FLUX ControlNet insere logos em superficies 3D com consciencia de contexto
- **Nano Banana**: descreva o ambiente → IA insere a arte organicamente com sombras reais

---

## 8. Formatos de Entrega

### Vetor (escalabilidade infinita)

| Formato | Uso principal | Specs |
|---|---|---|
| **SVG** | Web responsivo, animacoes CSS, tipografia digital | XML matematico, sem pixels |
| **EPS** | Impressao industrial (plotters, embalagens, outdoors) | CMYK obrigatorio |
| **PDF vetorial** | Entrega universal, impressao de grande escala | CMYK, perfis ICC |

### Raster (grids de pixels)

| Formato | Uso principal | Specs |
|---|---|---|
| **PNG** | Digital com transparencia | 72 PPI (tela) / 300 DPI (impressao) |
| **JPG** | Fotos, mockups, material digital | 72 PPI (tela) / 300 DPI (impressao proximidade) / 150 DPI (banners gigantes) |

### Regra: sempre entregue o vetor original + rasterizacoes derivadas.

---

## 9. Automacao Python

### Bibliotecas essenciais

| Biblioteca | Funcao |
|---|---|
| **py5** | Geracao de formas geometricas e padroes matematicos via codigo |
| **vpype** | Pos-processamento: otimiza rotas, remove linhas ocultas (plugin occult), simplifica caminhos |
| **Aspose.SVG** | Manipulacao e conversao em massa (SVG → PDF/PNG/JPEG) |
| **Blender Python API** | Renderiza 3D → exporta contornos vetoriais 2D (add-on Freestyle) |

### Pipeline tipico

```
1. LLM gera codigo SVG bruto (manipulando tags XML: <path>, <rect>)
2. Python processa em lote:
   - Remove redundancias
   - Ajusta cores programaticamente
   - Exporta variantes (light/dark, tamanhos)
3. vpype otimiza caminhos e reduz tamanho de arquivo
4. Aspose exporta formatos finais
```

---

## 10. IP Safety e Etica

### Matriz de risco por ferramenta

| Ferramenta | Dados de treino | Indenizacao IP | Risco |
|---|---|---|---|
| **Adobe Firefly** | Adobe Stock + dominio publico + licenciado | Sim | Baixo |
| **Midjourney** | Nao divulgado; acoes judiciais pendentes | Nao | Medio-Alto |
| **Stable Diffusion** | Nao divulgado; acoes judiciais pendentes | Nao | Medio-Alto |
| **DALL-E 3** | Parcialmente divulgado | Parcial (Enterprise) | Medio |

### Regras legais (BR e EUA)

- **Autoria e restrita a humanos** — imagens 100% geradas por IA nao tem protecao autoral
- Para obter protecao legal: **contribuicao criativa humana significativa** (pos-producao, edicao, composicao)
- UK tem legislacao mais branda (atribui autoria a quem fez "os arranjos necessarios")

### Recomendacao pratica

- Projetos corporativos com exigencia de IP → **Adobe Firefly**
- Projetos pessoais / exploratórios → qualquer ferramenta
- Sempre documente o processo criativo humano para defesa legal

---

## 11. Anti-patterns (Erros Comuns)

| Erro | Consequencia | Como evitar |
|---|---|---|
| Prompt sem restricoes negativas | Logo com gradientes/texturas inutilizaveis | Sempre liste o que a IA deve EVITAR |
| Upscaling com modelo fotografico em flat design | Graos e texturas de papel no logo | Use modelos Digital Art ou Gentle |
| Gerar sem briefing/arquetipo | "AI Slop" — visual generico sem identidade | Use RCAO/StoryBrand; defina 1 arquetipo dominante |
| Focar em sintaxe efemera da ferramenta | Skills obsoletas em meses | Domine fundamentos atemporais: semiotica, cor, composicao, Bezier |
| Nao documentar seeds e prompts | Impossivel reproduzir ou iterar | Arquive prompt + seed + parametros de toda geracao aprovada |
| Misturar arquetipos conflitantes | Marca incoerente | 1 arquetipo dominante, 1 secundario no maximo |
| Confiar cegamente no output da IA | Entregavel com erros estruturais | Curadoria manual + cleanup de Bezier SEMPRE |

---

## 12. Competencias do Designer 2025-2026

O designer evolui de executor para **Diretor de Criacao da IA**:

1. **Curadoria e Gosto Estetico** — filtrar centenas de outputs para encontrar o que tem potencial real
2. **Engenharia de Prompt Avancada** — vocabulario artistico + prompt chaining + XML sandwiches
3. **Fundamentos Matematicos** — algebra linear, calculo, probabilidade (entender como modelos manipulam matrizes)
4. **Python e Automacao** — py5, vpype, pipelines de geracao em lote
5. **Fundamentos Classicos** — semiotica, teoria da cor, composicao, Pen Tool, curvas de Bezier
6. **Etica e Governanca** — auditorias de vies, direitos autorais, uso comercial seguro

> "As interfaces de IA ficam defasadas em meses. Fundamentos duram decadas."
