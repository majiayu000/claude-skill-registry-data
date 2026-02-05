---
name: monte-carlo-scheduling
description: Probabilistic project scheduling using Monte Carlo simulation, confidence intervals, risk-adjusted timelines, and throughput-based forecasting.
allowed-tools: Read, Glob, Grep
---

# Monte Carlo Scheduling

Probabilistic scheduling techniques using Monte Carlo simulation for realistic project forecasting with confidence intervals.

## When to Use This Skill

- Forecasting project completion dates
- Understanding schedule risk and uncertainty
- Creating probabilistic roadmaps
- Answering "when will it be done?" questions
- Planning with incomplete information
- Communicating schedule confidence to stakeholders

## Quick Reference

### Confidence Level Guidelines

| Confidence | Meaning | Use Case |
|------------|---------|----------|
| **50%** | Median estimate, even odds | Internal planning |
| **70%** | Reasonably confident | Team commitments |
| **85%** | High confidence | Customer commitments |
| **95%** | Very high confidence | Contractual deadlines |

### Input Data Requirements

| Data Type | Minimum Sample | Ideal Sample |
|-----------|---------------|--------------|
| **Throughput** | 4 sprints | 10+ sprints |
| **Cycle Time** | 30 items | 100+ items |
| **Story Points** | 6 sprints | 12+ sprints |

## Monte Carlo Fundamentals

### Simulation Process

```yaml
monte_carlo_process:
  1_gather_historical_data:
    throughput:
      definition: "Items completed per time period"
      granularity: "Sprint, week, or day"
      example: "[8, 12, 10, 7, 11, 9, 13, 8, 10, 11]"

    cycle_time:
      definition: "Time from start to completion per item"
      units: "Days or hours"
      example: "[3, 5, 2, 8, 4, 3, 6, 4, 5, 3, 7, 4]"

  2_define_scope:
    backlog_size:
      known_items: "Count of defined stories"
      estimated_discovery: "Expected additional items"
      uncertainty_range: "Low to high item count"

  3_run_simulation:
    iterations: 10000  # Minimum recommended
    for_each_iteration:
      - "Randomly sample throughput from historical data"
      - "Accumulate until backlog complete"
      - "Record completion date"

  4_analyze_results:
    outputs:
      - "Probability distribution of completion dates"
      - "Confidence intervals (50%, 85%, 95%)"
      - "Risk of missing target date"
```

### Monte Carlo Simulator

```csharp
namespace EstimationPlanning.MonteCarlo;

/// <summary>
/// Monte Carlo schedule simulation using throughput-based forecasting.
/// </summary>
public sealed class MonteCarloScheduler
{
    private readonly Random _random = new();

    /// <summary>
    /// Run Monte Carlo simulation for project completion forecasting.
    /// </summary>
    public SimulationResult Simulate(
        int[] historicalThroughput,
        int backlogSize,
        int iterations = 10_000,
        DateOnly? startDate = null)
    {
        if (historicalThroughput.Length < 4)
        {
            throw new ArgumentException(
                "Need at least 4 historical data points for meaningful simulation");
        }

        startDate ??= DateOnly.FromDateTime(DateTime.Today);
        var completionPeriods = new int[iterations];

        for (var i = 0; i < iterations; i++)
        {
            completionPeriods[i] = SimulateOneRun(historicalThroughput, backlogSize);
        }

        Array.Sort(completionPeriods);

        return new SimulationResult(
            Iterations: iterations,
            BacklogSize: backlogSize,
            StartDate: startDate.Value,
            Percentile50: GetPercentile(completionPeriods, 50),
            Percentile70: GetPercentile(completionPeriods, 70),
            Percentile85: GetPercentile(completionPeriods, 85),
            Percentile95: GetPercentile(completionPeriods, 95),
            MinPeriods: completionPeriods[0],
            MaxPeriods: completionPeriods[^1],
            AllResults: completionPeriods);
    }

    private int SimulateOneRun(int[] historicalThroughput, int remainingWork)
    {
        var periods = 0;

        while (remainingWork > 0)
        {
            // Randomly sample from historical throughput
            var throughput = historicalThroughput[_random.Next(historicalThroughput.Length)];
            remainingWork -= throughput;
            periods++;
        }

        return periods;
    }

    private static int GetPercentile(int[] sorted, int percentile)
    {
        var index = (int)Math.Ceiling(percentile / 100.0 * sorted.Length) - 1;
        return sorted[Math.Max(0, index)];
    }

    /// <summary>
    /// Calculate probability of completing by target date.
    /// </summary>
    public double ProbabilityOfCompletion(
        SimulationResult simulation,
        DateOnly targetDate)
    {
        var targetPeriods = (targetDate.ToDateTime(TimeOnly.MinValue) -
                            simulation.StartDate.ToDateTime(TimeOnly.MinValue)).Days / 7; // Assuming weekly periods

        var completedBeforeTarget = simulation.AllResults.Count(p => p <= targetPeriods);
        return (double)completedBeforeTarget / simulation.Iterations;
    }
}

public sealed record SimulationResult(
    int Iterations,
    int BacklogSize,
    DateOnly StartDate,
    int Percentile50,
    int Percentile70,
    int Percentile85,
    int Percentile95,
    int MinPeriods,
    int MaxPeriods,
    int[] AllResults)
{
    public DateOnly GetDateForPercentile(int percentile, int daysPerPeriod = 7)
    {
        var periods = percentile switch
        {
            50 => Percentile50,
            70 => Percentile70,
            85 => Percentile85,
            95 => Percentile95,
            _ => throw new ArgumentException($"Unsupported percentile: {percentile}")
        };

        return StartDate.AddDays(periods * daysPerPeriod);
    }
}
```

## Throughput-Based Forecasting

### Data Collection

```yaml
throughput_collection:
  daily:
    granularity: "Items completed per day"
    use_when:
      - "Kanban teams"
      - "Continuous delivery"
      - "High throughput teams"
    data_points_needed: "30+ days"

  weekly:
    granularity: "Items completed per week"
    use_when:
      - "Mixed Kanban/Scrum"
      - "Medium throughput"
    data_points_needed: "12+ weeks"

  sprint:
    granularity: "Items completed per sprint"
    use_when:
      - "Scrum teams"
      - "Fixed cadence"
    data_points_needed: "6+ sprints"

  what_to_count:
    good:
      - "User stories completed"
      - "Features deployed"
      - "Tickets resolved"
    avoid:
      - "Sub-tasks (too granular)"
      - "Bugs only (not representative)"
      - "Points (use count for Monte Carlo)"
```

### Throughput Analysis

```csharp
namespace EstimationPlanning.MonteCarlo;

/// <summary>
/// Analyze historical throughput data for simulation.
/// </summary>
public static class ThroughputAnalyzer
{
    /// <summary>
    /// Calculate throughput statistics.
    /// </summary>
    public static ThroughputStats Analyze(int[] throughput)
    {
        if (throughput.Length == 0)
            throw new ArgumentException("Throughput data required");

        var sorted = throughput.OrderBy(t => t).ToArray();
        var mean = throughput.Average();
        var stdDev = Math.Sqrt(throughput.Average(t => Math.Pow(t - mean, 2)));
        var cv = stdDev / mean; // Coefficient of variation

        return new ThroughputStats(
            Count: throughput.Length,
            Mean: mean,
            StandardDeviation: stdDev,
            CoefficientOfVariation: cv,
            Min: sorted[0],
            Max: sorted[^1],
            Median: GetMedian(sorted),
            Percentile25: GetPercentile(sorted, 25),
            Percentile75: GetPercentile(sorted, 75),
            Stability: cv < 0.3 ? "Stable" : cv < 0.5 ? "Moderate" : "Volatile");
    }

    /// <summary>
    /// Detect trends in throughput (improving, stable, declining).
    /// </summary>
    public static TrendAnalysis AnalyzeTrend(int[] throughput)
    {
        if (throughput.Length < 4)
            return new TrendAnalysis("Insufficient data", 0);

        // Simple linear regression
        var n = throughput.Length;
        var sumX = Enumerable.Range(0, n).Sum();
        var sumY = throughput.Sum();
        var sumXY = Enumerable.Range(0, n).Zip(throughput, (x, y) => x * y).Sum();
        var sumX2 = Enumerable.Range(0, n).Sum(x => x * x);

        var slope = (n * sumXY - sumX * sumY) / (double)(n * sumX2 - sumX * sumX);
        var percentChange = slope / throughput.Average() * 100;

        var trend = percentChange switch
        {
            > 5 => "Improving",
            < -5 => "Declining",
            _ => "Stable"
        };

        return new TrendAnalysis(trend, percentChange);
    }

    private static double GetMedian(int[] sorted) =>
        sorted.Length % 2 == 0
            ? (sorted[sorted.Length / 2 - 1] + sorted[sorted.Length / 2]) / 2.0
            : sorted[sorted.Length / 2];

    private static int GetPercentile(int[] sorted, int percentile)
    {
        var index = (int)Math.Ceiling(percentile / 100.0 * sorted.Length) - 1;
        return sorted[Math.Max(0, index)];
    }
}

public sealed record ThroughputStats(
    int Count,
    double Mean,
    double StandardDeviation,
    double CoefficientOfVariation,
    int Min,
    int Max,
    double Median,
    int Percentile25,
    int Percentile75,
    string Stability);

public sealed record TrendAnalysis(string Trend, double PercentChangePerPeriod);
```

## Cycle Time Forecasting

### When-Will-Item-Complete Simulation

```csharp
namespace EstimationPlanning.MonteCarlo;

/// <summary>
/// Forecast individual item completion using cycle time data.
/// </summary>
public sealed class CycleTimeForecaster
{
    private readonly Random _random = new();

    /// <summary>
    /// Forecast when a single item starting today will complete.
    /// </summary>
    public CycleTimeForecast ForecastItem(
        double[] historicalCycleTimes,
        DateOnly startDate,
        int iterations = 10_000)
    {
        var completionDays = new double[iterations];

        for (var i = 0; i < iterations; i++)
        {
            completionDays[i] = historicalCycleTimes[
                _random.Next(historicalCycleTimes.Length)];
        }

        Array.Sort(completionDays);

        return new CycleTimeForecast(
            StartDate: startDate,
            Percentile50Days: completionDays[(int)(iterations * 0.50)],
            Percentile70Days: completionDays[(int)(iterations * 0.70)],
            Percentile85Days: completionDays[(int)(iterations * 0.85)],
            Percentile95Days: completionDays[(int)(iterations * 0.95)]);
    }

    /// <summary>
    /// Analyze cycle time distribution.
    /// </summary>
    public CycleTimeAnalysis AnalyzeCycleTimes(double[] cycleTimes)
    {
        var sorted = cycleTimes.OrderBy(c => c).ToArray();
        var mean = cycleTimes.Average();

        // Calculate percentiles
        var p50 = GetPercentile(sorted, 50);
        var p85 = GetPercentile(sorted, 85);
        var p95 = GetPercentile(sorted, 95);

        // Identify outliers (items taking > 2x the 85th percentile)
        var outlierThreshold = p85 * 2;
        var outlierCount = cycleTimes.Count(c => c > outlierThreshold);

        return new CycleTimeAnalysis(
            ItemCount: cycleTimes.Length,
            Mean: mean,
            Median: p50,
            Percentile85: p85,
            Percentile95: p95,
            OutlierCount: outlierCount,
            OutlierThreshold: outlierThreshold);
    }

    private static double GetPercentile(double[] sorted, int percentile)
    {
        var index = (int)Math.Ceiling(percentile / 100.0 * sorted.Length) - 1;
        return sorted[Math.Max(0, index)];
    }
}

public sealed record CycleTimeForecast(
    DateOnly StartDate,
    double Percentile50Days,
    double Percentile70Days,
    double Percentile85Days,
    double Percentile95Days)
{
    public DateOnly GetCompletionDate(int percentile) => percentile switch
    {
        50 => StartDate.AddDays((int)Math.Ceiling(Percentile50Days)),
        70 => StartDate.AddDays((int)Math.Ceiling(Percentile70Days)),
        85 => StartDate.AddDays((int)Math.Ceiling(Percentile85Days)),
        95 => StartDate.AddDays((int)Math.Ceiling(Percentile95Days)),
        _ => throw new ArgumentException($"Unsupported percentile: {percentile}")
    };
}

public sealed record CycleTimeAnalysis(
    int ItemCount,
    double Mean,
    double Median,
    double Percentile85,
    double Percentile95,
    int OutlierCount,
    double OutlierThreshold);
```

## Backlog Size Uncertainty

### Handling Unknown Scope

```yaml
backlog_uncertainty:
  known_backlog:
    description: "Well-defined items"
    handling: "Count directly"

  estimated_discovery:
    description: "Expected additional items during project"
    handling: "Add percentage or range"
    typical_ranges:
      low_uncertainty: "10-20% additional"
      medium_uncertainty: "20-40% additional"
      high_uncertainty: "40-80% additional"
      greenfield: "100%+ additional"

  simulation_approach:
    simple:
      method: "Use range: simulate with low, likely, high item counts"
      report: "Separate forecasts for each scenario"

    advanced:
      method: "Randomize backlog size within range for each iteration"
      report: "Single combined distribution"
```

### Uncertain Backlog Simulator

```csharp
namespace EstimationPlanning.MonteCarlo;

/// <summary>
/// Monte Carlo simulation with uncertain backlog size.
/// </summary>
public sealed class UncertainBacklogSimulator
{
    private readonly Random _random = new();

    /// <summary>
    /// Simulate with backlog size uncertainty.
    /// </summary>
    public SimulationResult SimulateWithUncertainty(
        int[] historicalThroughput,
        BacklogEstimate backlog,
        int iterations = 10_000,
        DateOnly? startDate = null)
    {
        startDate ??= DateOnly.FromDateTime(DateTime.Today);
        var completionPeriods = new int[iterations];

        for (var i = 0; i < iterations; i++)
        {
            // Randomize backlog size using triangular distribution
            var backlogSize = SampleTriangular(
                backlog.LowEstimate,
                backlog.LikelyEstimate,
                backlog.HighEstimate);

            completionPeriods[i] = SimulateOneRun(historicalThroughput, backlogSize);
        }

        Array.Sort(completionPeriods);

        return new SimulationResult(
            Iterations: iterations,
            BacklogSize: backlog.LikelyEstimate,
            StartDate: startDate.Value,
            Percentile50: GetPercentile(completionPeriods, 50),
            Percentile70: GetPercentile(completionPeriods, 70),
            Percentile85: GetPercentile(completionPeriods, 85),
            Percentile95: GetPercentile(completionPeriods, 95),
            MinPeriods: completionPeriods[0],
            MaxPeriods: completionPeriods[^1],
            AllResults: completionPeriods);
    }

    private int SampleTriangular(int low, int likely, int high)
    {
        var u = _random.NextDouble();
        var fc = (double)(likely - low) / (high - low);

        if (u < fc)
        {
            return (int)(low + Math.Sqrt(u * (high - low) * (likely - low)));
        }
        else
        {
            return (int)(high - Math.Sqrt((1 - u) * (high - low) * (high - likely)));
        }
    }

    private int SimulateOneRun(int[] historicalThroughput, int remainingWork)
    {
        var periods = 0;
        while (remainingWork > 0)
        {
            var throughput = historicalThroughput[_random.Next(historicalThroughput.Length)];
            remainingWork -= throughput;
            periods++;
        }
        return periods;
    }

    private static int GetPercentile(int[] sorted, int percentile)
    {
        var index = (int)Math.Ceiling(percentile / 100.0 * sorted.Length) - 1;
        return sorted[Math.Max(0, index)];
    }
}

public sealed record BacklogEstimate(
    int LowEstimate,
    int LikelyEstimate,
    int HighEstimate,
    string Assumptions);
```

## Communicating Results

### Forecast Presentation Template

```yaml
forecast_presentation:
  title: "Project Completion Forecast"
  date_generated: ""
  data_period: ""

  key_findings:
    target_date: ""
    probability_of_hitting_target: ""
    recommended_commitment_date: ""

  confidence_levels:
    fifty_percent:
      date: ""
      meaning: "50% chance of completing by this date"
      recommendation: "Use for internal planning only"

    eighty_five_percent:
      date: ""
      meaning: "85% chance of completing by this date"
      recommendation: "Use for customer commitments"

    ninety_five_percent:
      date: ""
      meaning: "95% chance of completing by this date"
      recommendation: "Use for contractual deadlines"

  assumptions:
    - "Team composition remains stable"
    - "No major scope changes"
    - "Historical throughput is representative"

  risks_not_modeled:
    - "Dependencies on external teams"
    - "Major technical unknowns"
    - "Resource constraints"

  recommendations:
    - ""
```

## References

- **Estimation Techniques**: See `../estimation-techniques/` for underlying estimation methods
- **Risk Assessment**: See `../risk-assessment/` for risk quantification

## Related Skills

- `estimation-techniques` - Story points and function points
- `risk-assessment` - Risk identification and analysis
- `feasibility-analysis` - Schedule feasibility evaluation

---

**Last Updated:** 2025-12-26
