---
name: fit
description: >
  Your personal fitness operating system. Not a workout plan. A complete system that figures
  out what your body actually needs, builds training around your real life, tracks what is
  working, and adapts when life gets in the way. Trigger for any fitness goal: losing fat,
  building muscle, running faster, getting stronger, recovering from injury, or simply
  moving better than you did last year.
---

# Fit

## What Most Fitness Advice Gets Wrong

Fitness advice is almost always written for someone with unlimited time, perfect recovery,
consistent sleep, no stress, no travel, and a body that responds predictably to training.

That person does not exist.

The people who actually get fit — who look different, move differently, and feel different
a year from now than they do today — are not the ones who followed the perfect program.
They are the ones who followed a good-enough program consistently for long enough that
consistency compounded into transformation.

This skill is built for real people with real constraints.

---

## The System
```
FITNESS_OS = {
  "assessment": {
    "current_state": ["Current weight and body composition if known",
                      "Current training frequency and type",
                      "Movement limitations or injuries",
                      "Energy levels across the day",
                      "Sleep quality and quantity"],
    "goal_clarity":  {
      "aesthetic":     "Body composition change — fat loss, muscle gain, or both",
      "performance":   "Specific metric — run 5K, deadlift bodyweight, 10 pullups",
      "health":        "Blood markers, blood pressure, longevity, pain reduction",
      "functional":    "Move better, carry more, hurt less"
    },
    "constraint_map": ["Days per week available for training",
                       "Minutes per session realistic",
                       "Equipment available",
                       "Injuries or restrictions",
                       "Travel frequency"]
  }
}
```

---

## Training Architecture
```
PROGRAM_DESIGN = {
  "minimum_effective_dose": {
    "principle": "The smallest training stimulus that produces the desired adaptation.
                  More is not better. Enough is better.",
    "research":  "2x per week per muscle group produces ~80% of the gains of 4x per week.
                  3x per week per muscle group captures nearly all available adaptation.",
    "implication": "A 3-day full-body program done consistently beats a 6-day program
                    done sporadically for the vast majority of non-competitive athletes."
  },

  "progressive_overload": {
    "definition": "Systematically increasing training stimulus over time to force adaptation",
    "methods":    ["Add weight to the bar",
                   "Add reps at same weight",
                   "Add sets",
                   "Reduce rest period",
                   "Improve movement quality"],
    "tracking":   """
      def log_workout(exercise, sets, reps, weight):
          session = {
              "date": today,
              "exercise": exercise,
              "volume": sets * reps * weight,
              "top_set": max_weight_lifted
          }
          compare_to_last_session(session)
          if no_progress_in_3_weeks:
              flag_for_program_adjustment()
    """
  },

  "recovery_management": {
    "signals_of_under_recovery": ["Resting HR elevated vs baseline",
                                   "Performance declining week over week",
                                   "Motivation to train is unusually low",
                                   "Sleep quality deteriorating",
                                   "Persistent muscle soreness beyond 72 hours"],
    "response":  "Reduce volume by 40-50% for one week before resuming progression"
  }
}
```

---

## Nutrition for Fitness Goals
```
NUTRITION_FRAMEWORK = {
  "fat_loss": {
    "principle":  "Caloric deficit is required. Protein is non-negotiable.",
    "target":     "0.7-1g protein per lb bodyweight preserves muscle during deficit",
    "deficit":    "250-500 calories below maintenance — aggressive enough to progress,
                   conservative enough to preserve muscle and sustain adherence",
    "rate":       "0.5-1% of bodyweight per week is sustainable fat loss"
  },
  "muscle_gain": {
    "principle":  "Caloric surplus + adequate protein + progressive overload",
    "target":     "0.7-1g protein per lb bodyweight",
    "surplus":    "200-300 calories above maintenance — minimize fat gain",
    "rate":       "0.25-0.5 lb per week for natural trainers is realistic muscle gain"
  },
  "body_recomposition": {
    "who":        "Beginners, detrained individuals, people returning from injury",
    "approach":   "Maintenance calories, high protein, progressive training",
    "reality":    "Simultaneous fat loss and muscle gain is possible but slower than
                   dedicated phases for either goal"
  }
}
```

---

## When Life Disrupts the Plan
```
DISRUPTION_PROTOCOLS = {
  "travel": {
    "hotel_gym":     "Minimum: 30 min, compound movements, maintain frequency",
    "no_gym":        "Bodyweight protocol — push, pull, hinge, squat, carry variations",
    "principle":     "Maintenance beats nothing. One session per week prevents detraining."
  },
  "injury": {
    "train_around":  "Almost every injury allows training something — find what is possible",
    "upper_body":    "Leg day continues. Lower body injury is not a rest day.",
    "return":        "Return at 60% intensity, progress over 2-3 weeks back to full load"
  },
  "missed_weeks": {
    "rule":          "Never miss twice. One disruption is life. Two is a pattern.",
    "return":        "Reduce weight by 20-30%, rebuild over 1-2 weeks — prevents injury"
  }
}
```

---

## Progress Tracking
```
METRICS_THAT_MATTER = {
  "performance":    "Weight lifted, reps completed, pace, distance — objective and motivating",
  "body":           "Weekly average weight, monthly measurements, photos every 4 weeks",
  "habits":         "Training sessions completed vs planned — consistency is the metric",
  "energy":         "Subjective energy and mood — leading indicator of program sustainability",
  "avoid":          "Daily scale weight as primary metric — noise overwhelms signal"
}
```

---

## Quality Check

- [ ] Goal is specific and time-bound
- [ ] Program is matched to actual available time and equipment
- [ ] Progressive overload built into the plan
- [ ] Nutrition targets provided for stated goal
- [ ] Disruption protocols ready for travel and injury
- [ ] Progress tracking is objective and scheduled
