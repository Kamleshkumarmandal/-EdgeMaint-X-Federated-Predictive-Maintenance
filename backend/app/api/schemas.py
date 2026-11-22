from pydantic import BaseModel, Field


class SignalInspectRequest(BaseModel):
    values: list[float] = Field(min_length=256, max_length=200_000)
    sample_rate_hz: float = Field(default=12_000.0, gt=0, le=1_000_000)
    source_label: str = Field(default="manual-upload", max_length=120)


class SignalInspectResponse(BaseModel):
    source_label: str
    sample_rate_hz: float
    duration_seconds: float
    summary: dict[str, int | float]
    notice: str
