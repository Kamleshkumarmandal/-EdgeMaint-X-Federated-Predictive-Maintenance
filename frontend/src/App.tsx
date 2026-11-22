import { useEffect, useMemo, useState } from "react";
import {
  Activity, AlertCircle, ArrowUpRight, BarChart3, Boxes, BrainCircuit,
  CheckCircle2, ChevronRight, CircleDot, Cpu, Database, Gauge,
  Layers3, Radio, RefreshCw, ShieldCheck, Signal, Workflow,
} from "lucide-react";
import {
  getDatasetStatus, getHealth, inspectSignal,
  type ApiHealth, type DatasetStatus, type SignalInspection,
} from "./api";

type Section = "overview" | "signal" | "experiments";

const nav: { id: Section; label: string; icon: typeof Activity }[] = [
  { id: "overview", label: "Overview", icon: Gauge },
  { id: "signal", label: "Signal inspector", icon: Signal },
  { id: "experiments", label: "Experiments", icon: Workflow },
];

function makeSyntheticSignal(size = 1024): number[] {
  return Array.from({ length: size }, (_, i) => {
    const carrier = Math.sin((2 * Math.PI * 42 * i) / 12000);
    const harmonic = 0.23 * Math.sin((2 * Math.PI * 126 * i) / 12000);
    const modulation = 1 + 0.16 * Math.sin((2 * Math.PI * 4 * i) / 12000);
    const deterministicNoise = 0.035 * Math.sin(i * 1.731);
    return Number((modulation * (carrier + harmonic) + deterministicNoise).toFixed(7));
  });
}

function Sparkline({ values }: { values: number[] }) {
  const points = useMemo(() => {
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;
    return values.map((v, i) => {
      const x = (i / Math.max(values.length - 1, 1)) * 560;
      const y = 92 - ((v - min) / range) * 76;
      return `${x},${y}`;
    }).join(" ");
  }, [values]);
  return (
    <svg className="signal-chart" viewBox="0 0 560 104" role="img" aria-label="Synthetic vibration waveform">
      <defs>
        <linearGradient id="waveFill" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor="#67e8d1" stopOpacity=".25" />
          <stop offset="100%" stopColor="#67e8d1" stopOpacity="0" />
        </linearGradient>
      </defs>
      {[18, 42, 66, 90].map((y) => <line key={y} x1="0" x2="560" y1={y} y2={y} className="chart-grid" />)}
      <polyline points={`0,104 ${points} 560,104`} fill="url(#waveFill)" stroke="none" />
      <polyline points={points} className="wave-line" />
    </svg>
  );
}

function App() {
  const [section, setSection] = useState<Section>("overview");
  const [health, setHealth] = useState<ApiHealth | null>(null);
  const [dataset, setDataset] = useState<DatasetStatus | null>(null);
  const [inspection, setInspection] = useState<SignalInspection | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function refresh() {
    setError("");
    try {
      const [apiState, dataState] = await Promise.all([getHealth(), getDatasetStatus()]);
      setHealth(apiState);
      setDataset(dataState);
    } catch (err) {
      setHealth(null);
      setError(err instanceof Error ? err.message : "Unable to connect to API");
    }
  }

  useEffect(() => { void refresh(); }, []);

  async function runSignalInspection() {
    setLoading(true);
    setError("");
    try {
      setInspection(await inspectSignal(makeSyntheticSignal(), 12000));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Signal inspection failed");
    } finally {
      setLoading(false);
    }
  }

  const activeNav = nav.find((item) => item.id === section)?.label ?? "Overview";

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><Activity size={21} /></div>
          <div><b>EdgeMaint<span>-X</span></b><small>INDUSTRIAL INTELLIGENCE</small></div>
        </div>
        <div className="nav-label">WORKSPACE</div>
        <nav>
          {nav.map(({ id, label, icon: Icon }) => (
            <button key={id} className={section === id ? "nav-item active" : "nav-item"} onClick={() => setSection(id)}>
              <Icon size={17} /><span>{label}</span>{section === id && <ChevronRight size={14} className="nav-chevron" />}
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="client-card">
            <div className="client-card-top"><span className="pulse-dot" /> DEVELOPMENT MODE</div>
            <b>Virtual plant network</b>
            <small>Simulation environment · no hardware</small>
          </div>
          <div className="sidebar-foot"><ShieldCheck size={15} /><span>Local-first experiment workspace</span></div>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div className="crumb"><span>EdgeMaint-X</span><i>/</i><b>{activeNav}</b></div>
          <div className="top-actions">
            <span className={health ? "api-status online" : "api-status offline"}><span />{health ? "API connected" : "API offline"}</span>
            <button className="icon-btn" title="Refresh connection" onClick={() => void refresh()}><RefreshCw size={16} /></button>
            <div className="avatar">EX</div>
          </div>
        </header>

        <div className="page">
          {error && <div className="error-banner"><AlertCircle size={16} />{error}<button onClick={() => setError("")}>Dismiss</button></div>}

          {section === "overview" && (
            <>
              <section className="hero">
                <div className="hero-copy">
                  <div className="eyebrow">PREDICTIVE MAINTENANCE / CONTROL CENTER</div>
                  <h1>Understand machine health.<br /><span>Before downtime happens.</span></h1>
                  <p>Explore vibration signals, build fault diagnosis models, and compare collaborative learning across virtual industrial sites.</p>
                  <div className="hero-actions">
                    <button className="primary-btn" onClick={() => setSection("signal")}><Signal size={16} /> Open signal lab</button>
                    <button className="secondary-btn" onClick={() => setSection("experiments")}>View experiment plan <ArrowUpRight size={15} /></button>
                  </div>
                </div>
                <div className="hero-orbit">
                  <div className="orbit orbit-a" /><div className="orbit orbit-b" /><div className="orbit orbit-c" />
                  <div className="orbit-core"><Activity size={33} /></div>
                  <span className="orbit-point point-a" /><span className="orbit-point point-b" /><span className="orbit-point point-c" />
                  <div className="orbit-label"><span className="pulse-dot" /> VIRTUAL PLANT</div>
                </div>
              </section>

              <div className="metric-grid">
                <Metric icon={Radio} label="API service" value={health ? "Online" : "Offline"} detail={health?.service ?? "Waiting for backend"} tone={health ? "mint" : "rose"} />
                <Metric icon={Database} label="Local dataset" value={dataset?.raw_directory_exists ? "Detected" : "Not loaded"} detail="CWRU recordings" tone="blue" />
                <Metric icon={BrainCircuit} label="Fault classifier" value={health?.model_loaded ? "Loaded" : "Not trained"} detail="1D-CNN inference" tone="violet" />
                <Metric icon={Workflow} label="Federated rounds" value="Not started" detail="FedAvg simulation" tone="amber" />
              </div>

              <div className="section-grid">
                <section className="panel">
                  <div className="panel-head"><div><div className="eyebrow">SIGNAL EXPLORATION</div><h2>Vibration signal lab</h2><p>Inspect a deterministic synthetic waveform through the API.</p></div><span className="mini-tag">DEMO SIGNAL</span></div>
                  <Sparkline values={makeSyntheticSignal(180)} />
                  <div className="chart-caption"><span><i /> Synthetic waveform preview</span><span>12 kHz · 180 points shown</span></div>
                  <button className="text-action" onClick={() => setSection("signal")}>Inspect signal characteristics <ArrowUpRight size={14} /></button>
                </section>
                <section className="panel">
                  <div className="panel-head"><div><div className="eyebrow">BUILD STATUS</div><h2>Platform foundation</h2><p>Implemented scaffolding versus planned capabilities.</p></div><Layers3 size={19} className="subtle-icon" /></div>
                  <StatusRow icon={CheckCircle2} label="Signal preprocessing API" state="Available" good />
                  <StatusRow icon={CheckCircle2} label="CWRU MAT-file loader" state="Available" good />
                  <StatusRow icon={CircleDot} label="Trained fault classifier" state="Planned" />
                  <StatusRow icon={CircleDot} label="Federated training rounds" state="Planned" />
                </section>
              </div>
            </>
          )}

          {section === "signal" && (
            <div className="page-stack">
              <div className="page-title"><div><div className="eyebrow">DATA / SIGNAL PROCESSING</div><h1>Signal inspector</h1><p>Call the backend to calculate descriptive statistics for a safe synthetic vibration signal.</p></div><span className="mini-tag">NO MODEL INFERENCE</span></div>
              <section className="panel">
                <div className="panel-head"><div><h2>Sample vibration waveform</h2><p>Generated in your browser. No external dataset is uploaded.</p></div><span className="soft-tag">1,024 samples</span></div>
                <Sparkline values={makeSyntheticSignal(220)} />
                <div className="button-row"><button className="primary-btn" onClick={() => void runSignalInspection()} disabled={loading}><Signal size={16} />{loading ? "Analyzing…" : "Analyze synthetic signal"}</button><span className="muted-note">Sample rate: 12,000 Hz</span></div>
              </section>
              {inspection && (
                <section className="panel">
                  <div className="panel-head"><div><div className="eyebrow">API RESPONSE</div><h2>Signal characteristics</h2><p>{inspection.notice}</p></div><span className="mini-tag">ANALYZED</span></div>
                  <div className="metric-grid compact">
                    <Metric icon={Activity} label="RMS amplitude" value={inspection.summary.rms.toFixed(4)} detail="Root mean square" tone="mint" />
                    <Metric icon={BarChart3} label="Peak-to-peak" value={inspection.summary.peak_to_peak.toFixed(4)} detail="Amplitude range" tone="blue" />
                    <Metric icon={Gauge} label="Crest factor" value={inspection.summary.crest_factor.toFixed(3)} detail="Peak / RMS" tone="violet" />
                    <Metric icon={Cpu} label="Kurtosis" value={inspection.summary.kurtosis.toFixed(3)} detail="Distribution shape" tone="amber" />
                  </div>
                </section>
              )}
            </div>
          )}

          {section === "experiments" && (
            <div className="page-stack">
              <div className="page-title"><div><div className="eyebrow">RESEARCH / MODEL EVALUATION</div><h1>Experiment workspace</h1><p>Planned, reproducible comparisons for the EdgeMaint-X model pipeline.</p></div><span className="mini-tag">ROADMAP</span></div>
              <div className="experiment-grid">
                <ExperimentCard number="01" title="Classical ML baseline" description="Random Forest and SVM trained on time- and frequency-domain vibration features." tags={["Scikit-learn", "Feature engineering"]} />
                <ExperimentCard number="02" title="Centralized 1D-CNN" description="Train a convolutional model on fixed-length vibration windows with recording-level splits." tags={["PyTorch", "Signal classification"]} />
                <ExperimentCard number="03" title="Federated FedAvg" description="Simulate virtual plant clients, aggregate local model weights, and measure convergence." tags={["Flower", "FedAvg"]} />
                <ExperimentCard number="04" title="Non-IID robustness" description="Compare client label distributions, communication volume, and held-out performance." tags={["Dirichlet split", "Macro-F1"]} />
              </div>
              <section className="panel note-panel"><ShieldCheck size={20} /><div><b>Reproducibility and honest reporting</b><p>Metrics will appear here only after experiments have been executed. The current repository contains preprocessing, API scaffolding, and experiment utilities; no trained model or benchmark result is being presented as complete.</p></div></section>
            </div>
          )}
        </div>
        <footer className="footer"><span>EdgeMaint-X · Portfolio engineering build</span><span><Boxes size={13} /> Software simulation · no physical hardware</span></footer>
      </main>
    </div>
  );
}

function Metric({ icon: Icon, label, value, detail, tone }: {
  icon: typeof Activity; label: string; value: string; detail: string; tone: string;
}) {
  return <article className="metric-card"><div className="metric-top"><span>{label}</span><i className={`metric-icon ${tone}`}><Icon size={17} /></i></div><b>{value}</b><small>{detail}</small></article>;
}

function StatusRow({ icon: Icon, label, state, good = false }: {
  icon: typeof Activity; label: string; state: string; good?: boolean;
}) {
  return <div className="status-row"><Icon size={15} className={good ? "good-icon" : "subtle-icon"} /><span>{label}</span><small className={good ? "good-text" : ""}>{state}</small></div>;
}

function ExperimentCard({ number, title, description, tags }: {
  number: string; title: string; description: string; tags: string[];
}) {
  return <article className="panel experiment-card"><div className="experiment-num">{number}</div><h2>{title}</h2><p>{description}</p><div className="tag-row">{tags.map((tag) => <span key={tag}>{tag}</span>)}</div><div className="planned-label"><CircleDot size={13} /> Planned experiment</div></article>;
}

export default App;
