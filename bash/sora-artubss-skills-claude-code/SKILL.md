---
name: "sora"
description: "Use quando o usuário solicita gerar, remixar, consultar, listar, baixar ou deletar vídeos Sora via API de vídeo da OpenAI usando a CLI incluída (`scripts/sora.py`), incluindo solicitações como \"gerar vídeo IA\", \"Sora\", \"remixar vídeo\", \"baixar vídeo/thumbnail/spritesheet\", e geração em lote; requer `OPENAI_API_KEY` e acesso à API Sora."
author: openai
---

# Skill de Geração de Vídeo Sora

Cria ou gerencia clipes de vídeo curtos para o projeto atual (demos de produto, spots de marketing, cenas cinematográficas, mockups de UI). Usa como padrão `sora-2` e um fluxo estruturado de aumento de prompt, preferindo a CLI incluída para execuções determinísticas. Nota: `$sora` é uma tag de skill em prompts, não um comando shell.

## Quando usar
- Gerar um novo clipe de vídeo a partir de um prompt
- Remixar um vídeo existente por ID
- Consultar status, listar jobs ou baixar assets (vídeo/thumbnail/spritesheet)
- Execuções em lote (muitos prompts ou variantes)

## Árvore de decisão (criar vs remixar vs status/download vs lote)
- Se o usuário tem um **video id** e quer uma mudança → **remix**
- Se o usuário tem um **video id** e quer status ou assets → **status/poll/download**
- Se o usuário precisa de muitos prompts/assets → **create-batch**
- Se o usuário pede duas versões com uma pequena mudança (mesmo shot, assunto/detalhe diferente) → **create** a base, depois **remix** para a variação
- Caso contrário → **create** (ou **create-and-poll** se precisarem de um asset pronto em uma etapa)

## Fluxo de trabalho
1. Decide a intenção: criar vs remixar vs status/download vs lote.
2. Colete inputs: prompt, modelo, tamanho, segundos e qualquer imagem de referência de entrada.
3. Se lote: escreva um JSONL temporário sob tmp/ (um job por linha), execute uma vez, depois delete o JSONL.
4. Prefira flags de aumento da CLI (`--use-case`, `--scene`, `--camera`, etc.) em vez de pré-escrever um prompt estruturado. Se você já produziu um arquivo de prompt estruturado, passe `--no-augment` para evitar dupla encapsulação.
5. Execute a CLI incluída (`scripts/sora.py`) com padrões sensatos (veja references/cli.md). Para prompts longos, prefira `--prompt-file` para evitar problemas de escape de shell; combine com `--no-augment` se o prompt já estiver estruturado.
6. Para jobs assíncronos, consulte até completar (ou use create-and-poll).
7. Baixe assets (vídeo/thumbnail/spritesheet) e salve localmente.
8. Remova arquivos intermediários criados durante a invocação (por exemplo `prompt.txt`, `remix_job.json`, JSONL temporário). Se a sandbox bloquear `rm`, pule a limpeza ou truncate os arquivos sem exibir um erro.
9. Itere com uma única mudança direcionada por prompt.

## Autenticação
- `OPENAI_API_KEY` deve estar definida para chamadas de API ativas.

Se a chave estiver faltando, forneça ao usuário estas etapas:
1. Crie uma chave de API na UI da plataforma OpenAI: https://platform.openai.com/api-keys
2. Defina `OPENAI_API_KEY` como uma variável de ambiente no seu sistema.
3. Ofereça orientação sobre como definir a variável de ambiente para seu SO/shell, se necessário.
- Nunca peça ao usuário para colar a chave completa no chat. Peça que a defina localmente e confirme quando estiver pronto.

## Padrões e regras
- Modelo padrão: `sora-2` (use `sora-2-pro` para maior fidelidade).
- Tamanho padrão: `1280x720`.
- Segundos padrão: `4` (permitidos: "4", "8", "12" como strings).
- Sempre defina tamanho e segundos via parâmetros de API; prosa não os mudará.
- Use o SDK Python da OpenAI (pacote `openai`); não use HTTP bruto.
- Exija `OPENAI_API_KEY` antes de qualquer chamada de API ativa.
- Se falhas de permissão de cache uv ocorrerem, defina `UV_CACHE_DIR=/tmp/uv-cache`.
- Imagens de referência de entrada devem ser jpg/png/webp e devem corresponder ao tamanho alvo.
- Download URLs expiram após cerca de 1 hora; copie assets para seu próprio armazenamento.
- Prefira a CLI incluída e **nunca modifique** `scripts/sora.py` a menos que o usuário solicite.
- Sora pode gerar áudio; se um usuário solicitar voiceover/áudio, especifique explicitamente nas linhas `Audio:` e `Dialogue:` e mantenha curto.

## Limitações de API
- Modelos limitados a `sora-2` e `sora-2-pro`.
- Acesso de API aos modelos Sora requer uma conta verificada pela organização.
- A duração é limitada a 4/8/12 segundos e deve ser definida via parâmetro `seconds`.
- A API espera `seconds` como enum de string ("4", "8", "12").
- Os tamanhos de saída são limitados pelo modelo (veja `references/video-api.md` para tamanhos suportados).
- Criação de vídeo é assíncrona; você deve consultar para conclusão antes de baixar.
- Limites de taxa se aplicam por tier de uso (não liste limites específicos).
- Restrições de conteúdo são aplicadas pela API (veja Guardrails abaixo).

## Guardrails (deve-se executar)
- Apenas conteúdo apropriado para públicos menores de 18 anos.
- Sem personagens com direitos autorais ou música com direitos autorais.
- Sem pessoas reais (incluindo figuras públicas).
- Imagens de entrada com rostos humanos são rejeitadas.

## Aumento de prompt
Reformate prompts em uma spec estruturada e orientada para produção. Apenas torne explícitos os detalhes implícitos; não invente novos requisitos criativos.

Template (inclua apenas linhas relevantes):
```
Caso de uso: <onde o clipe será usado>
Solicitação principal: <prompt principal do usuário>
Cena/background: <local, hora do dia, atmosfera>
Assunto: <assunto principal>
Ação: <ação única e clara>
Câmera: <tipo de shot, ângulo, movimento>
Iluminação/humor: <iluminação + humor>
Paleta de cores: <3-5 âncoras de cor>
Estilo/formato: <dicas de filme/animação/formato>
Timing/beats: <contagens ou beats>
Áudio: <dica ambiental / música / voiceover se solicitado>
Texto (verbatim): "<texto exato>"
Diálogo:
<diálogo>
- Personagem: "Linha curta."
</diálogo>
Restrições: <deve manter/deve evitar>
Evitar: <restrições negativas>
```

Regras de aumento:
- Mantenha curto; adicione apenas detalhes que o usuário já implícita ou explicitamente forneceu em outro lugar.
- Para remixes, liste explicitamente invariantes ("mesmo shot, mude apenas X").
- Se algum detalhe crítico estiver faltando e bloquear o sucesso, faça uma pergunta; caso contrário, prossiga.
- Se você passar um arquivo de prompt estruturado para a CLI, adicione `--no-augment` para evitar que a ferramenta o re-encapsule.

## Exemplos

### Exemplo de geração (single shot)
```
Caso de uso: teaser de produto
Solicitação principal: um close-up de uma câmera preta fosca em um pedestal
Ação: órbita lenta de 30 graus em 4 segundos
Câmera: 85mm, profundidade de campo rasa, drift handheld sutil
Iluminação/humor: soft key light, rim sutil, sensação premium de estúdio
Restrições: sem logos, sem texto
```

### Exemplo de remix (invariantes)
```
Solicitação principal: mesmo shot e framing, trocar paleta para azul-petróleo/areia/ferrugem com contraluz mais quente
Restrições: manter o assunto e movimento de câmera inalterados
```

## Melhores práticas de prompt (lista curta)
- Uma ação principal + um movimento de câmera por shot.
- Use contagens ou beats para timing ("dois passos, pausa, vira").
- Mantenha texto curto e câmera travada para UI ou texto na tela.
- Adicione uma linha breve de evitar quando artefatos aparecem (flicker, jitter, movimento rápido).
- Prompts mais curtos são mais criativos; prompts mais longos são mais controlados.
- Coloque diálogo em um bloco dedicado; mantenha linhas curtas para clipes de 4-8s.
- Declare invariantes explicitamente para remixes (mesmo shot, mesmo movimento de câmera).
- Itere com follow-ups de mudança única para preservar continuidade.

## Orientação por tipo de asset
Use estes módulos quando a solicitação for para um artefato específico. Eles fornecem templates direcionados e padrões.
- Shots cinematográficos: `references/cinematic-shots.md`
- Anúncios sociais: `references/social-ads.md`

## Notas de CLI e ambiente
- Comandos de CLI + exemplos: `references/cli.md`
- Referência rápida de parâmetros de API: `references/video-api.md`
- Orientação de prompt: `references/prompting.md`
- Prompts de exemplo: `references/sample-prompts.md`
- Solução de problemas: `references/troubleshooting.md`
- Dicas de rede/sandbox: `references/codex-network.md`

## Mapa de referência
- **`references/cli.md`**: como executar create/poll/remix/download/batch via `scripts/sora.py`.
- **`references/video-api.md`**: controles em nível de API (modelos, tamanhos, duração, variantes, status).
- **`references/prompting.md`**: estrutura de prompt e orientação de iteração.
- **`references/sample-prompts.md`**: receitas de prompt para copiar/colar (exemplos apenas; sem teoria extra).
- **`references/cinematic-shots.md`**: templates para shots fílmicos.
- **`references/social-ads.md`**: templates para beats curtos de anúncios sociais.
- **`references/troubleshooting.md`**: erros comuns e correções.
- **`references/codex-network.md`**: solução de problemas de rede/aprovação.