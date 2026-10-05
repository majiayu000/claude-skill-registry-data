---
name: specsfy-setup
description: Preparar, monitorar ou reconciliar o contexto persistente de um projeto Specsfy. Use ao iniciar o framework, antes e depois de mudanças na aplicação, ao verificar consistência documental, quando PROJECT.md ou os arquivos .specsfy/STACK.md, .specsfy/RULES.md e .specsfy/DATABASE.md estiverem ausentes, ou quando for necessário sugerir modelos coerentes com Laravel, Next.js, Astro ou um stack genérico. Pode ser executada repetidamente e deve preservar todo conteúdo já existente.
---

# Preparar contexto do projeto

1. Ler `AGENTS.md`, `CLAUDE.md` e instruções locais antes de escrever.
2. Ler [as diretrizes publicáveis](references/framework-instructions.md) quando
   precisar auditar o bloco reservado em arquivos de agentes.
3. Executar `python3 -B scripts/setup_context.py --project <raiz>`.
4. No início e no fim de cada mudança, executar:

```bash
python3 -B scripts/monitor_context.py --project <raiz> --check
```

5. Inspecionar os quatro arquivos e a evidência de stack usada pelo script.
6. Nunca substituir um arquivo de contexto existente, mesmo com conteúdo
   incompleto. Em `AGENTS.md` e `CLAUDE.md`, atualizar somente o bloco
   delimitado do framework e preservar tudo fora dele.
7. Para completar ou corrigir stack, regras ou dados, anunciar o handoff e
   carregar respectivamente `$specsfy-aux-stack`, `$specsfy-aux-rules` ou
   `$specsfy-aux-database`.
8. Quando aplicação ou persistência mudar, carregar `$specsfy-documentator`
   depois das auxiliares e reconstruir `docs/` a partir de todo o código.

Não contornar um resultado `PENDING`. Atualizar o documento indicado e executar
o monitor novamente. Para mudança de aplicação sem impacto material na história
ou finalidade, registrar essa avaliação na evidência da tarefa e repetir com
`--acknowledge-project-no-change`. Aplicar a mesma disciplina a regras com
`--acknowledge-rules-no-change`; nunca usar o reconhecimento para ocultar uma
mudança documental real.

Manter `PROJECT.md` na raiz. Manter `STACK.md`, `RULES.md` e `DATABASE.md` em
`.specsfy/`. Tratar esses documentos como contexto derivado do projeto, não como
spec, gate ou autorização de implementação.

Em projeto com mais de um framework, registrar todas as evidências observadas;
não escolher silenciosamente um único stack. Se nenhum framework for
identificado, criar o modelo genérico e declarar que a confirmação está
pendente.
