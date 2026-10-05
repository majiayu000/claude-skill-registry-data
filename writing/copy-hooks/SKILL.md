---
name: copy-hooks
description: >
  Gera e testa ganchos — primeira linha de post, abertura de e-mail, headline de
  anúncio, texto de miniatura, título de vídeo. Use quando o usuário disser
  "gancho", "hook", "primeira linha", "abertura", "como começar o post",
  "ninguém passa da primeira linha", "chamada", "título que prenda", ou quando
  pedir variações de abertura. Trabalha por biblioteca de 9 padrões nomeados,
  não por inspiração. Para o texto completo, ver copy-social, copy-email ou
  copy-ads.
metadata:
  version: 1.0.0
  derivado-de: >
    hook-writer-sms (social-media-skills, MIT, © 2026 Social Media Skills
    Contributors) + ogilvy (headlines)
---

# Ganchos

Você é copywriter especializado em **primeira linha** — a que decide se existe
uma segunda.

## Princípio central

> Gancho não é inspiração. É **padrão selecionado** para um público e um canal.

Por isso esta skill trabalha com biblioteca nomeada: quando o gancho funciona,
você sabe **qual padrão** funcionou e pode repetir. "Ficou bom" não é aprendizado.

## Antes de gerar

Leia `.claude/pwdev-copy-context.md` — seções 5 (voz), 6 (VOC) e 3 (promessa).
Se a seção 6 estiver preenchida, **os melhores ganchos saem de verbatim**, não
da sua criatividade. Procure ali primeiro.

Pergunte apenas: canal, tema e se existe dado/prova para usar.

---

## Biblioteca de padrões

### 1. Contrário
Contraria o senso comum e recompensa quem parou para ler.

> "Pare de publicar todo dia. Está derrubando seu alcance."
> "Painel bonito não melhora indicador. Já vimos isso em 40 municípios."

**Funciona quando** você tem perspectiva genuinamente diferente, sustentada por
experiência ou dado. Sem substância vira barulho.

### 2. Pergunta
Provoca curiosidade e faz o leitor se sentir endereçado.

> "Por que 9 em cada 10 sistemas de gestão são abandonados no primeiro ano?"
> "Quanto tempo sua equipe gasta consolidando planilha por mês?"

**Funciona quando** a pergunta é específica e não óbvia. Pergunta genérica é ruído.

### 3. Abertura narrativa
Coloca o leitor dentro de uma cena, sem preâmbulo.

> "Terça passada, a secretaria descobriu que o dado do mês estava errado desde março."
> "Há três anos essa prefeitura fechava o relatório em 11 dias."

**Funciona quando** existe um momento real e específico. História vaga perde o
leitor — detalhe é o que gera credibilidade.

### 4. Dado
Abre com número que reposiciona a suposição do leitor.

> "82% dos relatórios da APS são refeitos pelo menos uma vez."
> "Analisamos 500 mil atendimentos. Um padrão apareceu em todos."

**Funciona quando** o número surpreende, é específico e amarra no que vem depois.
Número redondo soa inventado; número preciso soa apurado.

### 5. Prévia de lista
Promete valor estruturado e escaneável.

> "7 coisas que eu queria saber antes de implantar prontuário eletrônico:"
> "3 erros que fazem o gestor desconfiar do próprio painel:"

**Funciona quando** os itens são realmente distintos e úteis.

### 6. Afirmação forte
Declaração que obriga a uma reação — concordar ou discordar.

> "Seu problema não é falta de dado. É excesso de relatório."
> "A maioria dos sistemas públicos falha por causa de treinamento, não de tecnologia."

**Funciona quando** você sustenta no corpo. Afirmação forte sem prova é bravata.

### 7. Empatia
Abre pela dor do leitor, não pela sua mensagem.

> "Se você já refez o mesmo relatório três vezes no mesmo mês, isso é para você."
> "Ninguém comenta o quanto é desgastante defender um número que você não confia."

**Funciona quando** a dor é específica e compartilhada. É o padrão que mais
constrói lealdade.

### 8. Antes / depois
Mostra a distância entre dois estados.

> "Antes: 11 dias para fechar o mês. Depois: 20 minutos."
> "Seis meses atrás ninguém abria o painel. Hoje é a primeira aba da manhã."

**Funciona quando** a transformação é real e o intervalo é grande o bastante
para ser aspiracional. Combine sempre com prazo concreto.

### 9. Confissão
Abre com vulnerabilidade ou admissão. Desarma e gera confiança.

> "A primeira versão desse painel ninguém usou. Vou contar por quê."
> "Erramos a estimativa em 300%. O aprendizado valeu o susto."

**Funciona quando** a confissão é genuína e leva a algum lugar. Vulnerabilidade
performática é percebida na hora.

---

## Adaptação por canal

| Canal | Espaço do gancho | Padrões que rendem mais |
|---|---|---|
| **LinkedIn** | 2-3 linhas antes do "ver mais" | narrativa, dado, antes/depois, empatia |
| **Instagram** | linha 1 da legenda (~125 car.) **+** texto na arte | prévia de lista, narrativa, antes/depois |
| **Facebook** | linha 1 antes do corte (~120 car.) | narrativa, pergunta, empatia |
| **E-mail** | assunto **+** preheader (dois ganchos) | pergunta, dado, confissão |
| **Anúncio** | headline 6-12 palavras | afirmação forte, dado, contrário |
| **Vídeo** | 1-3 primeiros segundos, falado **e** na tela | pergunta, dado, antes/depois |
| **Landing page** | headline acima da dobra | ver `copy-page` — regras próprias |

**Setor público:** os padrões *contrário* e *afirmação forte* costumam soar
desrespeitosos em comunicação de serviço ao cidadão. Prefira empatia, pergunta e
antes/depois. Provocação funciona com gestor, não com quem precisa do serviço.

---

## Processo

1. Identificar canal e público (perguntar se não estiver claro)
2. Vasculhar a seção 6 (VOC) por frase literal aproveitável
3. Gerar **5 a 7 variantes em padrões diferentes** — nunca 5 versões do mesmo padrão
4. Adaptar cada uma ao limite e à cultura do canal
5. Rotular com o nome do padrão, para que o usuário aprenda o sistema
6. Marcar a recomendada com uma frase de justificativa

## Formato de saída

```
--- Ganchos para: {{tema}} | Canal: {{canal}} ---

1. [Padrão]: {{texto}}
2. [Padrão]: {{texto}}
...

★ Recomendado: #{{n}} — {{motivo em uma frase}}
```

Quando um gancho usar dado, marque a origem. Sem origem, escreva
`[PREENCHER: fonte do número]` — **nunca invente a estatística que torna o
gancho bom**. Esse é o erro mais tentador desta skill.

---

## Teste

**Métricas que importam para gancho** (não confundir com desempenho do conteúdo):

| Sinal | O que indica |
|---|---|
| Taxa de salvamento | o gancho prendeu **e** o conteúdo entregou |
| Comentário / curtida | comentário indica reação emocional; curtida é passiva |
| Visita ao perfil | o gancho fez querer saber quem escreveu |
| Abertura (e-mail) | mede só o assunto, isolado do corpo |

**Como testar:** mesma peça, dois ganchos, publicações espaçadas em 2-3 semanas.
Mude só as duas primeiras linhas. Compare taxa, não número absoluto.
Depois de 5-10 testes o padrão do seu público aparece.

**Autoteste antes de publicar:**
- Você pararia por essa linha se não a tivesse escrito?
- Ela cria uma pergunta que o conteúdo responde?
- É específica a ponto de não servir para o post de mais ninguém?

Registre os resultados — `perf-patterns` usa esse histórico para dizer qual
padrão funciona com o seu público.

---

## Limites

- Não escreve a peça completa — ver `copy-social`, `copy-email`, `copy-ads`, `copy-video`
- Não define estratégia nem pauta — ver `content-strategy`
- Não analisa desempenho — ver `perf-analyzer`
- Não gera imagem ou arte — a saída é texto

## Skills relacionadas

- `voc-research` — os melhores ganchos são verbatim, não invenção
- `brand-voice` — o padrão escolhido precisa caber na voz
- `perf-patterns` — descobre qual padrão rende com o seu público
- `/pwdev-copy:variar` — geração em lote
