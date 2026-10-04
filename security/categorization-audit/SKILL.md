---
name: categorization-audit
description: Audit the fidelity of Eldritch Lich manuscript imports and automatically categorized data against a source text such as a PDF. Use when asked to verify or correct extracted characters, places, items, events, timelines, family trees, import/export fidelity, orphan references, automation histories, or category assignment in an Eldritch Lich project.
---

# Auditoria de categorização

Audite dados sem inventar fatos e sem aplicar correções automaticamente. Produza um relatório verificável; só altere dados ou código quando a solicitação também autorizar a correção.

## Antes de começar

1. Leia `references/schema-eldritch-lich.md` e `references/tipos-de-erro.md`.
2. Confirme o `projectId` e a fonte textual de referência.
3. Verifique se existe um dump completo do IndexedDB. O armazenamento principal é Dexie/IndexedDB no navegador; arquivos em `apps/web/src/db/*.json` são auxiliares e não contêm todo o estado.
4. Não trate o export legado de `EditorComponent.tsx` nem `/api/auth/export` como dump completo: eles não incluem as tabelas de universo, cronologia e automação.

## Evidências necessárias

Para uma auditoria completa, obtenha:

- dump filtrado pelo `projectId`, contendo ao menos `manuscripts`, `wikiEntities`, `characterSheets`, `familyRelations`, `factionSheets`, `locationSheets`, `creatureSheets`, `itemSheets`, `historicalEventSheets`, `timelines` e `timelineEvents`;
- texto-fonte, de preferência dividido em capítulos;
- nomes/IDs do projeto e, quando houver, o histórico `automationHistories`.

Se o dump completo não existir, informe isso claramente e proponha ou implemente, se autorizado, um export JSON de todas as tabelas relevantes. Não finja que uma leitura dos JSONs auxiliares equivale ao IndexedDB.

## Procedimento

1. **Importação.** Compare cada `manuscript.content` ao capítulo correspondente da fonte; diferencie perda de texto/formatação de erro de categorização.
2. **Entidades.** Verifique nome, tipo e campos-chave das tabelas de universo contra a fonte. Priorize falsos personagens, locais/facções trocados e objetos nomeados.
3. **Cronologia.** Valide datas, duplicatas e `sortOrder` de `timelineEvents` contra a ordem narrativa.
4. **Genealogia.** Valide `familyRelations`, direção e tipo da relação. Procure contradições e relações sem pessoas existentes.
5. **Integridade.** Para cada `*Id`, confirme que o registro referenciado existe na tabela adequada. Relate órfãos, mas não os delete sem autorização.
6. **Automação.** Use `automationHistories` para apontar a coleta de origem e a heurística que levou ao erro, quando disponível.

## Formato obrigatório do relatório

Organize por área e, em cada achado, registre: localização (`tabela` + `id` ou manuscrito + capítulo), evidência da fonte, problema, impacto e correção sugerida.

```md
## Importação/exportação
- [manuscript: Capítulo 3] Trecho ausente … Fonte: PDF p. 42. Sugestão: …

## Entidades
- [wikiEntities id=…] “…” foi classificado como …; a fonte o descreve como … Sugestão: …

## Cronologia
- [timelineEvents id=…] …

## Genealogia
- [familyRelations id=…] …

## Referências órfãs
- [itemSheets id=…] `ownerCharacterId=…` não existe em `characterSheets`.
```

## Limites

- Extraia somente relações explicitamente sustentadas pela fonte; suspeitas, sonhos e crenças não são fatos canônicos.
- Preserve autoria e dados existentes até a revisão/aprovação humana.
- Para o caso de referência atual, use o projeto “Senhor dos Anéis” de `zucchiryan07@gmail.com` e o PDF fornecido quando estiverem no escopo da solicitação.
