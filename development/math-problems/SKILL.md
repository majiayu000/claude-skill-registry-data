---
name: math-problems
description: Create PAES math problems/questions following project patterns. Use when the user wants to add new questions, create question files, or understand question structure.
---

# PAES Math Problems Creation Skill

This skill guides you through creating high-quality PAES mathematics practice questions for the Chilean university entrance exam preparation system.

## When to Use This Skill

Invoke this skill when:
- User asks to "create new questions" or "add math problems"
- User wants to add questions for a specific topic
- User needs help with question formatting or LaTeX
- User asks about difficulty scoring
- User wants to add visualizations to questions

---

# STEP 0: IDENTIFY THE SUBJECT

**Before creating any questions, identify which mathematical subject:**

```
+-------------------------------------------------------------+
|  ALGEBRA (algebra)                                          |
|  Expressions, equations, factoring, functions               |
|  -> Read: .claude/skills/math-problems/subjects/algebra-templates.md |
+-------------------------------------------------------------+
|  NUMEROS (numeros)                                          |
|  Fractions, percentages, decimals, operations, ratios       |
|  -> Read: .claude/skills/math-problems/subjects/numeros-templates.md |
+-------------------------------------------------------------+
|  GEOMETRIA (geometria)                                      |
|  Shapes, areas, volumes, theorems, coordinates              |
|  -> Read: .claude/skills/math-problems/subjects/geometria-templates.md |
+-------------------------------------------------------------+
|  PROBABILIDAD (probabilidad)                                |
|  Probability, statistics, data, graphs, frequency           |
|  -> Read: .claude/skills/math-problems/subjects/probabilidad-templates.md |
+-------------------------------------------------------------+
```

---

# QUESTION STRUCTURE

Every question MUST follow this TypeScript interface:

```typescript
interface Question {
  id: string;                    // Unique ID: 'm1-xxx' or 'm2-xxx'
  topic: string;                 // Display topic name
  level: 'M1' | 'M2';            // PAES competency level
  questionLatex: string;         // Question text with LaTeX
  options: string[];             // 4 answer options (LaTeX)
  correctAnswer: number;         // Index 0-3
  explanation: string;           // Solution explanation (LaTeX)
  difficulty: 'easy' | 'medium' | 'hard' | 'extreme';
  difficultyScore: number;       // 0.0 to 1.0 (fine-grained)
  subject: 'numeros' | 'algebra' | 'geometria' | 'probabilidad';
  operacionBase?: string;        // Base operation (LaTeX) - REQUIRED for algebra
  skills: string[];              // Required skills from taxonomy
  images?: QuestionImage[];      // Optional images
  visualData?: {                 // Optional visualization
    type: 'geometry' | 'graph' | 'table' | 'diagram';
    data: any;
  };
}
```

---

# FILE ORGANIZATION

## Directory Structure
```
lib/questions/
  m1/                           # M1 level questions
    algebra/
      m1-alg-001.ts             # Subsection files
      m1-alg-002.ts
      index.ts                  # Barrel exports
    geometria/
    numeros/
    probabilidad/
  m2/                           # M2 level questions (same structure)
  index.ts                      # Main exports
```

## File Naming Convention
- Pattern: `m{level}-{subject}-{number}.ts`
- Examples: `m1-alg-001.ts`, `m1-geo-002.ts`, `m2-num-003.ts`
- Each file: 15-35 questions per curriculum subsection

## Export Pattern
```typescript
// In m1-alg-001.ts
import { Question } from '../../../types';

/**
 * M1-ALG-001: Lenguaje algebraico y expresiones
 * Chilean PAES Curriculum - Algebra Subsection 001
 *
 * This subsection covers:
 * - Algebraic language and expressions
 * - Variables and constants
 * - Operations with monomials
 */
export const m1Alg001Questions: Question[] = [
  // questions here
];

// In subject index.ts
import { m1Alg001Questions } from './m1-alg-001';
export { m1Alg001Questions } from './m1-alg-001';

export const m1AlgebraQuestions = [
  ...m1Alg001Questions,
  // ...other subsections
];
```

---

# QUESTION CREATION CHECKLIST

## 1. Question Text (questionLatex)
- [ ] Use `\text{}` for narrative text
- [ ] 4-5 sentences real-world context
- [ ] Variables explained IN context
- [ ] NO explicit math operations in narrative
- [ ] All text in Spanish

## 2. Options
- [ ] Exactly 4 options
- [ ] One correct answer
- [ ] Distractors based on common mistakes
- [ ] Similar format across options
- [ ] Pure LaTeX (no $ delimiters)

## 3. Explanation
- [ ] Shows mathematical solution
- [ ] Step-by-step when needed
- [ ] LaTeX formatting for formulas

## 4. Skills
- [ ] 2-5 skills from taxonomy
- [ ] Primary skill first
- [ ] Skills must exist in `lib/skillTaxonomy.ts`

## 5. Difficulty
- [ ] difficulty: 'easy' | 'medium' | 'hard' | 'extreme'
- [ ] difficultyScore: 0.0-1.0 (see difficulty-scoring.md)

---

# VISUALDATA - WHEN TO ADD GRAPHICS

```
Does the question involve...
         |
    +----+----+----+----+
    |         |         |
GEOMETRY  STATISTICS  SETS
    |         |         |
    v         v         v
triangles,  bar/pie    Venn
circles,    charts,    diagrams
rectangles, frequency
angles      tables
    |         |         |
    v         v         v
  type:     type:     type:
'geometry' 'graph'   'diagram'
           'table'
```

## Supported Visualizations

### 1. Geometry (type: 'geometry')
Rendered by GeometryCanvas. Supports: triangle, rectangle, circle, angle, line, polygon.

```typescript
visualData: {
  type: 'geometry',
  data: [
    {
      type: 'triangle',
      points: [
        { x: 50, y: 200, label: 'A' },
        { x: 200, y: 200, label: 'B' },
        { x: 50, y: 80, label: 'C' }
      ],
      labels: { sides: ['8 m', '10 m', '6 m'] },
      dimensions: { showSides: true }
    }
  ]
}
```

### 2. Bar Chart (type: 'graph', chartType: 'bar')
```typescript
visualData: {
  type: 'graph',
  data: {
    chartType: 'bar',
    items: [
      { category: 'Lunes', value: 30 },
      { category: 'Martes', value: 45 },
      { category: 'Miercoles', value: 35 }
    ],
    showValues: true,
    showLabels: true
  }
}
```

### 3. Pie Chart (type: 'graph', chartType: 'pie')
```typescript
visualData: {
  type: 'graph',
  data: {
    chartType: 'pie',
    items: [
      { category: 'Futbol', value: 40, color: '#3B82F6' },
      { category: 'Basquet', value: 25, color: '#10B981' },
      { category: 'Tenis', value: 15, color: '#F59E0B' }
    ],
    showLegend: true,
    showPercentages: true
  }
}
```

### 4. Frequency Table (type: 'table')
```typescript
visualData: {
  type: 'table',
  data: {
    items: [
      { category: 'Rojo', frequency: 8 },
      { category: 'Azul', frequency: 12 },
      { category: 'Verde', frequency: 5 }
    ],
    showTally: true,
    showRelative: true,
    showPercentage: false
  }
}
```

### 5. Venn Diagram (type: 'diagram', diagramType: 'venn')
```typescript
visualData: {
  type: 'diagram',
  data: {
    diagramType: 'venn',
    mode: 'overlapping',  // or 'exclusive'
    labelA: 'Futbol',
    labelB: 'Basquet',
    countA: 15,
    countB: 10,
    countBoth: 5,
    showCounts: true
  }
}
```

**For complete templates, see:** `.claude/skills/math-problems/visualdata-templates.md`

---

# EXAMPLE: COMPLETE QUESTION

```typescript
{
  id: 'm1-geo-visual-1',
  level: 'M1',
  topic: 'Geometria',
  subject: 'geometria',
  operacionBase: 'c^2 = a^2 + b^2',
  questionLatex: '\\text{Una empresa de construccion esta instalando cables de soporte para una antena de telecomunicaciones. El cable debe conectar la punta de la antena con un punto de anclaje en el suelo. Los ingenieros midieron que el anclaje esta a 6 metros de la base de la antena, y la altura de la antena es de 8 metros. Para solicitar el cable correcto al proveedor, necesitan calcular la longitud exacta del cable de soporte. Cuantos metros de cable necesitan?}',
  options: ['9 m', '10 m', '12 m', '14 m'],
  correctAnswer: 1,
  explanation: 'c^2 = a^2 + b^2 = 6^2 + 8^2 = 36 + 64 = 100 \\quad \\Rightarrow \\quad c = \\sqrt{100} = 10 \\text{ m}',
  difficulty: 'easy',
  difficultyScore: 0.28,
  skills: ['geometria-triangulos', 'geometria-pitagoras', 'numeros-raices', 'numeros-potencias'],
  visualData: {
    type: 'geometry',
    data: [
      {
        type: 'triangle',
        points: [
          { x: 50, y: 200, label: 'A' },
          { x: 200, y: 200, label: 'B' },
          { x: 50, y: 80, label: 'C' }
        ],
        labels: { sides: ['8 m', '10 m', '6 m'] },
        dimensions: { showSides: true }
      }
    ]
  }
}
```

---

# ANTI-PATTERN QUICK CHECKS

Before completing, verify:
- [ ] No explicit math in narrative (wrong: "calcular 3x + 5")
- [ ] difficultyScore matches difficulty level
- [ ] All skills exist in `lib/skillTaxonomy.ts`
- [ ] ID is unique across all question files
- [ ] Options have similar format/length
- [ ] Explanation shows actual solution
- [ ] Algebra questions have operacionBase

**Read anti-patterns guide:** `.claude/skills/math-problems/anti-patterns.md`

---

# RELATED FILES

| Document | Purpose |
|----------|---------|
| `anti-patterns.md` | Common mistakes to avoid |
| `difficulty-scoring.md` | How to assign difficultyScore |
| `skills-reference.md` | Complete skills taxonomy |
| `visualdata-templates.md` | All visualization templates |
| `subjects/*.md` | Subject-specific templates |

---

# QUICK REFERENCE

## Difficulty Score Ranges
| Level | Score Range |
|-------|-------------|
| easy | 0.15-0.35 |
| medium | 0.36-0.55 |
| hard | 0.56-0.75 |
| extreme | 0.76-1.0 |

## Common Topics by Subject
| Subject | Topic String |
|---------|-------------|
| numeros | 'Numeros' |
| algebra | 'Algebra y Funciones' |
| geometria | 'Geometria' |
| probabilidad | 'Probabilidad y Estadistica' |

## Exemplar Question Files
- `lib/questions/m1/algebra/m1-alg-001.ts` - Algebra patterns
- `lib/questions/m1/geometria/m1-geo-001.ts` - Geometry with visualData
- `lib/questions/m1/probabilidad/m1-prob-001.ts` - Statistics patterns

## Key Source Files
- Question interface: `lib/types/core.ts`
- Skills taxonomy: `lib/skillTaxonomy.ts`
- Style guide: `lib/questions/FORMATO_PREGUNTAS_PAES.md`
- GeometryCanvas: `components/math/GeometryCanvas.tsx`
- QuestionRenderer: `components/quiz/QuestionRenderer.tsx`
