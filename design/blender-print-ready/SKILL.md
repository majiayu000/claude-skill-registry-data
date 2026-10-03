---
name: blender-print-ready
description: Use when creating, adjusting or exporting Blender models for FDM printing, especially separate assembly parts, supports, clearances and color-separated plates for a Bambu Lab H2C.
---

# Blender → peças para impressão FDM

Entregue a forma solicitada com dimensões, montagem e orientação de impressão verificáveis. **Manifold não significa imprimível; exportado não significa fatiado ou testado fisicamente.**

Ao definir uma peça nova ou rever sua construção, leia [decisões de projeto FDM](references/design-for-fdm.md): função/material antes da espessura, orientação da carga, fundo apoiado, resolução e cupons. Evite acrescentar rebaixos inferiores puramente ornamentais que criem plataformas suspensas. Preserve os necessários à função/aparência; compare reorientação, divisão e suporte quando o vão for necessário.

## 1. Preservar e identificar

- Descubra as ferramentas disponíveis; nomes de MCP, operadores e extensões variam. Se Blender/MCP estiver indisponível, use arquivos locais ou execução local disponível e informe o limite, sem inventar conexão.
- Salve uma cópia do `.blend` antes de mudanças em massa. Faça diagnósticos sem aplicar modifiers, recalcular normais, remover faces, preencher furos ou mover objetos na cena original. Reparos são uma etapa separada, em cópia, com comparação antes/depois.
- Liste **todas as peças entregáveis**, incluindo letras, tubos, flanges, pés e molduras. Não verifique somente `active_object`. Separe peças reais de cutters, câmeras e referências.
- Registre ID/nome, cor/material, quantidade, dimensões alvo, face de impressão, plate, montagem (cola/encaixe/parafuso), folgas e regiões críticas. Peças da mesma cor no mesmo plate quando couberem e isso for solicitado; se não couberem, use plates adicionais da mesma cor.
- Defina uso, carga/direção, flexão e calor esperados sem inventar requisitos. Justifique espessura por região: carcaça decorativa, fixação e presilha não pedem a mesma construção. Reforce localmente quando apropriado, verificando orientação e seção real; não use 100% de infill como substituto do desenho.

## 2. Unidades e montagem

- STL não declara unidade. Escolha e registre a convenção numérica antes de modelar. Para **1 BU = 1 mm numérico no STL**, use cena Metric, `scale_length=0.001`, `length_unit='MILLIMETERS'`, exportação sem conversão de unidade e escala global 1. Mudar a unidade da cena não redimensiona vértices existentes.
- Confirme escala com uma medida conhecida no Blender **e no arquivo reimportado/slicer**. Para outra convenção, faça uma única conversão explícita. A grade visual não prova milímetros.
- Use o perfil H2C instalado e o modo/bico selecionado para limites úteis e áreas excluídas. O tamanho nominal da placa não é a área imprimível por qualquer bico. Inclua brim, suporte e torre no espaço necessário.
- Mantenha cena de montagem e layout de impressão em cópias/coleções distintas. Rotacionar uma peça para imprimir não deve alterar sua posição na montagem de referência.
- Defina folga **radial ou diametral** e superfícies de contato. Meça encaixes críticos com cupom no mesmo material, orientação e perfil; não trate uma tolerância única como garantia. Não invente encaixes se o projeto é para colagem.

## 3. Modelar e reparar com propósito

- Boolean Union une volumes; Join só agrupa malhas. Use Boolean Exact quando apropriado, inspecione o resultado e evite contato apenas por linha/ponto. Nenhum solver garante por si só uma malha correta.
- Escala não uniforme muda Solidify/Bevel. Aplique transformações/modifiers na **cópia de exportação** quando necessário. Inspecione paredes após Boolean, Bevel, Solidify e Remesh.
- Não remova automaticamente faces interiores, preencha todos os furos ou faça remesh indiscriminado: isso pode destruir cavidades, detalhes e folgas. Compare dimensões e componentes após cada reparo.
- Paredes e traços dependem de largura de linha, material, função e gerador de paredes. Com bico 0,4 mm, duas linhas próximas de 0,45 mm dão um ponto de partida de 0,9 mm; confirme trajetórias no preview. Não afirme que qualquer detalhe abaixo de um número fixo some ou que qualquer parede acima dele é resistente.
- Para bordas voltadas à mesa, avalie chanfro em vez de fillet quando reduzir overhang. Considere carga entre camadas, acabamento, acesso para retirar suporte e superfícies de colagem.
- Ângulos e comprimentos de ponte são hipóteses para teste, não limites universais. Declare se o ângulo é medido da horizontal ou da vertical; o threshold do slicer pode usar outra convenção.

## 4. Checar a geometria avaliada e a parte de baixo

Inspecione cada peça **com modifiers e transformações efetivos, na orientação de impressão**:

1. Dimensões em mm, normais, faces degeneradas/duplicadas, bordas abertas/non-manifold, auto-interseções e componentes separados. Volume positivo isoladamente não prova validade; uma casca invertida pode ficar escondida no volume total.
2. Espessuras, texto e encaixes críticos. Use recursos presentes na versão do Blender/3D Print Toolbox, consultando a API instalada. Se um check não foi executado, marque **não verificado**, sem preencher “passou”.
3. `Z mínimo`, área real de contato e estabilidade. **Z mínimo = 0 só prova que algum ponto toca a mesa.** Pés, ressaltos e bordas podem deixar o resto elevado.
4. Vista inferior e cortes perto da mesa: liste a altura onde cada plataforma, moldura, teto de cavidade ou nova ilha começa. Inspecione também regiões internas e overhangs altos.
5. Para cada região suspensa: reorientar, redesenhar/dividir ou planejar suporte removível. Uma ponte só é aceita com ancoragem, vão medido e evidência de capacidade no perfil usado. Brim ajuda aderência; não preenche o vão de uma base elevada.

Para uma triagem repetível dos STLs exportados, use [fdm-print-preflight](../fdm-print-preflight/SKILL.md). Seu script **não modifica** arquivos e não mede espessura, auto-interseção, resistência ou capacidade de bridging.

## 5. Exportar e validar o que será entregue

- Preserve uma peça por arquivo/objeto independente para montagem separada. Cor é atributo, não uma obrigação de fundir todas as peças cinzas em uma casca.
- Para impressão multicolorida montada, preserve as transformações relativas das partes e atribua filamento por parte. Para peças independentes, mantenha cada uma apoiada e identificável no plate. Origens iguais por si só não garantem alinhamento; compare coordenadas efetivas.
- Confira o operador e parâmetros de exportação disponíveis. Exemplo para Blender com `bpy.ops.wm.stl_export`, na convenção numérica de mm acima, com **somente a cópia de exportação selecionada**:

```python
bpy.ops.wm.stl_export(
    filepath=destino, export_selected_objects=True, apply_modifiers=True,
    global_scale=1.0, use_scene_unit=False,
    forward_axis='Y', up_axis='Z', ascii_format=False,
)
```

- Reimporte o arquivo ou leia suas dimensões; compare quantidade, geometria e unidades com o manifesto. Um 3MF de geometria não equivale a um projeto Bambu com suportes, filamentos e plates configurados.
- Confirme o modo de avaliação da exportação (viewport/render), visibilidade e níveis de modifiers. Um STL pode diferir da malha visualizada; consulte versão do exportador/extensão e reimporte a entrega.
- Para uma entrega apenas de modelo/STL, execute a etapa de geometria do [fdm-print-preflight](../fdm-print-preflight/SKILL.md) e registre os limites; validação geométrica permite encaminhar ao fatiamento, não aprovar a impressão. Quando a entrega incluir fatiamento/projeto de impressão, faça também a conferência no [Bambu Studio](../bambu-h2c-slice-print/SKILL.md). Se essas skills não estiverem instaladas, abra os caminhos relativos neste repositório; se faltarem recursos necessários à etapa solicitada, registre a validação pendente.
- Entregue os formatos solicitados, preservando a fonte editável disponível e um registro das verificações. `.blend`, STLs e 3MF de projeto têm funções diferentes; não exija todos numa entrega simples de geometria. Informe o que foi modelado, verificado digitalmente, fatiado e efetivamente testado em uma impressão.

## Fontes

- [Blender: unidades](https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html#units), [STL](https://docs.blender.org/manual/en/latest/files/import_export/stl.html), [Boolean](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html), [Solidify](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/solidify.html).
- [Blender: dependency graph e malha avaliada](https://docs.blender.org/api/current/bpy.types.Depsgraph.html), [3D Print Toolbox](https://extensions.blender.org/add-ons/print3d-toolbox/).
- [Prusa: modelagem, orientação, tolerâncias e suportes](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135).
