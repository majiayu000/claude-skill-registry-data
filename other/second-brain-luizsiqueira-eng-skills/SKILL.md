---
name: second-brain
description: "Segundo cérebro do dia a dia em um vault Obsidian (markdown com wiki-links): tudo que você aprende trabalhando — investigações, debugs, decisões, reuniões, gotchas de sistemas e integrações, aprendizados — registrado com data e ligado por links. CONSULTAR antes de investigar, decidir ou responder ('o que já sabemos sobre X?') e ALIMENTAR ao fechar uma investigação, diagnóstico, decisão ou reunião. Na primeira execução cria o vault (estrutura, índice, templates) e oferece instalar o Obsidian. Invocar ao iniciar debug/investigação, ao encontrar comportamento estranho já visto, ao fechar um diagnóstico, ao tomar decisão de arquitetura, ou quando pedirem para 'registrar no cérebro', 'anotar isso', 'consultar o cérebro', 'o que já sabemos sobre X'."
---

# Second Brain — o que você aprende no dia a dia, sem se perder

Um vault Obsidian: markdown puro, wiki-links `[[Nome da nota]]`. Pode viver dentro de um
repositório (memória do time, versionada com o código) ou numa pasta sua (memória pessoal de
trabalho) — a skill funciona igual. **O agente lê e escreve os arquivos direto; o Obsidian é só
o visualizador** — grafo, busca e navegação. Sem Obsidian instalado, nada muda.

A tese: **tudo que custou esforço para descobrir entra com data** — uma investigação, um debug,
uma decisão, o que ficou combinado numa reunião, um comportamento estranho de sistema — para que
qualquer sessão futura (sua, de um colega ou do agente) recupere o contexto em minutos, não em
horas de re-investigação. É memória de trabalho, não documentação de projeto.

| Modo | Quando |
|---|---|
| **Setup** | não existe `.claude/second-brain.md` |
| **Consultar** | antes de investigar, debugar ou decidir |
| **Alimentar** | ao fechar investigação, diagnóstico, decisão ou reunião |

**Primeira coisa, sempre:** leia `.claude/second-brain.md`. Ele diz onde o vault está.

---

# Setup (primeira vez)

1. **Onde fica o vault.** Pergunte o uso: **do time** (dentro do repositório, versionado —
   sugira `./segundo-cerebro/`) ou **pessoal** (uma pasta sua, ex.: `~/segundo-cerebro/`,
   sincronizada como você preferir). Time com vários repos pode ter o vault num repo próprio e
   apontar para ele.
2. **Crie a estrutura** copiando os templates desta skill (pasta `templates/`):

   ```
   segundo-cerebro/
   ├── 00 Índice.md            ← mapa de tudo; ponto de entrada
   ├── Casos/                  ← investigações datadas (AAAA-MM-DD <resumo>.md)
   ├── Problemas conhecidos/   ← padrões de bug e comportamentos não óbvios
   ├── Decisões/               ← decisões de arquitetura e produto, com o porquê
   ├── Sistemas/               ← como cada sistema/módulo funciona de verdade
   ├── Integrações/            ← endpoints, gotchas, onde mora a credencial (nunca a credencial)
   ├── Reuniões/               ← o que ficou combinado, com quem, quando (opcional)
   └── .obsidian/app.json      ← `{}` basta; o Obsidian preenche o resto
   ```

   Pastas são sugestão — pergunte que outras fazem sentido (`Runbooks/`, `Aprendizados/`,
   `Pessoas/` para 1:1s, `Planejamento/`).
3. **Grave `.claude/second-brain.md`** e versione:

   ```markdown
   # Second brain
   - Vault: ./segundo-cerebro
   - Idioma das notas: pt-BR
   - Pastas: Casos, Problemas conhecidos, Decisões, Sistemas, Integrações, Reuniões
   - Fontes de verdade fora do vault: README e docs/ dos repos, ADRs em docs/adr/ (o vault aponta, não copia)
   ```
4. **Obsidian.** Verifique se está instalado (`ls /Applications/Obsidian.app`, `which obsidian`,
   `flatpak list | grep -i obsidian`). Se não estiver, **ofereça instalar e espere o sim** —
   instalar software é decisão da pessoa:

   | Sistema | Comando |
   |---|---|
   | macOS | `brew install --cask obsidian` |
   | Windows | `winget install Obsidian.Obsidian` |
   | Linux | `flatpak install flathub md.obsidian.Obsidian` ou `snap install obsidian --classic` |

   Depois abra o vault: macOS `open -a Obsidian "<caminho do vault>"`; qualquer sistema
   `obsidian://open?path=<caminho absoluto, URL-encoded>`. Na primeira abertura o Obsidian
   pede para confiar no vault — normal.
5. **Primeira nota útil na hora.** Um vault vazio morre. Pergunte: "qual foi a última coisa que
   custou horas para descobrir no seu trabalho?" e registre como o primeiro caso ou problema
   conhecido. Depois adicione a linha no índice.

---

# Consultar (antes de resolver)

Antes de investigar um comportamento, decidir algo ou responder "o que já sabemos sobre X":

1. Ler `00 Índice.md` e abrir as notas do tema.
2. Checar **`Problemas conhecidos/`** — o sintoma pode já ter diagnóstico pronto.
3. Checar **`Casos/`** — investigação passada parecida economiza horas (busque por sintoma,
   sistema, código de erro: `grep -ril "<termo>" segundo-cerebro/`).
4. Checar **`Decisões/`** antes de propor mudança de arquitetura — pode já ter sido decidido, e
   com motivo.
5. Só então ir para banco, logs e código.

Ao responder, **cite a nota** (`[[Nome]]`) que embasou — a pessoa precisa saber que aquilo veio
da memória do time e de quando. Se a nota estiver desatualizada em relação ao que você
descobriu agora, **corrija no mesmo turno** (ver Higiene).

O cérebro complementa a documentação, não a substitui: README e `docs/` dizem como o sistema
**deveria** funcionar; o cérebro guarda como ele **de fato** se comportou e o que se aprendeu.

---

# Alimentar (manter vivo)

Registrar **no final** de toda investigação, debug relevante, decisão ou reunião — não durante.

## Critério de entrada

Só entra o que ajuda no futuro: investigação ligada a card, cliente, incidente ou decisão;
acordo de reunião; aprendizado que você vai querer reencontrar. **Consulta rápida e curiosidade
não entram.** Se a curiosidade revelou um comportamento
genérico e reutilizável do sistema, registre só o comportamento na nota do tema, sem o caso.
Na dúvida, **pergunte** antes de criar a nota.

## Onde registrar

| O que aconteceu | Onde |
|---|---|
| Investigação relevante concluída (mesmo sem solução) | nota nova em `Casos/AAAA-MM-DD <resumo curto>.md` |
| Padrão de bug ou comportamento não óbvio confirmado | nota nova ou update em `Problemas conhecidos/` |
| Decisão de arquitetura/produto tomada | nota nova em `Decisões/AAAA-MM-DD <decisão>.md` com contexto, opções e o porquê |
| Detalhe novo de integração (endpoint, limite, gotcha, onde mora a credencial) | update na nota em `Integrações/` |
| Entendimento novo de como um sistema funciona | update em `Sistemas/` |
| Reunião com acordo, prazo ou decisão | nota em `Reuniões/AAAA-MM-DD <assunto>.md`: quem, o que ficou combinado, próximos passos |
| Aprendizado reutilizável (técnica, comando, atalho, lição) | nota em `Aprendizados/` ou update na nota do tema |
| Nota nova de qualquer tipo | **+ uma linha em `00 Índice.md`** |

Templates prontos em `templates/` (caso, problema, decisão, sistema/integração, reunião).

## Regras de escrita

- **Frontmatter** com `tags` e data: `data: AAAA-MM-DD` em casos e decisões, `atualizado:
  AAAA-MM-DD` nas notas vivas.
- **Wiki-links** `[[...]]` para as notas relacionadas — o valor do cérebro está no grafo. Nota
  sem link é nota perdida.
- **Fatos e datas, não prosa.** Enxuto, linguagem simples, sem adjetivo. O que foi observado,
  o que foi confirmado (e como), o que ficou em aberto.
- **Uma fonte de verdade por assunto.** Se a decisão vive em `docs/adr/`, a nota do vault
  aponta e resume — não duplica. Doc de projeto fica no projeto; o vault é síntese, ligação e
  memória de investigação. Nada de copiar ou symlinkar docs de repo para dentro do vault.
- **Nunca gravar segredo** (senha, token, chave, connection string). Registre **onde a
  credencial mora** (`secret manager X`, `.env do serviço Y`), nunca o valor.
- **Dado pessoal de cliente** (CPF, e-mail, telefone) só se for indispensável ao caso; prefira
  o id interno ou o número do card, que leva ao dado sem copiá-lo.

## Higiene

- Nota que se provou **errada**: corrigir na hora. Conhecimento venenoso custa mais que ausência.
- Consultou uma nota e descobriu algo que a contradiz: **atualizar no mesmo turno**, com a data.
- Caso que virou padrão recorrente: promova para `Problemas conhecidos/` e deixe o caso apontando.
- Uma vez por mês (ou ao fechar um projeto): passar o índice, arquivar o que morreu, ligar o
  que ficou solto.

---

## Checklist rápido

- [ ] `.claude/second-brain.md` lido; vault localizado
- [ ] **Antes** de investigar: índice, problemas conhecidos, casos e decisões consultados; nota citada na resposta
- [ ] **Depois**: passou no critério de entrada? Se sim, nota no lugar certo com frontmatter, data e wiki-links
- [ ] Nota nova → linha no `00 Índice.md`
- [ ] Nenhum segredo, nenhum dado pessoal desnecessário
- [ ] Nota desatualizada encontrada → corrigida no mesmo turno

## Adaptando ao seu time

| O que | Aqui | No seu time |
|---|---|---|
| Local do vault | `./segundo-cerebro/` (time) ou `~/segundo-cerebro/` (pessoal) | qualquer caminho em `.claude/second-brain.md` |
| Pastas | Casos, Problemas conhecidos, Decisões, Sistemas, Integrações, Reuniões | acrescente (Runbooks, Aprendizados, Pessoas…) e registre no índice |
| Idioma | pt-BR | o do time |
| Fontes de verdade externas | README, docs/, ADRs | wiki, Confluence, Notion — o vault aponta |
| Visualizador | Obsidian | qualquer editor de markdown; Logseq e Foam leem wiki-links também |
