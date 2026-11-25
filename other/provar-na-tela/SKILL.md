---
name: provar-na-tela
description: Usa ANTES de dizer pronto em qualquer mudanca que aparece na tela. Tambem quando o usuario mandar print dizendo "continua igual", "nao mudou", "ainda esta assim", "ficou feio", "arruma isso", ou pedir "confere na tela", "tira um print", "ve como ficou". NAO usa em mudanca so de servidor sem tela (ai a prova e teste ou contagem).
---

# Provar na tela: olhar antes de dizer pronto

Situacao comum: depois de uma mudanca, a tela continua igual ou ficou pior. Quase sempre o "pronto" saiu sem ninguem olhar a tela. O usuario testa UMA vez, no fim; cada print novo dele e retrabalho dele.

## Regra de ouro

Mudanca visual sem print lido = nao esta pronto. Nao deu pra abrir a tela? A linha de status diz "nao conferi na tela" e o motivo.

Nenhum caminho do passo 5 funcionou, ou o sistema nao sobe: nao passe de 3 tentativas por caminho. Entregue dizendo "nao conferi na tela", o motivo e a UNICA tela que ele precisa olhar.

## Passos (nesta ordem)

1. Descobrir como subir e como entrar no projeto. Se existir `PROJETOS.md` nesta pasta, leia a linha do projeto; senao, use README/CLAUDE.md do projeto, package.json e vite.config. Sem nenhum dos dois: descobrir pelos arquivos do projeto e, no fim, acrescentar a linha em `PROJETOS.md` (copie `PROJETOS.exemplo.md`) com os 8 itens: como subir, portas, banco local, como entrar, usuario de teste, como conferir a tela, como provar que subiu, gotchas.
2. O usuario reclamou de algo que ve: reproduzir ANTES de mexer. Mesma tela, mesmo tamanho (celular se o print e de celular), mesmo tema (claro ou escuro). Tirar o print "antes". Nao reproduziu: dizer isso e fazer UMA pergunta (o caminho exato ate a tela). Nao chutar conserto. O defeito so aparece em producao: abrir a producao em modo leitura (navegar e tirar print, sem clicar em nada que grava) com o acesso que a linha do projeto indica.
3. Subir local em segundo plano, nas portas da linha do projeto, com banco local ou descartavel. Nunca apontar pra producao com escrita. Derrube tudo o que subiu (servidor, navegador) antes de responder.
4. Entrar com o usuario de teste da linha do projeto. Local: se so houver o nome das variaveis de semente, defina-as voce mesmo com valor descartavel e rode a semente; nunca leia cofre nem .env. Producao sem acesso indicado: peca ao usuario 1 print ou que ele abra logado. A senha nunca aparece na resposta nem em arquivo.
5. Ferramenta, nesta ordem:
   - (a) navegador embutido do app, se a sessao tiver as ferramentas `mcp__Claude_Browser__*`;
   - (b) `playwright-cli` (abrir a skill `playwright-cli`, se estiver instalada);
   - (c) Chrome, Chromium ou Edge sem janela (`--headless=new --remote-debugging-port=<p>`, com pasta de perfil propria) controlado por CDP, com um script Python e `websocket-client`: `Page.navigate`, `Runtime.evaluate` (pra preencher campo React use o setter nativo do input e dispare o evento `input`), `Emulation.setDeviceMetricsOverride` (sem isso o viewport sai com 500 px), `Page.captureScreenshot`. Ao derrubar, mate so o processo cuja linha de comando contem a sua pasta de perfil, nunca todos os navegadores abertos.
   - Se um executavel for bloqueado pelo sistema, use o proximo caminho da lista.
6. Tirar o print "depois" da tela mexida E de cada componente interativo tocado, ABERTO (janela modal, lista suspensa, formulario). Ler o print com a ferramenta Read.
7. Conferir item por item contra o pedido, numa lista curta: "pedido -> vi na tela: sim/nao". Qualquer "nao" = voltar a mexer, nao entregar.
8. Conferir junto: console sem erro, nenhuma requisicao com 4xx/5xx, tema claro e escuro quando a tela tem os dois, largura de celular (375) quando ele usa no celular; se o print dele e de celular, e obrigatorio.
9. Depois de subir: provar que subiu pela regra do projeto (marcador no arquivo servido ou versao no health) e repetir o print em producao em modo leitura (navegar e tirar print, sem gravar nada).
10. Na resposta: o que foi conferido NA TELA, o que NAO foi e por que, e o caminho do print. Um print por tela mexida, nao galeria.

## Comandos do playwright-cli

```bash
playwright-cli open http://localhost:<porta>      # --mobile abre em celular
playwright-cli goto http://localhost:<porta>/tela # trocar de tela com o navegador ja aberto
playwright-cli resize 375 812                     # largura de celular
playwright-cli set-color-scheme dark              # tema escuro
playwright-cli snapshot                           # pega os refs (e3, e5...)
playwright-cli fill e5 "<valor>"                  # preencher
playwright-cli click e3                           # clicar (abre o modal)
playwright-cli screenshot --filename=depois.png   # print; depois Read no arquivo
playwright-cli console                            # erros do console
playwright-cli requests                           # requisicoes com erro
playwright-cli close
```

Duas armadilhas (vistas na versao 0.1.23):
- Endereco `file:///` e recusado ("Access to file: protocol is blocked"). Pagina solta em arquivo: sirva a pasta dela com `python -m http.server <porta> --bind 127.0.0.1`, abra por `http://127.0.0.1:<porta>/<arquivo>` e derrube esse servidor no fim.
- O `console` conta o 404 do `favicon.ico` como erro. Esse nao e defeito da tela; qualquer outro erro e.

## Desculpa -> realidade

| desculpa | realidade |
|---|---|
| "o teste passou" | teste nao ve cor, alinhamento nem texto cortado |
| "e so CSS" | mudanca de CSS tambem muda a tela e pode piorar; so olhando se sabe |
| "nao tenho navegador aqui" | tem 3 caminhos no passo 5 |
| "ele testa depois" | o usuario testa uma vez no fim e cada print novo dele e retrabalho dele |
| "a lista ficou boa" | em um projeto o botao cobriu o rotulo dentro do modal; so abrindo o modal aparece |
| "subi, entao mudou" | deploy que nao subiu parece "continua igual"; confira o marcador (passo 9) |

## Roteiros por projeto

Se existir `PROJETOS.md` nesta pasta, leia a linha do projeto; senao, use README/CLAUDE.md do projeto. Um teste de fumaca que so chama a API NAO prova a tela: abra a tela. Regra que vale em todo projeto: abrir cada modal, formulario e lista suspensa tocados, tambem em tela estreita.
