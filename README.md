# EdgeMaint-X

**AI-powered industrial bearing health intelligence with centralized and federated deep-learning experiments.**

EdgeMaint-X is a software-only portfolio project for analyzing public bearing-vibration recordings, classifying machine condition, and comparing centralized training with simulated federated learning. It combines an ML experimentation pipeline with a FastAPI service and a React dashboard.

> **Project status:** repository foundation and implementation plan. Model training, federated experiments, and production deployment are not yet complete. Results will be reported only after reproducible experiments have been run.

## Why this project

This project is deliberately different from the existing portfolio applications: it focuses on time-series signal processing, industrial condition monitoring, reproducible ML evaluation, and cross-client model training. It is not another general-purpose prediction dashboard.

## Current implementation status

The first repository scaffold is committed. The following components are present:

- FastAPI health, dataset-status, and descriptive signal-inspection endpoints.
- React dashboard with API health, signal-inspector workflow, and experiment roadmap.
- CWRU MATLAB recording loader and source-recording-level split helper.
- Signal validation, segmentation, descriptive statistics, and time/frequency feature extraction.
- Random Forest and SVM estimator factories and a 1D-CNN model definition.
- IID / Dirichlet virtual-client partitions and a framework-independent FedAvg tensor aggregator.
- Python tests, Docker scaffolding, setup guides, and GitHub Actions checks.

The following are **not complete yet**: an end-to-end training command, trained model artifacts, model inference endpoint, full Flower simulation adapter, persistent experiment registry, and production authentication. The dashboard explicitly reports that no classifier is loaded. This README will be updated as each milestone is implemented and tested.

## Planned capabilities

- Load approved public bearing-vibration recordings and maintain a dataset manifest.
- Segment signals into fixed-length windows without splitting the same source recording across train and test sets.
- Train reproducible baseline models and a 1D convolutional neural network (1D-CNN).
- Simulate multiple virtual sites that retain their local training records.
- Aggregate model updates using Federated Averaging (FedAvg).
- Compare centralized and federated approaches under IID and non-IID client partitions.
- Expose model metadata and predictions through a documented FastAPI service.
- Present machine condition, signal views, evaluation metrics, and experiment comparisons in a React dashboard.
- Run tests and quality checks through GitHub Actions.

## Initial scope

**In scope for the first portfolio release**

1. Bearing-condition classification using a curated subset of public vibration recordings.
2. Leakage-aware data preparation and repeatable train/validation/test splits.
3. Random Forest / SVM baselines and a 1D-CNN model.
4. Three to five simulated federated clients using FedAvg.
5. A web interface for dataset status, predictions, and experiment metrics.
6. Automated tests, Docker-based local setup, and clear documentation.

**Deferred until the core is stable**

- Remaining Useful Life (RUL) prediction.
- Physical IoT hardware and live factory integration.
- Production-grade secure aggregation or differential privacy.
- Multi-tenant enterprise features and hosted model serving at scale.

## Architecture

```text
Public bearing recordings
          |
          v
  Dataset manifest + validation
          |
          v
  Signal preprocessing / windows
          |
          +---------------------------+
          |                           |
          v                           v
   Centralized training        Virtual site clients
          |                     (local training data)
          |                           |
          |                      FedAvg coordinator
          |                           |
          +-------------+-------------+
                        |
                        v
                Model evaluation
                        |
                        v
                 FastAPI service
                        |
             +----------+----------+
             |                     |
             v                     v
       React dashboard       Experiment database
```

The initial federated simulation is a software experiment. Virtual clients are partitions of a public dataset, not physical machines. Keeping raw records local to each simulated client demonstrates a training topology; it does not by itself guarantee privacy against information leakage from model updates.

## Technology

| Area | Planned technology |
|---|---|
| API | Python, FastAPI, Pydantic |
| ML / signal processing | PyTorch, scikit-learn, NumPy, SciPy |
| Federated simulation | FedAvg utilities; Flower integration planned |
| Frontend | React, TypeScript, Vite |
| Data / experiments | CSV or Parquet manifests; SQLite locally, PostgreSQL when needed |
| Testing | pytest, frontend tests |
| Delivery | Docker Compose, GitHub Actions |

Dependencies will be separated so that API development does not require downloading the full deep-learning stack.

## Repository layout

```text
.
├── backend/          # FastAPI application
├── frontend/         # React dashboard
├── ml/               # Dataset, preprocessing, training, evaluation
├── federated/        # Virtual clients and FedAvg experiments
├── datasets/         # Dataset manifest and download instructions (no raw data)
├── experiments/      # Configurations and tracked result summaries
├── docs/             # Architecture, methodology, decisions and roadmap
├── tests/            # Automated tests
├── .github/workflows # CI
├── docker-compose.yml
├── requirements.txt
├── requirements-ml.txt
└── requirements-federated.txt
```

## Quick start

Clone the repository into a shell-friendly local directory name:

```bash
git clone https://github.com/Kamleshkumarmandal/-EdgeMaint-X-Federated-Predictive-Maintenance.git edgemaint-x
cd edgemaint-x
```

The initial FastAPI and React dashboard scaffold is available. Start the API and frontend in separate terminals:

```bash
# Backend (Python 3.11+)
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

# Frontend (Node.js 20+), in a second terminal
cd frontend
npm install
npm run dev
```

ML dependencies and federated-learning dependencies are installed separately:

```bash
pip install -r requirements-ml.txt
pip install -r requirements-federated.txt
```

See [docs/SETUP.md](docs/SETUP.md) for the evolving setup guide and [docs/ROADMAP.md](docs/ROADMAP.md) for milestones.

## Tests

Install the development dependencies and run the automated tests from the repository root:

```bash
pip install -r requirements-dev.txt
pytest -q
```

The GitHub Actions workflow runs Python compilation and tests, then builds the React dashboard.

## Docker

Run the API and dashboard together:

```bash
docker compose up --build
```

Open the dashboard at http://localhost:5173 and the API docs at http://localhost:8000/docs.

## Dataset policy

The repository will contain dataset instructions and manifests, not large raw recordings. Download public datasets directly from their official sources and check the relevant terms before use.

- Case Western Reserve University (CWRU) Bearing Data Center: https://engineering.case.edu/bearingdatacenter
- NASA IMS bearing dataset: https://data.nasa.gov/dataset/ims-bearings

The first implementation will focus on a manageable CWRU subset. NASA IMS is an optional follow-up for degradation-trend exploration; the project will not claim RUL capability merely from bearing fault-classification data.

## Evaluation plan

Results will be measured on held-out source recordings, not randomly mixed overlapping windows. Planned metrics include:

- Accuracy, macro precision, macro recall, and macro-F1.
- Per-class results and confusion matrix.
- Performance by operating condition where the dataset permits it.
- Centralized vs. federated convergence and classification performance.
- Communication volume, training duration, and inference latency.

No accuracy or performance numbers are claimed until the experiments have actually run.

## Security and responsible use

- Use only public, synthetic, or explicitly authorized machine telemetry.
- Validate file types, sizes, shapes, numeric ranges, and metadata before processing.
- Never commit credentials, private datasets, or generated model binaries.
- Keep API secrets in environment variables and use `.env.example` only as a template.
- Treat model predictions as decision support, not proof of machine failure.
- This is a portfolio prototype, not a certified industrial safety or maintenance system.

## Development

Contributions and issues are welcome. Use small, reviewable changes and keep data preparation and experiments reproducible.

## License

MIT. See [LICENSE](LICENSE).
