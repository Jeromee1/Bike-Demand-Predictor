# Week 4 Capstone — Agentic ML Production Sprint

A culminating **4-hour** sprint where students drive an AI coding agent (opencode recommended;
any agent is fine) to take a messy time-series dataset all the way to a **live ML product**:
cleaned data → MLflow-tracked models → Streamlit dashboard → Docker → GitHub Actions → deployed
on **Hugging Face Spaces**.

The point isn't typing speed — it's **agentic orchestration of a real production pipeline under
time pressure**: specify each deliverable, review what the agent produces, run it, fix it, ship it.

## The 4-hour arc

| Phase | Time | Deliverable |
|------:|:----:|-------------|
| 0 · Setup | 0:15 | Repo + HF token + GitHub secrets wired |
| 1 · Clean + EDA | 0:45 | Clean, leakage-free, feature-rich data + EDA |
| 2 · Train + MLOps | 1:00 | 2–3 models tracked in MLflow, champion saved |
| 3 · Streamlit | 0:45 | Dashboard + live prediction form |
| 4 · Container + CI | 0:30 | Docker builds; repo pushed; Actions green |
| 5 · Deploy + buffer | 0:45 | Live HF Space + model card / reflection |

## What's in this kit

| Path | For | Purpose |
|------|-----|---------|
| [`instructions/CAPSTONE_BRIEF.md`](instructions/CAPSTONE_BRIEF.md) | Students | The mission, phases, constraints, leakage trap, stub contracts |
| [`instructions/SETUP.md`](instructions/SETUP.md) | Students | One-time accounts/tokens/secrets setup (Phase 0) |
| [`instructions/EVALUATION_CHECKLIST.md`](instructions/EVALUATION_CHECKLIST.md) | Instructors | Artifact-based 100-pt grading rubric |
| [`data/README.md`](data/README.md) | Students | Dataset download, schema, **leakage warning** |
| [`data/bike_sharing_hourly_sample.csv`](data/bike_sharing_hourly_sample.csv) | Students | 505-row seeded sample for immediate smoke-testing |
| [`scaffold/`](scaffold/) | Students | Thin skeleton to clone: stubs, requirements, Dockerfile, CI/CD workflow |

## Dataset

UCI **Bike Sharing (hourly)** — ~17k hourly records, weather + calendar features, demand-forecasting
regression. Chosen for a real **data-leakage trap** (`casual + registered = cnt`) and genuine
datetime feature-engineering work. Details and download links in [`data/README.md`](data/README.md).

## Instructor notes

- **Reusable infra:** the deploy workflow and HF-frontmatter pattern are adapted from the
  battle-tested `SPD_LESSON/CI_CD_LESSON/` lesson, and the MLflow→Docker→HF loop mirrors
  `ML_FLOW_TEST/`. Students inherit the already-debugged CI/CD plumbing.
- **Reference solution:** not included here yet — authored as a separate follow-up task.
- **Tool-agnostic:** opencode is recommended, but the brief never hard-depends on it; any
  capable coding agent works.
