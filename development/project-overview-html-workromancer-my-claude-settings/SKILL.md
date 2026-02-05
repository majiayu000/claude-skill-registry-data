---
name: project-overview-html
description: Creates interactive HTML visualizations of project structure, dependencies, and statistics. Use when the user asks to visualize the project, create a project overview, or generate an HTML dashboard of the codebase.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
---

# Project Overview HTML Generator

Generate beautiful, interactive HTML visualizations of project structure and statistics.

## Instructions

When creating a project overview HTML:

1. **Gather project information:**
   - Run `git log --oneline -10` for recent commits
   - Use `find . -type f | head -100` or Glob to understand project structure
   - Check for package.json, requirements.txt, Cargo.toml, etc. for dependencies
   - Read README.md if it exists
   - Get file type statistics with: `find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20`

2. **Create an interactive HTML file** with these sections:
   - **Header**: Project name and description
   - **Quick Stats**: Total files, directories, lines of code, contributors
   - **Directory Tree**: Visual tree structure (collapsible)
   - **File Type Breakdown**: Chart showing language/file type distribution
   - **Dependencies**: List of main dependencies if applicable
   - **Recent Activity**: Git commit timeline
   - **README Content**: Rendered markdown from README

3. **Styling and interactivity:**
   - Use modern CSS with gradients, shadows, and smooth transitions
   - Include Chart.js or similar for data visualization
   - Make tree view collapsible with JavaScript
   - Use a dark/light theme toggle
   - Responsive design for mobile and desktop
   - Add smooth scroll animations

4. **Technical requirements:**
   - Single self-contained HTML file (inline CSS and JS)
   - No external dependencies required to view
   - Works offline
   - Fast loading with optimized code

## HTML Template Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Overview - [PROJECT_NAME]</title>
    <style>
        /* Modern CSS with variables for theming */
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            padding: 3rem 0;
            background: linear-gradient(135deg, var(--accent), #8b5cf6);
            border-radius: 1rem;
            margin-bottom: 2rem;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .stat-card {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 0.5rem;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
        }
        
        .section {
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 0.5rem;
            margin: 2rem 0;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .tree-item {
            cursor: pointer;
            padding: 0.25rem 0;
            user-select: none;
        }
        
        .tree-item:hover {
            color: var(--accent);
        }
        
        .collapsible {
            display: none;
            padding-left: 1.5rem;
        }
        
        .collapsible.active {
            display: block;
        }
        
        canvas {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <!-- Content sections go here -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        // Collapsible tree functionality
        // Chart.js visualizations
        // Theme toggle
    </script>
</body>
</html>
```

## Data Visualization

Use Chart.js for:
- **Pie chart**: File type distribution
- **Bar chart**: Lines of code by language
- **Line chart**: Commit activity over time
- **Doughnut chart**: Test coverage or other metrics

## Best Practices

1. **Performance**: Limit tree depth to avoid overwhelming the page
2. **Accessibility**: Use semantic HTML and ARIA labels
3. **Mobile-friendly**: Test on different screen sizes
4. **Color scheme**: Use consistent, professional colors
5. **Error handling**: Gracefully handle missing data

## Example Output

The generated HTML should save as `project-overview.html` in the project root and include:
- Clear visual hierarchy
- Interactive elements that respond to clicks
- Smooth animations
- Professional appearance suitable for documentation or presentations

## Additional Features

Consider adding:
- Search functionality for the file tree
- Filter by file type
- Export data as JSON
- Print-friendly CSS
- Shareable link generator
- Code snippets from key files
- Architecture diagrams if detectable
- Performance metrics if available
