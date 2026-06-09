# Capstone — Agentic ML Production Sprint

> **Time box: 4 hours. Working solo or in pairs. You drive an AI coding agent
> (opencode recommended; any agent is fine). The grade is on what you SHIP, not on
> how much you typed by hand.**

---

## The mission

A city bike-share operator wants to **forecast hourly rental demand** so they can
rebalance bikes across stations before the next rush. Your job: take the raw
[Bike Sharing dataset](../data/README.md) from messy CSV to a **live, public
Streamlit dashboard on Hugging Face Spaces** that shows demand analytics *and* serves
live predictions — with experiment tracking, containerisation, and CI/CD in between.

You will not hand-write most of this. You will **orchestrate an agent**: specify each
deliverable precisely, review what it produces, run it, and fix what's wrong. That
specify → review → run → correct loop is the skill being assessed.

## What you must ship (the only things that are graded)

1. A **public GitHub repo** containing your code, `mlruns/` (or screenshots of MLflow), and a green Actions run.
2. A **live Hugging Face Space URL** running your Streamlit app, which:
   - shows at least 2 EDA visualisations of the data, and
   - takes weather + time inputs and returns a **demand prediction** from your trained model.
3. A short **model card / reflection** (`MODEL_CARD.md`) — what the model does, its metrics, its limits, and 3–4 sentences on how you worked with the agent (what worked, what you had to correct).

## Hard constraints (non-negotiable)

- **MLflow** must track at least **2 model runs** (params + metrics + the model artifact).
- The deployed app must run the **champion model you selected** — not retrain blindly on startup with no tracking.
- You must **drop `casual`, `registered`, and `instant`** before training (see the leakage box).
- The GitHub Actions **deploy workflow must be green** — a broken pipeline is not "shipped".
- No secrets in code. The HF token lives in **GitHub Secrets**, never in a committed file.

---

## 🚨 LEAKAGE WARNING — the trap that fails this capstone

In this dataset, **`casual + registered = cnt`** (the target). Those two columns are recorded
*after* the hour is over. If you train with them, your model scores a near-perfect R² (~1.0) by
**cheating** — it just adds two numbers. In production you must predict `cnt` for a *future*
hour where you have **no** rider counts. A perfect score on this dataset is a **red flag, not a
win**. Drop `casual`, `registered`, and `instant` in your `data_prep` step. The evaluation
checklist verifies this explicitly.

---

## The 4-hour arc

You start from the **thin scaffold** in [`../scaffold/`](../scaffold/) — folders, pinned
`requirements.txt`, a CI/CD workflow, and **empty file stubs whose docstrings are contracts you
must fulfil**. Fill the bodies (with your agent), don't redesign the interfaces.

| Phase | Time | You deliver |
|------:|:----:|-------------|
| **0 · Setup** | 0:15 | Scaffold cloned into your own GitHub repo. HF write token created. `HF_TOKEN` secret + `HF_USERNAME`/`HF_SPACE` variables added in GitHub. (Full steps: [`SETUP.md`](./SETUP.md)) |
| **1 · Clean + EDA** | 0:45 | `src/data_prep.py` working: loads `hour.csv`, parses `dteday`, **drops the leakage columns**, handles missing `hum`/`windspeed`, dedupes, engineers datetime + cyclical features. Plus a short EDA summary (notebook or markdown) with ≥2 charts. |
| **2 · Train + MLOps** | 1:00 | `src/train.py` working: builds the feature pipeline, trains **2–3 regressors** (e.g. LinearRegression, RandomForest, GradientBoosting), logs each as an **MLflow run** (params, RMSE/MAE/R², model artifact), picks a **champion**, serialises it to `models/`. |
| **3 · Streamlit app** | 0:45 | `app.py` working: an analytics dashboard (your EDA charts) **plus** a prediction form (weather + hour + day inputs → predicted demand) that loads the champion via `src/predict.py`. Runs locally with `streamlit run app.py`. |
| **4 · Container + CI** | 0:30 | `Dockerfile` builds and runs the app locally. Repo pushed to GitHub. The CI/CD workflow runs **green**. |
| **5 · Deploy + buffer** | 0:45 | HF Space created; pushing to `main` triggers `deploy-hf.yml`, which mirrors your repo to the Space; the **live URL serves predictions**. Write `MODEL_CARD.md`. Use any leftover time to fix and polish. |

Total: **4:00**. Phases are guidelines — if Phase 2 runs long, ship a simpler model and keep moving; a **deployed** mediocre model beats a perfect model that never ships.

## What "good" looks like, per phase

- **Phase 1:** Re-running `data_prep` is deterministic; no leakage columns survive; missing values are imputed (not dropped wholesale); the EDA actually *says something* (e.g. "demand peaks at 8am & 6pm on working days").
- **Phase 2:** Each model is a separate, comparable MLflow run; champion choice is justified by a metric (lowest RMSE on a held-out split), not vibes; no train/test leakage in the split (respect time order if you can).
- **Phase 3:** The form can't crash on edge inputs; predictions are sane (non-negative, scale matches reality); the dashboard loads in a few seconds.
- **Phase 4:** `docker build` succeeds clean; the workflow log is green and readable.
- **Phase 5:** The Space is **public** and actually loads; a stranger could open the URL and get a prediction.

## The stub contracts (in `../scaffold/`)

| File | Must provide |
|------|--------------|
| `src/data_prep.py` | `load_and_clean(path) -> DataFrame`, `add_features(df) -> DataFrame`, and a constant listing the leakage columns to drop. |
| `src/train.py` | `train_and_log(df) -> champion_path` that runs the MLflow experiment and saves the champion to `models/`. |
| `src/predict.py` | `load_model(path)` and `predict(model, inputs: dict) -> float`. |
| `app.py` | Streamlit entry: renders EDA + a prediction form wired to `predict`. |
| `tests/test_smoke.py` | At least one real assertion (e.g. cleaned data has no leakage columns, prediction returns a float). |

## Submission checklist

- [ ] Public GitHub repo URL
- [ ] Live Hugging Face Space URL (loads + predicts)
- [ ] Green GitHub Actions run on the deploy workflow
- [ ] ≥2 MLflow runs visible in the repo (`mlruns/` or screenshots)
- [ ] `MODEL_CARD.md` with metrics, limits, and your agent-workflow reflection
- [ ] No leakage columns in the trained model; no secrets in the repo

Grading detail: [`EVALUATION_CHECKLIST.md`](./EVALUATION_CHECKLIST.md).
