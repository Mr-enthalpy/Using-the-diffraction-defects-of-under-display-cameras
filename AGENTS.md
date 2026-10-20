# Unified research agent rules

## Research ontology

The highest-level goal is intrinsic UDC display diffraction -> wavelength-dependent encoding -> spectral/material sensing beyond RGB. The present apparatus is a UDC-like laboratory prototype; do not equate it with a commercial phone or claim an unperformed mechanism experiment has passed.

Prioritize measurement repeatability, spectral information gain and task-level validity over algorithm complexity or reconstruction metrics. First establish useful wavelength dependence with a fixed display state. Dynamic display coding, material recognition, face presentation-attack detection and real-phone migration require separate evidence and explicit scope. Do not recast the project as a low-cost hyperspectral camera, a peak-cluster PSF pipeline, spectral-cube reconstruction, PSNR optimization or end-to-end mask optimization.

## Ownership and instruction hierarchy

This Meta Repository owns overall research direction, research roadmap, experiment-level acceptance criteria, cross-repository coordination, integration verification and Git Submodule version pins. Keep research decisions and integration context here when needed; do not add speculative stages or empty member directories.

`optic_system` owns camera/LCD/TLS hardware, calibration, capture, raw measurements, full-frame/ROI PSFs and local hardware/data tests. `reconstruction` owns offline dataset protocols, measured-PSF simulation, spectral representation estimation and task evaluation. Both members keep independent code, environments and Git histories. Do not move member implementations into the root or copy source between repositories.

This file governs cross-repository research and collaboration. Each member's `AGENTS.md` governs local implementation, boundaries, tests and data contracts. Read and respect both levels before changing a member. Maintain specific development progress once in its owning repository; do not duplicate the same progress table across instruction files.

## Cross-repository changes

For any future change affecting multiple repositories:

1. Confirm the real experimental need and measurable acceptance criteria.
2. Assign each change to its owning repository.
3. Modify, test and commit independently in those repositories.
4. Verify the proposed commit combination and data compatibility.
5. Update this repository's Submodule pins last, documenting the actual validation and remaining limits.

Experimental acceptance requires traceable observations, reliable completion/failure semantics, defined coordinates and intensity handling, and repeatable wavelength-dependent evidence. Distinguish no-hardware tests, hardware smoke checks and scientific mechanism experiments. Report which were actually performed; do not infer one from another.

Keep detailed dated experimental acceptance in the owning member and link to it from the root research status. An integration may combine separately validated source branches; record its own regression/compatibility checks and preserve the experiment's actual acquisition commit. Do not retroactively claim a newly combined version was hardware-tested, or redeploy it to the acquisition host merely because a Meta pin advanced.

## Complexity control

Unified research management does not merge engineering implementations. The root currently performs no experimental data storage, optical modelling or training, and has no shared Python package, virtual environment, aggregated requirements or root build system.

Without a concrete authorized need, do not introduce unified RPC/service meshes, generic artifact lifecycles, cross-repository schema registries, large workflow engines, global task schedulers, automatic code synchronization, speculative interfaces or placeholder directories for nonexistent members. Keep private device configuration, machine paths, environments and experimental outputs out of Git. Do not delete or relocate acquired data without explicit authorization.

## Source control and integration

- Each member owns its branches, commits, PRs, CI and history; this repository records compatible commit combinations through gitlinks.
- Do not automatically run `git submodule update --remote` or advance pins. A branch declaration in `.gitmodules` is not a version lock.
- Restore pins with `git submodule update --init --recursive`. Detached HEAD is normal for restoration; switch to a managed development/feature branch before producing development commits.
- Commit member code in its own history before updating a gitlink. Publish the pinned commit to the member remote so a fresh recursive clone can retrieve it.
- Uncommitted member changes are not completed integration. Verify member HEAD, cleanliness and the exact staged gitlink before committing a pin update.
- Do not rewrite other repositories' histories, force-push, replace submodules with copied source, or overwrite existing workspaces.
- Every integration must be recoverable from Git commits. Check both remotes, `.gitmodules`, the pinned SHA and a fresh recursive clone when initializing or changing repository membership.
- Use each member's documented local test environment. Keep hardware tests opt-in and report unexecuted checks accurately.

The currently admitted acquisition line is `optic_system` branch `udc-main`. Its exact accepted version is recorded solely by the Git Submodule pin, not by a manually maintained version table.
