---
name: evoluir-motor
description: Protocolo para melhorar o motor de tradução do Mangalate (detecção, OCR, balão ou arte, limpeza, tradução, letreiramento, emendas, velocidade) uma iteração por vez, guiado por baseline, teste que falha antes, mudança mínima e rodada sem regressão. Use ao corrigir ou melhorar qualquer coisa em server/ que muda a página traduzida.
---

# Evoluir o motor do Mangalate

Cada iteração resolve **um** problema e termina com uma decisão registrada: aceitar, reverter ou pedir revisão humana. As prioridades de qualidade e os comandos estão no `CLAUDE.md`; aqui está só o processo.

## 0. Preparar

- Confirme a branch de trabalho (uma `melhoria/<assunto>` a partir da `main`, ou a que o Lucas indicou) e que `git status` está limpo, ou que o que está sujo não é seu.
- Anote o commit de partida (`git log -1 --oneline`). Ele é o baseline do código.
- Rode `python -m unittest discover -s server/tests` e anote o resultado. Se já estiver vermelho, o problema é esse e vem antes de qualquer outro.

## 1. Escolher um problema

A fonte é a última rodada (`review.json`, `revisao.md`, `diagnostico/`, o log) ou um relato do Lucas com o original e o resultado. Escolha **um** problema e escreva a ficha:

| Campo | Conteúdo |
|---|---|
| Sintoma | O que se vê na página traduzida |
| Onde | Trecho, página e região (coordenadas de `regioes.json`) |
| Etapa | Detecção, OCR, balão ou arte, limpeza, tradução, letreiramento, emenda ou velocidade |
| Causa provável | O mecanismo, confirmado nas imagens de diagnóstico (máscara, regiões, limpa) |
| Generalidade | Por que o mesmo mecanismo aparece em outras obras e formatos (P&B e colorido) |
| Pronto quando | Critério observável, por exemplo "a fala sai em português e o contorno fica intacto" |

Na escolha entre vários problemas, vence o que fere a prioridade mais alta do `CLAUDE.md`; no empate, o que aparece em mais páginas. Se a única explicação for "essa obra é assim", o problema não está pronto para virar código: procure o mecanismo geral ou leve ao Lucas.

## 2. Medir o baseline

Com o commit de partida, meça o **trecho motivador** e o **conjunto de controle**. O controle é fixo durante a iteração: pelo menos um trecho de mangá P&B e um de webtoon ou manhwa colorido, de 5 a 6 páginas cada, tirados de `server/teste/`, de preferência os mesmos da última rodada. Se uma rodada recente no mesmo commit já tem esses trechos, reaproveite-a.

Para cada trecho, tire do `review.json` e do log:
- páginas por `status` (`review`, `no_text_review`, `translation_unusable_original_preserved`, `blocked_original_preserved`);
- regiões traduzidas e regiões que ficaram em inglês (`translation` igual ao `original` ou vazia);
- `preserved_regions` (falas deixadas na arte);
- `line_repairs` e `ocr_rescued`;
- "Bubble layout: X of Y" e qualquer "Bubble layout skipped" no log;
- `seconds` por página e `provider_events` (pausas e limites das IAs).

Some a isso a inspeção visual das páginas tocadas pelo problema, com os critérios do `server/QUALITY.md`: arte, balões, texto, português e escrita. Guarde a tabela do baseline, porque é com ela que o resultado vai ser comparado.

## 3. Escrever o teste que falha antes

- Reproduza o mecanismo num teste em `server/tests/`: `test_rounds.py` para achados de rodada, ou o arquivo do módulo (`test_quality.py`, `test_lettering.py`, `test_seams.py`...).
- Use imagem sintética (numpy/OpenCV) e regiões montadas à mão, como os testes que já existem. Nunca use página real, nome de obra nem fala copiada como condição.
- Escreva também o **caso vizinho que não pode mudar**: o balão parecido que tem que continuar como está, a arte que tem que continuar intacta. É ele que segura o overfitting.
- Rode o teste e confirme que falha **pelo motivo certo**, e não por import ou fixture quebrada.
- Problema de tradução (tom, gíria, gênero) nem sempre vira teste de unidade. Nesse caso, teste a parte determinística (validação, pós-processamento, montagem do pedido) e deixe a qualidade do texto para a rodada.

## 4. Mudança mínima

- Mexa no menor ponto do módulo certo. Um limiar novo vira constante nomeada, com a unidade num comentário, como as que já existem em `quality.py`.
- Mantenha o caminho seguro: se a heurística nova não tiver certeza, o resultado tem que ser o de antes, ou o original preservado.
- Não junte melhorias. Uma segunda ideia que aparecer no caminho vira o próximo problema da fila.
- Arquivos novos copiados para a imagem entram no `Dockerfile.worker` e no `CHECKED` do `rebuild.py`.

## 5. Validar sem regressão

1. Rode o teste novo e a suíte inteira: `python -m unittest discover -s server/tests -v`, tudo verde.
2. Se mexeu no app: `./gradlew :app:testDebugUnitTest --tests 'app.mangalate.*'`.
3. Rode no PC, no commit novo: `py rebuild.py`, depois o trecho motivador e o conjunto de controle com as mesmas opções do baseline (`--profile byok --speed fast --diagnostics` e o mesmo `--work`). Use uma pasta nova em `teste-curto/<rodada>/`.
4. Monte a tabela antes e depois, trecho a trecho, com as métricas do passo 2, e compare as imagens das páginas tocadas.
5. Chame o subagente `revisor-motor` com o diff, a ficha do problema e a tabela.

A IA varia entre execuções e entre provedores. Uma diferença só na tradução de uma região que a mudança não tocou é ruído: confira em `provider_events` se o provedor foi o mesmo antes de chamar de regressão.

## 6. Decidir

**Aceitar** quando tudo isto vale:
- o critério de pronto foi atingido no trecho motivador;
- nenhuma página do controle piorou em arte, limpeza, fala ou letreiramento;
- a suíte está verde e o teste novo falhava antes;
- o `revisor-motor` não deixou nada bloqueante.

Nesse caso, prepare o commit (um assunto, mensagem em português como as do histórico, CHANGELOG em "Em teste" e, se quem lê percebe a mudança, uma frase simples nas novidades do app em `MangalateWhatsNew.kt`) e só faça commit e push quando o Lucas pedir.

**Reverter** quando o critério não foi atingido, quando apareceu uma regressão que você não consegue explicar e corrigir dentro do mesmo problema, ou quando a mudança precisou ficar grande. Use `git restore` nos arquivos da iteração e anote o que se aprendeu na ficha.

**Pedir revisão humana** ao Lucas quando:
- a mudança melhora umas páginas e piora outras;
- o julgamento visual é ambíguo (tamanho da letra, posição, o que é balão e o que é arte);
- muda o tom ou o estilo da tradução, as instruções da IA ou a escolha de provedores;
- muda um padrão que o usuário sente, como velocidade, modo ou uso da cota;
- toca o app Android ou o que o app manda para o servidor.

Leve a ficha, a tabela antes e depois, os caminhos das imagens no PC e uma recomendação.

Todo resultado mostrado ao Lucas vem com as **páginas inteiras** afetadas, lado a lado (Original | 1ª versão traduzida | Correção), no tamanho de leitura, e com pelo menos um balão de controle que não pode mudar. Recortes ampliados só entram como complemento, depois da página inteira: sozinhos, deixam escapar detalhes (balão que virou dois, ênfase perdida, ordem de leitura). Salve em `teste-curto/<rodada>/amostras/` com um `amostras.html` que tenha uma legenda por amostra. Regras das amostras:
- **Ordem:** a mesma ordem e a mesma numeração dos grupos do texto (1, 1a, 1b...), com os controles no fim.
- **Página final:** as colunas mostram sempre a página **traduzida final** (`translated/`) de uma rodada real. Página limpa, máscara ou simulação offline só entram como coluna extra, com o nome dito na própria coluna, e nunca no lugar da traduzida.
- **Legenda conferida:** abra cada imagem antes de escrever a legenda e confira que o texto descrito é o que aparece.
- **Toda página que mudou:** cada página que a mudança alterou entra nas amostras, e não só as do motivador.

Antes de mostrar, faça você mesmo a inspeção visual que o `revisor-motor` faz (arte, limpeza, fala, tradução e letreiramento, balão por balão) e diga o que ainda está ruim.

## 7. Registrar

Feche a iteração com um resumo curto: ficha, commit de partida e final, tabela, decisão e o próximo problema da fila. A próxima iteração começa no passo 0.
