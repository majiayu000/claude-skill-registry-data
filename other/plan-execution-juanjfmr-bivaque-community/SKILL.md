---
name: plan-execution
description: >
  Execute a written plan (a launch phase, a card checklist or a plan file) todo by todo,
  gating between each one, with a stop rule when a todo is wrong or impossible. Use when
  running a phase of docs/LANCAMENTO.md, when pointed at a plan, or asked to "seguir o plano".
---

# plan-execution

O plano é **contrato**, não sugestão. Ele foi escrito com contexto que você não tem.

**Antes de executar, leia `docs/LANCAMENTO.md`**: a fase do plano, o que a fecha e os
critérios de pronto de uma jornada. Plano que contradiz esse arquivo está errado.

## O laço

Para cada todo, nesta ordem:

1. Leia o todo inteiro antes de tocar em qualquer arquivo.
2. **Implementação e teste são um todo só.** Nada fecha sem prova na mesma unidade.
3. Entre cada todo, `gate --fast` e os testes que o todo tocou; o gate completo roda uma vez no
   fechamento do lote (skill `gate-before-done`). Vermelho **para** a execução.
4. Um commit por todo, convencional (`feat/fix/chore(escopo): …`), com o escopo que o plano indica.

## Pare e diga — não improvise

- O todo está errado, ambíguo ou impossível → **pare**. Plano errado é informação.
- O todo pede sair da fronteira de confiança (RLS, dado pessoal, migration destrutiva)
  sem ADR aprovado → pare.
- O baseline do todo não reproduz → pare: o plano descreve outro estado do mundo.

Improvisar em fronteira de confiança é como este repositório produziu quatro vazamentos.

## Serial no banco

Frentes podem correr em paralelo em código, mas são **seriais no banco**, por dois motivos que não estão
no código: banco local único (cada onda precisa de `db:reset` exclusivo) e loop visual único
(a captura insere perfil no banco e quebra o pgTAP de outra onda). Termine, feche, comece a próxima.

## O que fecha uma fase

Os seis critérios de pronto de `docs/LANCAMENTO.md` em cada jornada que ela tocou, incluindo a
captura em 375/768/1440 nos dois temas e a revisão às cegas contra a régua. Não existe rodada de
auditoria "no fim".

## Onde a verdade mora

- O que o produto **deve** ser: `docs/LANCAMENTO.md` e os ADRs aceitos.
- O que o código **faz** hoje: código, migrations, testes e o quadro — nunca um texto.
- Nunca infira um do outro. Ler decisão como feature entregue é o erro mais caro deste
  repositório.
- Uma jornada só fecha quando a pessoa **fecha o ciclo** — entrada, ação, feedback, retorno e
  o caminho triste principal. Capacidade no banco não fecha jornada.
