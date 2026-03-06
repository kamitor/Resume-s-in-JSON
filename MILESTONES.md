# Milestones — Career OS voor Christiaan Verhoef

Living document. Update when milestones are reached or when scope changes.

---

## Milestone 1 — First Acceptable Results ✅ DONE

**Goal:** Reproducible PDF cover letters, locked to 1 A4 page, with CI validation.

**Delivered:**
- `_stijl/brief-modern.tex` — header, contact icons, certification badges
- `_stijl/brief-klassiek.tex` — classic formal layout
- `_quarto.yml` — project-wide Quarto config, auto-loads `profiel.yml`
- `sollicitaties/_template/` — `brief.qmd`, `vacature.md`, `cv_config.yml` starters
- `.github/workflows/render.yml` — CI: installs Quarto + XeLaTeX, renders all `brief.qmd` files, validates PDFs exist, uploads artifacts

**Open items:** none

---

## Milestone 2 — Correct Certifications in rxresu.me ✅ DONE (partial)

**Goal:** Certifications in `profiel.yml` are the single source of truth and sync correctly to rxresume JSON.

**Delivered:**
- `profiel.yml` — audited and split into:
  - `certificeringen_cv` — 7 confirmed certifications (on CV)
  - `certificeringen_onbevestigd` — ~28 unconfirmed (to verify)
  - `certificeringen` — short list for letter badges
- `scripts/sync_certifications.py` — one-way sync: `profiel.yml` → `christiaan-verhoef_*.json`

**Open items:**
- [ ] Verify ~28 certs in `certificeringen_onbevestigd` and promote confirmed ones to `certificeringen_cv`
- [ ] Re-run `sync_certifications.py` after verification

---

## Milestone 3 — Career Document for Chris ⬜ IN PROGRESS

**Goal:** A structured personal career document for reflection, positioning, and interview prep.

**Delivered:**
- `career/career.qmd` — skeleton (identity statement, career tracks, SWOT placeholders)

**Open items:**
- [ ] Write identity statement: who is Christiaan, what does he build, for whom
- [ ] Career track analysis: which roles fit ENFP-T + skill set
- [ ] SWOT: Strengths, Weaknesses, Opportunities, Threats
- [ ] Extract patterns from past CVs and `profiel.yml` — signature capabilities
- [ ] Roles to avoid (and why)
- [ ] Render as PDF and/or HTML

---

## Milestone 4 — Job-Specific CV Generation ✅ DONE

**Goal:** Each application gets a tailored CV JSON file, validated and importable into rxresume.

**Delivered:**
- `scripts/new_job.py` — creates application folder from template; seeds `tracker.yml`
- `scripts/generate_cv.py` — applies `cv_config.yml` to base JSON (filter/reorder projects, skills, certs)
- `scripts/validate_cv.py` — validates rxresume JSON schema (required fields, nanoid IDs)
- `scripts/build_job.py` — full pipeline: `cv_config.yml` → `cv.json` → validate → `quarto render`
- `scripts/rxresume_import.py` — HTTP client to import CV into local rxresume instance

**Open items:** none

---

## Milestone 5 — Application Dashboard ✅ DONE

**Goal:** Visual overview of all applications — status, pipeline, timeline.

**Delivered:**
- `sollicitaties/tracker.yml` — central YAML tracking all applications (status, dates, salary, notes)
- `sollicitaties/dashboard.qmd` — Quarto HTML dashboard with:
  - Header stats (totaal, verstuurd, gesprekken, aanbiedingen)
  - Status pipeline bar chart (per status)
  - Conversion funnel (verstuurd→gesprek rate)
  - Color-coded applications table with days-since-sent
  - "Needs attention" section (stale/overdue applications)
  - Timeline chart (when applications were sent)
- `scripts/status.py` — CLI to quickly update tracker status and dates
- `scripts/check_consistency.py` — sync check: tracker vs actual folders
- `scripts/validate_profiel.py` — validates `profiel.yml` required fields
- `scripts/test_tracker.py` — unit tests for tracker schema
- `.github/workflows/test.yml` — CI: validate tracker, validate profiel, consistency check, render dashboard
- `.github/workflows/pages.yml` — CD: deploys dashboard to GitHub Pages on push to main

**URL:** https://kamitor.github.io/Resume-s-in-JSON/

**Open items:** none

---

## Milestone 6 — Portfolio (socialchicken.net) ⬜ PENDING

**Goal:** Public portfolio website, Quarto → GitHub Pages, custom domain.

**Structure:**
```
portfolio/
├── _quarto.yml     — type: website, navbar, theme
├── index.qmd       — hero / landing
├── about.qmd       — who is Christiaan (pulls from profiel.yml)
├── projects.qmd    — 5 flagship projects (from CV JSON)
├── cv.qmd          — CV summary + PDF download link
├── styles.css      — accent color #2563EB
└── CNAME           — socialchicken.net
```

**Open items:**
- [ ] Decide hosting: `kamitor.github.io` (free) vs `socialchicken.net` (custom domain)
- [ ] Create `portfolio/` Quarto website project
- [ ] Write `index.qmd` hero section (positioning statement)
- [ ] Write `about.qmd` (pull from profiel.yml + career document)
- [ ] Write `projects.qmd` — 5 flagship projects with impact summaries
- [ ] Create `.github/workflows/portfolio.yml` — deploy to `gh-pages` branch
- [ ] Configure DNS for `socialchicken.net` (A records or CNAME)

---

## Pipeline Reference

```
New application:
  python scripts/new_job.py YYYY-MM-DD_bedrijf_functie

Fill in:
  sollicitaties/YYYY-MM-DD_.../vacature.md
  sollicitaties/YYYY-MM-DD_.../brief.qmd
  sollicitaties/YYYY-MM-DD_.../cv_config.yml

Build (generate CV + render letter):
  python scripts/build_job.py sollicitaties/YYYY-MM-DD_.../

Update tracker status:
  python scripts/status.py YYYY-MM-DD_bedrijf_functie verstuurd
  python scripts/status.py YYYY-MM-DD_bedrijf_functie gesprek --datum 2026-04-01

Check consistency:
  python scripts/check_consistency.py

Validate profiel:
  python scripts/validate_profiel.py

Sync certifications to rxresume JSON:
  python scripts/sync_certifications.py [--dry-run]
```
