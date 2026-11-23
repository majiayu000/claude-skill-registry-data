---
name: release-checklist
description: Checklist de liberação usado pelo Head de Qualidade para decidir o gate.
---

# Skill: release-checklist

- [ ] Todos os critérios de aceite da spec verificados com evidência
- [ ] Testes automatizados passam em ambiente limpo
- [ ] Nenhum defeito bloqueante aberto
- [ ] Nenhum achado de segurança alto aberto
- [ ] Nenhum segredo no repositório ou nos logs
- [ ] Pipeline e rollback revisados pelo Tech Lead
- [ ] README e documentação conferidos executando os passos
- [ ] Comunicação revisada pelo Head de Produto
- [ ] Risco residual documentado com responsável
- [ ] OK do humano para produção

Se algum item falhar, o veredito é `REJEITADO` com a lista dos itens pendentes.
