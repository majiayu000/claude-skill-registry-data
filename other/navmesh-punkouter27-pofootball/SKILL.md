---
name: navmesh
description: "Unity navigation — NavMeshAgent configuration, NavMeshSurface, off-mesh links, dynamic obstacles, pathfinding patterns."
globs: ["**/*Nav*.cs", "**/*Pathfind*.cs", "**/*Agent*.cs"]
---

# NavMesh Navigation

## Setup

1. Add `NavMeshSurface` component to environment parent object
2. Click "Bake" to generate NavMesh
3. Add `NavMeshAgent` to moving characters

## NavMeshAgent Configuration

```csharp
[SerializeField] private NavMeshAgent _agent;

private void Awake()
{
    _agent = GetComponent<NavMeshAgent>();
    _agent.speed = 3.5f;
    _agent.acceleration = 8f;
    _agent.angularSpeed = 120f;
    _agent.stoppingDistance = 0.5f;
    _agent.autoBraking = true;
}

public void MoveTo(Vector3 destination)
{
    _agent.SetDestination(destination);
}
```

## Path Status Checking

```csharp
private void Update()
{
    if (_agent.pathPending) return; // Still calculating

    switch (_agent.pathStatus)
    {
        case NavMeshPathStatus.PathComplete:
            // Full path found
            break;
        case NavMeshPathStatus.PathPartial:
            // Can only get partway — obstacle or unreachable
            break;
        case NavMeshPathStatus.PathInvalid:
            // No path possible
            break;
    }

    // Check if arrived
    if (!_agent.pathPending && _agent.remainingDistance <= _agent.stoppingDistance)
    {
        // Arrived at destination
    }
}
```

## Patrol Pattern

```csharp
public sealed class PatrolBehavior : MonoBehaviour
{
    [SerializeField] private Transform[] _waypoints;
    [SerializeField] private float _waitTime = 2f;

    private NavMeshAgent _agent;
    private int _currentWaypoint;
    private float _waitTimer;

    private void Update()
    {
        if (_agent.pathPending) return;

        if (_agent.remainingDistance <= _agent.stoppingDistance)
        {
            _waitTimer -= Time.deltaTime;
            if (_waitTimer <= 0f)
            {
                _currentWaypoint = (_currentWaypoint + 1) % _waypoints.Length;
                _agent.SetDestination(_waypoints[_currentWaypoint].position);
                _waitTimer = _waitTime;
            }
        }
    }
}
```

## NavMeshObstacle

- **Carve:** cuts a hole in the NavMesh (expensive, use for static/rare movement)
- **Block:** agents path around without modifying NavMesh (cheaper, use for moving obstacles)

## Off-Mesh Links

For jumps, ladders, teleporters — connections between disconnected NavMesh areas.
- Auto-generated: set Jump Distance and Drop Height on NavMeshSurface
- Manual: `NavMeshLink` component between two points

## Runtime NavMesh Modification

```csharp
// Rebake at runtime (e.g., after terrain change)
_navMeshSurface.BuildNavMesh();

// Or update only:
_navMeshSurface.UpdateNavMesh(_navMeshSurface.navMeshData);
```

## Areas and Costs

- Define areas: Walkable, Water, Road (in Navigation settings)
- Set area cost: higher cost = agents avoid that area
- Override per-agent: `_agent.SetAreaCost(areaIndex, cost)`
- Use for: roads (low cost = preferred), mud (high cost = avoided)
