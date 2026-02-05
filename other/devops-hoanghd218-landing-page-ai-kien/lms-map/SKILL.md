---
name: lms-map
description: NWEA MAP Growth assessment data integration for KCIS LMS. Use this skill when implementing MAP assessment features including data import from CDF CSV, displaying student RIT scores, tracking growth trends across terms, showing goal area performance, benchmark classification (E1/E2/E3), and group statistics for Reading and Language Usage courses (G3-G6).
---

# NWEA MAP Growth - KCIS LMS

## Quick Reference

| Item            | Value                                    |
| --------------- | ---------------------------------------- |
| **Grades**      | G3, G4, G5, G6                           |
| **Courses**     | Reading, Language Usage                  |
| **Terms**       | Fall, Spring (per academic year)         |
| **Student ID**  | `LE12001` format (school student number) |
| **Data Source** | CDF (Combined Data File) CSV             |

## Core Concepts

### Benchmark Classification (E1/E2/E3)

Students are classified based on **Spring semester Average RIT score**:

- **Average** = (Language Usage RIT + Reading RIT) / 2
- Classification used for **next year's English Level placement**
- E1 (Advanced), E2 (Intermediate), E3 (Developing)

→ See: [references/benchmarks.md](references/benchmarks.md)

### Growth Index

| Growth Type   | Time Span | Data Source  | Displayed Metrics                              |
| ------------- | --------- | ------------ | ---------------------------------------------- |
| Fall → Spring | ~6 months | Official CDF | Growth, Expected, Index, Met/Not Met, Quintile |
| Spring → Fall | ~4 months | Calculated   | Growth only (no official benchmark)            |

- Index = Actual Growth ÷ Expected Growth
- Index ≥ 1.0 means met or exceeded expectations

→ See: [references/growth.md](references/growth.md)

### NWEA Norms

National percentile reference values by grade and term for comparison.

→ See: [references/norms.md](references/norms.md)
→ **Technical Manual**: [../map-growth-norms-2025/SKILL.md](../map-growth-norms-2025/SKILL.md)

### Conditional Growth Percentile (cGP)

成長百分位數是 NWEA 官方方法（Technical Manual Section 3.3.2-3.3.3），基於起始 RIT 的「條件分佈」，用於公平評估學生成長表現。

**Growth Index vs Growth Percentile (cGP)**:

| 指標 | Growth Index (成長指數) | Growth Percentile (cGP) |
|------|------------------------|-------------------------|
| 來源 | CDF 報告欄位 | **Technical Manual 3.3.3** |
| 公式 | Actual Growth ÷ Expected Growth | 條件正態分佈 Φ(z) |
| 用途 | 快速判斷是否達標 (Index ≥ 1.0) | 公平比較不同起點學生 (Percentile 1-99) |
| 優點 | 簡單直觀 | 考慮 regression to mean 效應 |
| 欄位 | `conditional_growth_index` | 本地計算 |

→ See: `lib/map/conditional-growth.ts`
→ See: `lib/map/growth-params.ts`
→ See: [references/glossary.md](references/glossary.md)

## Data Flow

```
1. Import   : CDF CSV → map_assessments table
2. Link     : Match student_number → students.id
3. Analyze  : Group by English Level, calculate averages
4. Display  : Student page + Stats page
```

## Key Files

| Purpose                | Location                              |
| ---------------------- | ------------------------------------- |
| **Import Script**      | `scripts/import-map-cdf.ts`           |
| **Database Types**     | `types/database.ts` (map_assessments) |
| **Student API**        | `lib/api/map-student-analytics.ts`    |
| **Stats API**          | `lib/api/map-analytics.ts`            |
| **Chart Components**   | `components/map/charts/`              |
| **Student Components** | `components/map/student/`             |
| **Color Constants**    | `lib/map/colors.ts`                   |
| **Utility Functions**  | `lib/map/utils.ts`                    |
| **Norm Lookup**        | `lib/map/norms.ts`                    |

## Pages

### Stats Page (`/browse/stats/map`)

Group-level analysis with tabs:

- **School**: Cross-grade (G3-G6) school-wide performance analysis
- **Grades**: (formerly Overview) Growth trend charts by English Level (Grid/Single view toggle)
- **Growth**: Growth analysis with period selector, cross-grade comparison, class comparison (v1.66.1+)
- **Goals**: Goal area performance (Radar + Table)
- **Lexile**: Reading level distribution
- **Quality**: Rapid guessing analysis
- **Transitions**: Benchmark level transitions

### Growth Tab Components (v1.66.1+)

| Component                   | File                                                | Description                                   |
| --------------------------- | --------------------------------------------------- | --------------------------------------------- |
| **GrowthPeriodSelector**    | `components/map/growth/GrowthPeriodSelector.tsx`    | Dropdown for selecting growth period          |
| **GrowthContextBanner**     | `components/map/growth/GrowthContextBanner.tsx`     | Shows current period, student count, benchmark status |
| **CrossGradeGrowthChart**   | `components/map/growth/CrossGradeGrowthChart.tsx`   | Bar chart comparing G3-G6 Growth Index        |
| **GrowthSpotlight**         | `components/map/growth/GrowthSpotlight.tsx`         | Student-level growth details with cGP         |
| **ClassComparisonTable**    | `components/map/growth/ClassComparisonTable.tsx`    | Sortable table comparing classes              |

**API Functions** (`lib/api/map-growth-analytics.ts`):

- `getCrossGradeGrowth()` - Cross-grade growth index comparison
- `getGrowthSpotlight()` - Student-level growth data with cGP
- `getClassComparison()` - Class-level comparison

**Key Features**:

- Dynamic period selection (Within-Year, Year-over-Year, Summer)
- `isGraduated` field for historical G6 students
- cGP (Conditional Growth Percentile) display
- Quintile-based color coding

### School Tab Components (v1.65+)

| Component                   | File                                                | Description                                   |
| --------------------------- | --------------------------------------------------- | --------------------------------------------- |
| **SchoolTab**               | `components/map/school/SchoolTab.tsx`               | Main tab container with term/course selectors |
| **CrossGradeChart**         | `components/map/school/CrossGradeChart.tsx`         | Line chart comparing G3-G6 RIT vs NWEA Norm   |
| **SchoolSummaryTable**      | `components/map/school/SchoolSummaryTable.tsx`      | Statistics table with vs Norm indicators      |
| **GrowthDistributionChart** | `components/map/school/GrowthDistributionChart.tsx` | Fall-to-Fall growth histogram                 |
| **RitGrowthScatterChart**   | `components/map/school/RitGrowthScatterChart.tsx`   | Starting RIT vs Growth correlation            |

**API Functions** (`lib/api/map-school-analytics.ts`):

- `getCrossGradeStats()` - Cross-grade RIT statistics
- `getAvailableSchoolTerms()` - Available terms (newest first)
- `getSchoolGrowthDistribution()` - Growth distribution buckets
- `getRitGrowthScatterData()` - Scatter plot data with correlation

**Key Features**:

- Grade selector shows "All Grades" when School tab active
- Dynamic Fall term detection for growth analysis
- Pearson correlation coefficient for ceiling effect detection
- Colors: KCISLK=green (#16a34a), Norm=gray (#64748b)

**Chart Features** (v1.64.0):

- Full-width line charts with end-point labels
- Hybrid view mode: Grid (3 charts) / Single (tabbed)
- Norm reference line (dashed)
- Enhanced tooltip with color indicators

### Student Page (`/student/[id]` → MAP Tab)

Individual student analysis with 4 collapsible sections:

1. **Current Performance**: Score cards, benchmark status, test validity
2. **Growth & Progress**: Progress charts, growth index, projections, peer comparison
3. **Instructional Focus**: Goal areas, Lexile level
4. **Historical Data**: Benchmark history, raw assessment tables

## Import Command

```bash
# Dry run
npx tsx scripts/import-map-cdf.ts \
  --file="Kang Chiao International School--Linkou Campus.csv" \
  --dry-run --verbose

# Production import
npx tsx scripts/import-map-cdf.ts \
  --file="Kang Chiao International School--Linkou Campus.csv"
```

## References

| Topic           | File                                                     |
| --------------- | -------------------------------------------------------- |
| Data Import     | [references/data-import.md](references/data-import.md)   |
| Database Schema | [references/database.md](references/database.md)         |
| Benchmark Rules | [references/benchmarks.md](references/benchmarks.md)     |
| NWEA Norms      | [references/norms.md](references/norms.md)               |
| Growth Logic    | [references/growth.md](references/growth.md)             |
| Chart Specs     | [references/charts.md](references/charts.md)             |
| Student Page    | [references/student-page.md](references/student-page.md) |
| **School Tab**  | [references/school-tab.md](references/school-tab.md)     |
| **Glossary**    | [references/glossary.md](references/glossary.md)         |
