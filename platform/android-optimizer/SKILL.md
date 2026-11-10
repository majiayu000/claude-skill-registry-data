---
name: android-optimizer
description: Guia passo a passo para otimizar qualquer celular ou tablet Android conectado por USB com ADB e Fastboot, sempre perguntando antes até onde a pessoa quer ir, desde ajustes reversíveis e remoção de apps até desbloqueio do bootloader, troca de ROM, root, modo desempenho e overclock. Também melhora a câmera (varredura do hardware, app de câmera, vídeo, filtros, recursos ocultos e foto noturna) e instala um emulador de PlayStation 1 com o jogo da pessoa. Use sempre que alguém pedir para deixar um Android mais rápido, tirar travamentos, limpar bloatware, trocar ou atualizar o sistema, instalar LineageOS, TWRP, root ou overclock, reaproveitar um celular antigo próprio, melhorar a câmera, a foto noturna ou o vídeo, pôr filtros, ou instalar emulador de PS1, mesmo sem citar ADB. Use também para "my Android phone is slow", "debloat", "custom ROM", "improve Android camera" e "PS1 emulator on Android". Não serve para iPhone.
---

# Android Optimizer

Conduza a otimização de um aparelho Android pela sequência abaixo. A pessoa pode não ser técnica, e o aparelho é dela: ela decide o nível de risco, e você mede, explica e executa com cuidado. Responda no idioma dela e explique termos técnicos em uma frase.

## Princípios

- **Pergunte antes de agir.** O aparelho não pode ser alterado antes da entrevista do passo 1, porque o que é "otimizar" muda muito de uma pessoa para outra.
- **Cada autorização vale só para o que foi descrito.** "Faça tudo" autoriza o trabalho dentro do nível escolhido. Apagar dados, desbloquear o bootloader e gravar partições continuam exigindo uma confirmação específica, feita depois de explicar o efeito daquele passo.
- **Meça e guarde o que dá para desfazer.** Registre os valores anteriores antes de mudar. Mantenha uma mudança só se a medição não piorar. Muita dica popular não ajuda: no caso que originou esta skill, `ro.config.low_ram` piorou o resultado.
- **Só diga o que verificou.** Separe o que foi medido do que é suposição. Prometer velocidade que o hardware não entrega só gera frustração.
- **Nunca mire no aparelho errado.** Use sempre `-s <serial>`, porque outro aparelho pode aparecer no USB a qualquer momento.

## Limites: verifique antes de tudo

Este é o primeiro filtro, antes da entrevista.

Não ajude a contornar proteção de aparelho alheio ou possivelmente roubado: bloqueio de tela, FRP (a trava da conta Google), MDM de empresa, bloqueio de operadora, IMEI ou rastreamento. Formatar, desbloquear ou instalar outra ROM para usar um aparelho assim é o mesmo contorno, mesmo que o pedido seja só "reaproveitar" ou "trocar o sistema".

Se a pessoa disser que achou o aparelho, ou se houver sinais claros de que é de outra pessoa e ela não tem autorização, pare: não entreviste nem execute comandos. Explique o motivo sem acusar e sugira como devolver, como uma delegacia, achados e perdidos, a operadora ou a loja. Se a tela mostrar contato do dono, use esse contato. A conta conectada pode ajudar o dono a localizar o aparelho.

Para quem é dono e esqueceu a senha, indique só os caminhos oficiais do fabricante, deixando claro que costumam apagar os dados. Para um aparelho comprado usado ou recebido de presente que ainda tenha a conta de outra pessoa, oriente a pedir ao antigo dono que remova a conta, ou a procurar o fabricante com o comprovante de compra.

Você não tem como provar quem é o dono. Acredite na pessoa, a menos que haja sinais em contrário, como uma tela de aparelho perdido ou uma trava de conta que ela não consiga abrir.

Recuperar arquivos apagados ou acessar dados só é aceitável com o dono ou com autorização dele. Se, durante o trabalho, aparecer uma conta diferente no aparelho, pergunte uma vez de quem é. Nunca entre em contas online da pessoa.

**Jogos e BIOS:** para o emulador, use só o arquivo que a pessoa fornecer. Não baixe jogos nem BIOS, e não indique sites para isso. Se ela não tiver o arquivo, explique as opções legais e instale só o emulador.

**Privacidade:** não mostre nem grave em arquivos o serial, IMEI, contas, senhas de Wi-Fi, códigos de desbloqueio ou MAC/BSSID, além do mínimo necessário para o comando. Prefira que senhas sejam digitadas no próprio aparelho. Se a pessoa as colar na conversa, avise que ficaram registradas.

## Passo 1: entrevista

Não execute nada no aparelho antes desta etapa, nem comandos de leitura.

Use a ferramenta de perguntas do agente, se houver; caso contrário, pergunte em texto e espere. Faça uma entrevista só, em uma mensagem. Faça a entrevista mesmo que a pessoa diga "faça tudo" ou "não pergunte nada": aproveite o que ela já disse, peça para confirmar o nível e faça apenas as perguntas que faltam. Pergunte:

1. **Objetivo:** abrir apps mais rápido, fluidez, bateria, liberar espaço, sistema mais novo ou reaproveitar o aparelho?
2. **Até onde ir com a otimização?**
   - **A. Só diagnóstico:** nada muda.
   - **B. Ajustes reversíveis (recomendado para começar):** configurações e compilação de apps.
   - **C. B + limpeza de apps:** desativar ou remover apps dispensáveis para o usuário.
   - **D. C + root e modo desempenho:** mais risco, pode afetar apps de banco e pode apagar dados se exigir desbloqueio.
   - **E. D + kernel e overclock:** experimental, com risco de travamentos e dano.
3. **Quer trocar o sistema operacional?**
   - **Não, manter o atual (recomendado).**
   - **Só se houver ganho real:** pesquisar e voltar com a recomendação antes de qualquer mudança.
   - **Sim, o mais novo possível**, aceitando instabilidade.
   - **Sim, o mais estável possível**, mesmo sendo mais antigo.
4. **Dados e uso:** há algo a salvar? O aparelho continuará sendo usado para banco, trabalho ou chip principal? Se for trocar o sistema, quer apps do Google?
5. **Quer também um emulador de PlayStation 1?** Não, ou sim, e nesse caso onde está o arquivo do jogo, se vai usar botões na tela ou controle físico, e se tem uma BIOS extraída do próprio console.
6. **Quer melhorar a câmera?** Não, ou sim, e nesse caso o que mais incomoda (pouca luz, vídeo, câmera lenta, filtros) e até onde ir: só apps, recursos ocultos do driver ou arquivos do sistema com root.

**Se o pedido for só o emulador ou só a câmera,** não exija os níveis de otimização: pergunte uma vez se quer otimizar também, faça as perguntas da referência ([references/ps1-emulator.md](references/ps1-emulator.md) ou [references/camera.md](references/camera.md)) e confirme que o aparelho é da pessoa. Depois, se ela não quiser otimizar, faça o passo 2, rode só `scripts/diagnose.sh` do passo 3 e siga direto para a referência, que tem a própria medição e o próprio relatório: pule o resto dos passos 3 a 6. O emulador não precisa de root, desbloqueio nem troca de sistema. A câmera só precisa de root no último nível, e então valem as confirmações específicas do passo 4.

Se a resposta incluir trocar o sistema, root ou kernel, avise antes de continuar que pode apagar tudo, perder a garantia, afetar apps de banco e deixar o aparelho sem ligar. Em Samsung, avise também que o desbloqueio queima o Knox de forma permanente e usa Odin ou Heimdall, não Fastboot.

"Máximo" não significa ignorar limites: significa o último valor estável, medido, com as proteções de temperatura ativas.

## Passo 2: identificar o aparelho

Leia [references/setup-and-diagnostics.md](references/setup-and-diagnostics.md). Instale as ferramentas, liste os aparelhos e confirme qual deve ser usado pelo modelo, sem pressupor. Depois, confirme que é da pessoa ou que ela tem autorização, sem interrogatório.

## Passo 3: diagnóstico e plano

Ainda sem mudar configurações. Os scripts só criam arquivos temporários, que devem ser removidos ao final:

1. Rode `scripts/diagnose.sh` no aparelho.
2. Rode `scripts/launch-bench.sh` para ter uma referência, depois de perguntar quais apps importam e avisar que eles serão fechados e abertos. Se o sistema for trocado, essa referência serve só de contexto: repita a medição no sistema novo, antes dos ajustes.
3. Crie `android-optimizer-log.md` na pasta de trabalho, com o modelo, a referência e os valores originais. Não coloque dados pessoais nele.
4. Apresente, em poucas linhas, o estado do aparelho, o plano para o nível escolhido, o ganho que dá para esperar e o que não vai melhorar. Em seguida, peça a confirmação.

## Passo 4: executar por etapas

Siga esta ordem, pulando o que não foi escolhido, e pare ao chegar ao nível definido. O emulador e a câmera só dependem de a pessoa ter pedido, qualquer que seja o nível; as partes da câmera que exigem root seguem o nível escolhido. Leia só a referência da etapa atual:

| # | Etapa | Referência | Precisa de confirmação específica para |
|---|---|---|---|
| 1 | Salvar ou recuperar dados | [references/data.md](references/data.md) | Qualquer cópia de dados pessoais |
| 2 | Desbloqueio e recovery | [references/unlock-and-recovery.md](references/unlock-and-recovery.md) | Desbloquear e gravar recovery |
| 3 | Troca de sistema | [references/rom.md](references/rom.md) | Formatar e instalar |
| 4 | Ajustes reversíveis | [references/tweaks.md](references/tweaks.md) | Ajustes que desligam funções usadas |
| 5 | Limpeza de apps | [references/apps.md](references/apps.md) | A lista de apps |
| 6 | Emulador de PS1 | [references/ps1-emulator.md](references/ps1-emulator.md) | Instalar o app e apagar saves ou o jogo |
| 7 | Câmera | [references/camera.md](references/camera.md) | Instalar apps, ligar recursos ocultos e qualquer arquivo de sistema |
| 8 | Root e modo desempenho | [references/root-and-kernel.md](references/root-and-kernel.md) | Instalar root e cada mudança de CPU/GPU |
| 9 | Kernel e overclock | [references/root-and-kernel.md](references/root-and-kernel.md) | Cada kernel e cada faixa de frequência |

A ordem importa: **salve os dados antes de desbloquear**, porque o desbloqueio costuma apagar tudo, e **troque o sistema antes de otimizar**, porque ajustes, limpeza, emulador e apps de câmera se perdem na troca. Confira [references/lessons.md](references/lessons.md) antes de escrever comandos, pois lá estão falhas reais a evitar.

Antes de cada ação destrutiva, diga:

- o que vai acontecer;
- o que será perdido;
- se dá para desfazer;
- o que a pessoa precisa fazer.

Depois, espere a resposta.

## Passo 5: medir e decidir

Depois de cada grupo de mudanças, reinicie se necessário, espere o sistema assentar e repita a mesma medição nas mesmas condições. Compare a mediana de 3 aberturas. Se piorou ou não mudou e tem efeito colateral, desfaça e registre.

## Passo 6: relatório final

Entregue, sem exagerar os resultados:

1. Tabela de antes e depois, só com números medidos.
2. O que foi mudado, o que foi testado e descartado, e como desfazer.
3. O que **não** foi verificado, como chamada, câmera ou chip, quando não testado.
4. Efeitos colaterais e riscos que ficaram, como patch de segurança antigo, sem Play Store, bootloader aberto, depuração USB ligada ou notificações atrasadas.
5. O caminho do `android-optimizer-log.md`.

Antes de terminar, sugira desligar a depuração USB quando ela não for mais necessária.
