const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export type ApiHealth = {
  status: string;
  service: string;
  model_loaded: boolean;
  environment: string;
};

export type DatasetStatus = {
  dataset_directory: string;
  directory_exists: boolean;
  raw_directory_exists: boolean;
  note: string;
};

export type SignalSummary = {
  sample_count: number;
  mean: number;
  standard_deviation: number;
  rms: number;
  peak_to_peak: number;
  crest_factor: number;
  kurtosis: number;
};

export type SignalInspection = {
  source_label: string;
  sample_rate_hz: number;
  duration_seconds: number;
  summary: SignalSummary;
  notice: string;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  if (!headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers,
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail ?? `API request failed (${response.status})`);
  }
  return payload as T;
}

export const getHealth = () => request<ApiHealth>("/api/v1/health");
export const getDatasetStatus = () => request<DatasetStatus>("/api/v1/dataset/status");
export const inspectSignal = (values: number[], sampleRateHz: number) =>
  request<SignalInspection>("/api/v1/signals/inspect", {
    method: "POST",
    body: JSON.stringify({
      values,
      sample_rate_hz: sampleRateHz,
      source_label: "Browser-generated synthetic signal",
    }),
  });
