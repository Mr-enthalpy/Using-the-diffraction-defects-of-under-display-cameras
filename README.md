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
- **reconstruction**: offline dataset protocols, measured-PSF simulation, spectral representations and task evaluation. See [README](reconstruction/README.md) and [local rules](reconstruction/AGENTS.md). The admission pin now points at the member `main` commit that carries the merged D5.3 block (`aeccd48`); the independent research that used to live on `codex/*` branches is merged there and those branches are deleted. `optic_system` keeps its previously admitted pin. Branch names quoted inside older member reports are historical.

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

## Research branch for review

The [D2 report](https://github.com/Mr-enthalpy/reconstruction/blob/main/docs/reports/2026-10-20-d2/README.md)
and [revised architecture](https://github.com/Mr-enthalpy/reconstruction/blob/main/docs/architecture.md)
are retained on the independent reconstruction research branch. Current D5 status
is recorded in the [D5 experiment report](https://github.com/Mr-enthalpy/reconstruction/blob/main/docs/reports/2026-10-21-d5/EXPERIMENT_REPORT.md).
The [D5.2 single-GPU server run](https://github.com/Mr-enthalpy/reconstruction/blob/main/docs/reports/2026-10-28-d5.2-server-run/README.md)
adds 24,800 measured-PSF A6 steps on the acceptance test server (RTX 3090), ended by the
pre-declared patience rule: best-checkpoint validation PSNR 30.725 dB, SSIM 0.9400,
SAM 9.899°, high-frequency relative L2 0.762. Longer training clearly reduces the early
high-frequency deficit, but what dominates the remaining error is not established.
The [S1/S3 matched pair](https://github.com/Mr-enthalpy/reconstruction/blob/main/docs/reports/2026-10-28-d5.2-s1-s3/README.md)
then trained chromatic and achromatic arms under identical data, config and seed: the
chromatic arm is 0.42 dB better in PSNR and 0.063 lower in high-frequency error, in 9/9
scenes, while spectral-angle error does not improve. Both remain validation-only results
without a frozen-test evaluation.
The [D5.3 mechanism block](https://github.com/Mr-enthalpy/reconstruction/blob/main/docs/reports/2026-10-29-d5.3/README.md)
repeats the pair with three seeds at a uniform 400-epoch budget and adds a
fixed-wideband counterfactual test. SSIM, spatial-gradient and measurement-residual
gains pass a pre-registered stability rule in 3/3 seeds; the PSNR and high-frequency
gains are directionally consistent but fail the scene-consistency clause, and SAM moves
the other way. The counterfactual result is negative for the spectral-information
claim: an achromatic operator is exactly blind to zero-sum spectral changes, the
chromatic difference is invisible per pixel although detectable as an integrated
pattern, and the frozen reconstructor recovers 1.9% of it with no directional
agreement. A [per-band breakdown](https://github.com/Mr-enthalpy/reconstruction/blob/main/docs/reports/2026-10-29-d5.3/per_band_analysis.md)
adds one dimension that moves opposite to the spectral-angle error: the chromatic
arm is lower in 21/21 bands and in all three seeds, and 19/21 bands clear the
cross-seed spread, but only 6/21 also pass the per-seed scene-consistency clause,
so the 450/460 nm and 600-650 nm bands are explicitly not claimed. The dimension
is therefore reported as a direction with limited stability, not as a win. The
[S3 control](https://github.com/Mr-enthalpy/reconstruction/blob/main/docs/reports/2026-10-29-d5.3/s3_control_analysis.md)
then replaced the mean kernel with a real 550 nm band kernel, same code, same
budget, three seeds: the direction does not flip and six of eight metrics now pass
the rule, so the mean kernel's frequency response is not the explanation. The
larger gap is entirely due to the 550 nm reference arm being weaker (0.127 dB), so
the S1 figure of +0.32 dB remains the conservative one and no "+0.44 dB" claim is
made. S4 is not executed.
The approved baseline separates task-independent spatial-spectral reconstruction
from frozen reconstructor plus downstream classification. The architecture
revision and pilot results are not a claim of newly accepted training. Existing
pins remain unchanged.
