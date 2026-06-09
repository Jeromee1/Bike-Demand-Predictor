# Evaluation Checklist — Agentic ML Production Sprint

**Artifact-based grading.** You grade what was *shipped* — the GitHub repo and the live
Hugging Face Space — not a hand-written code diff. Open the two URLs the student submits and
work down this list. Total: **100 points**.

Submitted artifacts to collect first:
- [ ] Public **GitHub repo** URL
- [ ] Live **Hugging Face Space** URL
- [ ] `MODEL_CARD.md` (in the repo)

---

## 1. Data cleaning & leakage — Phase 1 — **20 pts**

| Check | Pts | How to verify |
|-------|----:|---------------|
| `casual`, `registered`, `instant` dropped before training | **8** | Read `src/data_prep.py`; confirm the leakage constant is applied. **Auto-fail this row if model R² ≈ 1.0** on a fair split. |
| `dteday` parsed; datetime/cyclical features engineered | 5 | `hour`, `dayofweek`/`is_weekend`, cyclical `hr`/`mnth` present |
| Missing `hum`/`windspeed` imputed (not row-dropped wholesale) | 4 | Cleaning handles the injected NaNs |
| Duplicate row removed; cleaning is deterministic on re-run | 3 | Re-running produces the same shape |

## 2. EDA quality — Phase 1 — **10 pts**

| Check | Pts |
|-------|----:|
| ≥2 charts present (notebook or in-app) | 5 |
| At least one written insight tied to the data (e.g. commute peaks) | 5 |

## 3. MLflow tracking & model selection — Phase 2 — **25 pts**

| Check | Pts | How to verify |
|-------|----:|---------------|
| ≥2 model runs logged (params + metrics + artifact) | **10** | `mlruns/` in repo or MLflow screenshots in `MODEL_CARD.md` |
| Metrics include RMSE/MAE/R² on a held-out split | 6 | Visible per run |
| Champion selected by a stated metric, serialised to `models/` | 6 | `train.py` picks lowest-RMSE; model file committed |
| Split avoids leakage (ideally respects time order) | 3 | No target/leakage cols in features; sensible split |

## 4. Streamlit app — Phase 3 — **15 pts**

| Check | Pts | How to verify |
|-------|----:|---------------|
| Analytics dashboard renders EDA visuals | 5 | On the live Space |
| Prediction form returns a demand value from the champion | **7** | Enter inputs on the live Space → get a sane, non-negative number |
| Loads cleanly without errors / doesn't crash on edge inputs | 3 | Try extreme values |

## 5. Containerisation & CI/CD — Phase 4 — **15 pts**

| Check | Pts | How to verify |
|-------|----:|---------------|
| `Dockerfile` builds the app | 5 | `docker build .` succeeds (or CI proves it) |
| Repo pushed; CI/CD workflow run is **green** | **7** | GitHub → Actions tab |
| No secrets committed (token only in GitHub Secrets) | 3 | `git grep -i hf_` finds nothing real |

## 6. Deployment — Phase 5 — **10 pts**

| Check | Pts | How to verify |
|-------|----:|---------------|
| HF Space is **public and live** (loads in a browser) | **6** | Open the URL incognito |
| Push-to-deploy works (a commit triggers a fresh deploy) | 4 | Actions history shows the mirror push |

## 7. Model card & agentic reflection — Phase 5 — **5 pts**

| Check | Pts |
|-------|----:|
| `MODEL_CARD.md` states purpose, metrics, and limitations | 3 |
| 3–4 sentence reflection on working with the agent (what worked, what was corrected) | 2 |

---

## Auto-fail / red-flag conditions

- **R² ≈ 1.0** on a fair evaluation → leakage not handled → cap Section 1 at 0 and flag.
- A committed file containing a real `hf_...` token → security violation; require token rotation.
- The Space URL does not load → Section 6 scores 0 regardless of repo quality ("not shipped").

## Quick band guide

| Band | Score | Meaning |
|------|-------|---------|
| Exceptional | 90–100 | Clean leakage handling, ≥3 tracked runs, polished live app, green CI |
| Strong | 75–89 | Everything shipped and live; minor gaps |
| Pass | 60–74 | Deployed and predicts, but leakage/MLflow/CI weak in places |
| Incomplete | <60 | Not deployed, or leakage uncaught, or pipeline red |
