---
name: bambu-print-troubleshoot
description: Use when a Bambu H2C print fails, spaghetti or floating-cantilever warnings appear, an HMS code is reported, or a printed part has adhesion, extrusion, dimensional or support defects.
---

# Diagnosticar antes de mudar parâmetros

Fluxo: **evidência → objeto/camada → hipótese testável → correção mínima → novo slice → validação**. Siga a autorização da sessão para operar a máquina; pedir diagnóstico ou corrigir um arquivo não autoriza iniciar, retomar ou cancelar um print. Pausa preventiva cabe em operação/monitoramento já autorizado. Não repita pedidos de autorização já concedida.

## 1. Localizar a falha real

- Reúna o arquivo **que foi impresso**, plate e peça, material/preset, placa, versão/perfis, altura/camada/tempo e código HMS completo. Leia arquivos/fotos disponíveis antes de pedir informações repetidas.
- Distinga **foto real**, liveview, render e a imagem genérica “Example Photo” de um alerta. Um recorte do layout identifica uma peça, mas não mostra sua aderência durante a impressão.
- Leia o código completo na [wiki HMS](https://wiki.bambulab.com/en/hms/home), considerando modelo e firmware. Prefixo/código parcial não identifica sozinho a causa. Se a fonte não estiver disponível, explique o que foi inferido do texto do alerta e da evidência, sem inventar tradução de código.
- “Spaghetti” descreve filamento solto. Pode resultar de desprendimento, suporte quebrado, colisão **ou uma superfície que começa no ar**. Não conclua automaticamente “filamento úmido” ou “mesa suja”.

## 2. Primeiro descarte geometria sem apoio

Se a falha está concentrada numa base, pé, moldura, tubo, teto ou já se repetiu no mesmo local, inspecione o modelo **agora**, antes de recomendar outra impressão:

1. Identifique a peça na orientação efetiva do plate. Meça contato com a mesa e superfícies inferiores elevadas, usando [fdm-print-preflight](../fdm-print-preflight/SKILL.md).
2. Encontre a altura onde começou a região problemática e compare com a foto/relato. `Z mínimo = 0`, “Lay on Face”, uma casca manifold e ausência de warning não eliminam esse risco.
3. Confira overrides por objeto, blockers, suporte só na mesa e “don't support bridges”. Refaça o slice e veja o apoio **sob a face**, antes/no início/depois da transição.
4. Se há uma plataforma grande sobre pés sem apoio, escolha reorientação, redesenho/divisão ou suporte removível. Brim não resolve impressão no ar. Veja o [caso de regressão da base com pés](../fdm-print-preflight/references/support-and-slice-review.md#caso-de-regressão-base-com-pés).

Quando o relevo inferior for apenas decorativo e opcional, compare uma base plana ou pés separados antes de tentar aperfeiçoar o suporte. Não preencha encaixes ou cavidades funcionais. Para essa decisão, use [modelagem FDM](../blender-print-ready/references/design-for-fdm.md).

Separe **fato encontrado** (“vão de 2 mm sem suporte no arquivo”) de **causa provável** (“compatível com o espaguete na base”). Foto isolada pode não mostrar se a peça se soltou primeiro.

## 3. Outras hipóteses e evidências

| Sintoma | O que distinguir antes de ajustar | Correção orientada pela evidência |
|---|---|---|
| Desprendimento/warping | Peça deslocou? canto levantou? contato real pequeno? placa/perfil corretos? | Limpeza conforme fabricante, nivelamento, brim/orelhas ou orientação; temperatura/ambiente apenas se necessário |
| Stringing/estalos/bolhas | Umidade, vazamento, retração, temperatura ou extrusão sem apoio | Secagem conforme produto/equipamento; teste de temperatura/retração se justificado, não todos juntos |
| Falta de extrusão | Caminho do filamento, hotend/nozzle correto, entupimento, limite volumétrico | Inspeção/calibração apropriada; não encobrir com aumento indiscriminado de flow |
| Ponte/overhang caído | Vão e ancoragem, suporte/interface, direção e trajetória da ponte | Reorientar, apoiar ou testar bridge speed/flow/cooling. Não prescrever sempre aumentar bridge flow |
| Parede/letra ausente | Trajetória já falta no preview ou falha só na peça real? | Geometria/largura de linha se falta no slice; fluxo/adesão se a trajetória existe |
| Furo/encaixe errado | Medida projetada, importada e impressa; seam, orientação, contração | Cupom e compensação definida como radial/diametral; não ativar opções de precisão sem diagnóstico |
| Layer shift | Colisão, canto/suporte levantado, placa solta, mecânica | Resolver o obstáculo ou mecânica; velocidade só se a evidência indicar |
| Topo aberto/peça fraca | Espessura de topo, infill, paredes, orientação da carga, material | Ajuste estrutural localizado, confirmado no preview e em teste adequado |
| Hotend/AMS incompatível | Perfil versus rack/bico/material/slot reais | Corrigir mapeamento; nunca ignorar mismatch ou trocar o modelo de impressora para passar |

Não use uma recomendação universal de cola, porta aberta, secagem ou temperatura: consulte o filamento e a placa específicos. Não desative detecção de espaguete para permitir a continuação de uma falha.

Para suporte preso, interface que se solta, detalhes omitidos, colisões com infill ou problemas em camada variável, siga [ajustes por sintoma](../bambu-h2c-slice-print/references/support-and-process-tuning.md). Para fluxo, cooling, secagem e compatibilidade, leia [materiais/H2C](../bambu-h2c-slice-print/references/materials-and-h2c.md). Relatos comunitários geram hipóteses; confirme produto, versão e geometria antes de copiar parâmetros.

## 4. Aplicar e provar a correção

- Preserve original e configuração atual; salve nova versão. Faça a menor mudança coerente com a hipótese. Uma estratégia de suporte pode exigir vários parâmetros relacionados: registre-os como uma correção, em vez de mudar também temperatura, velocidade e fluxo sem evidência.
- Reavalie **todas as peças afetadas** e os parâmetros efetivos. Siga [bambu-h2c-slice-print](../bambu-h2c-slice-print/SKILL.md) para revisar as camadas críticas e reabrir a entrega. Não reimprima o mesmo arquivo que falhou esperando que o novo projeto tenha efeito nele.
- Quando necessário, proponha um teste que preserve vão, pés, orientação, material e suporte da região defeituosa. Um cubo genérico, ou um recorte que encurta a ponte, não valida uma base suspensa. Não inicie o teste sem autorização de impressão.
- Se a causa continuar incerta, peça a informação discriminante (por exemplo, se a peça se soltou antes ou depois de o material embolar) enquanto conclui a inspeção independente possível. Não mude várias causas candidatas ao mesmo tempo.
- Registre peça/plate, evidência, hipótese, antes→depois, arquivo final, slice, localização do suporte e resultado físico. “Corrigido no arquivo”, “fatiamento conferido” e “impressão física passou” são estados diferentes.

## Fontes

- [Bambu: HMS](https://wiki.bambulab.com/en/hms/home), [detecção H2](https://wiki.bambulab.com/en/h2/manual/intelligent-detection).
- [Suporte no Studio](https://wiki.bambulab.com/en/software/bambu-studio/support), [bridging](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/bridging).
- [Placas](https://wiki.bambulab.com/en/filament-acc/acc/plates), [secagem](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament).
