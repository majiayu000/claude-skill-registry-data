---
name: cocktail-party-prep
description: Backward-schedule cocktail-party preparation from a fixed service time, supplied task durations and dependencies, sourced safety limits, sensory-quality windows, owners, and cold or transport capacity. Use for make-ahead sequencing, constrained storage or transport, delay review, and unresolved prep inputs. Exclude menu design, beverage quantities, live service, and universal freshness estimates.
---

# Cocktail party prep

Run a backward pass from service time, then prove that every scheduled task satisfies its dependencies, capacity, safety, and review constraints.

The result is a pre-event review artifact. It never orders supplies, changes a menu, contacts anyone, controls live service, or claims that storage conditions were physically verified.

## 1. Fix the boundary

Accept an approved drink menu or supplied task list plus one fixed service time.

Keep adjacent jobs outside this procedure.

| Requested work | Boundary |
|---|---|
| Beverage quantities | Route to an event quantity plan |
| Menu or recipe choice | Require an approved menu before scheduling |
| Universal ingredient life | Require an applicable authority or product instruction |
| Live prep control | Leave execution with the named task owner |
| Service pacing | Route to a service run sheet |

Retain the scheduling portion of a mixed request and record every excluded job without performing it.

Complete this step when the fixed service time, scheduling scope, and exclusions are explicit.

## 2. Freeze the task graph

Record each value with one source label chosen from `authority instruction`, `product instruction`, `host approved`, `provider confirmed`, `measured`, or `unknown`.

Every task requires the fields below.

| Field | Required content |
|---|---|
| Identity | Stable task ID and produced component |
| Timing | Duration in minutes and any fixed deadline |
| Dependencies | Every prerequisite task ID |
| Ownership | One owner or a supplied parallel-work limit |
| Execution resources | Equipment and capacity units occupied while work runs |
| Holding resources | Refrigeration or transport units occupied after completion |
| Safety inputs | Applicable limit, required storage state, and controlling source |
| Quality input | Optional user-selected sensory window, labeled `QUALITY ONLY` |
| Verification | A check the owner performs at completion |

A task whose duration is unknown remains unresolved. Missing refrigeration state, safe window, prerequisite duration, or required resource capacity also stops the affected task.

Propagate an unresolved state to every dependent task. Preserve independent lanes, but never assign a start or finish to an unresolved task.

Complete this step when the graph is acyclic and every task is either fully specified or listed with its unresolved descendants. Otherwise, completion is the unresolved-task stop in [the output contract](references/output-contract.md).

## 3. Separate safety from sensory quality

Read [the safety and quality rules](references/safety-and-quality.md) completely for any perishable, refrigerated, transported, juice-based, egg-containing, or quality-window task.

Applicable authority guidance and product instructions remain controlling inputs. A sensory-quality preference never establishes safety, and elapsed time inside a quality window never proves safe handling.

If controlling sources conflict or leave the needed safe window unknown, stop the affected task. Record the conflict without choosing a value.

Complete this step when every scheduled task has a supported safety classification and each quality preference remains separately labeled.

## 4. Run the backward pass

Read [the backward-pass method](references/backward-pass.md) completely before calculating.

Start from the fixed service time or a supplied earlier deadline. Place terminal tasks as late as their constraints allow, then move backward through prerequisites. Resolve owner, equipment, refrigeration, and transport conflicts with the declared capacities.

Preserve every subtraction, dependency boundary, and capacity assignment. Never compress a supplied duration to force a fit.

Complete this step when each schedulable task has one reproduced latest start, finish, owner, resource assignment, and nonnegative dependency slack.

## 5. Prove hold windows

Measure each component's hold interval from task completion until its consuming task starts or service begins. Include transport and setup time inside that interval.

Check the entire interval against all applicable safety limits and required storage states. Compare the same interval with any user-selected sensory-quality window in a separate column.

Capacity must cover every overlapping holding interval. A planned refrigerator or transport assignment does not verify the actual temperature, condition, or product state.

Complete this step when every scheduled component fits its declared capacity and safety constraints, while each quality result is labeled `WITHIN QUALITY WINDOW`, `QUALITY REVIEW`, or `NOT APPLICABLE`.

## 6. Route delays and decisions

Calculate task slack after the schedule is placed. A task with zero slack belongs to the critical path.

Recalculate affected descendants when a supplied duration, deadline, or capacity changes. Keep an unresolved quality preference as `REVIEW REQUIRED` without presenting it as unsafe.

Reassignment, added equipment, changed preparation method, or menu edits remain proposed options until the host or provider approves the change and supplies any new duration, capacity, or safety input.

Complete this step when every delay or decision has a named owner, reviewer, deadline, and unchanged or recalculated schedule state.

## 7. Emit the prep packet

Read [the output contract](references/output-contract.md) completely and render every required section.

A fully resolved schedule receives `READY FOR HOST REVIEW` when dependency and capacity checks pass, safety limits hold, and no quality decision remains open.

When the safety-valid schedule still contains a quality-only or recovery decision, assign `NOT READY: REVIEW DECISIONS`.

Any unknown duration, safe window, storage state, prerequisite, or capacity forces `STOPPED: UNRESOLVED TASKS`.

Complete the skill when the packet passes its completion audit and no external action has occurred.
