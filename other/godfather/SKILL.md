---
name: godfather
description: GPU and CPU pods on the org's RunPod account that members reach with the Godfather CLI.
---

# Godfather

Use it to manage member pods: create them, start and stop them, schedule sessions, set who may connect, and read or write files on a running pod.

## Flow

1. `godfather.pods` first. It has each pod's status, hardware, who may connect and `image_current`.
2. `godfather.connected` before a stop or restart: it shows who is on the pod now.
3. `godfather.pod_action` starts, stops, restarts, terminates or recreates a pod.
4. `godfather.add_session` schedules a start and a stop, 24 hours at most.
5. `godfather.update_pod` sets `is_public` or `allowed_users` (Discord ids).
6. Files: `godfather.list_files`, `godfather.read_file`, then `godfather.write_file`, `godfather.move_file`, `godfather.make_folder` or `godfather.delete_file`. The pod must be running.

## Watch out

- A pod costs money while it runs. Say the hardware and that it bills before `godfather.create_pod` or a start.
- Terminate and recreate delete the pod's disk. Members lose files that are not on the volume they saved to. Ask before either.
- `image_current: false` means members cannot connect until the pod is recreated.
