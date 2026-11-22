# Local development setup

## Prerequisites

- Python 3.11 or newer.
- Node.js 20 or newer.
- Git.
- Docker Desktop or Docker Engine with Compose (optional).
- A dataset download from an approved public source for ML experiments.

## 1. Clone the repository

    git clone https://github.com/Kamleshkumarmandal/-EdgeMaint-X-Federated-Predictive-Maintenance.git edgemaint-x
    cd edgemaint-x

The repository name begins with a hyphen. When using shell commands, the quoted or explicit path shown above avoids treating the directory name as an option.

## 2. Configure Python

Windows PowerShell:

    py -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements-dev.txt

macOS / Linux:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-dev.txt

The API and tests use the lightweight requirements. Install the ML packages only when working on model training:

    pip install -r requirements-ml.txt

Install the optional federated-learning extras when working on Flower simulations:

    pip install -r requirements-federated.txt

## 3. Start the API

From the repository root:

    uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

Useful URLs:

- API health: http://localhost:8000/api/v1/health
- Dataset directory status: http://localhost:8000/api/v1/dataset/status
- Interactive API documentation: http://localhost:8000/docs

The signal-inspection endpoint currently calculates descriptive statistics. It does not claim to run a trained fault classifier.

## 4. Start the dashboard

Open a second terminal:

    cd frontend
    npm install
    npm run dev

Open http://localhost:5173. The dashboard expects the API at http://localhost:8000 by default. Set VITE_API_URL to change the API origin.

Build the frontend:

    npm run build

## 5. Run tests

From the repository root with the development dependencies installed:

    pytest -q

Run Python compilation checks:

    python -m compileall -q backend ml federated tests

## 6. Run with Docker Compose

From the repository root:

    docker compose up --build

- Dashboard: http://localhost:5173
- API docs: http://localhost:8000/docs

Docker is a convenience for local development; it is not a production deployment recipe.

## Dataset setup

Follow datasets/README.md. Raw recordings and trained model binaries are intentionally excluded from Git.
