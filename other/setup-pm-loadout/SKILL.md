---
name: setup-pm-loadout
description: Use no primeiro uso do PM Loadout em um workspace para configurar fontes canônicas, conectores autorizados e política de persistência.
invocation: user
inputs: estado do repositório e preferências do workspace
outputs: proposta de configuração e, após confirmação, arquivo local de configuração
side_effects: write-confirmed
context: services/skill-contract.md, config/pm-loadout.example.yaml
completion: fontes canônicas, permissões de escrita e integrações em uso estão explícitas e confirmadas
---

# Setup PM Loadout

Configure o PM Loadout uma vez por workspace. Esta skill não conecta serviços nem grava configurações sem confirmação explícita.

## Processo

1. Inspecione o repositório: `AGENTS.md`, `knowledge/`, skills instaladas, conectores disponíveis e qualquer `config/pm-loadout.local.yaml` existente.
2. Mostre o que já está definido e o que falta, sem presumir que ClickUp, banco de dados ou context pack estão disponíveis.
3. Resolva, nesta ordem: idioma, fontes canônicas de contexto, destinos permitidos para persistência, integrações autorizadas e política de escrita.
4. Recomende os valores conservadores do template e faça apenas perguntas que alterem uma decisão de configuração.
5. Após a confirmação, copie o template para `config/pm-loadout.local.yaml`, aplique somente os valores aprovados e confirme o caminho criado.

## Regras

- Não armazene segredos, tokens, PII ou conteúdo de cards no arquivo.
- Conector disponível não é autorização para escrita: respeite `write-confirmed`.
- Se uma integração não existe, mantenha-a desabilitada e entregue artefatos na conversa.
- Reexecutar a skill atualiza a configuração existente; preserve campos não relacionados.
