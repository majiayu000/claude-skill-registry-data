---
name: fdm-print-preflight
description: Use before delivering an FDM model or sliced project, or after changing geometry, orientation or supports, to check actual bed contact, elevated undersides, critical layers and the saved print artifact.
---

# Preflight de geometria, apoio e fatiamento

Detecte peças que parecem apoiadas, mas começam regiões no ar. Este check complementa a modelagem e o Bambu Studio; não opera a impressora e não promete eliminar todas as falhas físicas.

## 1. Inventário e triagem não destrutiva

- Preserve fontes e projetos. Liste todas as peças e plates entregáveis; registre nome/ID, cor/material, quantidade, dimensões, orientação, montagem e perfil. Use o **arquivo exportado na orientação de impressão**, com a mesma escala e transformação do projeto final.
- Não valide só o objeto ativo ou a imagem renderizada. Inspecione malha avaliada, espessuras, encaixes e detalhes. Reparos devem ocorrer em cópia; o diagnóstico não deve aplicar modifiers ou excluir faces.
- Confirme a justificativa de construção: função/material, espessuras locais e direção de carga, com [modelagem FDM](../blender-print-ready/references/design-for-fdm.md) quando necessário. Para relevos opcionais que criam vãos, considere uma construção apoiada antes de aceitar o custo/risco de suporte.
- Para STLs binários/ASCII, execute o helper Python 3 sem dependências externas:

```bash
python3 scripts/audit_stl.py pecas/*.stl --output preflight-geometria.json
```

O caminho `scripts/` é relativo à pasta desta skill. O helper assume **coordenadas numéricas em mm** e mesa `Z=0`; use `--unit-scale` e `--bed-z` explicitamente quando isso diferir. Não lê `.blend`/3MF nem suas transformações. Para um 3MF, exporte cópias por objeto com a transformação final, ou inspecione a geometria transformada com ferramentas disponíveis; não trate o STL de montagem como o STL do plate.

- Saídas: `0` = triagem sem achados, **ainda requer revisão de slice**; `2` = geometria bloqueada ou apoio precisa de revisão; `1` = erro de leitura/entrada. O JSON distingue `blocked`, `review_required` e `screen_pass`. O programa não corrige nem sobrescreve STLs.
- O relatório inclui dimensões, topologia por aresta, cascas e volume por casca, contato plano com a mesa, faces voltadas para baixo e seus intervalos de altura. Faces horizontais agrupadas por altura ajudam a achar plataformas suspensas; a soma de áreas não é uma medição de aderência.
- **Limites:** não testa auto-interseção, espessura, manifold por vértice, contenção exata de cascas, resistência, ponte ancorada, estabilidade, colisão entre objetos ou suporte efetivo. Faces inclinadas/curvas e tetos internos podem gerar achados legítimos para revisão. Uma casca negativa potencialmente interna exige conferir cavidade/orientação antes de reparar. “Suporte planejado” não fecha o achado até conferir o slice.

## 2. Resolver cada região que começa sem apoio

- Confira a vista inferior e cortes em cada altura sinalizada, incluindo rebaixos de fração de milímetro e overhangs altos. `Z mínimo = 0` não comprova apoio do resto da peça.
- Registre uma decisão por região: reorientar; redesenhar/dividir; suporte removível acessível; ou ponte com ancoragem/vão verificados e justificativa baseada no perfil/teste.
- Contato de ponto/linha, objetos inteiros suspensos, shells flutuantes e base penetrando a mesa precisam de correção ou explicação coerente no projeto. Não use uma porcentagem de contato como passe automático.
- Ao adicionar suporte, use as condições do material/perfil real; não copie automaticamente o preset da base de exemplo. Consulte [suportes e revisão de slice](references/support-and-slice-review.md).

## 3. Evidência no artefato final

1. Fatie cada plate novo/alterado com o perfil real. Confira os demais plates por comparação ao corrigir apenas um. Preserve agrupamento por cor quando solicitado.
2. Revise primeira camada **e cada início de plataforma/ilha/ponte**, antes/no início/depois. Veja se existe apoio exatamente onde precisa, com interface e separação coerentes. Suporte em outro objeto ou região não vale como evidência.
   Confira também fechamento sobre infill, espessuras sólidas em mm, detalhes XY e restrições de suporte/torre se houver camada variável. Resolva incompatibilidades com os [ajustes de processo](../bambu-h2c-slice-print/references/support-and-process-tuning.md).
3. Resolva avisos; não aprove por “sem warning”, `return_code=0`, malha manifold ou presença de algum suporte no G-code. Considere também erros de parsing/configuração.
4. Salve o 3MF de projeto versionado, reabra o arquivo que será entregue e confirme quantidades, orientação, filamentos e ajustes efetivos por objeto. Novo slice após qualquer edição; não reutilize G-code antigo. Se só entregar STL, declare que suportes e perfis não estão incluídos.
5. Registre evidência e pendências no [modelo de relatório](references/preflight-report.md). Marque **não verificado** quando uma ferramenta/perfil/check faltar, sem inventar sucesso. Pode entregar um rascunho com limites claros; não o chame de pronto para impressão.

Resumo ao usuário: arquivo, mudança, validação feita, suportes a remover e teste físico pendente/concluído. Um protótipo ou fatiamento conferido não comprova sucesso na impressora.
