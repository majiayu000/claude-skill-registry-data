---
name: bambu-h2c-slice-print
description: Use when preparing, slicing or validating a Bambu Studio project for the H2C, including per-object supports, color-separated plates and AMS/nozzle mapping, or operating a print the user has authorized.
---

# Bambu Studio + H2C

Fluxo: **preservar projeto → confirmar modelo/perfis → orientar e apoiar cada peça → fatiar → revisar camadas críticas → salvar e reabrir a entrega**. Envio, retomada, cancelamento e monitoramento da impressora só entram no fluxo quando autorizados pelo usuário; preparar um modelo não autoriza imprimir. Respeite autorizações já dadas, sem pedir confirmação novamente.

Leia apenas o guia relevante à decisão: [materiais, H2C e calibração](references/materials-and-h2c.md) para escolher filamento/hotend ou investigar extrusão; [suportes e ajustes de processo](references/support-and-process-tuning.md) para interfaces, camadas, paredes e defeitos de acabamento. As referências distinguem documentação, ensaio e relato comunitário; receitas de outro material/equipamento não são presets H2C validados.

## 1. Perfil real, sem presumir hardware

- Descubra as ferramentas e a versão do Studio instaladas. Use um perfil **H2C**, sem substituir silenciosamente por H2D/Orca. Registre máquina, bico/diâmetro/fluxo, rack Vortek, placa, filamentos e processo efetivos.
- H2C tem bico esquerdo e sistema de troca Vortek à direita. Área útil, compatibilidade por bico, alimentação de TPU e recursos dependem do modo/perfil/firmware. Leia o perfil instalado e a documentação atual antes de atribuir material a um bico. Não codifique uma regra universal “TPU sempre à direita” ou um volume antigo.
- Confirme áreas exclusivas de cada bico, volume comum, regiões excluídas e altura. Suporte, brim e torre também precisam caber. O envelope total dos dois bicos não é acessível por ambos individualmente.
- Use presets compatíveis existentes. Temperatura, ventilação/porta, secagem, cola e remoção da peça dependem do filamento **e da placa exatos**; consulte suas instruções. Não aplique uma tabela genérica de temperatura ou secagem a todos os produtos.
- Calibre fluxo/dinâmica quando os sintomas ou uma mudança de material/bico justificarem. Não altere vários parâmetros para encobrir uma plataforma começando no ar.
- Registre fabricante/variante, não apenas cor ou nome do preset. Distinga Flow Rate, Flow Dynamics/K e limite volumétrico; use a calibração suportada pela H2C instalada e salve o contexto. Escolha espessuras/material por função antes de afinar velocidade.

## 2. Importar sem perder a intenção

- Salve a configuração aberta antes de substituí-la. Trabalhe em uma nova versão, preservando original, IDs, quantidades, dimensões, cores e montagem.
- Abra 3MF Bambu **como projeto** para carregar configurações; importar só geometria/STL perde suportes e outros ajustes de processo. Confira no projeto aberto que os ajustes pretendidos realmente foram carregados.
- “Single object with multiple parts”: **Yes** quando as partes devem manter posição para impressão montada; **No** para peças independentes. Split to Objects pode mover cascas à mesa; Split to Parts preserva relações. Reconfira após qualquer split.
- Lay on Face, Auto Orient, Arrange, Cut, Fix Model e Boolean podem mudar geometria ou layout. Use só quando necessário, em cópia, e repita o preflight depois. Não reorganize ou gire automaticamente um projeto já disposto e validado.
- Agrupe peças por cor/material nos plates conforme o pedido. Cor visual do objeto não prova o preset do filamento; PLA cinza e PETG cinza não são intercambiáveis. Preserve folgas para suporte/brim e a ordem de impressão.

## 3. Apoio efetivo por objeto

Use [fdm-print-preflight](../fdm-print-preflight/SKILL.md) para conferir a parte de baixo de **todas** as peças. Leia [suportes e camadas críticas](../fdm-print-preflight/references/support-and-slice-review.md) ao encontrar pés, cavidades, bordas elevadas, pontes, tubos ou avisos de cantilever.

- Inspecione a configuração **efetiva**: Global, Object, Part/Modifier e pinturas de suporte podem divergir. Um checkbox global ou `enable_support=1` não prova que apareceu apoio sob a face necessária.
- Decida por região: orientação, redesenho/divisão ou suporte. Base de contato pequena pode precisar de brim; brim não substitui suporte. Um teto plano grande perto da mesa pode exigir suporte normal, mesmo que o slicer o classifique como ponte e não mostre aviso.
- Se o vão só existe por um ornamento opcional, avalie removê-lo/movê-lo no desenho antes de adicionar suporte. Para vãos necessários, compare Normal/Hybrid em faces amplas e Tree/Hybrid em regiões pequenas, com acesso de retirada. Não imponha o mesmo tipo a todas as peças.
- Confira tipo/estilo, restrição “on build plate only”, blockers/enforcers, “don't support bridges”, ângulo, espaçamento, interface, distância superior/inferior e filamento. “Só na mesa” é adequado apenas quando o apoio consegue chegar à região; cavidades podem exigir outra solução.
- Com o **mesmo material**, use a separação recomendada pelo perfil, ajustada às camadas e verificada no preview. `0,20 mm` de distância superior e 3 camadas de interface foram usados no caso da base em PLA; **não são preset universal**.
- Distância zero pode ser apropriada para pares de interface compatíveis seguindo o fabricante. Outro bico ou outra cor por si só não tornam materiais separáveis. Confira acesso para retirada e não prometa “superfície perfeita”.
- Não force material/bico extra para um projeto de uma cor. Suporte com o mesmo PLA pode ser suficiente. Se houver material de interface, confirme disponibilidade, compatibilidade e agrupamento; menor purga não significa ausência de priming, torre ou desperdício.

## 4. Fatiar e revisar as camadas certas

Para **cada plate entregue**, confirme:

1. Objetos, dimensões, posições, materiais, perfil, regiões de exclusão e colisões (inclusive brim/suportes; impressão por objeto requer espaço do cabeçote).
2. Primeira camada: trajetória e área de contato de cada peça, não apenas sua caixa delimitadora.
3. Camadas imediatamente **antes, no início e depois** de cada plataforma/ilha/ponte/rebaixo listado no preflight. Uma falha a 2 mm pode ocorrer depois das primeiras cinco camadas; altura variável impede presumir um número fixo de camada.
4. Suporte visível exatamente sob a região necessária, alcançando a interface com separação coerente; pontes com ancoragem. Somente contar linhas “Support” no G-code não prova localização ou cobertura.
5. Paredes, letras, tubos e detalhes presentes no preview; overhangs resolvidos ou justificados; tempo, gramas, trocas e uso de filamentos plausíveis.
6. Avisos e reparos interpretados. **Zero avisos ou código de saída 0 não substituem essa revisão.** Leia também falhas de parsing, perfis incompatíveis e mensagens de ferramenta desconhecida. Não entregue G-code de uma execução com erros sem entender sua relevância.

Salve um **3MF de projeto versionado**, reabra esse arquivo e confira os ajustes por objeto. Faça novo slice após qualquer mudança; não reutilize preview/G-code antigo. Se estiver corrigindo um plate, revalide os plates alterados e comprove que os demais foram preservados. Para uma entrega nova, revise todos.

Se usar altura variável, confira espessura sólida em mm, compatibilidade do suporte e perfis de altura dos objetos/torre. Verifique a combinação na versão instalada; não desative a torre para contornar uma incompatibilidade. Confira detalhes com o gerador de paredes escolhido e evite compensações dimensionais duplicadas no CAD e no slicer.

## 5. CLI local (somente fatiamento)

Consulte `--help` da versão instalada e a [CLI oficial](https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage). Use o projeto com seus próprios perfis quando disponíveis. Exemplo de correção do plate 2 **preservando layout e orientação**:

```bash
bambu-studio --slice 2 --arrange 0 \
  --export-3mf verificacao.3mf --outputdir ./verificacao projeto.3mf
```

O exemplo omite `--orient`: a CLI oficial documenta uma flag independente, e a ajuda local pode ter descrição ambígua. Não acrescente um `0` presumindo que toda versão aceita esse argumento; confirme a sintaxe e compare as transformações do resultado. `--slice 0` fatia todos os plates nas versões que documentam esse comportamento. Não use `--allow-newer-file`, auto-orientação ou perfis substitutos para suprimir incompatibilidades sem investigação. Quando carregar JSONs externos, resolva `inherits` e confira a configuração resultante: flags/arquivos externos podem sobrescrever o 3MF. `--load-filaments` aceita uma lista separada por `;` na CLI oficial; não presuma que Bambu e Orca compartilham todas as flags.

Mantenha logs e resultado de validação separados da entrega. Se CLI, perfil ou GUI não estiverem disponíveis, entregue o que foi possível verificar e marque **fatiamento pendente**, sem declarar pronto para imprimir.

## 6. Impressão e acompanhamento, se autorizados

- Descubra MCP/CLI presentes; não instale um servidor comunitário nem ative Developer/LAN Mode sem necessidade e autorização. Não grave access code, IP privado ou tokens em relatórios públicos.
- Antes do envio autorizado: estado da impressora, mesa livre, placa física e perfil, material real/preset, AMS/spool externo, bico/rack, calibrações disponíveis e arquivo correto. Não presuma limpeza, secagem ou mesa livre sem evidência. Mantenha detecção de falhas ligada.
- Acompanhe a primeira camada **e as transições críticas identificadas**, dentro da capacidade de acompanhamento autorizada. Cinco camadas bem-sucedidas não validam a peça inteira; não prometa vigilância contínua sem mecanismo ativo.
- Siga [bambu-print-troubleshoot](../bambu-print-troubleshoot/SKILL.md) se houver falha. Pausa preventiva só dentro de operação/monitoramento autorizado. Recomeçar um trabalho antigo não aplica a correção feita no arquivo novo.
- Informe arquivo/versionamento, plate, orientação, suporte removível ou não, material, estimativa, verificações realizadas e teste físico pendente/concluído. Registre detalhes no relatório; resuma para o usuário sem despejar todos os parâmetros.

## Fontes

- [H2C: manual oficial](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf), [Bambu: H2C e Vortek](https://blog.bambulab.com/bambu-lab-h2c-where-multi-material-vortek-system-meets-engineering-precision/).
- [Bambu Studio: suporte](https://wiki.bambulab.com/en/software/bambu-studio/support), [pintura](https://wiki.bambulab.com/en/software/bambu-studio/support-painting), [agrupamento por bico](https://wiki.bambulab.com/en/software/bambu-studio/manual/dual-nozzles-slicing-filament-grouping), [mapeamento](https://wiki.bambulab.com/en/software/bambu-studio/filament-mapping-principle).
- [Placas](https://wiki.bambulab.com/en/filament-acc/acc/plates), [materiais](https://wiki.bambulab.com/en/general/filament-guide-material-table), [CLI](https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage).
