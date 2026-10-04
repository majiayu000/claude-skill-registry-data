---
name: mira-chart-race
description: >-
  Cria um slide de gráfico de corrida no Mira: série temporal animada que corre
  no tempo, toca uma vez e para no fim. Dois modos: "bars" (barras que trocam de
  posição no ranking) e "lines" (linhas desenhadas com o rótulo perseguindo a
  ponta); dados em CSV largo embutidos, roda por file:// offline, gera section em
  D3 v7 no tema do Mira.
  Use SEMPRE que o usuário disser /mira-chart-race, gráfico de corrida, corrida
  de barras, bar chart race, racing chart, gráfico animado no tempo, dados
  temporais animados, ranking ao longo do tempo, barras que mudam de posição,
  linhas crescendo no tempo. Para gráfico estático use /mira-chart; para
  enquete ao vivo use /mira-survey.
---

# Skill: Mira Chart Race, dados temporais viram corrida animada

Pega uma série temporal (vários períodos, várias séries) e devolve um slide onde os dados **correm no tempo**: o período avança, as barras trocam de posição (ou as linhas vão sendo desenhadas) e, ao chegar no fim, para no quadro final (não reinicia). É o gráfico animado de "X ao longo do tempo" (linguagens mais usadas, fatia de mercado, população, etc.).

> **Artefato de referência:** `decks/teste-chart-race/index.html` tem os dois modos com dados de exemplo. O motor abaixo é o mesmo desse arquivo.

## Regras herdadas (obrigatórias)

1. **Idioma**: siga `agents/_shared/idioma.md`. Todo texto visível revisado, acentuação 100% correta. Nenhum travessão.
2. **Cores**: laranja da marca `#FF904D` como primeira cor da paleta; tema `mira-dark`. Nunca roxo como cor principal.
3. **D3 v7**: o motor usa o `d3` global que já vem no `<head>` do deck. Consulte `agents/mira-animator/references/diretrizes-d3.md` se precisar ajustar.
4. **Toca uma vez e para**: entra animando e **para no último período**, sem reiniciar. É uma exceção consciente à regra zero do Mira (loop perpétuo), escolhida para esta skill por ser um gráfico de apresentação.
5. **Output**: salve em `decks/<nome-do-deck>/`. Nunca escreva em fontes vinculadas.

## O modelo mental

O slide recebe **um CSV no formato largo** e transforma cada período num quadro da animação. Sem servidor nem `fetch`: os dados entram **embutidos inline** no `<script>`, então o slide roda por duplo-clique (`file://`) e offline.

| Modo | O que faz | Quando usar |
|---|---|---|
| **`bars`** (padrão) | Corrida de barras horizontais; reordenam por ranking a cada período; relógio grande no canto | Comparar muitas categorias e mostrar quem ultrapassa quem |
| **`lines`** | Linhas desenhadas progressivamente; rótulo (nome + valor) persegue a ponta de cada linha | Mostrar a tendência/evolução de poucas séries contínuas |

## Formato do CSV (largo)

- **Primeira coluna**: o período (rótulo do "relógio"). Pode ser ano (`2004`), trimestre (`2025 Q1`), mês, qualquer texto ordenado. As linhas já devem estar **em ordem cronológica**.
- **Demais colunas**: uma por série. O cabeçalho é o nome que aparece no slide.
- **Célula vazia**: série que ainda não existia naquele período (em `lines`, a linha só começa quando há dado). `0` é um valor real, diferente de vazio.

```
periodo,Java,Python,JavaScript,Rust
2004,34,4,21,
2014,26,13,20,0.3
2025,17,32,18.8,5.3
```

Se o usuário colar uma tabela no chat em vez de um arquivo, monte o CSV a partir dela. Se vier no formato "longo" (`periodo,serie,valor`), faça o pivô para largo antes de seguir.

## Passos

1. **Obter os dados.** Leia o CSV fornecido (Read) ou monte-o da tabela colada. Confirme que a 1ª coluna é o período e as linhas estão em ordem cronológica.
2. **Definir os parâmetros.**
   - `mode`: `bars` ou `lines`. Se o usuário indicou, use; senão escolha pela tabela acima sem travar (barras é o padrão).
   - `topN`: quantas barras por quadro (padrão 12; ignorado em `lines`).
   - `unit`: sufixo dos valores (`%`, ` M`, etc.; vazio se não houver).
   - `decimals`: casas decimais do valor exibido (padrão 1).
   - **Velocidade**: `stepMs` (ms por período, padrão 1400) ou `durationMs` (duração total em ms); se `durationMs` vier, ele tem prioridade e o passo é calculado. Menor = mais rápido.
3. **Montar a section.** Use o "Template da section" abaixo: `<section>` com o palco `.anim-stage`, título/subtítulo e o `<script>` com **motor** + **dados embutidos** + **chamada**.
4. **Salvar.** Grave em `decks/<nome-do-deck>/index.html` (deck novo) ou **insira a section** no `index.html` existente, antes do bloco de controles de slide. O `<head>` do deck já traz D3, Tailwind e o tema; a section é autossuficiente.
5. **Reportar.** Caminho do arquivo, o modo usado, e que o slide roda por `file://`, anima uma vez ao entrar na tela e **para no quadro final**. Para trocar os dados, edite o CSV embutido no `<script>`.

## Template da section (copie e preencha)

Substitua título, subtítulo, `id` do palco, CSV embutido e parâmetros da chamada. Se já houver outro chart-race no deck, **mantenha o motor `miraChartRace` uma vez só** e repita apenas a `<section>` + chamada com `id` e dados próprios.

```html
<!-- ============ SLIDE: CHART RACE ============ -->
<section class="min-h-screen flex flex-col items-center justify-center px-6 py-16">
    <div class="text-center mb-8" data-aos="fade-up">
        <h2 class="text-5xl font-black">[TITULO_DO_SLIDE]</h2>
        <p class="text-soft text-lg mt-3">[SUBTITULO_OU_FONTE]</p>
    </div>
    <div class="glass-card w-full max-w-5xl p-6" data-aos="fade-up">
        <div id="[ID_DO_PALCO]" class="anim-stage"></div>
    </div>
</section>

<script>
    // ===== MOTOR CHART-RACE (D3 v7) — inclua UMA vez por deck =====
    const PALETTE = ['#FF904D', '#4DC4D9', '#7DD957', '#FFD24D', '#FF6B6B', '#5C9DFF', '#FF9EC4', '#B388FF', '#FFB74D', '#4DD0A0', '#E573C7', '#9CCC65'];
    const PRIMARY = getComputedStyle(document.documentElement).getPropertyValue('--mira-primary').trim() || '#FF904D';

    function miraChartRace(cfg) {
        const o = Object.assign({ mode: 'bars', topN: 12, unit: '', decimals: 1, stepMs: 1400 }, cfg);
        const root = d3.select(o.selector);
        if (typeof d3 === 'undefined' || root.empty()) return;

        const rows = d3.csvParse(o.csv.trim());
        const periodKey = rows.columns[0];
        const series = rows.columns.slice(1);
        const periods = rows.map(r => r[periodKey]);
        const n = periods.length;
        const data = rows.map(r => {
            const obj = {};
            series.forEach(s => { const v = r[s]; obj[s] = (v === '' || v == null) ? null : +v; });
            return obj;
        });
        const firstIdx = {};
        series.forEach(s => { firstIdx[s] = data.findIndex(d => d[s] != null); });

        const color = {};
        series.forEach((s, i) => color[s] = PALETTE[i % PALETTE.length]);

        const W = 960, H = 540;
        const svg = root.append('svg').attr('viewBox', `0 0 ${W} ${H}`);
        const fmt = v => d3.format(',.' + o.decimals + 'f')(v) + (o.unit || '');

        // velocidade: stepMs = ms por periodo; durationMs (se vier) define a duracao total e tem prioridade
        const periodMs = (o.durationMs && n > 1) ? o.durationMs / (n - 1) : o.stepMs;
        function posAt(elapsed) { return Math.min(elapsed / periodMs, n - 1); } // avanca uma vez e para no fim

        const frame = o.mode === 'lines' ? buildLines() : buildBars();
        const io = new IntersectionObserver(es => {
            es.forEach(e => {
                if (e.isIntersecting) {
                    let timer = d3.timer(elapsed => { if (frame(elapsed)) timer.stop(); });
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.3 });
        io.observe(root.node());

        function buildBars() {
            const m = { top: 56, right: 110, left: 160, bottom: 22 };
            const N = Math.min(o.topN, series.length);
            const x = d3.scaleLinear().range([m.left, W - m.right]);
            const y = d3.scaleBand().domain(d3.range(N)).range([m.top, H - m.bottom]).padding(0.22);
            const gGrid = svg.append('g'), gAxis = svg.append('g'), gBars = svg.append('g');
            const clock = svg.append('text').attr('x', W - 30).attr('y', H - 26).attr('text-anchor', 'end')
                .attr('font-size', 58).attr('font-weight', 900).attr('fill', PRIMARY).attr('opacity', 0.9);
            let dispMax = 0;
            return function (elapsed) {
                const pos = posAt(elapsed);
                const i = Math.min(Math.floor(pos), n - 1), j = Math.min(i + 1, n - 1), f = pos - i;
                const cur = series.map(s => {
                    const a = data[i][s] || 0, b = data[j][s] || 0;
                    return { name: s, value: a + (b - a) * f };
                }).sort((p, q) => (q.value - p.value) || (p.name < q.name ? -1 : 1));
                cur.forEach((d, r) => d.rank = r);
                const shown = cur.slice(0, N);
                const targetMax = d3.max(shown, d => d.value) || 1;
                dispMax = (dispMax < 1 || pos >= n - 1) ? targetMax : dispMax + (targetMax - dispMax) * 0.12;
                x.domain([0, dispMax]);
                const ticks = x.ticks(5);
                gGrid.selectAll('line').data(ticks).join('line')
                    .attr('x1', d => x(d)).attr('x2', d => x(d)).attr('y1', m.top - 10).attr('y2', H - m.bottom)
                    .attr('stroke', 'rgba(255,255,255,0.08)');
                gAxis.selectAll('text').data(ticks).join('text')
                    .attr('x', d => x(d)).attr('y', m.top - 18).attr('text-anchor', 'middle')
                    .attr('fill', 'rgba(255,255,255,0.4)').attr('font-size', 13).text(d => d3.format('~s')(d));
                gBars.selectAll('g.bar').data(shown, d => d.name).join(enter => {
                    const g = enter.append('g').attr('class', 'bar');
                    g.append('rect').attr('rx', 5).attr('height', y.bandwidth());
                    g.append('text').attr('class', 'nm').attr('text-anchor', 'end').attr('dy', '0.35em');
                    g.append('text').attr('class', 'vl').attr('text-anchor', 'start').attr('dy', '0.35em');
                    return g;
                }).each(function (d) {
                    const g = d3.select(this), cy = y(d.rank) + y.bandwidth() / 2;
                    g.select('rect').attr('x', m.left).attr('y', y(d.rank))
                        .attr('width', Math.max(0, x(d.value) - m.left)).attr('fill', color[d.name]);
                    g.select('.nm').attr('x', m.left - 12).attr('y', cy).attr('fill', '#fff')
                        .attr('font-size', 18).attr('font-weight', 600).text(d.name);
                    g.select('.vl').attr('x', x(d.value) + 10).attr('y', cy).attr('fill', 'rgba(255,255,255,0.85)')
                        .attr('font-size', 17).attr('font-weight', 700).text(fmt(d.value));
                });
                clock.text(periods[Math.round(pos)]);
                return pos >= n - 1; // chegou ao fim: para o timer
            };
        }

        function buildLines() {
            const m = { top: 40, right: 150, left: 56, bottom: 42 };
            const gmax = d3.max(data, d => d3.max(series, s => d[s] || 0));
            const x = d3.scaleLinear().domain([0, n - 1]).range([m.left, W - m.right]);
            const y = d3.scaleLinear().domain([0, gmax]).nice().range([H - m.bottom, m.top]);
            const line = d3.line().x(d => x(d[0])).y(d => y(d[1])).curve(d3.curveMonotoneX);
            const yticks = y.ticks(5);
            svg.append('g').selectAll('line').data(yticks).join('line')
                .attr('x1', m.left).attr('x2', W - m.right).attr('y1', d => y(d)).attr('y2', d => y(d))
                .attr('stroke', 'rgba(255,255,255,0.07)');
            svg.append('g').selectAll('text').data(yticks).join('text')
                .attr('x', m.left - 10).attr('y', d => y(d)).attr('dy', '0.32em').attr('text-anchor', 'end')
                .attr('fill', 'rgba(255,255,255,0.4)').attr('font-size', 12).text(d => d3.format('~s')(d) + (o.unit || ''));
            const step = Math.max(1, Math.ceil(n / 7));
            svg.append('g').selectAll('text').data(d3.range(0, n, step)).join('text')
                .attr('x', d => x(d)).attr('y', H - m.bottom + 22).attr('text-anchor', 'middle')
                .attr('fill', 'rgba(255,255,255,0.4)').attr('font-size', 12).text(d => periods[d]);
            const gLines = svg.append('g'), gDots = svg.append('g'), gLabels = svg.append('g');
            const clock = svg.append('text').attr('x', W - 24).attr('y', m.top + 6).attr('text-anchor', 'end')
                .attr('font-size', 30).attr('font-weight', 900).attr('fill', PRIMARY);
            return function (elapsed) {
                const pos = posAt(elapsed), fi = Math.floor(pos);
                const items = series.map(s => {
                    const start = firstIdx[s];
                    if (start < 0 || pos < start) return null;
                    const pts = [];
                    for (let k = start; k <= Math.min(fi, n - 1); k++) if (data[k][s] != null) pts.push([k, data[k][s]]);
                    if (fi + 1 < n && pos > fi) {
                        const a = data[fi][s], b = data[fi + 1][s];
                        if (a != null && b != null) pts.push([pos, a + (b - a) * (pos - fi)]);
                    }
                    if (!pts.length) return null;
                    return { name: s, pts, head: pts[pts.length - 1] };
                }).filter(Boolean);
                gLines.selectAll('path.ln').data(items, d => d.name)
                    .join(e => e.append('path').attr('class', 'ln').attr('fill', 'none')
                        .attr('stroke-width', 3).attr('stroke-linecap', 'round').attr('stroke-linejoin', 'round'))
                    .attr('stroke', d => color[d.name]).attr('d', d => line(d.pts));
                gDots.selectAll('circle.hd').data(items, d => d.name)
                    .join(e => e.append('circle').attr('class', 'hd').attr('r', 5))
                    .attr('fill', d => color[d.name]).attr('cx', d => x(d.head[0])).attr('cy', d => y(d.head[1]));
                gLabels.selectAll('g.lb').data(items, d => d.name).join(e => {
                    const g = e.append('g').attr('class', 'lb');
                    g.append('text').attr('class', 'n').attr('font-size', 15).attr('font-weight', 700);
                    g.append('text').attr('class', 'v').attr('font-size', 13).attr('dy', '1.25em').attr('fill', 'rgba(255,255,255,0.6)');
                    return g;
                }).each(function (d) {
                    const g = d3.select(this);
                    g.attr('transform', `translate(${x(d.head[0]) + 10},${y(d.head[1])})`);
                    g.select('.n').attr('fill', color[d.name]).text(d.name);
                    g.select('.v').text(fmt(d.head[1]));
                });
                clock.text(periods[Math.round(pos)]);
                return pos >= n - 1; // chegou ao fim: para o timer
            };
        }
    }

    // ===== DADOS + CHAMADA (repita por slide; troque o CSV e os parâmetros) =====
    const CSV_[ID_EM_MAIUSCULAS] = `
[COLE_AQUI_O_CSV_LARGO]
`;
    miraChartRace({ selector: '#[ID_DO_PALCO]', csv: CSV_[ID_EM_MAIUSCULAS], mode: '[bars_OU_lines]', topN: 12, unit: '[UNIDADE_OU_VAZIO]', decimals: 1 });
</script>
```

## Princípios de design

1. **O período é o herói.** O relógio (texto grande no canto) mostra "onde no tempo estamos" e prende o olhar.
2. **A virada conta a história.** Prepare os dados para que a ultrapassagem importante apareça (quem assume a liderança, quando uma série dispara). Em `bars` é o reordenamento; em `lines`, o cruzamento.
3. **Cores estáveis por série.** Cada série mantém a mesma cor do início ao fim (paleta determinística pela ordem das colunas). Laranja da marca primeiro.
4. **Leveza.** Eixos discretos, poucos ticks, números em formato humano (`d3.format('~s')`: 1.2k, não 1200). Sem grade pesada.
5. **Ritmo legível.** `stepMs` entre ~1000 e ~2000 ms por período é confortável; séries muito longas pedem passo mais curto.

## Checklist

- [ ] CSV no formato largo, 1ª coluna = período, linhas em ordem cronológica.
- [ ] Modo escolhido (`bars` padrão; `lines` para tendência de poucas séries) e parâmetros definidos (`topN`, `unit`, `decimals`, ritmo).
- [ ] Dados **embutidos inline** no `<script>` (sem `fetch`); roda por `file://`.
- [ ] Motor `miraChartRace` incluído **uma única vez** por deck; uma `<section>` + chamada por gráfico.
- [ ] Anima uma vez ao entrar na viewport e **para no fim** (não reinicia); relógio mostrando o período.
- [ ] Laranja `#FF904D` como primeira cor; tema escuro; texto revisado, acentuação correta, sem travessão.
- [ ] Salvo em `decks/<deck>/`; nada escrito em fontes vinculadas.
