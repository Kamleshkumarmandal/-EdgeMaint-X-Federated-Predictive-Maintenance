from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.app.api.schemas import SignalInspectRequest, SignalInspectResponse
from backend.app.core.config import settings
from ml.preprocessing.signal import summarize_signal, validate_signal

router = APIRouter(prefix="/api/v1", tags=["EdgeMaint-X"])


@router.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "service": "edgemaintx-api",
        "model_loaded": False,
        "environment": settings.app_env,
    }


@router.get("/dataset/status")
def dataset_status() -> dict[str, object]:
    dataset_dir = Path(settings.dataset_dir)
    return {
        "dataset_directory": str(dataset_dir),
        "directory_exists": dataset_dir.exists(),
        "raw_directory_exists": (dataset_dir / "raw").exists(),
        "note": "Raw public datasets are downloaded locally and are not committed to Git.",
    }


@router.post("/signals/inspect", response_model=SignalInspectResponse)
def inspect_signal(payload: SignalInspectRequest) -> SignalInspectResponse:
    try:
        signal = validate_signal(
            payload.values,
            min_points=256,
            max_points=settings.max_signal_points,
        )
        summary = summarize_signal(signal)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    duration = signal.size / payload.sample_rate_hz
    return SignalInspectResponse(
        source_label=payload.source_label,
        sample_rate_hz=payload.sample_rate_hz,
        duration_seconds=round(duration, 6),
        summary=summary.to_dict(),
        notice=(
            "Descriptive signal statistics only. No trained fault-classification "
            "model is connected to this endpoint yet."
        ),
    )
