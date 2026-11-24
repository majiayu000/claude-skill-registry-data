---
name: configurar-projetor
description: Guia passo a passo que conduz uma pessoa leiga, do zero, a deixar o projetor HY320 Mini mais rápido usando só o Claude Code - instala o que falta no computador, diz exatamente o que apertar no controle do projetor, encontra o aparelho na rede, pergunta as preferências em linguagem simples, aplica a otimização, instala os apps de streaming e confere tudo no final. Use sempre que alguém disser "configure meu projetor", "otimiza meu projetor", "instala tudo para mim", "por onde eu começo", "não sei usar isso", ou abrir este repositório pedindo ajuda sem saber o que fazer, mesmo que não cite o modelo do projetor.
---

# Configurar o projetor, passo a passo

Você está ajudando alguém que provavelmente nunca abriu um terminal. A pessoa tem um projetor HY320 Mini, um computador com Windows e este repositório aberto no Claude Code. O objetivo é levá-la do zero até o projetor otimizado sem que ela precise digitar nenhum comando.

Como conduzir:

- **Faça você tudo o que puder.** Rode os comandos e scripts; não peça para a pessoa copiar e colar nada. Ela só entra em cena no que é físico: apertar botões no controle do projetor e reiniciar o aparelho.
- **Um passo por vez.** Diga o que vai acontecer, faça, confirme que deu certo e só então siga. Se despejar a lista inteira, a pessoa se perde no segundo item.
- **Confira em vez de perguntar.** Depois de pedir que ela ligue a depuração, procure o projetor na rede; o resultado diz se ela conseguiu. Só pergunte o que não dá para verificar.
- **Linguagem do dia a dia.** "Depuração USB" é o nome que aparece na tela, então use; "ADB", "pacote" e "DNS" precisam de uma frase de explicação ou podem ficar de fora.
- **Não avance com um passo falhando.** Cada etapa depende da anterior.

Os detalhes técnicos (comandos, o que cada pacote faz, armadilhas) estão na skill [otimizar-projetor-android](../otimizar-projetor-android/SKILL.md) e na referência [hy320-mini.md](../otimizar-projetor-android/references/hy320-mini.md). Leia a skill técnica antes de começar e consulte a referência quando precisar. Os scripts ficam na raiz do repositório, três pastas acima deste arquivo.

## Abertura

Explique em poucas linhas, antes de qualquer comando:

- o que vai ser feito: deixar o projetor mais rápido desligando o que ele não usa e preparando os apps;
- quanto demora: cerca de 30 minutos, a maior parte de espera;
- que nada é apagado e tudo pode ser desfeito depois;
- o que ela vai precisar ter em mãos: o projetor ligado e no Wi-Fi, e o controle remoto.

## Passo 1: preparar o computador (você faz)

1. Confirme que o sistema é Windows. Os scripts são PowerShell; em macOS ou Linux, siga o fluxo da skill técnica com os comandos `adb` diretos.
2. Veja se o ADB já existe: `Get-Command adb`. Os scripts também o procuram sozinhos na pasta do winget.
3. Se não existir, avise que vai instalar o programa oficial do Google para conversar com aparelhos Android e instale:

```powershell
winget install --id Google.PlatformTools -e --accept-source-agreements --accept-package-agreements
```

Se o `winget` não existir no computador, oriente o download em <https://developer.android.com/tools/releases/platform-tools> e peça para a pessoa extrair o ZIP; copie `adb.exe`, `AdbWinApi.dll` e `AdbWinUsbApi.dll` para a raiz do repositório.

## Passo 2: ligar a depuração no projetor (a pessoa faz)

Dê as instruções abaixo, uma tela por vez se ela parecer insegura. As imagens de cada tela estão em `docs/img/` e no `TUTORIAL.md`; indique-as se ajudar.

1. Na tela inicial, abrir **Configurações** (engrenagem) e entrar em **Preferências do dispositivo**.
2. Entrar em **Sobre**, o primeiro item.
3. Descer até **Número da versão** e apertar **OK sete vezes seguidas**, até aparecer o aviso de que agora é desenvolvedor.
4. Apertar **Voltar** uma vez. No fim da lista apareceu **Opções do desenvolvedor**; entrar nele.
5. Descer até **Depuração USB** e ligar a chave (fica azul). Não mexer em mais nada nessa tela.

Peça que ela avise quando terminar.

## Passo 3: encontrar e autorizar (você faz, ela confirma na tela)

Rode a busca a partir da raiz do repositório:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\encontrar-projetor.ps1
```

Interprete o resultado:

- **"este e o projetor"**: guarde o IP e siga.
- **"aguardando autorizacao"**: peça para ela olhar a tela do projetor, marcar **Sempre permitir deste computador** e escolher **OK**. Rode a busca de novo.
- **Outro aparelho encontrado** (celular, tablet): ignore-o e não toque nele. Diga à pessoa que achou outro aparelho e continue procurando.
- **Nada encontrado**: o projetor pode estar em outra faixa de rede (computador no cabo, projetor no Wi-Fi). Peça para ela abrir **Configurações > Rede e Internet**, entrar na rede conectada e ler o **endereço IP**. Com os três primeiros números, rode `.\encontrar-projetor.ps1 -Rede 192.168.0` (trocando pelos números dela). Se ainda assim não aparecer, volte ao passo 2 e confira a chave da Depuração USB.

Os scripts só continuam se o aparelho for mesmo um HY320 Mini. Se abortarem dizendo que não é, o projetor é de outra variante: explique isso e use a skill técnica, que cobre a análise de qualquer aparelho, em vez de forçar os scripts.

## Passo 4: perguntar o que a pessoa quer

A otimização básica não tem contrapartida e entra sempre. As opções abaixo têm, então pergunte (use a ferramenta de perguntas, se houver, com seleção múltipla). Explique cada uma assim:

| Opção | Em palavras simples | O que ela perde |
|---|---|---|
| Bloquear anúncios | Menos propaganda e rastreamento em apps e sites, sem instalar nada | Não tira anúncio do YouTube; as consultas de endereços passam por um serviço de bloqueio (Control D) |
| Navegador com bloqueador (TV Bro) | Para quem abre sites no projetor: um navegador feito para controle remoto que esconde os anúncios das páginas | Ocupa espaço como qualquer app; alguns sites recentes podem aparecer desalinhados |
| Desligar a loja e os atualizadores do fabricante | Libera memória e impede apps instalados sem pedir | O projetor não recebe mais atualizações do fabricante; a Play Store continua |
| Bluetooth desligado ao ligar | Libera memória | Precisa ligar nas Configurações quando for usar caixa de som ou fone |
| Tela inicial nova (Projectivy) | Tela mais organizada | Usa mais memória que a original |

Pergunte também **quais apps de streaming ela quer**. Isso muda a ordem do trabalho: a Netflix só instala pela loja do fabricante, então precisa ser instalada antes de essa loja ser desligada (ou a loja tem de ser religada por um instante, como descrito no passo 6).

## Passo 5: otimizar (você faz)

Monte o comando com as opções escolhidas (`-BloquearAnuncios`, `-DesativarFabricante`, `-DesligarBluetooth`, `-InstalarProjectivy`; ou `-Completo` para as quatro) e rode em segundo plano, porque leva pouco mais de 10 minutos:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\otimizar-hy320.ps1 -Ip <ip> <opções>
```

O bloqueio de anúncios entra no nível `forte`. Só use `-NivelBloqueio maximo` se a pessoa pedir o máximo e aceitar que o "Entrar com Facebook" e um ou outro site podem parar; use `-NivelBloqueio padrao` se algum app deixar de funcionar.

Avise antes: o projetor fica lento enquanto isso roda, e ela não deve desligá-lo. Ao terminar, leia a saída e conte: quantos apps foram preparados, se houve falha, e se o bloqueio de anúncios validou. Se o script disser que o DNS privado não validou, ele já desfez essa parte sozinho; explique que a rede dela não permite e siga.

## Passo 6: apps de streaming (opcional)

Siga a seção "Instalar apps" da skill técnica: abra a página do app na loja, olhe a tela por uma captura e só então acione o botão.

- **YouTube, HBO Max, Prime Video, Paramount+**: pela Google Play Store do projetor. No Brasil o Paramount+ que instala é o pacote `com.cbs.ca`. Se aparecer "Não foi possível instalar", tente de novo; costuma passar na segunda.
- **Netflix**: a Play Store recusa. O caminho é a loja do fabricante (aparece como **Appstore** ou **Loja de Aplicativos**), que tem a Netflix original em versão antiga ("7.120_NetFlix"). Essa loja exige aceitar uma política de privacidade que avisa que coleta dados de uso: explique isso e deixe a decisão com a pessoa. Se ela concordar, peça que ela mesma aperte **Concordar** no controle, ou que autorize você a fazê-lo. Depois de instalar, confira a assinatura do app como a skill técnica descreve, antes de ela digitar a senha, e desligue a loja de novo se a pessoa pediu isso no passo 4. Avise que essa versão se usa com o modo mouse do controle.
- **Disney+**: não funciona neste projetor (exige Android mais novo) e a loja do fabricante não tem. Diga isso com clareza e sugira um aparelho de streaming na entrada HDMI. Não procure o app em outros sites.

- **TV Bro** (se ela quis o navegador com bloqueador): pela Play Store do projetor, pacote `com.phlox.tvwebbrowser`. Ele já abre com o bloqueador ligado; não há nada para configurar.
- **YouTube sem anúncios**: se ela perguntar, explique que nenhum bloqueio de rede tira os anúncios do app do YouTube, que o app alternativo que faz isso não está na Play Store e que este guia não instala apps de fora dela. A decisão é dela; os detalhes estão em `docs/bloqueio-de-anuncios.md`.

Entrar com a conta em cada app é com a pessoa; não peça nem digite senhas.

## Passo 7: reiniciar e conferir

1. Peça para ela desligar e ligar o projetor.
2. Espere ele voltar à rede e confira você mesmo: os itens desligados continuam desligados, o bloqueio de anúncios está ativo (se foi escolhido; `ferramentas/testar-bloqueio.sh` conta quantos endereços de anúncio estão bloqueados e se os apps continuam alcançando o que precisam), o Bluetooth iniciou desligado (se foi escolhido) e a tela inicial é a esperada.
3. Se o Projectivy foi instalado, ele mostra uma tela de boas-vindas: peça que ela siga com o controle.
4. Mostre o antes e depois com os números do aparelho dela, em uma tabela curta: quantos apps estavam compilados para código nativo de fábrica (`status=speed` em `backup\dexopt-original.txt`) e quantos estão agora (`dumpsys package dexopt`), e quais itens ficaram desligados. Pergunte se ela sentiu diferença nos menus. Se quiser um número de cronômetro, `ferramentas/medir-abertura.sh` mede a abertura dos apps; avise que leva 15 minutos e que o ganho nesse teste costuma ser pequeno (2% a 8% no aparelho de referência), porque ele não mede transições nem memória livre.

## Passo 8: encerrar

1. Peça para ela voltar em **Configurações > Preferências do dispositivo > Opções do desenvolvedor** e **desligar a Depuração USB**. Explique o motivo em uma frase: ligada, qualquer aparelho da rede consegue controlar o projetor.
2. Faça um resumo curto: o que mudou, o que ficou instalado, o que não foi possível e por quê.
3. Diga como desfazer: basta abrir o Claude Code nesta pasta de novo e pedir para desfazer a otimização. Você então liga a depuração com ela (passo 2) e roda `.\restaurar-hy320.ps1 -Ip <ip>`.

## Se algo der errado

| O que aparece | O que fazer |
|---|---|
| A busca não encontra o projetor | Conferir a chave da Depuração USB, o Wi-Fi do projetor e a faixa de rede (passo 3) |
| "ABORTADO: não é o HY320 Mini" | É outro aparelho ou outra variante; não force. Use a skill técnica |
| Projetor sem internet depois do bloqueio de anúncios | Rodar `.\restaurar-hy320.ps1 -Ip <ip>`; ele funciona pela rede local, sem internet |
| Um botão do controle parou de funcionar | Rodar o `restaurar-hy320.ps1` e investigar com a skill técnica antes de repetir |
| O projetor trocou de IP | Rodar a busca de novo |
| A pessoa quer parar no meio | Tudo bem em qualquer ponto antes do passo 5; durante o passo 5, é melhor esperar terminar |

## O que nunca fazer

- Alterar qualquer aparelho que não seja o projetor confirmado pelos scripts.
- Trocar o sistema (firmware) do projetor. Não existe versão mais nova para este modelo, e a de outro modelo pode inutilizá-lo.
- Baixar apps de sites de terceiros. Só a Play Store e a loja do próprio fabricante.
- Aceitar termos ou políticas de privacidade sem a pessoa autorizar.
- Enviar teclas ao projetor sem antes conferir, por captura de tela, o que está em foco.
