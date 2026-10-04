---
name: entity-lifecycle
description: Load when implementing deletion, listing, addition, or updates of entities. Entities that reference each other require careful planning to avoid leaving the database in an invalid state.
---

## Lifecycle States

Most business entities in AutoAssure carry a `LifecycleState` field with three
possible values. Not all of them do, see below.

**Active**

- Default state for new entities.
- The entity is in use.

**Archived**

- User has explicitly archived it.
- Hidden from normal list APIs.
- Still accessible via "list archived" or "get" APIs.
- No new entities should reference archived entities.

**Deleting**

- User has explicitly deleted it.
- Deletion is processed in a background queue.
- Once complete, the entity is physically deleted.
- No new entities should reference deleting entities.

## Entities With No Lifecycle State

A leaf entity — one that nothing else points at — may skip the field entirely, if archive is not needed.

## Adding Rows

When adding a row to DynamoDB, use a conditional update to ensure referenced
entities are active.

- Example: When adding a scenario, add a condition to verify the application
  exists and is active.
- Method name: `TrySaveX()`. Return false if the condition fails.

## Updating Rows

When updating a row that changes a reference, verify the new reference exists
using a condition.

- Example: When moving a scenario from application A to B, add a condition to
  verify B exists.
- Method name: `TryUpdateX()`. Return false if the condition fails.

## Listing Rows

For entities that have a `LifecycleState`, repository methods must support an
option to exclude archived or deleting rows.

## Deleting Rows

The deletion strategy depends on the entity's role:

**Leaf entity** (nothing references it)

- Delete immediately. One write, no worker queue.
- If the leaf has no `LifecycleState`, there is nothing else to do.

**Parent entity** (other entities reference it)

- Mark as "Deleting".
- Submit a worker queue request for background deletion.
- Delete children and grandchildren first.

**Friend/Sibling entity** (references exist in complex ways)

- Discuss the deletion strategy with Nam before implementing.
- Example: Runs reference deleted Scenarios/Environments. We handle this by
  snapshotting the Scenarios/Environments at Run creation time.

## Special Case: Organization

Organizations have a global filter that returns 403 when accessing data from an
archived org. No additional actions needed when adding records—no need to verify
the org is active.

## Special Case: Scenario

Scenario deletion uses a single atomic transaction instead of the general
mark-Deleting-and-queue pattern described above. This relies on Scenario's
child count (Activities) being hard-capped at 90
(`Quota.MaxActivityCountPerScenario`), which comfortably fits under DynamoDB's
100-item `TransactWriteItems` limit on its own. When deleting a Scenario, the
transaction deletes the Scenario row, its folder and tag mapping rows, and all
its Activities in one go — Tags currently have no equivalent cap, so a Scenario
with both close to 90 Activities and many tags can still push the transaction
over the 100-item limit; this is a known, accepted gap, not something this
pattern protects against.

**This is a one-off shortcut specific to Scenario.** Do not reuse this
single-transaction delete pattern for a parent entity whose child count is not
bounded (e.g., Application, which can own far more rows than that).