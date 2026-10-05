---
name: descriptive-statistics
description: "Summary statistics, data exploration, and descriptive analysis. Use for: summary stats, describe data, data exploration, distributions, means, medians, correlations, cross-tabs."

---

<skill_content>

<overview>
Descriptive statistics are the foundation of all statistical analysis. They reveal data structure, quality issues, and patterns that inform subsequent modeling choices. ALWAYS start with descriptive statistics before any inferential or causal analysis.

This skill ensures you understand your data thoroughly before making statistical claims.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Complete Summary Statistics</name>
  <description>Generate comprehensive summary statistics for all variables</description>
  <rationale>You cannot choose appropriate methods without understanding distributions, missingness, and ranges (Tukey, 1977: "Exploratory Data Analysis")</rationale>
  <consequence>Using wrong methods (e.g., linear regression on bounded outcomes, t-tests on skewed distributions)</consequence>
</requirement>

<requirement priority="critical">
  <name>Missing Data Analysis</name>
  <description>Report missingness patterns for all variables used in analysis. NEVER fabricate or impute values to "fill in" missing data without explicit justification and documentation. Report actual missing data patterns, not synthetic replacements</description>
  <rationale>Missing data mechanisms (MCAR/MAR/MNAR) affect validity of all subsequent analyses (Little & Rubin, 2002). Fabricating missing values masks true data limitations and can introduce undetectable bias. See core-methodology skill for data authenticity requirements</rationale>
  <consequence>Biased estimates if missingness is informative. Fabricated values presented as real data invalidate findings</consequence>
</requirement>

<requirement priority="critical">
  <name>Distribution Visualization</name>
  <description>Plot distributions for all key variables</description>
  <rationale>Summary statistics can hide bimodality, outliers, and skewness (Anscombe's Quartet demonstrates this)</rationale>
  <consequence>Inappropriate method selection and violated assumptions</consequence>
</requirement>

<requirement priority="high">
  <name>Sample Size Reporting</name>
  <description>Report N for overall sample and by groups</description>
  <rationale>Statistical power and precision depend on sample size</rationale>
  <consequence>Underpowered analyses or false precision claims</consequence>
</requirement>

</mandatory_requirements>

<thinking_process>
When implementing descriptive statistics:
1. Check data types (numeric, categorical, dates)
2. Inspect multi-select question formats (binary columns vs concatenated strings)
3. Generate appropriate summaries for each type
4. Identify missingness patterns
5. Visualize distributions to detect issues
6. Check for data quality problems
7. Report everything clearly
</thinking_process>

<implementation_pattern>

<code_template>
```python
@app.cell
def comprehensive_descriptive_stats(df):
    #Following Tukey's EDA principles, we examine the data from multiple
    # angles before any modeling. This reveals quality issues, appropriate methods,
    # and potential problems that could invalidate subsequent analyses.

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os

    # MANDATORY: Dataset overview
    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)
    print(f"Observations: {len(df):,}")
    print(f"Variables: {len(df.columns)}")
    print(f"\nVariable Types:")
    print(df.dtypes.value_counts())

    # MANDATORY: Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # MANDATORY: Summary statistics for numeric variables
    if numeric_cols:
        print("\n" + "=" * 60)
        print("NUMERIC VARIABLES SUMMARY")
        print("=" * 60)
        summary = df[numeric_cols].describe(percentiles=[.01, .05, .25, .5, .75, .95, .99])
        print(summary.round(3))

        # MANDATORY: Check for outliers using IQR method
        print("\n" + "=" * 60)
        print("OUTLIER DETECTION (IQR Method)")
        print("=" * 60)
        for col in numeric_cols[:10]:  # Limit to first 10 for brevity
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)][col]
            if len(outliers) > 0:
                print(f"{col}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.1f}%)")

    # MANDATORY: Missing data analysis
    print("\n" + "=" * 60)
    print("MISSING DATA ANALYSIS")
    print("=" * 60)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing_Count': missing,
        'Missing_Percentage': missing_pct
    })
    missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

    if len(missing_df) > 0:
        print(missing_df.round(2))
        print(f"\nTotal rows with any missing: {df.isnull().any(axis=1).sum()} ({df.isnull().any(axis=1).sum()/len(df)*100:.1f}%)")
    else:
        print("No missing values detected")

    # MANDATORY: Categorical variables summary
    if categorical_cols:
        print("\n" + "=" * 60)
        print("CATEGORICAL VARIABLES SUMMARY")
        print("=" * 60)
        for col in categorical_cols[:10]:  # Limit to first 10
            n_unique = df[col].nunique()
            print(f"\n{col}: {n_unique} unique values")
            if n_unique <= 20:
                print(df[col].value_counts().head(10))

    # MANDATORY: Distribution plots for numeric variables
    if numeric_cols:
        n_cols = min(len(numeric_cols), 9)  # Max 9 subplots
        n_rows = (n_cols + 2) // 3
        n_cols_plot = min(3, n_cols)

        fig, axes = plt.subplots(n_rows, n_cols_plot, figsize=(15, n_rows*4))
        axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes

        for i, col in enumerate(numeric_cols[:9]):
            data = df[col].dropna()

            # Histogram with KDE
            axes[i].hist(data, bins=30, density=True, alpha=0.7, edgecolor='black')
            axes[i].set_title(f'{col}\nSkew: {data.skew():.2f}, Kurt: {data.kurtosis():.2f}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Density')

            # Add KDE if enough data
            if len(data) > 10:
                from scipy import stats
                kde = stats.gaussian_kde(data)
                x_range = np.linspace(data.min(), data.max(), 100)
                axes[i].plot(x_range, kde(x_range), 'r-', linewidth=2)

        # Hide unused subplots
        for i in range(len(numeric_cols[:9]), len(axes)):
            axes[i].set_visible(False)

        plt.tight_layout()
        os.makedirs("./images", exist_ok=True)
        plt.savefig("./images/distributions_overview.png", dpi=144, bbox_inches="tight")
        print(f"\nSUCCESS: Distribution plots saved to ./images/distributions_overview.png")

        # Save figure for inline display
        fig = plt.gcf()
        return summary, fig,
    else:
        return None, None,
```
</code_template>

</implementation_pattern>

<examples>

<example context="clean_data" difficulty="basic">
<description>Basic descriptive statistics for clean survey data</description>
<code>
```python
@app.cell
def describe_survey_data(df):
    #Survey data requires checking for response patterns,
    # missing data from non-response, and scale distributions to
    # identify potential response biases or data entry errors.

    import pandas as pd
    import numpy as np

    # Check response scales
    likert_cols = [col for col in df.columns if 'rating' in col.lower() or 'scale' in col.lower()]

    if likert_cols:
        print("Likert Scale Variables:")
        for col in likert_cols:
            print(f"\n{col}:")
            print(f"  Range: {df[col].min()} - {df[col].max()}")
            print(f"  Mean: {df[col].mean():.2f}, Median: {df[col].median():.2f}")
            print(f"  % at ceiling: {(df[col] == df[col].max()).mean()*100:.1f}%")
            print(f"  % at floor: {(df[col] == df[col].min()).mean()*100:.1f}%")

    # Check for response patterns (straight-lining)
    if len(likert_cols) > 3:
        straight_line = (df[likert_cols].std(axis=1) == 0).sum()
        print(f"\nStraight-lining detected: {straight_line} respondents ({straight_line/len(df)*100:.1f}%)")

    return None,
```
</code>
<output_interpretation>
Look for:
- Ceiling/floor effects (>15% at extremes suggests scale problems)
- Straight-lining (>5% suggests inattentive respondents)
- Unexpected ranges (values outside scale bounds indicate data errors)
</output_interpretation>
</example>

<example context="multiselect_questions" difficulty="basic">
<description>Handling multi-select survey questions in different formats</description>
<code>
```python
@app.cell
def inspect_multiselect_format(df):
    """Multi-select questions appear in two common formats depending on survey platform.
    ALWAYS inspect before analyzing to avoid counting errors.

    Format 1 (Binary/Dummy): ODK, SurveyCTO, Qualtrics, RedCap
      - One column per option with values {0, 1, NaN}
      - Example: 'activities/Business', 'activities/Farming'

    Format 2 (Concatenated): Google Forms, Excel, TypeForm
      - One column with space/comma-separated text
      - Example: 'activities' = "Business Farming CHE"
    """

    import pandas as pd

    # STEP 1: Identify potential multi-select columns
    # Look for column name patterns
    potential_multiselect = [col for col in df.columns
                            if 'select all' in col.lower()
                            or col.count('/') > 0  # Binary format indicator
                            or 'activities' in col.lower()]

    print("=" * 70)
    print("MULTI-SELECT QUESTION FORMAT INSPECTION")
    print("=" * 70)

    # STEP 2: For each potential column, check format
    for col in potential_multiselect[:5]:  # Check first 5
        print(f"\nColumn: {col}")
        print(f"Data type: {df[col].dtype}")

        # Check unique values
        unique_vals = df[col].dropna().unique()
        n_unique = len(unique_vals)

        print(f"Unique values: {n_unique}")

        # DIAGNOSTIC: Is this binary format?
        if df[col].dtype in ['float64', 'int64'] and set(unique_vals).issubset({0, 1}):
            print("→ FORMAT: Binary/Dummy variable (count where value = 1)")
            missing = df[col].isna().sum()
            zeros = (df[col] == 0).sum()
            ones = (df[col] == 1).sum()
            print(f"  Missing: {missing} ({missing/len(df)*100:.1f}%)")
            print(f"  0 (not selected): {zeros}")
            print(f"  1 (selected): {ones}")

        # DIAGNOSTIC: Is this concatenated format?
        elif df[col].dtype == 'object':
            print("→ FORMAT: Concatenated string (parse with .str.contains)")
            missing = df[col].isna().sum()
            print(f"  Missing: {missing} ({missing/len(df)*100:.1f}%)")
            print(f"  Sample values:")
            for val in df[col].dropna().head(3):
                val_str = str(val)[:70] + "..." if len(str(val)) > 70 else str(val)
                print(f"    - {val_str}")
        else:
            print(f"→ UNKNOWN FORMAT - Manual inspection needed")

    return None,
```

```python
@app.cell
def analyze_multiselect_binary(df):
    """Count responses for binary/dummy format multi-select questions.
    Common in ODK/SurveyCTO exports.
    """

    import pandas as pd

    # Identify all binary columns for a multi-select question
    question_prefix = "What are your main income-generating activities? (select all that apply)/"
    activity_cols = [col for col in df.columns if col.startswith(question_prefix)]

    print("=" * 70)
    print("BINARY FORMAT MULTI-SELECT ANALYSIS")
    print("=" * 70)
    print(f"Total respondents: {len(df)}")
    print()

    results = []
    for col in activity_cols:
        activity_name = col.replace(question_prefix, "")

        # CRITICAL: Count only where value = 1 (NOT .notna() which counts 0s too!)
        count = (df[col] == 1).sum()
        percentage = (count / len(df)) * 100

        results.append({
            'Activity': activity_name,
            'N': count,
            'Percentage': percentage
        })

    results_df = pd.DataFrame(results).sort_values('N', ascending=False)
    print(results_df.to_string(index=False))

    # Calculate average selections per person
    total_selections = sum(r['N'] for r in results)
    avg_per_person = total_selections / len(df)
    print(f"\nAverage selections per person: {avg_per_person:.2f}")

    return results_df,
```

```python
@app.cell
def analyze_multiselect_concatenated(df):
    """Parse concatenated string format multi-select questions.
    Common in Google Forms/Excel exports.
    """

    import pandas as pd

    col = 'main_income_generating'  # Adjust column name
    assert col in df.columns, f"Column {col} not found"

    # Define possible options to search for
    possible_activities = [
        'Community Health Entrepreneur (CHE)',
        'Community Health Promoter (CHP)',
        'Business',
        'Farming',
        'Casual work',
        'Teaching',
        'Tailoring',
        'Other'
    ]

    print("=" * 70)
    print("CONCATENATED STRING MULTI-SELECT ANALYSIS")
    print("=" * 70)
    print(f"Total respondents: {len(df)}")
    print(f"Missing: {df[col].isna().sum()}")
    print()

    results = []
    for activity in possible_activities:
        # CRITICAL: Use regex=False for literal matching (parentheses are special in regex!)
        count = df[col].str.contains(activity, na=False, regex=False).sum()
        percentage = (count / len(df)) * 100

        if count > 0:  # Only include if found
            results.append({
                'Activity': activity,
                'N': count,
                'Percentage': percentage
            })

    results_df = pd.DataFrame(results).sort_values('N', ascending=False)
    print(results_df.to_string(index=False))

    # Calculate average selections per person
    total_selections = sum(r['N'] for r in results)
    avg_per_person = total_selections / len(df)
    print(f"\nAverage selections per person: {avg_per_person:.2f}")

    return results_df,
```
</code>
<output_interpretation>
**Binary format**:
- Value counts show {0, 1} → Use `(df[col] == 1).sum()` to count selections
- Using `.notna().sum()` counts BOTH 0s and 1s → Wrong totals (will show 100% for all)
- Missing values (NaN) represent true non-response, not "not selected"

**Concatenated format**:
- Sample values show multiple activities in one string
- MUST use `regex=False` in `.str.contains()` if options have special chars like parentheses
- Delimiter varies (space, comma, semicolon) - inspect samples first
- Person can select multiple activities → counts will sum to > 100%

**Common error**: Using `.notna()` on binary format → counts all non-missing as "selected"
**Fix**: Always use `== 1` for binary, `.str.contains()` for strings
</output_interpretation>
<best_practice>
ALWAYS run format inspection first:
1. Check data type (float/int = binary, object = string)
2. Check unique values (`value_counts(dropna=False)`)
3. View sample rows to confirm structure
4. Choose appropriate counting method

Survey platforms export differently:
- **Binary**: ODK, SurveyCTO, Qualtrics, RedCap, LimeSurvey
- **Concatenated**: Google Forms, TypeForm, some Excel/manual entry

Document which format you found and method used!
</best_practice>
</example>

<example context="skewed_data" difficulty="intermediate">
<description>Handling highly skewed income data</description>
<code>
```python
@app.cell
def describe_skewed_income(df):
    #Income data is typically right-skewed with outliers.
    # We report both standard statistics and robust alternatives,
    # and consider log transformation for modeling.

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    income_col = 'income'  # Adjust as needed
    assert income_col in df.columns, f"Column {income_col} not found"

    income = df[income_col].dropna()

    # Report both parametric and robust statistics
    print("Income Distribution Analysis")
    print("=" * 50)
    print(f"N: {len(income):,}")
    print(f"\nCentral Tendency:")
    print(f"  Mean: ${income.mean():,.2f}")
    print(f"  Median: ${income.median():,.2f}")
    print(f"  Trimmed Mean (5%): ${stats.trim_mean(income, 0.05):,.2f}")

    print(f"\nDispersion:")
    print(f"  Std Dev: ${income.std():,.2f}")
    print(f"  IQR: ${income.quantile(0.75) - income.quantile(0.25):,.2f}")
    print(f"  MAD: ${stats.median_abs_deviation(income):,.2f}")

    print(f"\nDistribution Shape:")
    print(f"  Skewness: {income.skew():.2f}")
    print(f"  Kurtosis: {income.kurtosis():.2f}")

    # Suggest transformation if highly skewed
    if abs(income.skew()) > 2:
        print(f"\nHigh skewness detected. Consider log transformation.")
        log_income = np.log1p(income)  # log(1+x) to handle zeros
        print(f"  Log-transformed skewness: {log_income.skew():.2f}")

    # Percentiles for inequality measures
    print(f"\nPercentiles:")
    for p in [10, 25, 50, 75, 90, 95, 99]:
        print(f"  P{p}: ${income.quantile(p/100):,.2f}")

    print(f"\nInequality Measures:")
    print(f"  P90/P10 ratio: {income.quantile(0.9) / income.quantile(0.1):.2f}")
    print(f"  P90/P50 ratio: {income.quantile(0.9) / income.quantile(0.5):.2f}")

    # Visualize with both linear and log scales
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Original scale histogram
    axes[0].hist(income, bins=50, edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Income ($)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Income Distribution (Linear Scale)')

    # Log scale histogram
    axes[1].hist(income, bins=50, edgecolor='black', alpha=0.7)
    axes[1].set_xlabel('Income ($)')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Income Distribution (Log Scale)')
    axes[1].set_xscale('log')

    # Box plot to show outliers
    axes[2].boxplot(income, vert=True)
    axes[2].set_ylabel('Income ($)')
    axes[2].set_title('Income Box Plot')
    axes[2].set_yscale('log')

    plt.tight_layout()
    os.makedirs("./images", exist_ok=True)
    plt.savefig("./images/income_distribution.png", dpi=144, bbox_inches="tight")

    # Return figure for inline display
    return plt.gcf(),
```
</code>
<lesson>
For skewed data:
1. Always report both mean and median
2. Consider robust statistics (trimmed mean, MAD)
3. Visualize on both linear and log scales
4. Document transformation decisions
</lesson>
</example>

<example context="panel_data" difficulty="advanced">
<description>Descriptive statistics for panel/longitudinal data</description>
<code>
```python
@app.cell
def describe_panel_data(df):
    #Panel data requires checking both cross-sectional
    # and time-series properties. We examine balance, attrition,
    # and within vs. between variation.

    import pandas as pd
    import numpy as np

    # Identify panel structure columns
    unit_col = 'unit_id'  # Adjust as needed
    time_col = 'year'      # Adjust as needed

    assert {unit_col, time_col}.issubset(df.columns), f"Panel columns not found"

    print("PANEL DATA STRUCTURE")
    print("=" * 60)

    # Basic panel properties
    n_units = df[unit_col].nunique()
    n_periods = df[time_col].nunique()
    n_obs = len(df)

    print(f"Units: {n_units:,}")
    print(f"Time periods: {n_periods}")
    print(f"Total observations: {n_obs:,}")
    print(f"Theoretical balanced panel size: {n_units * n_periods:,}")

    # Check balance
    obs_per_unit = df.groupby(unit_col).size()
    is_balanced = (obs_per_unit == n_periods).all()

    print(f"\nPanel balance: {'Balanced' if is_balanced else 'Unbalanced'}")
    if not is_balanced:
        print(f"  Units with complete data: {(obs_per_unit == n_periods).sum()} ({(obs_per_unit == n_periods).sum()/n_units*100:.1f}%)")
        print(f"  Mean observations per unit: {obs_per_unit.mean():.1f}")
        print(f"  Min observations: {obs_per_unit.min()}")
        print(f"  Max observations: {obs_per_unit.max()}")

    # Attrition analysis
    first_period = df[time_col].min()
    last_period = df[time_col].max()

    units_first = set(df[df[time_col] == first_period][unit_col])
    units_last = set(df[df[time_col] == last_period][unit_col])

    attrition = len(units_first - units_last)
    entry = len(units_last - units_first)

    print(f"\nPanel dynamics:")
    print(f"  Units at start: {len(units_first):,}")
    print(f"  Units at end: {len(units_last):,}")
    print(f"  Attrition: {attrition} units ({attrition/len(units_first)*100:.1f}%)")
    print(f"  Late entry: {entry} units")

    # Within vs. between variation for numeric variables
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [c for c in numeric_cols if c not in [unit_col, time_col]]

    if numeric_cols:
        print(f"\nWITHIN VS. BETWEEN VARIATION")
        print("=" * 60)

        for col in numeric_cols[:5]:  # First 5 numeric variables
            # Overall variation
            overall_std = df[col].std()

            # Between variation (across units)
            unit_means = df.groupby(unit_col)[col].mean()
            between_std = unit_means.std()

            # Within variation (within units over time)
            df_demeaned = df[col] - df.groupby(unit_col)[col].transform('mean')
            within_std = df_demeaned.std()

            print(f"\n{col}:")
            print(f"  Overall SD: {overall_std:.3f}")
            print(f"  Between SD: {between_std:.3f} ({between_std/overall_std*100:.1f}% of total)")
            print(f"  Within SD:  {within_std:.3f} ({within_std/overall_std*100:.1f}% of total)")

            # Check if mostly cross-sectional or time-series variation
            if between_std > within_std * 2:
                print(f"  → Primarily cross-sectional variation")
            elif within_std > between_std * 2:
                print(f"  → Primarily time-series variation")
            else:
                print(f"  → Substantial both between and within variation")

    return obs_per_unit,
```
</code>
<best_practice>
For panel data:
1. Always check balance and attrition patterns
2. Decompose variation (within/between) to inform model choice
3. Consider if fixed effects will absorb key variables
4. Document entry/exit patterns for external validity
</best_practice>
</example>

</examples>

<common_mistakes>

<mistake severity="critical">
  <what>Using .notna() or .count() to tally binary multi-select questions</what>
  <consequence>Counts both 0s and 1s as "selected" → inflated percentages (often 100% for all options)</consequence>
  <prevention>ALWAYS use (df[col] == 1).sum() for binary format. Inspect format first with value_counts(dropna=False)</prevention>
  <real_world_example>Builder activities showing 100% participation in all activities because code counted zeros as selections</real_world_example>
</mistake>

<mistake severity="high">
  <what>Using regex=True (default) on .str.contains() with special characters</what>
  <consequence>Parentheses, brackets, dots treated as regex patterns → missing matches</consequence>
  <prevention>Use regex=False for literal string matching in concatenated multi-select fields</prevention>
  <real_world_example>CHE and CHP activities not detected because parentheses in "Community Health Entrepreneur (CHE)" treated as regex grouping</real_world_example>
</mistake>

<mistake severity="high">
  <what>Computing means without checking distributions</what>
  <consequence>Mean is misleading for skewed data (e.g., income)</consequence>
  <prevention>Always visualize distributions and report median alongside mean</prevention>
</mistake>

<mistake severity="high">
  <what>Ignoring missing data patterns</what>
  <consequence>Biased estimates if missingness is not random</consequence>
  <prevention>Test for patterns in missingness (e.g., missing income correlated with age)</prevention>
</mistake>

<mistake severity="medium">
  <what>Not checking data types before analysis</what>
  <consequence>Treating categorical as numeric or vice versa</consequence>
  <prevention>Explicitly check dtypes and convert as needed</prevention>
</mistake>

<mistake severity="medium">
  <what>Using sample statistics on population data</what>
  <consequence>Incorrect uncertainty quantification</consequence>
  <prevention>Distinguish between sample and population analyses</prevention>
</mistake>

</common_mistakes>

<interpretation_guide>

<interpreting_results>
- Mean vs. Median difference > 20% → Consider skewness
- Kurtosis > 3 → Heavy tails, expect outliers
- Missing > 10% → Need missing data strategy
- Between-SD > Within-SD → Fixed effects may not be appropriate
</interpreting_results>

<red_flags>
- Skewness > 2 or < -2 → Distribution far from normal
- Multiple modes in histogram → Distinct subpopulations
- Straight-lining in surveys → Data quality issues
- Sudden changes in panel balance → Selection bias risk
</red_flags>

<next_steps>
- All checks pass → Proceed to inferential analysis
- Skewed outcomes → Consider transformations or GLM
- Missing data → Implement appropriate handling strategy
- Outliers detected → Robustness checks needed
</next_steps>

</interpretation_guide>

<references>
<paper>Tukey, J.W. (1977). "Exploratory Data Analysis." Addison-Wesley. Foundation of EDA principles.</paper>
<paper>Little, R.J.A. & Rubin, D.B. (2002). "Statistical Analysis with Missing Data." Wiley. Missing data mechanisms.</paper>
<paper>Anscombe, F.J. (1973). "Graphs in Statistical Analysis." American Statistician. Why visualization matters.</paper>
</references>

</skill_content>