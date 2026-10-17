---
name: test-assets
description: Choose and manage reproducible worlds, models, datasets, and recordings for robotics tests.
---

# Test assets

A fixture earns its place by being a pinned input with a known consumer, not by
being realistic or popular.

## Choose what the test needs

- Start from the behavior under test, then select the smallest representative
  world, model, recording, dataset slice, checkpoint, or golden.
- Prefer a recognizable public asset when it matches the behavior. It gives
  reviewers context and avoids maintaining an equivalent private fixture.
- Add an asset only when an active test consumes it. Record the upstream
  revision, license, verification method, entrypoint, and derivation.
- Reuse outputs from verified scenarios when useful: a generated map or bag can
  become the pinned input to the next layer.

## Choose how it is owned

- Use a pinned pointer for large or independently maintained assets. Verify an
  immutable revision and checksum, and cache the fetched bytes.
- Vendor only when the test must survive upstream availability or inspect the
  exact bytes, redistribution is allowed, and the project has a stated size
  budget.
- Generate project-specific bags and goldens from a committed, seeded producer
  when no canonical source exists.
- Compare re-simulated behavior with tolerance bands. Reserve byte equality for
  pure replay or deterministic transforms.

## Go deeper only when needed

- To select a known world, robot model, dataset, or recording, read
  [references/canonical-assets.md](references/canonical-assets.md) and verify
  its dated evidence against the current source before adoption.
- To define a project catalog, manifest, slice, or golden, read
  [references/test-assets-layout.md](references/test-assets-layout.md).
- Use [examples/catalog.yaml](examples/catalog.yaml) only as a proven catalog
  shape, not as a universal asset set.
- Use [scripts/fetch_assets.py](scripts/fetch_assets.py) only for
  checksum-pinned pointer archives that match its supported manifest shape.
- Testing owns the test layers and pass bars. Data owns training-data sourcing;
  the simulator and Hub skills own loading and transfer mechanics.

## Done

- Every fixture has an active consumer, reproducible source or generator,
  license evidence, and an assertion whose tolerance matches how the fixture is
  produced.
