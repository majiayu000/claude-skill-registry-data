---
name: design-system-governance
description: Detect and track design token drift between Figma design systems and code implementations - report-only skill that identifies inconsistencies and creates wrangler issues for resolution
---

# Design System Governance

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: design-system-governance | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: design-system-governance | Auditing design token drift between Figma and codebase
```

This creates an audit trail showing which skills were applied during the session.

## Overview

Use this skill to detect and track design token drift between Figma design systems and code implementations. This is a REPORT-ONLY skill that identifies inconsistencies and creates wrangler issues for resolution, but does not auto-fix tokens.

## When to Use This Skill

Use this skill when:

1. **Periodic governance checks** - Regular audits (weekly/monthly) to ensure design-code alignment
2. **After Figma updates** - Design team publishes new token values in Figma
3. **Before releases** - Pre-deployment verification of design token consistency
4. **Onboarding new projects** - Initial baseline assessment of design system health
5. **Design system migrations** - Tracking progress during token standardization efforts
6. **Post-implementation review** - Verifying developers used correct design tokens

Do NOT use this skill for:
- One-off component styling (use regular development workflow)
- Custom/bespoke designs that intentionally deviate from the system
- Projects without established design systems

## Prerequisites

Before running governance checks, ensure:

1. **Figma design system exists** with published styles/variables
2. **Code tokens are exported** in at least one format (CSS variables, Tailwind config, design tokens JSON)
3. **Figma MCP server is configured** with access to the design file
4. **Token naming conventions are documented** (if custom normalization needed)
5. **Wrangler MCP is initialized** for issue tracking

## Workflow

```
1. Extract Design Tokens from Figma
   ↓
2. Parse Code Token Sources
   ↓
3. Normalize Token Names
   ↓
4. Compare & Detect Drift
   ↓
5. Classify Drift Severity
   ↓
6. Generate Reconciliation Recommendations
   ↓
7. Create Wrangler Issues (one per drift category)
   ↓
8. Update Governance Metadata
```

## Phase 1: Extract Design Tokens from Figma

Use Figma MCP tools to extract tokens from the design file:

### Color Tokens

```typescript
// Extract all color styles
const colorStyles = await mcp__plugin_figma_figma_mcp__get_styles({
  fileKey: "ABC123",
  styleType: "FILL"
});

// Parse into normalized format
const figmaColorTokens = colorStyles.styles.map(style => ({
  name: normalizeTokenName(style.name), // e.g., "primary/500" → "primary-500"
  category: "color",
  value: rgbaToHex(style.fills[0].color),
  source: "figma",
  rawName: style.name,
  nodeId: style.styleId
}));
```

### Typography Tokens

```typescript
// Extract text styles
const textStyles = await mcp__plugin_figma_figma_mcp__get_styles({
  fileKey: "ABC123",
  styleType: "TEXT"
});

// Parse into normalized format
const figmaTypographyTokens = textStyles.styles.map(style => ({
  name: normalizeTokenName(style.name), // e.g., "Heading/H1" → "heading-h1"
  category: "typography",
  value: {
    fontFamily: style.fontFamily,
    fontSize: style.fontSize,
    fontWeight: style.fontWeight,
    lineHeight: style.lineHeight,
    letterSpacing: style.letterSpacing
  },
  source: "figma",
  rawName: style.name,
  nodeId: style.styleId
}));
```

### Spacing/Layout Tokens

```typescript
// Extract layout grid styles (for spacing)
const layoutGrids = await mcp__plugin_figma_figma_mcp__get_styles({
  fileKey: "ABC123",
  styleType: "GRID"
});

// Many teams document spacing in component sets
// Alternative: Parse from specific "Spacing" frame/page
const spacingFrame = await mcp__plugin_figma_figma_mcp__get_file_nodes({
  fileKey: "ABC123",
  nodeIds: ["spacing-frame-id"]
});

const figmaSpacingTokens = parseSpacingFromFrame(spacingFrame);
```

### Border Radius Tokens

```typescript
// Extract effect styles (often includes border radius documentation)
// Note: Figma doesn't have native border radius styles
// Teams typically document these in component instances or dedicated frames

const borderRadiusFrame = await mcp__plugin_figma_figma_mcp__get_file_nodes({
  fileKey: "ABC123",
  nodeIds: ["border-radius-frame-id"]
});

const figmaBorderRadiusTokens = parseBorderRadiusFromFrame(borderRadiusFrame);
```

### Shadow/Effect Tokens

```typescript
// Extract effect styles
const effectStyles = await mcp__plugin_figma_figma_mcp__get_styles({
  fileKey: "ABC123",
  styleType: "EFFECT"
});

const figmaShadowTokens = effectStyles.styles
  .filter(style => style.effects.some(e => e.type === "DROP_SHADOW"))
  .map(style => ({
    name: normalizeTokenName(style.name),
    category: "shadow",
    value: style.effects.find(e => e.type === "DROP_SHADOW"),
    source: "figma",
    rawName: style.name,
    nodeId: style.styleId
  }));
```

## Phase 2: Parse Code Token Sources

Support multiple token formats commonly used in codebases:

### CSS Variables

```typescript
async function parseCSSVariables(filePath: string): Promise<Token[]> {
  const content = await fs.readFile(filePath, 'utf-8');
  const tokens: Token[] = [];

  // Match CSS variable declarations: --token-name: value;
  const cssVarRegex = /--([a-zA-Z0-9-_]+):\s*([^;]+);/g;

  let match;
  while ((match = cssVarRegex.exec(content)) !== null) {
    const [, name, value] = match;
    tokens.push({
      name: normalizeTokenName(name),
      category: inferCategory(name), // e.g., "color-primary" → "color"
      value: value.trim(),
      source: "css",
      rawName: name,
      filePath
    });
  }

  return tokens;
}

// Example: Parse from :root declarations
// :root {
//   --color-primary-500: #3b82f6;
//   --spacing-md: 16px;
//   --font-size-lg: 18px;
// }
```

### Tailwind Config

```typescript
async function parseTailwindConfig(filePath: string): Promise<Token[]> {
  // Import the config (assumes it's JS/TS)
  const config = await import(filePath);
  const tokens: Token[] = [];

  // Parse colors
  if (config.theme?.extend?.colors || config.theme?.colors) {
    const colors = config.theme?.extend?.colors || config.theme?.colors;
    flattenObject(colors, 'color').forEach(({ path, value }) => {
      tokens.push({
        name: normalizeTokenName(path),
        category: 'color',
        value: value,
        source: 'tailwind',
        rawName: path,
        filePath
      });
    });
  }

  // Parse spacing
  if (config.theme?.extend?.spacing || config.theme?.spacing) {
    const spacing = config.theme?.extend?.spacing || config.theme?.spacing;
    flattenObject(spacing, 'spacing').forEach(({ path, value }) => {
      tokens.push({
        name: normalizeTokenName(path),
        category: 'spacing',
        value: value,
        source: 'tailwind',
        rawName: path,
        filePath
      });
    });
  }

  // Parse typography
  if (config.theme?.extend?.fontSize || config.theme?.fontSize) {
    const fontSize = config.theme?.extend?.fontSize || config.theme?.fontSize;
    flattenObject(fontSize, 'fontSize').forEach(({ path, value }) => {
      tokens.push({
        name: normalizeTokenName(path),
        category: 'typography',
        value: value,
        source: 'tailwind',
        rawName: path,
        filePath
      });
    });
  }

  // Parse border radius
  if (config.theme?.extend?.borderRadius || config.theme?.borderRadius) {
    const borderRadius = config.theme?.extend?.borderRadius || config.theme?.borderRadius;
    flattenObject(borderRadius, 'borderRadius').forEach(({ path, value }) => {
      tokens.push({
        name: normalizeTokenName(path),
        category: 'borderRadius',
        value: value,
        source: 'tailwind',
        rawName: path,
        filePath
      });
    });
  }

  // Parse shadows
  if (config.theme?.extend?.boxShadow || config.theme?.boxShadow) {
    const boxShadow = config.theme?.extend?.boxShadow || config.theme?.boxShadow;
    flattenObject(boxShadow, 'boxShadow').forEach(({ path, value }) => {
      tokens.push({
        name: normalizeTokenName(path),
        category: 'shadow',
        value: value,
        source: 'tailwind',
        rawName: path,
        filePath
      });
    });
  }

  return tokens;
}

// Helper: Flatten nested objects into dot-notation paths
function flattenObject(obj: any, prefix: string): Array<{ path: string, value: any }> {
  const result: Array<{ path: string, value: any }> = [];

  function recurse(current: any, path: string[]) {
    if (typeof current === 'object' && current !== null && !Array.isArray(current)) {
      Object.keys(current).forEach(key => {
        recurse(current[key], [...path, key]);
      });
    } else {
      result.push({
        path: path.join('.'),
        value: current
      });
    }
  }

  recurse(obj, [prefix]);
  return result;
}
```

### Design Tokens JSON (W3C Format)

```typescript
async function parseDesignTokensJSON(filePath: string): Promise<Token[]> {
  const content = await fs.readFile(filePath, 'utf-8');
  const tokensData = JSON.parse(content);
  const tokens: Token[] = [];

  function traverse(obj: any, path: string[] = []) {
    for (const [key, value] of Object.entries(obj)) {
      if (value && typeof value === 'object') {
        // Check if this is a token definition (has $value or value)
        if ('$value' in value || 'value' in value) {
          const tokenValue = value.$value || value.value;
          const tokenType = value.$type || value.type || inferCategory(key);

          tokens.push({
            name: normalizeTokenName([...path, key].join('.')),
            category: tokenType,
            value: tokenValue,
            source: 'design-tokens-json',
            rawName: [...path, key].join('.'),
            filePath,
            metadata: {
              description: value.$description || value.description,
              deprecated: value.$deprecated || value.deprecated
            }
          });
        } else {
          // Recurse into nested groups
          traverse(value, [...path, key]);
        }
      }
    }
  }

  traverse(tokensData);
  return tokens;
}

// Example JSON structure:
// {
//   "color": {
//     "primary": {
//       "500": {
//         "$value": "#3b82f6",
//         "$type": "color",
//         "$description": "Primary brand color"
//       }
//     }
//   }
// }
```

### Multi-Source Parsing Strategy

```typescript
async function parseAllCodeTokens(config: {
  cssFiles?: string[];
  tailwindConfig?: string;
  designTokensJSON?: string;
}): Promise<Token[]> {
  const allTokens: Token[] = [];

  // Parse CSS variables
  if (config.cssFiles) {
    for (const file of config.cssFiles) {
      const tokens = await parseCSSVariables(file);
      allTokens.push(...tokens);
    }
  }

  // Parse Tailwind config
  if (config.tailwindConfig) {
    const tokens = await parseTailwindConfig(config.tailwindConfig);
    allTokens.push(...tokens);
  }

  // Parse design tokens JSON
  if (config.designTokensJSON) {
    const tokens = await parseDesignTokensJSON(config.designTokensJSON);
    allTokens.push(...tokens);
  }

  return allTokens;
}
```

## Phase 3: Normalize Token Names

Normalize token names from different sources for accurate comparison:

```typescript
function normalizeTokenName(name: string): string {
  return name
    .toLowerCase()
    // Replace various separators with hyphens
    .replace(/[_\/.]/g, '-')
    // Remove special characters
    .replace(/[^a-z0-9-]/g, '')
    // Collapse multiple hyphens
    .replace(/-+/g, '-')
    // Trim leading/trailing hyphens
    .replace(/^-|-$/g, '');
}

// Examples:
// "Primary/500" → "primary-500"
// "color_primary_500" → "color-primary-500"
// "color.primary.500" → "color-primary-500"
// "Color/Primary/500" → "color-primary-500"
```

### Fuzzy Matching for Renamed Tokens

```typescript
function calculateSimilarity(name1: string, name2: string): number {
  // Levenshtein distance / longest string length
  const distance = levenshteinDistance(name1, name2);
  const maxLength = Math.max(name1.length, name2.length);
  return 1 - (distance / maxLength);
}

function findPotentialRenames(
  figmaToken: Token,
  codeTokens: Token[],
  threshold: number = 0.75
): Token[] {
  return codeTokens
    .filter(codeToken => {
      const similarity = calculateSimilarity(figmaToken.name, codeToken.name);
      return similarity >= threshold && similarity < 1.0; // Not exact match
    })
    .sort((a, b) => {
      const simA = calculateSimilarity(figmaToken.name, a.name);
      const simB = calculateSimilarity(figmaToken.name, b.name);
      return simB - simA; // Descending order
    });
}

// Simple Levenshtein implementation
function levenshteinDistance(str1: string, str2: string): number {
  const matrix: number[][] = [];

  for (let i = 0; i <= str2.length; i++) {
    matrix[i] = [i];
  }

  for (let j = 0; j <= str1.length; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= str2.length; i++) {
    for (let j = 1; j <= str1.length; j++) {
      if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1, // substitution
          matrix[i][j - 1] + 1,     // insertion
          matrix[i - 1][j] + 1      // deletion
        );
      }
    }
  }

  return matrix[str2.length][str1.length];
}
```

## Phase 4: Compare & Detect Drift

Identify all types of drift between Figma and code:

```typescript
interface DriftReport {
  missingInCode: Token[];        // Figma tokens not found in code
  missingInFigma: Token[];       // Code tokens not in Figma
  valueMismatches: TokenMismatch[]; // Same name, different values
  potentialRenames: TokenRename[];  // Fuzzy matches suggesting renames
}

interface TokenMismatch {
  name: string;
  figmaValue: any;
  codeValue: any;
  figmaSource: Token;
  codeSource: Token;
}

interface TokenRename {
  figmaToken: Token;
  possibleCodeTokens: Array<{ token: Token; similarity: number }>;
}

async function detectDrift(
  figmaTokens: Token[],
  codeTokens: Token[]
): Promise<DriftReport> {
  const report: DriftReport = {
    missingInCode: [],
    missingInFigma: [],
    valueMismatches: [],
    potentialRenames: []
  };

  // Create lookup maps
  const figmaMap = new Map(figmaTokens.map(t => [t.name, t]));
  const codeMap = new Map(codeTokens.map(t => [t.name, t]));

  // Detect missing in code
  for (const figmaToken of figmaTokens) {
    if (!codeMap.has(figmaToken.name)) {
      report.missingInCode.push(figmaToken);

      // Check for potential renames
      const potentialMatches = findPotentialRenames(figmaToken, codeTokens);
      if (potentialMatches.length > 0) {
        report.potentialRenames.push({
          figmaToken,
          possibleCodeTokens: potentialMatches.map(token => ({
            token,
            similarity: calculateSimilarity(figmaToken.name, token.name)
          }))
        });
      }
    }
  }

  // Detect missing in Figma
  for (const codeToken of codeTokens) {
    if (!figmaMap.has(codeToken.name)) {
      report.missingInFigma.push(codeToken);
    }
  }

  // Detect value mismatches
  for (const [name, figmaToken] of figmaMap) {
    const codeToken = codeMap.get(name);
    if (codeToken) {
      const valuesMatch = compareTokenValues(figmaToken, codeToken);
      if (!valuesMatch) {
        report.valueMismatches.push({
          name,
          figmaValue: figmaToken.value,
          codeValue: codeToken.value,
          figmaSource: figmaToken,
          codeSource: codeToken
        });
      }
    }
  }

  return report;
}

function compareTokenValues(token1: Token, token2: Token): boolean {
  // Normalize values for comparison
  const val1 = normalizeTokenValue(token1.value, token1.category);
  const val2 = normalizeTokenValue(token2.value, token2.category);

  // Deep equality check
  return JSON.stringify(val1) === JSON.stringify(val2);
}

function normalizeTokenValue(value: any, category: string): any {
  switch (category) {
    case 'color':
      // Normalize colors to hex
      return normalizeColor(value);

    case 'spacing':
    case 'borderRadius':
      // Normalize units (convert rem to px if needed)
      return normalizeLength(value);

    case 'typography':
      // Normalize typography object
      if (typeof value === 'object') {
        return {
          fontFamily: value.fontFamily,
          fontSize: normalizeLength(value.fontSize),
          fontWeight: parseInt(value.fontWeight),
          lineHeight: normalizeLength(value.lineHeight),
          letterSpacing: normalizeLength(value.letterSpacing)
        };
      }
      return value;

    case 'shadow':
      // Normalize shadow values
      return normalizeShadow(value);

    default:
      return value;
  }
}

function normalizeColor(color: string | object): string {
  if (typeof color === 'string') {
    // Convert rgb/rgba to hex
    if (color.startsWith('rgb')) {
      return rgbToHex(color);
    }
    // Ensure lowercase hex
    return color.toLowerCase();
  }

  // RGBA object from Figma
  if (typeof color === 'object' && 'r' in color) {
    return rgbaToHex(color);
  }

  return String(color);
}

function normalizeLength(value: string | number): string {
  if (typeof value === 'number') {
    return `${value}px`;
  }

  // Convert rem to px (assuming 16px base)
  if (value.endsWith('rem')) {
    const rem = parseFloat(value);
    return `${rem * 16}px`;
  }

  return value;
}

function normalizeShadow(shadow: any): string {
  // Normalize shadow to CSS string format
  if (typeof shadow === 'string') {
    return shadow;
  }

  // Figma shadow object
  if (shadow.offset) {
    const { x, y } = shadow.offset;
    const blur = shadow.radius || 0;
    const spread = shadow.spread || 0;
    const color = normalizeColor(shadow.color);
    return `${x}px ${y}px ${blur}px ${spread}px ${color}`;
  }

  return String(shadow);
}
```

## Phase 5: Classify Drift Severity

Classify each drift item by severity and impact:

```typescript
type DriftSeverity = 'critical' | 'high' | 'medium' | 'low';

interface ClassifiedDrift {
  severity: DriftSeverity;
  category: string;
  items: Array<{
    type: 'missing-in-code' | 'missing-in-figma' | 'value-mismatch' | 'potential-rename';
    token: Token | TokenMismatch | TokenRename;
    impact: string;
    recommendation: string;
  }>;
}

function classifyDrift(report: DriftReport): ClassifiedDrift[] {
  const classified: ClassifiedDrift[] = [];

  // Classify missing in code (Figma → Code drift)
  const missingInCodeByCategory = groupBy(report.missingInCode, t => t.category);
  for (const [category, tokens] of Object.entries(missingInCodeByCategory)) {
    const severity = getSeverityForMissingTokens(category, tokens);
    classified.push({
      severity,
      category: `missing-in-code-${category}`,
      items: tokens.map(token => ({
        type: 'missing-in-code',
        token,
        impact: getImpactForMissingInCode(token),
        recommendation: getRecommendationForMissingInCode(token)
      }))
    });
  }

  // Classify missing in Figma (Code → Figma drift)
  const missingInFigmaByCategory = groupBy(report.missingInFigma, t => t.category);
  for (const [category, tokens] of Object.entries(missingInFigmaByCategory)) {
    const severity = 'low'; // Usually lower priority
    classified.push({
      severity,
      category: `missing-in-figma-${category}`,
      items: tokens.map(token => ({
        type: 'missing-in-figma',
        token,
        impact: 'Code uses tokens not documented in design system',
        recommendation: getRecommendationForMissingInFigma(token)
      }))
    });
  }

  // Classify value mismatches
  const mismatchesByCategory = groupBy(
    report.valueMismatches,
    m => m.figmaSource.category
  );
  for (const [category, mismatches] of Object.entries(mismatchesByCategory)) {
    const severity = getSeverityForMismatches(category, mismatches);
    classified.push({
      severity,
      category: `value-mismatch-${category}`,
      items: mismatches.map(mismatch => ({
        type: 'value-mismatch',
        token: mismatch,
        impact: getImpactForMismatch(mismatch),
        recommendation: getRecommendationForMismatch(mismatch)
      }))
    });
  }

  // Classify potential renames
  if (report.potentialRenames.length > 0) {
    classified.push({
      severity: 'medium',
      category: 'potential-renames',
      items: report.potentialRenames.map(rename => ({
        type: 'potential-rename',
        token: rename,
        impact: 'Token may have been renamed, causing confusion',
        recommendation: getRecommendationForRename(rename)
      }))
    });
  }

  return classified;
}

function getSeverityForMissingTokens(category: string, tokens: Token[]): DriftSeverity {
  // Critical: Core brand colors missing
  if (category === 'color' && tokens.some(t => t.name.includes('primary') || t.name.includes('brand'))) {
    return 'critical';
  }

  // High: Many tokens missing (suggests systematic issue)
  if (tokens.length >= 10) {
    return 'high';
  }

  // High: Typography or spacing (affects layout significantly)
  if (category === 'typography' || category === 'spacing') {
    return 'high';
  }

  // Medium: Some tokens missing
  if (tokens.length >= 3) {
    return 'medium';
  }

  // Low: Few tokens missing
  return 'low';
}

function getSeverityForMismatches(category: string, mismatches: TokenMismatch[]): DriftSeverity {
  // Critical: Brand color mismatches
  if (category === 'color' && mismatches.some(m =>
    m.name.includes('primary') || m.name.includes('brand')
  )) {
    return 'critical';
  }

  // High: Many mismatches
  if (mismatches.length >= 10) {
    return 'high';
  }

  // High: Typography mismatches (affects readability)
  if (category === 'typography') {
    return 'high';
  }

  // Medium: Some mismatches
  if (mismatches.length >= 3) {
    return 'medium';
  }

  // Low: Few mismatches
  return 'low';
}

function getImpactForMissingInCode(token: Token): string {
  const impacts = {
    color: 'Developers may use hardcoded values instead of design system colors',
    typography: 'Text styling may be inconsistent across components',
    spacing: 'Layout spacing may not follow design system',
    borderRadius: 'Component roundness may be inconsistent',
    shadow: 'Elevation/depth may not match designs'
  };
  return impacts[token.category] || 'Design token not available in code';
}

function getRecommendationForMissingInCode(token: Token): string {
  const source = token.source === 'figma' ? 'Figma' : 'code';
  return `Add ${token.rawName} to code tokens (value: ${JSON.stringify(token.value)})`;
}

function getRecommendationForMissingInFigma(token: Token): string {
  return `Document ${token.rawName} in Figma design system or remove from code if deprecated`;
}

function getImpactForMismatch(mismatch: TokenMismatch): string {
  return `Implemented value (${JSON.stringify(mismatch.codeValue)}) differs from design (${JSON.stringify(mismatch.figmaValue)})`;
}

function getRecommendationForMismatch(mismatch: TokenMismatch): string {
  return `Update code token ${mismatch.name} to match Figma value: ${JSON.stringify(mismatch.figmaValue)}`;
}

function getRecommendationForRename(rename: TokenRename): string {
  const topMatch = rename.possibleCodeTokens[0];
  return `Verify if ${rename.figmaToken.rawName} was renamed to ${topMatch.token.rawName} (${Math.round(topMatch.similarity * 100)}% similar)`;
}

// Helper: Group array by key function
function groupBy<T>(array: T[], keyFn: (item: T) => string): Record<string, T[]> {
  return array.reduce((acc, item) => {
    const key = keyFn(item);
    if (!acc[key]) acc[key] = [];
    acc[key].push(item);
    return acc;
  }, {} as Record<string, T[]>);
}
```

## Phase 6: Generate Reconciliation Recommendations

Provide actionable recommendations for each sync direction:

```typescript
interface ReconciliationPlan {
  direction: 'figma-to-code' | 'code-to-figma';
  actions: ReconciliationAction[];
}

interface ReconciliationAction {
  type: 'add' | 'update' | 'remove' | 'verify';
  target: 'code' | 'figma';
  tokenName: string;
  currentValue?: any;
  newValue?: any;
  reason: string;
  priority: DriftSeverity;
}

function generateReconciliationPlan(
  classified: ClassifiedDrift[],
  direction: 'figma-to-code' | 'code-to-figma'
): ReconciliationPlan {
  const actions: ReconciliationAction[] = [];

  if (direction === 'figma-to-code') {
    // Figma is source of truth
    for (const drift of classified) {
      for (const item of drift.items) {
        if (item.type === 'missing-in-code') {
          const token = item.token as Token;
          actions.push({
            type: 'add',
            target: 'code',
            tokenName: token.rawName,
            newValue: token.value,
            reason: `Add missing design token from Figma`,
            priority: drift.severity
          });
        } else if (item.type === 'value-mismatch') {
          const mismatch = item.token as TokenMismatch;
          actions.push({
            type: 'update',
            target: 'code',
            tokenName: mismatch.name,
            currentValue: mismatch.codeValue,
            newValue: mismatch.figmaValue,
            reason: `Update code value to match Figma`,
            priority: drift.severity
          });
        } else if (item.type === 'missing-in-figma') {
          const token = item.token as Token;
          actions.push({
            type: 'verify',
            target: 'code',
            tokenName: token.rawName,
            currentValue: token.value,
            reason: `Verify if this code token is deprecated or should be added to Figma`,
            priority: 'low'
          });
        }
      }
    }
  } else {
    // Code is source of truth
    for (const drift of classified) {
      for (const item of drift.items) {
        if (item.type === 'missing-in-figma') {
          const token = item.token as Token;
          actions.push({
            type: 'add',
            target: 'figma',
            tokenName: token.rawName,
            newValue: token.value,
            reason: `Add missing design token to Figma`,
            priority: drift.severity
          });
        } else if (item.type === 'value-mismatch') {
          const mismatch = item.token as TokenMismatch;
          actions.push({
            type: 'update',
            target: 'figma',
            tokenName: mismatch.name,
            currentValue: mismatch.figmaValue,
            newValue: mismatch.codeValue,
            reason: `Update Figma value to match code`,
            priority: drift.severity
          });
        } else if (item.type === 'missing-in-code') {
          const token = item.token as Token;
          actions.push({
            type: 'verify',
            target: 'figma',
            tokenName: token.rawName,
            currentValue: token.value,
            reason: `Verify if this Figma token is deprecated or should be added to code`,
            priority: 'low'
          });
        }
      }
    }
  }

  // Sort by priority (critical → high → medium → low)
  const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
  actions.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);

  return { direction, actions };
}
```

## Phase 7: Create Wrangler Issues

Create one issue per drift category with detailed recommendations:

```typescript
async function createDriftIssues(
  classified: ClassifiedDrift[],
  reconciliationPlan: ReconciliationPlan
): Promise<void> {
  for (const drift of classified) {
    if (drift.items.length === 0) continue;

    const issueTitle = `Design Token Drift: ${drift.category} (${drift.severity})`;

    const issueDescription = formatDriftIssueDescription(drift, reconciliationPlan);

    await mcp__plugin_wrangler_wrangler_mcp__issues_create({
      title: issueTitle,
      description: issueDescription,
      type: 'issue',
      status: 'open',
      priority: drift.severity,
      labels: ['design-system', 'token-drift', drift.category, `sync-${reconciliationPlan.direction}`],
      project: 'Design System Governance',
      wranglerContext: {
        agentId: 'design-governance',
        estimatedEffort: estimateEffort(drift.items.length)
      }
    });
  }
}

function formatDriftIssueDescription(
  drift: ClassifiedDrift,
  reconciliationPlan: ReconciliationPlan
): string {
  const sections: string[] = [];

  // Summary
  sections.push(`## Summary\n`);
  sections.push(`Detected ${drift.items.length} design token drift issue(s) in category: ${drift.category}\n`);
  sections.push(`**Severity**: ${drift.severity}\n`);
  sections.push(`**Sync Direction**: ${reconciliationPlan.direction === 'figma-to-code' ? 'Figma → Code' : 'Code → Figma'}\n`);

  // Drift Details
  sections.push(`## Drift Details\n`);

  for (const item of drift.items) {
    sections.push(`### ${item.type.replace(/-/g, ' ').toUpperCase()}\n`);

    if (item.type === 'missing-in-code') {
      const token = item.token as Token;
      sections.push(`**Token**: \`${token.rawName}\`\n`);
      sections.push(`**Figma Value**: \`${JSON.stringify(token.value)}\`\n`);
      sections.push(`**Impact**: ${item.impact}\n`);
    } else if (item.type === 'missing-in-figma') {
      const token = item.token as Token;
      sections.push(`**Token**: \`${token.rawName}\`\n`);
      sections.push(`**Code Value**: \`${JSON.stringify(token.value)}\`\n`);
      sections.push(`**Source**: \`${token.filePath || token.source}\`\n`);
      sections.push(`**Impact**: ${item.impact}\n`);
    } else if (item.type === 'value-mismatch') {
      const mismatch = item.token as TokenMismatch;
      sections.push(`**Token**: \`${mismatch.name}\`\n`);
      sections.push(`**Figma Value**: \`${JSON.stringify(mismatch.figmaValue)}\`\n`);
      sections.push(`**Code Value**: \`${JSON.stringify(mismatch.codeValue)}\`\n`);
      sections.push(`**Impact**: ${item.impact}\n`);
    } else if (item.type === 'potential-rename') {
      const rename = item.token as TokenRename;
      sections.push(`**Figma Token**: \`${rename.figmaToken.rawName}\`\n`);
      sections.push(`**Possible Code Matches**:\n`);
      for (const match of rename.possibleCodeTokens) {
        sections.push(`- \`${match.token.rawName}\` (${Math.round(match.similarity * 100)}% similar)\n`);
      }
      sections.push(`**Impact**: ${item.impact}\n`);
    }

    sections.push(`\n`);
  }

  // Reconciliation Recommendations
  sections.push(`## Reconciliation Recommendations\n`);

  const relevantActions = reconciliationPlan.actions.filter(action =>
    drift.items.some(item => {
      if (item.type === 'missing-in-code') {
        return action.tokenName === (item.token as Token).rawName;
      } else if (item.type === 'missing-in-figma') {
        return action.tokenName === (item.token as Token).rawName;
      } else if (item.type === 'value-mismatch') {
        return action.tokenName === (item.token as TokenMismatch).name;
      }
      return false;
    })
  );

  for (const action of relevantActions) {
    sections.push(`### ${action.type.toUpperCase()} in ${action.target}\n`);
    sections.push(`**Token**: \`${action.tokenName}\`\n`);
    if (action.currentValue) {
      sections.push(`**Current Value**: \`${JSON.stringify(action.currentValue)}\`\n`);
    }
    if (action.newValue) {
      sections.push(`**New Value**: \`${JSON.stringify(action.newValue)}\`\n`);
    }
    sections.push(`**Reason**: ${action.reason}\n`);
    sections.push(`**Priority**: ${action.priority}\n`);
    sections.push(`\n`);
  }

  // Implementation Steps
  sections.push(`## Implementation Steps\n`);
  sections.push(`1. Review drift details above\n`);
  sections.push(`2. Verify recommendations align with design system strategy\n`);
  sections.push(`3. Update ${reconciliationPlan.direction === 'figma-to-code' ? 'code tokens' : 'Figma styles'} as recommended\n`);
  sections.push(`4. Run governance check again to verify resolution\n`);
  sections.push(`5. Mark this issue as complete\n`);

  return sections.join('');
}

function estimateEffort(itemCount: number): string {
  if (itemCount <= 3) return '30 minutes';
  if (itemCount <= 10) return '1-2 hours';
  if (itemCount <= 30) return '2-4 hours';
  return '1 day';
}
```

## Phase 8: Update Governance Metadata

Track governance check history:

```typescript
interface GovernanceMetadata {
  lastCheckTimestamp: string;
  lastCheckBy: string;
  figmaFileKey: string;
  figmaVersion?: string;
  totalDriftItems: number;
  criticalDriftItems: number;
  highDriftItems: number;
  mediumDriftItems: number;
  lowDriftItems: number;
  syncDirection: 'figma-to-code' | 'code-to-figma';
  issuesCreated: string[]; // Issue IDs
}

async function updateGovernanceMetadata(
  classified: ClassifiedDrift[],
  issueIds: string[],
  config: {
    figmaFileKey: string;
    syncDirection: 'figma-to-code' | 'code-to-figma';
  }
): Promise<void> {
  const metadata: GovernanceMetadata = {
    lastCheckTimestamp: new Date().toISOString(),
    lastCheckBy: 'design-governance-skill',
    figmaFileKey: config.figmaFileKey,
    totalDriftItems: classified.reduce((sum, c) => sum + c.items.length, 0),
    criticalDriftItems: classified.filter(c => c.severity === 'critical').reduce((sum, c) => sum + c.items.length, 0),
    highDriftItems: classified.filter(c => c.severity === 'high').reduce((sum, c) => sum + c.items.length, 0),
    mediumDriftItems: classified.filter(c => c.severity === 'medium').reduce((sum, c) => sum + c.items.length, 0),
    lowDriftItems: classified.filter(c => c.severity === 'low').reduce((sum, c) => sum + c.items.length, 0),
    syncDirection: config.syncDirection,
    issuesCreated: issueIds
  };

  // Store metadata in .wrangler/cache/governance/
  const metadataPath = path.join(
    process.env.WRANGLER_WORKSPACE_ROOT || process.cwd(),
    '.wrangler',
    'cache',
    'governance',
    `design-token-drift-${Date.now()}.json`
  );

  await fs.ensureDir(path.dirname(metadataPath));
  await fs.writeJSON(metadataPath, metadata, { spaces: 2 });

  console.log(`Governance metadata saved to: ${metadataPath}`);
}

async function getLastGovernanceCheck(): Promise<GovernanceMetadata | null> {
  const governanceDir = path.join(
    process.env.WRANGLER_WORKSPACE_ROOT || process.cwd(),
    '.wrangler',
    'cache',
    'governance'
  );

  if (!await fs.pathExists(governanceDir)) {
    return null;
  }

  const files = await fs.readdir(governanceDir);
  const metadataFiles = files
    .filter(f => f.startsWith('design-token-drift-') && f.endsWith('.json'))
    .sort()
    .reverse();

  if (metadataFiles.length === 0) {
    return null;
  }

  const latestFile = path.join(governanceDir, metadataFiles[0]);
  return await fs.readJSON(latestFile);
}
```

## Complete Workflow Implementation

```typescript
async function runDesignSystemGovernance(config: {
  figmaFileKey: string;
  figmaAccessToken?: string;
  codeTokenSources: {
    cssFiles?: string[];
    tailwindConfig?: string;
    designTokensJSON?: string;
  };
  syncDirection: 'figma-to-code' | 'code-to-figma';
  createIssues?: boolean; // Default: true
}): Promise<void> {
  console.log('Starting design system governance check...\n');

  // Phase 1: Extract Figma tokens
  console.log('Phase 1: Extracting design tokens from Figma...');
  const figmaTokens = await extractFigmaTokens(config.figmaFileKey);
  console.log(`Extracted ${figmaTokens.length} tokens from Figma\n`);

  // Phase 2: Parse code tokens
  console.log('Phase 2: Parsing code token sources...');
  const codeTokens = await parseAllCodeTokens(config.codeTokenSources);
  console.log(`Parsed ${codeTokens.length} tokens from code\n`);

  // Phase 3: Normalize (handled in parsing)
  console.log('Phase 3: Normalizing token names...');
  console.log('Token names normalized during parsing\n');

  // Phase 4: Detect drift
  console.log('Phase 4: Detecting drift...');
  const driftReport = await detectDrift(figmaTokens, codeTokens);
  console.log(`Found ${driftReport.missingInCode.length} tokens missing in code`);
  console.log(`Found ${driftReport.missingInFigma.length} tokens missing in Figma`);
  console.log(`Found ${driftReport.valueMismatches.length} value mismatches`);
  console.log(`Found ${driftReport.potentialRenames.length} potential renames\n`);

  // Phase 5: Classify severity
  console.log('Phase 5: Classifying drift severity...');
  const classified = classifyDrift(driftReport);
  console.log(`Classified into ${classified.length} drift categories\n`);

  // Phase 6: Generate reconciliation plan
  console.log('Phase 6: Generating reconciliation recommendations...');
  const reconciliationPlan = generateReconciliationPlan(classified, config.syncDirection);
  console.log(`Generated ${reconciliationPlan.actions.length} reconciliation actions\n`);

  // Phase 7: Create issues
  if (config.createIssues !== false) {
    console.log('Phase 7: Creating wrangler issues...');
    await createDriftIssues(classified, reconciliationPlan);
    console.log(`Created ${classified.length} drift tracking issues\n`);
  }

  // Phase 8: Update metadata
  console.log('Phase 8: Updating governance metadata...');
  const issueIds = classified.map(c => c.category); // Simplified
  await updateGovernanceMetadata(classified, issueIds, {
    figmaFileKey: config.figmaFileKey,
    syncDirection: config.syncDirection
  });
  console.log('Governance metadata updated\n');

  // Summary
  console.log('=== GOVERNANCE CHECK COMPLETE ===\n');
  console.log(`Total drift items: ${classified.reduce((sum, c) => sum + c.items.length, 0)}`);
  console.log(`Critical: ${classified.filter(c => c.severity === 'critical').reduce((sum, c) => sum + c.items.length, 0)}`);
  console.log(`High: ${classified.filter(c => c.severity === 'high').reduce((sum, c) => sum + c.items.length, 0)}`);
  console.log(`Medium: ${classified.filter(c => c.severity === 'medium').reduce((sum, c) => sum + c.items.length, 0)}`);
  console.log(`Low: ${classified.filter(c => c.severity === 'low').reduce((sum, c) => sum + c.items.length, 0)}`);
  console.log(`\nSync direction: ${config.syncDirection === 'figma-to-code' ? 'Figma → Code' : 'Code → Figma'}`);
  console.log(`Issues created: ${config.createIssues !== false ? 'Yes' : 'No'}`);
}
```

## Usage Examples

### Example 1: Figma → Code Sync (Design is source of truth)

```typescript
await runDesignSystemGovernance({
  figmaFileKey: 'ABC123XYZ',
  codeTokenSources: {
    cssFiles: [
      'src/styles/design-tokens.css',
      'src/styles/variables.css'
    ],
    tailwindConfig: 'tailwind.config.js'
  },
  syncDirection: 'figma-to-code',
  createIssues: true
});

// Expected output:
// - Issues created for tokens missing in code
// - Issues created for value mismatches (code should match Figma)
// - Recommendations to add/update code tokens
```

### Example 2: Code → Figma Sync (Code is source of truth)

```typescript
await runDesignSystemGovernance({
  figmaFileKey: 'ABC123XYZ',
  codeTokenSources: {
    designTokensJSON: 'design-tokens/tokens.json'
  },
  syncDirection: 'code-to-figma',
  createIssues: true
});

// Expected output:
// - Issues created for tokens missing in Figma
// - Issues created for value mismatches (Figma should match code)
// - Recommendations to add/update Figma styles
```

### Example 3: Dry Run (Report without creating issues)

```typescript
await runDesignSystemGovernance({
  figmaFileKey: 'ABC123XYZ',
  codeTokenSources: {
    cssFiles: ['src/styles/tokens.css'],
    tailwindConfig: 'tailwind.config.js',
    designTokensJSON: 'tokens/design-tokens.json'
  },
  syncDirection: 'figma-to-code',
  createIssues: false // Just report, don't create issues
});

// Expected output:
// - Console report of all drift
// - Metadata saved for historical tracking
// - No wrangler issues created
```

### Example 4: Scheduled Governance (Weekly Check)

```bash
# Add to cron or GitHub Actions
0 9 * * 1 /path/to/run-governance-check.sh

# run-governance-check.sh
#!/bin/bash
cd /path/to/project
claude-code --execute "
import { runDesignSystemGovernance } from './governance';
await runDesignSystemGovernance({
  figmaFileKey: process.env.FIGMA_FILE_KEY,
  codeTokenSources: {
    cssFiles: ['src/styles/tokens.css'],
    tailwindConfig: 'tailwind.config.js'
  },
  syncDirection: 'figma-to-code',
  createIssues: true
});
"
```

## Best Practices

### 1. Choose the Right Sync Direction

**Figma → Code** when:
- Design team is authoritative for design tokens
- Code is implementation layer
- Designers update tokens in Figma first
- Common in design-led organizations

**Code → Figma** when:
- Engineering maintains design tokens
- Figma is used for visual documentation
- Tokens are generated/computed programmatically
- Common in engineering-led organizations

### 2. Run Governance Checks Regularly

- **Weekly**: Catch drift early
- **Before releases**: Ensure consistency
- **After design updates**: Verify implementation
- **During audits**: Comprehensive health check

### 3. Prioritize Critical Drift First

- **Critical**: Brand colors, primary typography
- **High**: Systematic issues (10+ tokens)
- **Medium**: Secondary tokens, spacing
- **Low**: Edge cases, deprecated tokens

### 4. Document Token Naming Conventions

- Use consistent separators (hyphens recommended)
- Document prefix/suffix conventions
- Maintain naming glossary for custom normalization

### 5. Archive Historical Checks

- Keep governance metadata for trend analysis
- Track improvement over time
- Identify recurring drift patterns

### 6. Coordinate with Design Team

- Communicate governance findings
- Align on source of truth
- Establish token update workflows
- Review potential renames together

## Troubleshooting

### Issue: False Positives in Value Mismatches

**Cause**: Different value representations (e.g., `#3B82F6` vs `rgb(59, 130, 246)`)

**Solution**: Enhance normalization in `compareTokenValues()`:
```typescript
function normalizeColor(color: string): string {
  // Convert all color formats to lowercase hex
  if (color.startsWith('rgb')) {
    return rgbToHex(color).toLowerCase();
  }
  if (color.startsWith('#')) {
    return color.toLowerCase();
  }
  return color;
}
```

### Issue: Tokens Missing Due to Naming Differences

**Cause**: Inconsistent naming conventions between Figma and code

**Solution**: Customize `normalizeTokenName()` for your conventions:
```typescript
function normalizeTokenName(name: string): string {
  return name
    .toLowerCase()
    .replace(/primary color/g, 'primary') // Project-specific normalization
    .replace(/[_\/.]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}
```

### Issue: Too Many Potential Rename Matches

**Cause**: Fuzzy matching threshold too low

**Solution**: Increase similarity threshold:
```typescript
const potentialMatches = findPotentialRenames(figmaToken, codeTokens, 0.85); // Higher threshold
```

### Issue: Governance Check Takes Too Long

**Cause**: Large number of tokens or code files

**Solution**:
- Cache parsed code tokens
- Use parallel processing for file parsing
- Filter to specific token categories

### Issue: Can't Parse Tailwind Config

**Cause**: Dynamic config or unsupported format

**Solution**: Export static tokens:
```javascript
// tailwind.config.js
const tokens = require('./design-tokens.json');
module.exports = {
  theme: {
    extend: tokens
  }
};
```

## Integration with Other Skills

- **design-system-setup**: Initialize design system before governance
- **figma-design-workflow**: Extract designs after governance finds drift
- **systematic-debugging**: Investigate complex drift patterns
- **writing-plans**: Create implementation plans for large-scale token updates

## Success Metrics

Track governance health over time:

- **Drift reduction rate**: Decrease in total drift items week-over-week
- **Time to resolution**: Average time from drift detection to issue closure
- **Critical drift count**: Should trend toward zero
- **Token coverage**: Percentage of Figma tokens in code (or vice versa)
- **Governance frequency**: Regular checks maintained (e.g., weekly)

## Limitations

1. **Report-only**: Does not auto-fix tokens (intentional safety measure)
2. **Manual sync**: Requires human review of recommendations
3. **Single file key**: Checks one Figma file at a time
4. **No component usage tracking**: Doesn't verify which components use drifted tokens
5. **Naming conventions**: Assumes consistent naming (or requires custom normalization)

## Future Enhancements

- Component impact analysis (which components use drifted tokens)
- Auto-fix mode with approval workflow
- Multi-file governance (check multiple Figma files)
- Historical drift trending dashboard
- Integration with CI/CD for automated checks
- Token usage statistics (which tokens are most used)
