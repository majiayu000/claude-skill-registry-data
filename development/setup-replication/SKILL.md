---
name: setup-replication
description: Configure an actor class for network replication in multiplayer UE games.
---
# Skill: Setup Actor Replication
## Description
Configure an actor class for network replication in multiplayer UE games.
## Arguments
- {{arg}}: Actor class to configure replication for
## Steps

### Option A: Blueprint Native Tool Routes (In-Editor Asset Configuration)

1. **Configure Actor Network Replication (`configure_actor_replication`)**:
   Use `configure_actor_replication` to set network replication defaults on a Blueprint actor CDO:
   ```json
   {
     "TargetAsset": "/Game/Blueprints/BP_NetworkPawn",
     "bReplicates": true,
     "bReplicateMovement": true,
     "NetDormancy": "DORM_Never",
     "NetUpdateFrequency": 100.0,
     "NetPriority": 1.0
   }
   ```

2. **Configure Variable Replication & RepNotify (`set_variable_replication`)**:
   
   - **Standard Variable Replication**:
     ```json
     {
       "TargetAsset": "/Game/Blueprints/BP_NetworkPawn",
       "VariableName": "Health",
       "ReplicationType": "Replicated",
       "ReplicationCondition": "COND_None"
     }
     ```

   - **Replication with RepNotify Callback**:
     Setting `ReplicationType` to `"RepNotify"` and specifying `RepNotifyFunc` will automatically generate the `OnRep_Shield` callback graph:
     ```json
     {
       "TargetAsset": "/Game/Blueprints/BP_NetworkPawn",
       "VariableName": "Shield",
       "ReplicationType": "RepNotify",
       "RepNotifyFunc": "OnRep_Shield",
       "ReplicationCondition": "COND_None"
     }
     ```

   - **Replication with Lifetime Condition (Owner Only / Skip Owner)**:
     ```json
     {
       "TargetAsset": "/Game/Blueprints/BP_NetworkPawn",
       "VariableName": "SecretData",
       "ReplicationType": "Replicated",
       "ReplicationCondition": "COND_OwnerOnly"
     }
     ```

### Option B: C++ Code Patterns (Base Class Implementation)

1. **Constructor**: Enable replication
   ```cpp
   bReplicates = true;
   SetReplicateMovement(true);
   ```

2. **Add GetLifetimeReplicatedProps**:
   ```cpp
   void {{arg}}::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
   {
       Super::GetLifetimeReplicatedProps(OutLifetimeProps);
       DOREPLIFETIME({{arg}}, Health);
       DOREPLIFETIME_CONDITION({{arg}}, bIsVisible, COND_OwnerOnly);
   }
   ```

3. **Mark properties for replication**:
   
   **Standard Replication (No callback)**:
   ```cpp
   UPROPERTY(Replicated)
   float Health;
   ```
   
   **Replication with RepNotify Callback (Client side effect)**:
   ```cpp
   UPROPERTY(ReplicatedUsing=OnRep_Shield)
   float Shield;
   
   UFUNCTION()
   void OnRep_Shield(float OldShield);
   ```

4. **Server RPCs** for player actions:
   ```cpp
   UFUNCTION(Server, Reliable)
   void ServerDoAction();
   ```

5. **Required include**: `#include "Net/UnrealNetwork.h"`

## Python API Tip (UE 5.8)
- To set replication on a Blueprint CDO via Unreal Python: `cdo = bp.get_editor_property('generated_class').get_default_object()`, call `cdo.set_replicates(True)`, and compile with `unreal.BlueprintEditorLibrary.compile_blueprint(bp)`.
