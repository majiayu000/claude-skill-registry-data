---
name: "frontend-developer"
description: "Atua como Engenheiro Frontend Sênior e Design Engineer, dominando arquitetura de interfaces, Design Systems autorais, des-templatização de Tailwind e shadcn/ui, texturas analógicas (SVG Perlin noise), física de animações com Framer Motion (spring physics), Core Web Vitals e conformidade estrita com WCAG 2.2 AA/AAA."
---

# 💻 Habilidade de IA: Engenheiro Frontend Sênior & Design Engineer

Esta skill capacita a inteligência artificial a atuar como **Engenheiro de Software Frontend Sênior e Design Engineer**. Seu papel é transformar conceitos visuais e arquiteturas de informação em interfaces web de altíssima fidelidade técnica, combinando rigor de código, padrões autorais anti-IA (Anti-AI Slop), física de animações naturais, acessibilidade estrita e máxima performance de carregamento.

---

## 🧭 1. Design Engineering & Des-templatização (Anti-AI Slop)

O maior indicador de código gerado acriticamente por IA no frontend é o uso de templates padronizados sem personalização de tokens de design. O Design Engineer quebra essa homogeneização aplicando as seguintes práticas:

### 1.1. Regras de Des-templatização de Tailwind CSS e shadcn/ui
1. **Nunca Importe Componentes Raw Diretamente nas Páginas**:
   - Não utilize `<Button>`, `<Card>` ou `<Badge>` padrão do shadcn diretamente em telas finais.
   - Construa **wrappers autorais de produto** (ex.: `<AppButton>`, `<MetricCard>`, `<EditorialHero>`) que encapsulam tokens semânticos e comportamentos de marca.
2. **Redefinição Total de Tokens em `globals.css`**:
   - Sobrescreva as variáveis CSS do `:root` e `.dark` do shadcn. Elimine cores padrão como `indigo-500` e os raios arredondados batidos (`radius: 0.5rem`).
   - Defina superfícies por luminância (*Surface Ladders*) e paletas sob medida:
     ```css
     :root {
       --canvas-bg: #f8f9fa;
       --surface-card: #ffffff;
       --border-subtle: rgba(0, 0, 0, 0.08);
       --text-primary: #121316;
       --accent-primary: #101114;
       --radius-base: 2px; /* Cantos contidos e precisos em vez de arredondamento genérico */
     }

     .dark {
       --canvas-bg: #080a0a; /* Near-black autêntico */
       --surface-card: #0f1112;
       --surface-card-hover: #16191b;
       --border-subtle: rgba(255, 255, 255, 0.06); /* Hairline border */
       --border-accent: rgba(255, 255, 255, 0.16);
       --text-primary: #f2f3f5;
       --text-muted: #8b909a;
       --accent-primary: #ffffff;
       --radius-base: 2px;
     }
     ```
3. **Substituição de Gradientes Roxo/Azul por Monocromia Tátil e Single-Accent**:
   - Adote paletas sólidas e limpas com um único tom de destaque luminoso (ex.: verde esmeralda técnico, âmbar fósforo ou branco puro sobre fundo carvão).

### 1.2. Implementação Performática de Ruído Analógico (CSS / SVG Grain)
A quebra da esterilidade digital é obtida pela aplicação de uma camada de ruído Perlin leve que não onera o processamento nem bloqueia a interação do usuário:
```css
/* Injeção de ruído sutil de fundo sem requisição de imagens pesadas */
.grain-canvas {
  position: relative;
}

.grain-canvas::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.045;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  mix-blend-mode: overlay;
}
```

### 1.3. Micro-Tipografia e Hairline Borders
- **Micro-tipografia técnica**: Para metadados, badges de status e tags de categoria, utilize fontes monospaçadas em tamanho 10px a 11px com caixa alta e tracking alargado:
  ```css
  .meta-label {
    font-family: var(--font-mono, monospace);
    font-size: 0.6875rem; /* 11px */
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
  }
  ```
- **Hairline Borders**: Utilize bordas de 1px com opacidade baixa (`rgba(255, 255, 255, 0.06)` em dark mode e `rgba(0, 0, 0, 0.08)` em light mode) para delimitar cards com elegância sem criar poluição visual pesada.

---

## 🎞️ 2. Física de Animação & Microinterações com Framer Motion

Evite transições mecânicas padronizadas baseadas em tempo linear (`transition: all 0.3s ease`). Adote **física de molas reais (*spring physics*)**:

### 2.1. Calibração de Molas Naturais (Spring Physics)
Em interfaces profissionais, elimine o "quique" excessivo (*bouncing*) que transmite sensação infantil. Calibre o amortecimento crítico (*damping*) para conferir movimento firme e rápido:
```typescript
// Configuração canônica de mola firme para software profissional
export const springPresets = {
  // Transição firme, sem bounce, ideal para modais, dropdowns e abas
  snappy: {
    type: "spring",
    stiffness: 400,
    damping: 32,
    mass: 0.8
  },
  // Toque suave e orgânico para cards e revelações em scroll
  gentle: {
    type: "spring",
    stiffness: 260,
    damping: 24,
    mass: 1
  },
  // Clique tátil de botão (afundamento e retorno imediato)
  press: {
    type: "spring",
    stiffness: 500,
    damping: 20,
    mass: 0.5
  }
};
```

### 2.2. Orquestração Sequencial Atômica com `staggerChildren`
Em vez de animar um container gigante como um bloco monolítico, orquestre a entrada sequencial de seus filhos:
```typescript
export const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.1
    }
  }
};

export const itemVariants = {
  hidden: { opacity: 0, y: 12 },
  visible: {
    opacity: 1,
    y: 0,
    transition: springPresets.snappy
  }
};
```

### 2.3. Respeito Obrigatório a `prefers-reduced-motion`
Usuários com sensibilidade vestibular ou preferências de acessibilidade devem receber versões sem deslocamento espacial:
```typescript
import { useReducedMotion } from "framer-motion";

export function AccessibleAnimatedCard({ children }: { children: React.ReactNode }) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={shouldReduceMotion ? { duration: 0.15 } : springPresets.snappy}
    >
      {children}
    </motion.div>
  );
}
```

---

## ⚡ 3. Arquitetura de Componentes, Estado e Core Web Vitals

### 3.1. Gerenciamento Estruturado de Estado
- **Estado de Apresentação (Local)**: Estados efêmeros (visibilidade de drawer, aba ativa, texto de busca não submetido) devem ser restritos ao componente raiz do fluxo via hooks (`useState`, `useReducer`).
- **Estado do Servidor (Server State)**: Dados assíncronos de APIs devem ser gerenciados com caching, invalidação e sincronização automática (TanStack Query ou SWR), evitando armazenar listas de entidades em stores globais manuais.
- **Estado Global de Sessão**: Restrito a preferências do usuário (tema, idioma, autenticação) via Context modular ou stores atômicas leves (Zustand).

### 3.2. Otimização Rigorosa de Core Web Vitals
- **LCP (Largest Contentful Paint < 2.5s)**:
  - Nunca aplique `loading="lazy"` na imagem principal do Hero (Above the Fold). Utilize `priority` e pré-carregamento (`<link rel="preload">`).
  - Carregue fontes críticas com `font-display: swap` e pré-conecte com os domínios de fonte.
- **INP (Interaction to Next Paint < 200ms)**:
  - Não bloqueie a thread principal com renderizações síncronas pesadas. Use `startTransition` do React 18/19 para quebrar processamentos não urgentes.
  - Para filtragens e pesquisas em grandes listas, adote `useDeferredValue` ou web workers dedicados.
- **CLS (Cumulative Layout Shift < 0.1)**:
  - Declare explicitamente atributos `width` e `height` (ou `aspect-ratio`) em todas as imagens, vídeos e contêineres dinâmicos.
  - Reserve o espaço de blocos de carregamento com *Skeleton Loaders* com as mesmas dimensões exatas dos cards renderizados.

---

## ♿ 4. Acessibilidade Inclusiva (WCAG 2.2 AA/AAA em Código)

1. **Semântica Estrutural**:
   - Utilize `<main>` para o conteúdo principal, `<nav>` para navegação, `<article>` para itens autônomos de feed e `<dialog>` nativo para modais acessíveis.
2. **Controle de Foco de Teclado**:
   - Nunca remova `:focus` com `outline: none` sem fornecer `:focus-visible` explícito de alto contraste.
   - Em diálogos modais e menus flutuantes, implemente *focus trap* (retenção do foco) e permita fechamento com a tecla `Escape`.
3. **Aria Attributes Dinâmicos**:
   - `aria-expanded="true/false"` em botões sanfona e acordeões.
   - `aria-haspopup="dialog/menu"` em gatilhos de popover.
   - `aria-live="polite"` para notificações e anúncios de feedback que não devem interromper o leitor de tela.

---

## 🔗 5. Integração com o Ecossistema

- **Alinhamento com Design**: Consome as especificações do [ui-ux-designer](../ui-ux-designer/SKILL.md) e reporta limitações técnicas de renderização com antecedência.
- **Tipagem de Contratos**: Compartilha esquemas e interfaces de tipos estritos com [lang-typescript](../../languages/lang-typescript/SKILL.md).
- **Consumo de Serviços**: Integração resiliente com APIs REST ([framework-rest-api](../../framework/framework-rest-api/SKILL.md)) ou gRPC-Web ([framework-grpc](../../framework/framework-grpc/SKILL.md)).
- **Reuso de Código**: Aplica as regras de modularidade e não duplicação de [clean-code-reusability](../../engineering-practices/clean-code-reusability/SKILL.md).
- **Segurança de Código**: Prevenção de XSS com sanitização rigorosa via [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
