# Dataset setup

EdgeMaint-X does not commit source datasets or model artifacts. Download files from the official dataset owner and review the applicable terms before use.

## CWRU Bearing Data Center

Official source: https://engineering.case.edu/bearingdatacenter

1. Select a manageable set of drive-end (DE) recordings for the first experiment.
2. Keep the original downloaded files under datasets/raw/cwru/.
3. Record the source URL, file name, bearing condition, fault location, fault size, load, motor speed, channel and sampling rate in the experiment manifest.
4. Do not infer the sampling rate from a variable name. CWRU recordings have different acquisition configurations; pass the correct rate when loading a file.
5. Use source-recording identifiers when splitting windows into training and test sets. Never put overlapping windows from the same recording in both splits.

Expected local layout:

    datasets/
    └── raw/
        └── cwru/
            ├── 12k_drive_end/
            └── 48k_drive_end/

The project loader reads a MATLAB .mat file and searches for a variable ending in _DE_time or _FE_time. It loads the first matching variable. The sampling rate must be provided explicitly by the experiment configuration.

## NASA IMS (optional follow-up)

Official dataset landing page: https://data.nasa.gov/dataset/ims-bearings

NASA IMS may be used for an additional degradation-trend exploration after the first CWRU classification pipeline is stable. It is not required for the initial milestone, and this repository does not claim a Remaining Useful Life model yet.

## Data integrity

- Keep downloaded raw data out of Git.
- Store dataset source, retrieval date, file hashes, labels and sampling rates in a manifest.
- Keep train/validation/test splits grouped by source recording.
- Do not claim benchmark accuracy until the experiment is run on held-out recordings.
