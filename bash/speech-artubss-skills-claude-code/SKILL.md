---
name: "speech"
description: "Use quando o usuário solicita narração em texto-para-fala, voiceovers de acessibilidade, prompts de áudio ou geração em lote via OpenAI Audio API; execute a CLI incluída (`scripts/text_to_speech.py`) com vozes integradas e requer `OPENAI_API_KEY` para chamadas diretas. Criação de vozes customizadas está fora do escopo."
author: openai
---


# Skill de Geração de Fala

Gere áudio falado para o projeto atual (narração, voiceover de demo de produto, prompts de IVR, leituras de acessibilidade). Padrão: `gpt-4o-mini-tts-2025-12-15` e vozes integradas, com preferência pela CLI incluída para execuções determinísticas e reproduzíveis.

## Quando usar
- Gerar um único clipe falado a partir de texto
- Gerar um lote de prompts (múltiplas linhas, múltiplos arquivos)

## Árvore de decisão (único vs lote)
- Se o usuário fornece múltiplas linhas/prompts ou deseja muitos outputs -> **lote**
- Caso contrário -> **único**

## Workflow
1. Decida a intenção: único vs lote (veja árvore de decisão acima).
2. Colete inputs antecipadamente: texto exato (palavra por palavra), voz desejada, estilo de entrega, formato e qualquer restrição.
3. Se lote: escreva um JSONL temporário em tmp/ (um job por linha), execute uma vez, depois delete o JSONL.
4. Aumente instruções em uma especificação curta e rotulada sem reescrever o texto de entrada.
5. Execute a CLI incluída (`scripts/text_to_speech.py`) com padrões sensatos (veja references/cli.md).
6. Para clipes importantes, valide: inteligibilidade, pacing, pronúncia e conformidade com restrições.
7. Itere com uma única mudança direcionada (voz, velocidade ou instruções), depois revise.
8. Salve/retorne os outputs finais e anote o texto final + instruções + flags utilizadas.

## Convenções de temp e output
- Use `tmp/speech/` para arquivos intermediários (por exemplo, lotes JSONL); delete ao terminar.
- Escreva artefatos finais em `output/speech/` ao trabalhar neste repositório.
- Use `--out` ou `--out-dir` para controlar paths de output; mantenha nomes de arquivo estáveis e descritivos.

## Dependências (instale se faltarem)
Prefira `uv` para gerenciamento de dependências.

Pacotes Python:
```
uv pip install openai
```
Se `uv` não estiver disponível:
```
python3 -m pip install openai
```

## Ambiente
- `OPENAI_API_KEY` deve estar definida para chamadas diretas de API.

Se a chave estiver faltando, forneca ao usuário estas etapas:
1. Crie uma API key na UI da plataforma OpenAI: https://platform.openai.com/api-keys
2. Configure `OPENAI_API_KEY` como variável de ambiente em seu sistema.
3. Ofereça-se para guiá-lo através da configuração da variável de ambiente para seu SO/shell, se necessário.
- Nunca peça ao usuário que cole a chave completa no chat. Peça que configure localmente e confirme quando pronto.

Se a instalação não for possível neste ambiente, informe ao usuário qual dependência está faltando e como instalá-la localmente.

## Padrões & regras
- Use `gpt-4o-mini-tts-2025-12-15` a menos que o usuário solicite outro modelo.
- Voz padrão: `cedar`. Se o usuário quer um tom mais brilhante, prefira `marin`.
- Apenas vozes integradas. Vozes customizadas estão fora do escopo desta skill.
- `instructions` são suportadas para modelos GPT-4o mini TTS, mas não para `tts-1` ou `tts-1-hd`.
- O comprimento da entrada deve ser <= 4096 caracteres por requisição. Divida textos mais longos em chunks.
- Enforce 50 requisições/minuto. A CLI limita `--rpm` a 50.
- Requer `OPENAI_API_KEY` antes de qualquer chamada de API direto.
- Forneça uma divulgação clara aos usuários finais de que a voz é gerada por IA.
- Use o SDK Python da OpenAI (pacote `openai`) para todas as chamadas de API; não use HTTP bruto.
- Prefira a CLI incluída (`scripts/text_to_speech.py`) em vez de escrever novos scripts pontuais.
- Nunca modifique `scripts/text_to_speech.py`. Se algo estiver faltando, pergunte ao usuário antes de fazer qualquer coisa.

## Aumento de instrução
Reformate a direção do usuário em uma especificação curta e rotulada. Apenas torne explícitos detalhes implícitos; não invente novos requisitos.

Esclarecimento rápido (aumento vs invenção):
- Se o usuário diz "narração para uma demo", você pode adicionar restrições de entrega implícitas (clara, pacing constante, tom amigável).
- Não introduza uma nova persona, sotaque ou estilo emocional que o usuário não tenha solicitado.

Template (inclua apenas linhas relevantes):
```
Textura de Voz: <caráter geral e textura da voz>
Tom: <atitude, formalidade, calidez>
Pacing: <lento, constante, rápido>
Emoção: <emoções-chave a transmitir>
Pronúncia: <palavras a enunciar ou enfatizar>
Pausas: <onde adicionar pausas intencionais>
Ênfase: <palavras ou frases-chave a estressar>
Entrega: <notas de cadência ou ritmo>
```

Regras de aumento:
- Mantenha breve; adicione apenas detalhes que o usuário já implícita ou explicitamente forneceu.
- Não reescreva o texto de entrada.
- Se algum detalhe crítico estiver faltando e bloquear sucesso, faça uma pergunta; caso contrário, prossiga.

## Exemplos

### Exemplo único (narração)
```
Texto de entrada: "Bem-vindo à demo. Hoje vamos mostrar como funciona."
Instruções:
Textura de Voz: Quente e composta.
Tom: Amigável e confiante.
Pacing: Constante e moderado.
Ênfase: Estresse "demo" e "mostrar".
```

### Exemplo de lote (prompts de IVR)
```
{"input":"Obrigado por ligar. Por favor, aguarde.","voice":"cedar","response_format":"mp3","out":"hold.mp3"}
{"input":"Para vendas, pressione 1. Para suporte, pressione 2.","voice":"marin","instructions":"Tom: Claro e neutro. Pacing: Lento.","response_format":"wav"}
```

## Melhores práticas de instrução (lista breve)
- Estruture direções como: textura -> tom -> pacing -> emoção -> pronúncia/pausas -> ênfase.
- Mantenha 4 a 8 linhas curtas; evite orientação conflitante.
- Para nomes/acrônimos, adicione dicas de pronúncia (ex: "enuncie A-I") ou forneça uma soletração fonética no texto.
- Para edições/iterações, repita invariantes (ex: "mantenha pacing constante") para reduzir desvios.
- Itere com follow-ups de mudança única.

Mais princípios: `references/prompting.md`. Especificações para colar: `references/sample-prompts.md`.

## Orientação por caso de uso
Use estes módulos quando a solicitação é para um estilo de entrega específico. Eles fornecem padrões e templates direcionados.
- Narração / explainer: `references/narration.md`
- Demo de produto / voiceover: `references/voiceover.md`
- IVR / prompts de telefone: `references/ivr.md`
- Leituras de acessibilidade: `references/accessibility.md`

## Notas CLI + ambiente
- Comandos CLI + exemplos: `references/cli.md`
- Referência rápida de parâmetros de API: `references/audio-api.md`
- Padrões de instrução + exemplos: `references/voice-directions.md`
- Se aprovações de rede / configurações de sandbox estão atrapalhando: `references/codex-network.md`

## Mapa de referência
- **`references/cli.md`**: como executar geração de fala/lotes via `scripts/text_to_speech.py` (comandos, flags, receitas).
- **`references/audio-api.md`**: parâmetros de API, limites, lista de vozes.
- **`references/voice-directions.md`**: padrões de instrução e exemplos.
- **`references/prompting.md`**: melhores práticas de instrução (estrutura, restrições, padrões de iteração).
- **`references/sample-prompts.md`**: receitas de instrução pronta para colar (apenas exemplos; sem teoria extra).
- **`references/narration.md`**: templates + padrões para narração e explainers.
- **`references/voiceover.md`**: templates + padrões para voiceovers de demo de produto.
- **`references/ivr.md`**: templates + padrões para prompts de IVR/telefone.
- **`references/accessibility.md`**: templates + padrões para leituras de acessibilidade.
- **`references/codex-network.md`**: troubleshooting de ambiente/sandbox/aprovação de rede.