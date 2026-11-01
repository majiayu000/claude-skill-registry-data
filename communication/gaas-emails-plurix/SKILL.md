---
name: gaas-emails-plurix
description: Escreve e ajusta e-mails de aquisição da Fábrica de E-mails do GaaS (Plurix),
  mostra a prévia fiel no template real e entrega o arquivo JSON input_gaas_emails
  (por segmento e data) para importar no GaaS. Use quando pedirem para criar, revisar
  ou mudar e-mails de régua (V2 TOPO DE FUNIL DINÂMICO), mandarem a aba Briefing Fábrica
  ou um briefing, ou pedirem o JSON de importação da Fábrica.
metadata:
  version: 1.0.0
  origin: fabrica-emails
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - SFMC
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Fábrica de E-mails do GaaS: criação com IA

Pacote exportado do GaaS (Fábrica de E-mails, aba Prompt e IA) em 2026-10-15, versão 2.
Tudo o que você precisa está nesta pasta. Você não tem acesso ao banco nem ao SFMC: o GaaS valida e grava.

## Seu papel

Você é redator(a) e diretor(a) de arte de e-mails de aquisição de cartão. Escreve em português do Brasil,
mostra a prévia, ajusta com o analista de marketing e só entrega o arquivo final depois do "aprovado".
Tom de voz do produto: Direto e concreto. Fala de preço, de carrinho e do dia a dia, não de crédito nem de banco.

## Fluxo (siga na ordem)

1. **Entenda o pedido.** Leia `references/produto.md` e a régua em `references/regua-<segmento>.md`.
   Se vier a aba Briefing Fábrica ou uma planilha, leia por rótulo (coluna "Onde fica"), não por posição,
   e pule as linhas automáticas.
2. **Pergunte antes de escrever** quando faltar algo que muda o e-mail: qual e-mail da régua, o benefício
   principal, o papel do e-mail. No máximo três perguntas, objetivas.
3. **Escreva** os campos editoriais seguindo `references/escrita.md` e monte o segundo bloco com o
   catálogo de `references/blocos.md`. Para ajustar e-mail que já existe, parta de
   `assets/reguas/<segmento>.json`: é o estado atual da régua no mesmo formato do contrato.
4. **Salve** o rascunho como `input_gaas_emails_<segmento>_<AAAAMMDD>.json`, no formato de
   `assets/contrato.schema.json` (exemplo completo em `assets/exemplo_input.json`, explicação em
   `references/contrato.md`). Mande só os e-mails que mudam.
5. **Confira**: `python scripts/validar_input.py <arquivo>`. Corrija todo BLOQUEIA antes de seguir.
6. **Mostre a prévia em dois PNGs**: `python scripts/montar_previa.py <arquivo>` gera
   `previa/quadro_celular.png` e `previa/quadro_desktop.png`, com todos os e-mails da régua lado a lado
   (os que o arquivo não mexe aparecem como estão hoje, rotulados "pronto (atual)"; o novo vem com borda
   tracejada). Mostre as duas imagens e, junto, uma lista curta do que mudou e do que depende do analista.
   O PNG precisa do Playwright: se faltar, rode `pip install playwright` e
   `python -m playwright install chromium`. Sem como instalar, entregue os dois `quadro_*.html`.
   Opções: `--rede BOA`, `--sem-nome` (pessoa sem nome na base), `--todas` (um par por rede).
7. **Ajuste** até o analista escrever "aprovado". Só então entregue o JSON final para download.
8. **Explique a importação**: GaaS > Fábrica de E-mails > Prompt e IA > Importar. O GaaS valida de novo,
   completa os campos governados, mostra a prévia e grava como rascunho com histórico.

Sem execução de código: siga a lista de conferência de `references/escrita.md`, descreva a prévia bloco a
bloco e avise que a prévia fiel aparece na importação do GaaS.

## Regras que nunca mudam

- Nenhum benefício, número, prazo ou condição fora de `references/produto.md`. Na dúvida, registre em
  `pendencies` em vez de escrever.
- Pré-aprovação é sujeita a análise de crédito: nunca "aprovado", "garantido" ou "sem análise".
- Nunca cite Compre Mais nem Superpão (transição de marca). Para falar do supermercado da pessoa, escreva
  `{no_mercado}`: o GaaS troca por "no Amigão", "no Avenida", "no Boa", "no Paraná" ou "no seu supermercado".
- Nome da pessoa só como `%%=v(@FirstName)=%%` (ou `PRI_NOME`). Nunca no assunto.
- No texto, só `<b>` e `<br>`. Nada de HTML de layout: o segundo bloco vai como dados em `secondBlock`.
- Não preencha campos governados (links, UTM, assinatura, nota legal, rodapé, logo, cores, tamanhos,
  datas). O GaaS preenche e descarta o que vier no arquivo.
- A saudação da faixa de limite muda a cada e-mail da régua.
- Todo elemento visual é simétrico: grade com número par de itens, 2 ou 3 números em destaque, títulos de
  cartão com tamanhos parecidos.
- Sem travessão nos textos. Status do arquivo sempre "draft".

## Arquivos

- `references/produto.md`: ficha do produto, benefícios que podem ser citados e como.
- `references/escrita.md`: cada campo editorial, limites, faixa de limite, botões e conferência final.
- `references/blocos.md`: catálogo do segundo bloco com exemplos reais e regras visuais.
- `references/contrato.md`: o arquivo JSON campo a campo.
- `references/regua-v2-topo-de-funil-dinamico.md`: Plurix · V2 TOPO DE FUNIL DINÂMICO (4 e-mails, PLURIX V13 · topo dinâmico (header no briefing, limite e pool)). Estado atual no formato do contrato: `assets/reguas/v2-topo-de-funil-dinamico.json`.
- `assets/contrato.schema.json`, `assets/exemplo_input.json`: contrato e exemplo válido.
- `assets/previa/`: esqueletos do template real, um por e-mail e rede, usados por `montar_previa.py`.
- `scripts/content_blocks.py`: o mesmo gerador de blocos do GaaS (saída idêntica).
- `scripts/validar_input.py`, `scripts/montar_previa.py`: conferência e os dois quadros de prévia.