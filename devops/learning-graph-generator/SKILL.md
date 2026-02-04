---
name: learning-graph-generator
description: Generates a comprehensive learning graph from a course description, including 200 concepts with dependencies, taxonomy categorization, and quality validation reports. Use this when the user wants to create a structured knowledge graph for educational content.
---

# Learning Graph Generator

You are tasked with generating a comprehensive learning graph from a course description. Follow these steps carefully:

## Step 1: Quality Assessment

First, analyze the provided course description to ensure it has enough content to generate 200 high-quality concepts:

1. Verify the course has a title, prerequisites, intended audience, objectives, and outcomes (after this course students will be able to...).  If these fields are missing ask the user for this information.
1. Examine the depth and breadth of topics covered
2. Assess whether the material has sufficient granularity for 200 distinct concepts
3. Check for diverse topic areas and learning objectives
4. Provide detailed feedback to the user about:
   - List the expected content that you found
   - Estimated number of concepts you can derive
   - Compare this concept number with similar courses
   - Describe areas where the course description is strong
   - Any gaps or areas that might be under-represented
   - Suggest how the Bloom 2001 taxonomy could improve the course description
   - Overall quality assessment

5. **Ask the user if you should proceed** with generating the learning graph

## Step 2: Generate Concept Labels

Once approved, generate 200 concept labels from the course content:

**Requirements:**
- Each label must be in Title Case
- Maximum length: 32 characters
- Labels should be clear, specific, and pedagogically sound
- Cover the full breadth of the course material

**Output:**
- Save the numbered list to `/data/course-concepts-v1.md`
- Format: Simple numbered list (1-200) in a markdown file
- Make sure that each number is unique so it can be used as a concept ID
- Inform the user the file has been created
- Tell them you can add or remove concepts if they'd like to review and provide feedback

## Step 3: Generate Dependency Graph

Create a CSV file mapping dependencies between concepts:

**Format:**
- Filename: `/data/concept-dependencies.csv`
- Columns: `ConceptID,ConceptLabel,Dependencies`
- ConceptID: Integer (1-200)
- ConceptLabel: The exact label from Step 2
- Dependencies: Pipe-delimited list of ConceptIDs (e.g., "1|3|7")

**Dependency Rules:**
- Foundational/prerequisite concepts have NO dependencies (empty Dependencies field)
- All other concepts must have at least one dependency
- No concept can depend on itself
- The graph must be a Directed Acyclic Graph (DAG) - no cycles
- Create meaningful learning pathways, not just linear chains
- Consider prerequisite relationships carefully

## Step 4: Quality Validation

Perform comprehensive quality checks on the dependency graph:

1. **Verify DAG structure**: Ensure no cycles exist
2. **Check for self-dependencies**: No concept should depend on itself
3. **Foundational concepts**: Identify concepts with zero dependencies
4. **Orphaned nodes**: Identify concepts that nothing depends on (potential dead ends)
5. **Disconnected subgraphs**: Check if all concepts are connected to the main graph
6. **Linear chains**: Flag if too many concepts only depend on the immediately prior concept
7. **Indegree analysis**: Calculate indegree (number of concepts that depend on each concept)

**Generate quality metrics report:**
- Total concepts with zero dependencies (foundational)
- Total concepts with 1+ dependencies
- Average number of dependencies per concept
- Maximum dependency chain length
- Number of orphaned nodes
- Number of disconnected subgraphs
- Top 10 concepts with highest indegree (most depended-upon concepts)

Save this report to `/data/quality-metrics.md`

## Step 5: Create Concept Taxonomy

Develop a categorical taxonomy for organizing concepts:

**Requirements:**
- Target: ~12 categories (can vary by 2-3 if natural groupings emerge)
- Categories should evenly distribute concepts
- Avoid having any single category exceed 30% of total concepts
- Use clear, descriptive category names
- Create 3-5 letter abbreviations for each category (TaxonomyID)

**Output:**
- Save taxonomy to `/data/concept-taxonomy.md`
- Format as markdown with:
  - Category name
  - TaxonomyID abbreviation
  - Brief description of what concepts belong in this category

## Step 6: Add Taxonomy to CSV

Update the dependencies CSV file:

1. Add a new column: `TaxonomyID`
2. For each concept, assign the best matching TaxonomyID
3. Use "MISC" for concepts without a clear category match
4. Save the updated file to `/data/concept-dependencies.csv`

**Final CSV columns:** `ConceptID,ConceptLabel,Dependencies,TaxonomyID`

## Step 7: Taxonomy Distribution Report

Generate a distribution analysis:

1. Count concepts in each category
2. Calculate percentages
3. Identify over-represented categories (>30%)
4. Suggest alternative categorization if needed

**Output:**
- Save to `/data/taxonomy-distribution.md`
- Format as markdown table with columns:
  - Category Name
  - TaxonomyID
  - Count
  - Percentage

## Step 8: Completion

Inform the user that the learning graph generation is complete! Congratulate them and wish them success on their textbook or course material.

**Files created:**
- `/data/course-concepts-v1.md` - Numbered list of 200 concepts
- `/data/concept-dependencies.csv` - Full dependency graph with taxonomy
- `/data/concept-taxonomy.md` - Category definitions
- `/data/quality-metrics.md` - Quality validation report
- `/data/taxonomy-distribution.md` - Category distribution analysis

---

## Important Notes

- Maintain pedagogical integrity throughout the process
- Dependencies should reflect actual prerequisite knowledge
- Balance between granularity and comprehensiveness
- Ensure concepts build upon each other logically
- The learning graph should support multiple learning pathways, not just one linear path
