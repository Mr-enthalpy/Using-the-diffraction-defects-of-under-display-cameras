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

The only current member is **optic_system**: camera/LCD/TLS hardware control, optical calibration, synchronized capture, raw observations, full-frame PSF surveys and dense measured ROI PSFs. Its local setup, data contracts and tests are documented in [its README](optic_system/README.md) and [local AGENTS.md](optic_system/AGENTS.md). Other repositories will be admitted only when a concrete need exists.

This root does not store experimental data, implement optical models or run training. It has no shared Python environment or root build system.

## Clone and restore

```powershell
git clone --recurse-submodules git@github.com:Mr-enthalpy/Using-the-diffraction-defects-of-under-display-cameras.git udc-research
```

After an ordinary clone:

```powershell
git submodule update --init --recursive
```

SSH access to both repositories is required. Submodules have independent Git histories and can be cloned and developed without this workspace. The Meta Repository locks each member to a specific commit; it never automatically follows the newest branch commit. The branch in `.gitmodules` identifies the development line, while the committed gitlink determines the restored version.

A restored submodule normally has a detached HEAD. Before changing its code, switch to its development branch or create a feature branch inside that repository. Commit and test there first, verify compatibility, then explicitly update and commit the Meta Repository gitlink. Do not use `git submodule update --remote` as an automatic update workflow.

[Root AGENTS.md](AGENTS.md) defines research coordination; member instructions define local implementation and testing. Software tests do not establish the optical mechanism or replace real hardware validation.
