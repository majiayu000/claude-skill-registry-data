---
name: otimizar-projetor-android
description: Analisa e otimiza projetores e TV boxes Android baratos (HY320 Mini, HY300, Magcubic, Allwinner H713 e similares) pela rede via ADB, de forma segura e reversível - localiza o aparelho, confirma a identidade, mede, faz backup, compila os apps, desativa bloatware, ajusta o sistema e verifica após reiniciar. Use sempre que o usuário pedir para deixar um projetor, TV box ou Android TV "mais rápido", "mais leve" ou "sem travar", remover bloatware, bloquear anúncios, ver o que inicia com o sistema, trocar a tela inicial, investigar "obsolescência programada" ou mexer em um aparelho Android pela rede Wi-Fi, mesmo que ele não mencione ADB.
---

# Otimizar projetor / TV box Android via ADB

Projetores baratos (HY320 Mini e parentes) saem de fábrica com hardware fraco (1 GB de RAM, 4 núcleos) e firmware mal cuidado: apps rodando sem compilação nativa, serviços do fabricante sempre ativos e logs de depuração ligados. Quase todo o ganho possível vem de corrigir isso **sem trocar o sistema**.

O aparelho é o único do usuário e normalmente **não existe imagem de fábrica pública** para recuperá-lo. Por isso o trabalho inteiro segue quatro regras, e cada uma existe por um motivo concreto:

1. **Só mudanças reversíveis.** Desative (`pm disable-user`), não desinstale nem apague. Um erro precisa poder ser desfeito com um comando.
2. **Confirme a identidade antes de alterar qualquer coisa.** Em redes domésticas é comum haver outro Android com ADB aberto (tablet, celular). Otimizar o aparelho errado é o pior erro possível aqui.
3. **Meça antes de afirmar.** Diga o que foi medido, em que condição, e o que não foi verificado. "Parece mais rápido" não é resultado.
4. **Pergunte quando houver contrapartida.** Desativar atualizações ou uma loja de apps muda o que o usuário pode fazer; a decisão é dele.

Se este repositório estiver presente, a raiz já tem scripts prontos para o HY320 Mini (`encontrar-projetor.ps1`, `otimizar-hy320.ps1`, `restaurar-hy320.ps1`). Para esse modelo, use-os. Para qualquer outro aparelho, siga o fluxo abaixo e adapte as listas de pacotes ao que a análise mostrar. Os dados do caso de referência estão em [references/hy320-mini.md](references/hy320-mini.md): leia quando o aparelho for um HY320/HY300 ou quando precisar de um exemplo do que manter e do que desativar.

## Fluxo

### 1. Entender o alvo

A pasta do projeto pode estar vazia: o "projeto" costuma ser o aparelho físico. Confirme que o pedido é sobre um dispositivo na rede do usuário e que ele é o dono.

### 2. Localizar o aparelho

```bash
adb devices -l                      # algo já conectado?
```

Se não houver, procure apenas a porta 5555 na rede local do usuário. O PC pode estar no cabo em uma faixa (ex.: 192.168.10.x) e o projetor no Wi-Fi em outra (ex.: 192.168.0.x), então olhe também a faixa do Wi-Fi. Não faça varredura completa de portas: se a 5555 não aparecer, peça ao usuário o IP e que ative a depuração.

Como ativar a depuração (Android TV / AOSP 11):
`Configurações > Preferências do dispositivo > Sobre > Número da versão` (pressionar 7 vezes) e depois `Opções do desenvolvedor > Depuração USB`. Em muitos desses aparelhos, ligar a "Depuração USB" já abre o ADB na rede.

```bash
adb connect <ip>:5555
```

Se aparecer `unauthorized`, o aparelho está mostrando a janela "Permitir depuração USB?". Peça ao usuário para marcar "Sempre permitir" e confirmar, e aguarde em um laço curto até o estado virar `device`.

### 3. Confirmar a identidade (obrigatório)

Use sempre `adb -s <ip>:5555` em todos os comandos; nunca confie no dispositivo padrão.

```bash
adb -s $ALVO shell getprop ro.product.model
adb -s $ALVO shell getprop ro.hardware           # ex.: sun50iw12p1 = Allwinner H713
adb -s $ALVO shell getprop ro.board.platform
adb -s $ALVO shell "dumpsys battery | grep -E 'present|level'"
adb -s $ALVO shell wm size
```

O nome do modelo sozinho não basta: firmwares baratos falsificam marca e modelo. Cruze sinais físicos. Projetor não tem bateria, não tem tela touch integrada e tem apps de projeção (keystone, entrada HDMI). Um aparelho com bateria Li-ion, tela 1200x1920 e dezenas de pacotes Samsung é um tablet, por mais que o usuário diga o contrário: mostre a evidência e continue procurando o aparelho certo.

### 4. Analisar (somente leitura)

Colete tudo antes de mexer. O que cada comando responde:

```bash
# Hardware e memória
adb -s $ALVO shell "cat /proc/meminfo | head -5; cat /proc/swaps; df -h /data"
adb -s $ALVO shell "dumpsys meminfo | sed -n '/Total PSS by process/,/Total PSS by OOM/p' | head -40"

# Quem gasta CPU (duas amostras, ordenado por CPU)
adb -s $ALVO shell "top -b -n 2 -d 4 -s 4 -m 14 -o PID,USER,RES,%CPU,ARGS | tail -15"

# Pacotes: terceiros, sistema, desativados
adb -s $ALVO shell "pm list packages -3; pm list packages -s; pm list packages -d"

# Estado de compilação de cada app (o achado mais importante)
adb -s $ALVO shell "dumpsys package dexopt | grep -oE 'status=[a-z-]+' | sort | uniq -c"

# Quem acorda no boot
adb -s $ALVO shell "cmd package query-receivers --brief -a android.intent.action.BOOT_COMPLETED | grep /"

# Ajustes relevantes
adb -s $ALVO shell "settings get global window_animation_scale; dumpsys wifi | grep -m1 'Verbose logging'"

# Serviço de acessibilidade do fabricante (ver seção "Não mexer")
adb -s $ALVO shell "dumpsys accessibility | grep -E 'Bound services|capabilities'"
```

Leitura dos resultados:

- **`status=verify` na maioria dos apps** significa que rodam interpretados. É o maior gargalo e o maior ganho.
- **Processos do fabricante com dezenas de MB** que ninguém abriu (lojas, atualizadores, "assist") são candidatos a desativação.
- **Carga média acima de 1 em repouso** pede uma olhada nas threads (`top -H`). Threads do kernel (ex.: `sugov`) não se resolvem sem root; apenas relate.
- **Rede**: não conclua pelo "link speed" mostrado em repouso, ele engana. Meça com um `adb push` de um arquivo de 8 MB e veja a taxa real.

### 5. Backup

Antes da primeira alteração, salve em uma pasta `backup/` no PC: `settings list global|secure|system`, `pm list packages -e`, `pm list packages -d` e `dumpsys package dexopt`. Mantenha também um arquivo com cada pacote que você desativar; é ele que permite restaurar exatamente o que foi mudado. Esses arquivos têm identificadores do aparelho e nomes de rede: não devem ir para repositório público.

### 6. Aplicar, do maior ganho para o menor

**a) Compilar os apps para código nativo.** Leva de 10 a 15 minutos em um H713 e o aparelho fica lento enquanto isso; avise o usuário e rode em segundo plano.

```bash
adb -s $ALVO shell cmd package compile -m speed <pacote>          # um por um, registrando Success/Failure
adb -s $ALVO shell cmd package compile -m speed-profile <pacote>  # para apps que já têm perfil de uso
```

Compile todos os pacotes ativos em `speed`, exceto os muito grandes (Google Play Services, Play Store, Chrome), que ficam em `speed-profile` ou como estão. Código compilado é memória de arquivo, recuperável; o JIT que ele substitui é memória suja. Em aparelho de 1 GB isso ajuda nos dois sentidos.

**b) Desativar o que roda sem necessidade.**

```bash
adb -s $ALVO shell pm disable-user --user 0 <pacote>
adb -s $ALVO shell am force-stop <pacote>
```

Sem perguntar: ferramentas de teste de fábrica (em Allwinner: `dragonbox`, `agingdragonbox`, `dragonatt`; "aging" é teste de burn-in, não envelhecimento proposital).

Perguntando antes, com a contrapartida explicada: loja de apps do fabricante, atualizadores automáticos e atualização de firmware (FOTA). Costumam ter permissão de instalar apps silenciosamente, o que é motivo de segurança além de desempenho, mas desativá-los encerra as atualizações.

**c) Ajustes de sistema.**

```bash
adb -s $ALVO shell settings put global window_animation_scale 0.5
adb -s $ALVO shell settings put global transition_animation_scale 0.5
adb -s $ALVO shell settings put global animator_duration_scale 0.5
adb -s $ALVO shell cmd wifi set-verbose-logging disabled
```

Use 0.5 e não 0: com 0, alguns apps deixam de animar indicadores de carregamento e parecem travados.

**d) Bluetooth desligado no boot (se o usuário pedir).** Verifique antes se o controle remoto é Bluetooth (`dumpsys bluetooth_manager | grep -A5 'Bonded devices'`); se houver controle pareado, desligar deixa o usuário sem controle. No Android 11, `svc bluetooth disable` falha por um bug (packageName nulo) e `cmd bluetooth_manager` não existe; o caminho que funciona é gravar o estado lido no boot:

```bash
adb -s $ALVO shell settings put global bluetooth_on 0     # vale a partir do próximo reinício
```

Explique a limitação: o Android lembra o último estado, então se o usuário ligar e reiniciar sem desligar, volta ligado.

**e) Trocar a tela inicial (se o usuário quiser).** Instale de fonte oficial (ex.: Projectivy, releases em `github.com/spocky/miproja1`), defina como padrão e teste a tecla Home:

```bash
adb -s $ALVO install <apk>
adb -s $ALVO shell cmd package set-home-activity com.spocky.projengmenu/.ui.home.MainActivity
adb -s $ALVO shell "input keyevent KEYCODE_HOME; sleep 5; dumpsys activity activities | grep mResumedActivity"
```

Deixe a tela original instalada e ativa como reserva. Meça a memória das duas e conte o resultado como ele é: no HY320 Mini o Projectivy usou cerca de 87 MB contra 42 MB da original. É mais organizado, não mais leve.

**f) Bloquear anúncios (se o usuário pedir).** Em aparelho de 1 GB, não instale app bloqueador: ele fica rodando como VPN e consome a memória que se acabou de liberar. Use o DNS privado do Android (DNS sobre TLS, Android 9+) com um servidor que já aplica as listas de bloqueio. Custo de memória zero e vale para o sistema inteiro.

A força do bloqueio depende da lista do servidor, e a diferença é grande: no HY320 Mini, com os mesmos 101 endereços de anúncio, `dns.adguard-dns.com` bloqueou 72 e `x-hagezi-proplus.freedns.controld.com` (Control D com a lista HaGeZi Pro++) bloqueou 91, os dois sem quebrar nenhum endereço necessário. Escolha pelo que mede, não pela fama: o servidor precisa ter ponto de presença perto do usuário (os que respondem em 200 ms atrasam cada endereço novo) e não pode quebrar os apps de streaming. A comparação completa e os níveis `forte`, `maximo` e `padrao` do script estão em `docs/bloqueio-de-anuncios.md`. Os comandos abaixo usam o AdGuard como exemplo; troque o nome pelo servidor escolhido.

```bash
adb -s $ALVO shell "toybox nc -w 4 dns.adguard-dns.com 853 </dev/null && echo aberta"   # a rede deixa passar?
adb -s $ALVO shell settings put global ntp_server 216.239.35.0      # hora por IP, ver abaixo
adb -s $ALVO shell settings put global private_dns_mode off
adb -s $ALVO shell settings put global private_dns_specifier dns.adguard-dns.com
adb -s $ALVO shell settings put global private_dns_mode hostname
```

Três cuidados, todos aprendidos na prática:

- **Grave a configuração uma única vez.** No Android 11, duas gravações seguidas das chaves `private_dns_*` cancelam a validação em andamento (`Server ... was removed during private DNS validation` no log) e o sistema não tenta de novo: o aparelho fica sem DNS. Por isso a sequência acima desliga, grava o servidor e só então liga. Se já estiver ativo e validado, não regrave.
- **Confirme e esteja pronto para reverter.** Verifique `dumpsys connectivity | grep ValidatedPrivateDnsAddresses` (lista não vazia), teste um domínio de anúncio (`ping -c1 doubleclick.net` deve resolver para `127.0.0.1` ou `0.0.0.0`) e um normal. Se não validar, apague as duas chaves (`settings delete global private_dns_mode` e `private_dns_specifier`) na hora. O ADB continua funcionando por IP mesmo com o DNS quebrado. Depois acompanhe por alguns minutos com domínios diferentes.
- **Relógio.** O DNS privado valida certificado, então exige data correta; e o servidor de hora padrão é um nome, que precisa de DNS. Se o relógio zerar por falta de energia, isso vira um impasse. Apontar `ntp_server` para um IP (ex.: `216.239.35.0`, time1.google.com) evita depender de DNS para acertar a hora.

- **Meça antes e depois, e espere o cache.** `ferramentas/testar-bloqueio.sh` roda no aparelho e conta quantos endereços de anúncio estão bloqueados e se os endereços necessários continuam resolvendo. Logo depois de trocar de servidor o Android ainda devolve respostas guardadas do anterior; a contagem só estabiliza depois de alguns minutos. Em seguida abra cada app de streaming e confira a tela.

**Páginas da internet.** O DNS só enxerga o nome do servidor; um bloqueador dentro do navegador enxerga o endereço completo e a página, que é como o Brave trabalha. Se o usuário navega no aparelho, instale pela Play Store dele um navegador com bloqueador. No HY320 Mini o Brave é recusado ("dispositivo não compatível") e o TV Bro (`com.phlox.tvwebbrowser`) instala, já com o bloqueador ligado e sem serviço em segundo plano.

Diga ao usuário os limites, sem prometer "bloquear tudo": nenhum bloqueio de rede remove os anúncios do app do YouTube (vêm dos mesmos servidores dos vídeos) nem os intervalos dos planos de streaming com anúncios, e as consultas de DNS passam a ir para o provedor escolhido. App alternativo de YouTube só existe fora da Play Store: explique o que é e deixe a decisão e a instalação com o usuário.

**g) Instalar apps (se o usuário pedir).** Use a Play Store do próprio aparelho: é a fonte oficial e já diz se o app é compatível. Abra a página do app, confira a tela e só então acione o botão.

```bash
adb -s $ALVO shell "am start -a android.intent.action.VIEW -d 'market://details?id=<pacote>'"
adb -s $ALVO shell screencap -p /sdcard/x.png      # puxe e olhe: há botão "Instalar" em foco?
adb -s $ALVO shell input keyevent KEYCODE_DPAD_CENTER
adb -s $ALVO shell pm list packages <pacote>       # repita até aparecer
```

- Aparelhos não certificados pelo Google mostram "Seu dispositivo não é compatível com esta versão" para Netflix e Disney+. A certificação não tem correção por software. Não baixe APKs desses apps de sites de terceiros.
- Antes de concluir que a Netflix é impossível, veja a **loja de apps do próprio fabricante**: nesses projetores ela costuma oferecer uma versão antiga da Netflix de celular (ex.: "7.120_NetFlix"), anterior às checagens de certificação atuais, usada com o modo mouse do controle. Essa loja pode ser justamente o pacote que foi desativado como bloatware; reative só durante a instalação e desative depois. Ela exige aceitar uma política de privacidade com coleta de dados: essa decisão é do usuário, não aceite sem ele autorizar. Depois de instalar, puxe o APK do aparelho (`pm path` + `adb pull`) e confira com `apksigner verify --print-certs` se a assinatura é válida e em nome da Netflix antes de o usuário digitar a senha; confira também se nenhum outro pacote foi instalado junto. O app bloqueia captura de tela (o `screencap` sai vazio), então verifique a abertura por `dumpsys activity` e pelo log.
- Para o que a loja do fabricante não tiver (ex.: Disney+), sugira um aparelho de streaming certificado na entrada HDMI.
- Se o usuário trouxer um arquivo `.apk` (baixado ou recebido de alguém), inspecione antes de instalar, sem executar nada: `aapt2 dump badging arquivo.apk` mostra pacote, versão e `minSdkVersion`; `apksigner verify --print-certs` mostra quem assinou; `aapt2 dump xmltree arquivo.apk --file AndroidManifest.xml | grep requiredSplitTypes` mostra se ele é só a parte "base" de um app dividido. Dois motivos comuns de fracasso, ambos visíveis nessa inspeção: `minSdkVersion` maior que o Android do aparelho (`INSTALL_FAILED_OLDER_SDK`) e APK base sem as partes de arquitetura e densidade (instala, mas fecha ao abrir). Um app dividido só funciona com todas as partes, instaladas juntas com `adb install-multiple`. Se instalar e não abrir, desinstale para não deixar ícone quebrado, e conte ao usuário o que faltou.
- Um mesmo serviço pode ter pacotes diferentes por região e por tipo de aparelho (ex.: no Brasil o Paramount+ que instala é `com.cbs.ca`, enquanto `com.cbs.ott` aparece como indisponível no país; Prime Video para TV é `com.amazon.amazonvideo.livingroom`). "Este item não está disponível em seu país" significa pacote errado, não bloqueio.
- A instalação pode falhar uma vez com "Não foi possível instalar" (uma parte do download trava). Feche o aviso com Voltar, reabra a página, confira a tela e tente de novo antes de investigar.
- Depois de instalar, compile (`cmd package compile -m speed <pacote>`), abra o app uma vez para confirmar que chega à tela de login e veja se ele se registrou para iniciar no boot.

### 7. Verificar após reiniciar

Peça ao usuário para reiniciar e detecte o novo boot comparando `grep btime /proc/stat` antes e depois. Em seguida:

```bash
# Ordem e motivo de cada processo iniciado no boot
adb -s $ALVO shell "logcat -d -b events -v time -s am_proc_start"
# O que continua rodando, com memória
adb -s $ALVO shell "dumpsys meminfo | sed -n '/Total PSS by process/,/Total PSS by OOM/p' | head -30"
adb -s $ALVO shell "pm list packages -d"
```

Confirme que os pacotes desativados não voltaram e separe "ficou rodando" de "iniciou e foi encerrado em segundos" (estes só custam tempo de boot).

Ao comparar antes e depois, cuide das condições: apps abertos, compilação em andamento e os primeiros minutos após o boot distorcem a memória e a carga. Se as condições diferem, diga isso em vez de apresentar a diferença como ganho.

### 8. Encerrar

Lembre o usuário de **desligar a Depuração USB** ao terminar: enquanto ligada, a porta 5555 aceita conexões de qualquer aparelho da rede.

## Não mexer

Desativar estes itens quebra funções que o usuário só percebe depois:

- **Serviço de sensor / keystone** do fabricante (correção de imagem, foco).
- **Serviço de entrada HDMI** (`tvinput`, `awtvinputservice` e similares).
- **Serviço de acessibilidade do fabricante**, quando `dumpsys accessibility` mostra que ele filtra teclas (capacidade 8 no campo `capabilities`): costuma tratar botões do controle remoto.
- **Menu de fábrica**: pode aplicar ajustes do painel no boot.
- **Google Play Services, teclado, provedor de mídia, SystemUI.**
- **Apps que o usuário instalou ou usa** (streaming, IPTV): não são bloatware só por estarem lá.

## Fora de escopo

- **Trocar o firmware ou o sistema operacional.** Os firmwares alternativos são feitos para variantes específicas de placa; a errada resulta em Wi-Fi morto ou imagem inutilizável, sem volta se não houver backup completo. Explique o risco e mantenha o sistema de fábrica otimizado.
- **Usar acessos privilegiados deixados pelo fabricante.** Alguns firmwares trazem um serviço de root ativo. Se encontrar, relate como achado de segurança (o aparelho não é confiável para contas importantes) e não o utilize.
- **Engenharia reversa dos apps do fabricante.** A análise de desempenho não precisa disso; permissões, consumo e comportamento no boot já sustentam as decisões.

## "Obsolescência programada"

Quando o usuário suspeitar de lentidão proposital, verifique com evidência e relate o que encontrou, inclusive se não encontrou nada:

```bash
adb -s $ALVO shell "cd /sys/devices/system/cpu/cpu0/cpufreq; cat scaling_available_frequencies scaling_cur_freq; cat stats/time_in_state"
adb -s $ALVO shell "for z in /sys/class/thermal/thermal_zone*; do echo \$(cat \$z/type) \$(cat \$z/temp); done"
adb -s $ALVO shell "for c in /sys/class/thermal/cooling_device*; do echo \$(cat \$c/type) \$(cat \$c/cur_state)/\$(cat \$c/max_state); done"
```

CPU alcançando a frequência máxima, limitador térmico em 0 e temperatura abaixo do ponto de corte indicam que não há estrangulamento. Na prática a lentidão desses aparelhos se explica por hardware fraco somado a firmware descuidado. Diga também o que ficou sem verificar.

## Armadilhas conhecidas

- **PowerShell com `-File`**: `-Parametro a,b` chega como um texto único; separe por vírgula dentro do script.
- **`$` dentro de `adb shell "..."` no PowerShell** precisa de crase (`` `$ ``) para não ser expandido pelo PowerShell.
- **Captura de tela**: no PowerShell 5.1, `adb exec-out screencap -p > arquivo.png` corrompe a imagem. Use `screencap -p /sdcard/x.png` e depois `adb pull`.
- **Teclas às cegas**: `am start` pode trazer para a frente uma tela antiga do app de Configurações, e uma sequência de `input keyevent` cai no item errado (já abriu a confirmação de "Revogar autorizações de depuração USB"). Antes de enviar teclas, feche o app (`am force-stop com.android.tv.settings`), confira a tela ativa com `dumpsys activity activities | grep mResumedActivity` e tire um print antes de qualquer `DPAD_CENTER`. Rolar com `DPAD_DOWN` é seguro; confirmar não é.
- **Prints para publicar**: confira cada imagem; telas de configuração mostram o nome da rede Wi-Fi e a conta Google.
- **`grep` sem resultado** devolve código de saída 1 pelo `adb shell`; isso não é erro do comando.
- **Mais de um aparelho no ADB**: sem `-s`, o comando falha ou, pior, vai para o aparelho errado.
- **Scripts idempotentes**: um script que será rodado mais de uma vez precisa checar o estado antes de gravar. Regravar um valor "igual" não é inofensivo no Android: dispara os mesmos observadores (foi assim que o DNS privado quebrou na segunda execução).
- **Usuário usando o aparelho**: veja o app em primeiro plano antes de mudanças que afetam rede ou tela. Se ele estiver assistindo algo, teste rápido e reverta rápido.

## Relatório final

Entregue ao usuário, nesta ordem:

1. O que mudou no aparelho, em uma lista curta.
2. Números medidos, com a condição de cada medição.
3. O que foi investigado e não deu em nada (ex.: estrangulamento de CPU).
4. O que não pôde ser resolvido e por quê (ex.: exige root).
5. Como desfazer.
6. O que falta o usuário fazer (reiniciar, desligar a depuração).
