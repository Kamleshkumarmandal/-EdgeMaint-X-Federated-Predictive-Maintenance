# Development roadmap

## Milestone 1 — Foundation
- [x] Public repository created.
- [x] Project README and implementation scope.
- [x] FastAPI health and dataset status endpoints.
- [x] Signal validation, segmentation and summary statistics.
- [x] CWRU MATLAB file loader.
- [x] Statistical and frequency-domain feature extraction.
- [x] Recording-level split helper.
- [x] Random Forest and SVM baseline factories.
- [x] 1D-CNN model definition.
- [x] FedAvg tensor aggregation and virtual-client partitions.
- [x] React dashboard foundation.
- [x] Docker and GitHub Actions scaffolding.
- [ ] Verify CI and frontend build on GitHub Actions.

## Milestone 2 — Reproducible ML training
- [ ] Add and validate CWRU dataset manifest.
- [ ] Build an end-to-end window-generation command.
- [ ] Train baseline models and record metrics.
- [ ] Add CNN training, checkpointing and inference.
- [ ] Add model comparison artifacts and plots.

## Milestone 3 — Federated experiment
- [ ] Add local client training loop.
- [ ] Integrate Flower simulation.
- [ ] Compare IID and non-IID partitions.
- [ ] Record FedAvg convergence and communication cost.
- [ ] Add held-out centralized vs federated evaluation.

## Milestone 4 — Product integration
- [ ] Add model registry and version metadata.
- [ ] Add validated inference API.
- [ ] Persist experiment metadata.
- [ ] Connect model and experiment screens in the dashboard.
- [ ] Add authentication before any shared deployment.

## Milestone 5 — Portfolio release
- [ ] Add reproducible demo data/configuration.
- [ ] Add screenshots and a short walkthrough.
- [ ] Publish verified evaluation results.
- [ ] Harden deployment settings and secret handling.
- [ ] Tag a versioned release.

A checked milestone records repository implementation, not a claim of production readiness. Model training and federated experiments remain outstanding until their tests and results are committed.
