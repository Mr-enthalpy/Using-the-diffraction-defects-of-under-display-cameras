# Local research source snapshots

These are byte-identical snapshots of the authored D1-Data scripts, published for code inspection. They are not an installed Meta package, an optic_system feature, or a root training entrypoint. No new runtime, dependency aggregation or repository membership is introduced. The optical operator implementation is not copied here.

- `dataset_build.py`: eye-derived shared-band crops, review-gated production, train-only shared transforms.
- `validate_build.py`: file hashes, numerical targets, group separation and augmentation replay.
- `oracle_check.py`: fixed low-capacity logistic-regression audit; no N1 training.

Their hashes match `../local_evidence_hashes.json`. The configuration example has intentionally substituted local paths and therefore does not match the original config hash. This is a fixed experiment snapshot, not a general CLI: some thresholds are literal in the script. Changing the YAML alone does not guarantee all processing changes.

Do not run in this tracked directory. Authorized local reproduction requires copying these scripts into a new ignored research directory, placing a valid `preprocessing_config.yaml` there, and supplying the independently licensed archive, original sample index, frozen subject groups and visual review decisions. These restricted inputs are not included. Build refuses existing output directories; preserve all existing data. Finalize/negative stages require the reviewed local records. Validators and oracle read the resulting local manifest beside the scripts. Never glob intermediate NPZ files as independent samples.

The executed environment used Python 3.13, NumPy, OpenCV, Pillow, PyYAML and SciPy from an existing local environment; no dependencies were installed for publication. Results are documented in the parent reports. Public source inspection is possible; full numerical reproduction still requires the restricted inputs and their exact hashes.
