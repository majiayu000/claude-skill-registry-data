---
name: tarefa
description: Executa uma tarefa de desenvolvimento do HealthPrior seguindo o fluxo planejar, implementar, testar e verificar, ancorada nas histórias US-xx de docs/user-stories.md e nos componentes C-xx de docs/fluxo-sistema.md.
argument-hint: [US-xx, C-xx ou descrição da tarefa]
disable-model-invocation: true
---

Tarefa: $ARGUMENTS

Siga este fluxo, sem pular etapas:

1. **Contexto.** Leia a história em `docs/user-stories.md` (critérios de aceite, lado back/front, endpoint e contrato da §5) e, em `docs/fluxo-sistema.md`, o componente relacionado (C-xx), as invariantes (§9), as decisões (§10) e as questões abertas (§11). Se a tarefa não corresponde a nenhuma história/componente ou depende de uma questão aberta, pare e pergunte. Se for back, leia também `docs/arquitetura-backend.md` (camada certa e receitas da §6). Se for front, use os tipos gerados do OpenAPI; não invente campos.
2. **Plano.** Em até 8 linhas: o que muda, arquivos afetados, como testar. Se tocar mais de 3 arquivos ou mudar a ordenação, mostre o plano e espere OK.
3. **Implementação mínima.** Sem abstrações extras. No back, respeite a regra de dependência (domain puro; rotas sem regra de negócio). Respeite `AGENTS.md` (idioma, REF=2026-10-23, nada é apagado, CID e não flag).
4. **Teste.** Use casos reais do dataset (exemplos da §7 do fluxo). No back, rode `cd backend && pytest -q` (inclui o teste de arquitetura).
5. **Verificação.** Se a ordenação, a classe ou o status de pacientes podem ter mudado, gere o `fila_priorizada.csv` e rode `/verificar-fila`. Peça ao subagente `guardiao-invariantes` para revisar o diff.
6. **Fechamento.** Atualize docs se o comportamento mudou; registre decisão nova com `/registrar-decisao`; sugira a mensagem de commit no formato `tipo(US-xx): descrição`.

Responda ao final com: o que foi feito, como foi testado, resultado do verificador (se aplicável) e pendências.
