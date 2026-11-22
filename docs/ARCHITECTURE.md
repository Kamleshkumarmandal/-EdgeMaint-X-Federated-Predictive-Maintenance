# EdgeMaint-X architecture

## Component responsibilities

### Frontend
React + TypeScript dashboard for API health, dataset readiness, signal inspection, experiment status and later model comparisons.

### Backend
FastAPI service for health checks, dataset status and signal-inspection requests. Model inference endpoints will be added after a model artifact format and lifecycle are established.

### ML pipeline
- Data ingestion: reads local CWRU MATLAB recordings.
- Preprocessing: validation, fixed-window segmentation and recording-level splitting.
- Features: time-domain and frequency-domain indicators.
- Baselines: Random Forest and SVM.
- Deep learning: 1D-CNN over fixed-length vibration windows.
- Evaluation: macro-averaged classification metrics and confusion matrices.

### Federated experiment layer
Virtual clients receive separate training partitions. A coordinator aggregates model state using sample-weighted FedAvg. IID and Dirichlet non-IID partitions can be compared. Flower integration is an optional execution layer planned after the local aggregation and data contracts are tested.

### Storage
Raw public datasets and model artifacts remain local and are excluded from Git. Experiment metadata and model registry persistence will be selected after the first end-to-end training workflow is implemented.

## Request flow

1. Browser connects to the FastAPI health and dataset-status endpoints.
2. An approved vibration signal is submitted for inspection.
3. The API validates dimensionality, sample count and finite values.
4. Signal statistics are calculated and returned with an explicit note that this is not a model prediction.
5. Later, a trained model service will return class probabilities and model metadata after artifact validation.

## Federated learning flow

1. A dataset manifest identifies source recordings and labels.
2. Recording-level splits create train, validation and test partitions without overlapping source recordings.
3. Training records are divided among virtual clients.
4. Each client trains a copy of the same model on its local partition.
5. FedAvg combines floating-point model parameters weighted by local example counts.
6. The global model is evaluated on a held-out test set that was not used by any client.

Keeping raw records local in a simulation demonstrates decentralized training topology. It is not a formal privacy guarantee: model updates can still reveal information. Secure aggregation and differential privacy are not implemented in the initial scope.

## Trust boundaries

- Dataset files are treated as untrusted input.
- The API bounds signal sample counts and rejects non-finite values.
- CORS is configured through environment variables.
- Secrets must not be committed.
- The initial API is a local development service and does not yet provide user authentication or production-grade authorization.
