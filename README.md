# UDC diffraction for spectral sensing

This research investigates whether intrinsic display-layer diffraction in an under-display camera topology can act as a wavelength-dependent spectral encoding channel, giving a camera spectral/material information beyond ordinary RGB imaging.

```text
Under-Display Camera Topology
    -> Display-Induced Diffraction
    -> Wavelength-Dependent Optical Encoding
    -> Measured Calibration and Computational Decoding
    -> Spectral / Material Information Beyond RGB
    -> Task-Level Sensing
```

The current system is a UDC-like laboratory optical prototype, not a commercial phone UDC. The first stage measures reproducibility and useful wavelength dependence under a fixed display state. Dynamic display coding is a separate later experimental variable. Material identification, face presentation-attack detection and transfer to a real phone are later possibilities requiring measured evidence. Complete spectral-cube reconstruction and reconstruction PSNR are not necessary research goals.

## Workspace ownership

This Meta Repository is the unified research entry point. It owns research context, planning, experiment acceptance, cross-repository coordination and verified Git Submodule version pins. Engineering implementations remain in independent repositories.

The current members are:

- **optic_system**: camera/LCD/TLS hardware, calibration, capture and measured PSFs. See [README](optic_system/README.md) and [local rules](optic_system/AGENTS.md).
- **reconstruction**: offline dataset protocols, measured-PSF simulation, spectral representations and task evaluation. See [README](reconstruction/README.md) and [local rules](reconstruction/AGENTS.md). The admission pin restores its existing published initialization; D2 development proceeds independently on `codex/d2-spatial-spectral`. Admission does not claim unpublished research is included in the pin.

This root does not store experimental data, implement optical models or run training. It has no shared Python environment or root build system.

## Current research status

The current [D0–D1-Data research audit](docs/research/2026-10-19-dataset-audit/README.md) records the 21-band PSF evidence link, dataset acquisition, standardized Face / Non-face ROI production, quality checks and limited oracle baselines. The present task is fixed-candidate-region Face / Non-face; identity recognition and presentation-attack detection are separate tasks. Subsequent D2 simulation and small N1 unrolling experiments belong to `reconstruction`, with their own versioned reports. The three-band proxy is not a calibrated RGB baseline.

The following paragraph records the earlier hardware milestone; the latest 21-band report is linked in the audit above without changing this workspace’s accepted Submodule pin.

On 2026-10-17 the UDC-like prototype completed its first real calibration and fixed-display 450/550/650 nm measurement cycle, verified acquisition-to-analysis delivery, and repeated wavelength-response diagnostics. The configured system showed repeatable wavelength-dependent PSF shapes. Separating the display contribution from source, lens and sensor effects, and establishing useful spectral/material task information, remain the next research questions.

The member owns the [dated experimental acceptance and limitations](optic_system/docs/reports/2026-10-17-fixed-display-psf.md) and [local measurement roadmap](optic_system/docs/roadmap.md). The workspace now admits the combined dual-host workflow and acquisition-integrity fixes through its exact gitlink; a newly integrated software version is distinct from the historical experiment's acquisition commit. Raw data, private host configuration and generated experimental outputs remain outside Git.

## Clone and restore

```powershell
git clone --recurse-submodules git@github.com:Mr-enthalpy/Using-the-diffraction-defects-of-under-display-cameras.git udc-research
```

After an ordinary clone:

```powershell
git submodule update --init --recursive
```

SSH access to the root and both member repositories is required. Submodules have independent Git histories and can be cloned and developed without this workspace. The Meta Repository locks each member to a specific commit; it never automatically follows the newest branch commit. The branch in `.gitmodules` identifies the development line, while the committed gitlink determines the restored version.

A restored submodule normally has a detached HEAD. Before changing its code, switch to its development branch or create a feature branch inside that repository. Commit and test there first, verify compatibility, then explicitly update and commit the Meta Repository gitlink. Do not use `git submodule update --remote` as an automatic update workflow.

[Root AGENTS.md](AGENTS.md) defines research coordination; member instructions define local implementation and testing. Software tests do not establish the optical mechanism or replace real hardware validation.
