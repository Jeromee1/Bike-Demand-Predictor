# Setup — do this in Phase 0 (15 minutes)

Get every account, token, and secret in place **before** the clock pressure of building.
Do these once; the rest of the sprint is just `git push`.

## 0. Prerequisites (have these installed)

| Tool | Check | If missing |
|------|-------|-----------|
| Python 3.10+ | `python --version` | python.org / pyenv |
| Git | `git --version` | git-scm.com |
| GitHub CLI | `gh --version` | `brew install gh` / cli.github.com |
| Hugging Face CLI | `hf --version` | `pip install -U "huggingface_hub[cli]"` |
| Docker | `docker --version` | docker.com/get-started |
| An AI coding agent | `opencode --version` | opencode.ai (or use your preferred agent) |

Log in once: `gh auth login` and `hf auth login`.

## 1. Get the scaffold into your own GitHub repo

```bash
# Copy the scaffold out of the course repo into a fresh project folder
cp -r Week4/Capstone_AgenticSprint/scaffold ~/bike-demand-capstone
cd ~/bike-demand-capstone
git init && git add . && git commit -m "chore: scaffold"

# Create the GitHub repo AND push in one step
gh repo create bike-demand-capstone --public --source=. --remote=origin --push
```

Also drop the dataset in: copy `bike_sharing_hourly_sample.csv` into `data/`, and download the
real `hour.csv` (see [`../data/README.md`](../data/README.md)) during Phase 1.

## 2. Create a Hugging Face **write** token

1. Go to https://huggingface.co/settings/tokens → **New token** → role **Write**.
2. Copy it (looks like `hf_xxxxxxxxxxxxxxxxxxxxxxxx`). Treat it like a password.

## 3. Create the Hugging Face Space (Streamlit SDK)

```bash
hf repos create <your-hf-username>/bike-demand-capstone \
  --type space --space-sdk streamlit --exist-ok
```

(Or via the web UI: https://huggingface.co/new-space → SDK **Streamlit** → **Public** → CPU basic.)

> The deploy workflow **pushes to an existing Space** — it does not create one. Make the Space first.

## 4. Wire the GitHub repo to Hugging Face

The deploy workflow (`.github/workflows/deploy-hf.yml`) reads **one secret** and **two variables**.
In your GitHub repo → **Settings → Secrets and variables → Actions**:

**Secrets tab → New repository secret**
| Name | Value |
|------|-------|
| `HF_TOKEN` | the write token from step 2 |

**Variables tab → New repository variable**
| Name | Value |
|------|-------|
| `HF_USERNAME` | your Hugging Face username |
| `HF_SPACE` | `bike-demand-capstone` (the Space name from step 3) |

Or do it all from the terminal:

```bash
gh secret set HF_TOKEN --body "hf_xxxxxxxxxxxxxxxxxxxxxxxx"
gh variable set HF_USERNAME --body "<your-hf-username>"
gh variable set HF_SPACE --body "bike-demand-capstone"
```

## 5. Make the Space see your app

Hugging Face reads YAML front-matter at the top of `README.md`. The scaffold already includes it —
just set `title` and confirm:

```yaml
---
title: Bike Demand Forecaster
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
---
```

(Streamlit Spaces serve `app_file` automatically — no port config needed.)

## 6. Verify the loop (smoke test)

Push a trivial change and watch it flow through:

```bash
git commit --allow-empty -m "ci: trigger deploy" && git push
```

- **GitHub → Actions tab:** "Deploy to Hugging Face Space" should go green.
- **HF Space page:** status flips *Building → Running* and the app loads.
- Live URL: `https://huggingface.co/spaces/<your-hf-username>/bike-demand-capstone`

Inspect from the terminal if needed:
```bash
hf spaces logs <your-hf-username>/bike-demand-capstone --tail 100
```

## Common gotchas

- **Shallow clone rejected by HF** — the workflow already uses `fetch-depth: 0`; don't change that.
- **First deploy fails to push** — the workflow force-pushes onto the Space's empty initial commit; that's expected on run #1.
- **App builds but errors** — check that `requirements.txt` lists every import your agent added.
- **Model file too big for git** — if your serialised model is large, track it with Git LFS (`git lfs track "models/*.pkl"`).
- **Token leaked** — if you ever paste the token into code, revoke it immediately in HF settings and issue a new one.
