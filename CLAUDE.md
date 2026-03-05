# CLAUDE.md — Career OS voor Christiaan Verhoef

This project is a **Career Operating System**: a reproducible pipeline that generates tailored CVs and cover letters (sollicitatiebrieven) for job applications.

## Project Owner
Christiaan Verhoef — ENFP-T, positioning as a system-driven innovation leader.

---

## Project Structure

```
Resume-s-in-JSON/
├── _quarto.yml                          # Quarto project config
├── profiel.yml                          # Personal data (auto-loaded into all letters)
├── _stijl/
│   ├── brief-modern.tex                 # Modern template (header + icons + badges)
│   └── brief-klassiek.tex              # Classic formal template
├── sollicitaties/
│   ├── _template/                       # Starting point for new applications
│   │   ├── brief.qmd
│   │   └── vacature.md
│   └── YYYY-MM-DD_bedrijf_functie/      # One folder per application
│       ├── brief.qmd
│       ├── vacature.md
│       └── brief.pdf                    # Generated after render
├── christiaan-verhoef_*.json            # CV data (Reactive Resume export)
└── jsoncv's/                            # Additional CV JSON variants
```

---

## rxresume — CV Builder Stack

Running locally via Podman (rootless). Docker CE is installed but NOT used (iptables/nftables conflict on Fedora).

```bash
# Start the stack
./rxresume.sh up

# Stop
./rxresume.sh down

# Check status
./rxresume.sh status
```

UI: http://localhost:3000
Import `christiaan-verhoef_20260303_1718.json` to load the base CV.
`DOCKER_HOST=unix:///run/user/1000/podman/podman.sock` is set in `~/.bashrc`.

**CV pipeline (do not edit JSON manually):**
```bash
# New application
python scripts/new_job.py 2026-04-01_bedrijf_functie

# Build (generate cv.json + render brief.pdf)
python scripts/build_job.py sollicitaties/2026-04-01_bedrijf_functie/

# Sync certifications after changing profiel.yml
python scripts/sync_certifications.py [--dry-run]
```

---

## How to Start a New Application

1. Copy the template folder:
   ```bash
   cp -r sollicitaties/_template/ sollicitaties/YYYY-MM-DD_bedrijfsnaam_functie/
   ```
2. Fill in `vacature.md` — company details, requirements, contact person.
3. Edit `brief.qmd` — YAML frontmatter (company, role, date, salutation, certifications) and the letter body.
4. Render:
   ```bash
   quarto render sollicitaties/YYYY-MM-DD_bedrijfsnaam_functie/brief.qmd
   ```
   Output: `brief.pdf` in the same folder.

---

## Templates

- **`brief-modern.tex`** — Header with name + headline, contact icons, certification badges. Accent color configurable via `\definecolor{accent}{HTML}{...}`.
- **`brief-klassiek.tex`** — Traditional formal layout, no icons.

---

## Key Files

- **`profiel.yml`** — Single source of truth for personal data and default certifications. All letters load this automatically.
- **`_quarto.yml`** — Quarto project configuration.
- **`christiaan-verhoef_*.json`** — Reactive Resume CV exports.

---

## Requirements

- [Quarto](https://quarto.org) >= 1.4
- XeLaTeX: `sudo apt install texlive-xetex`
- LaTeX packages: `fontawesome5`, `xcolor`, `fontspec` (included in TeX Live)

---

## Active Milestones

### Milestone 1 — First Acceptable Results ✅ DONE
- [x] Letter template always renders on exactly 1 page (A4, locked margins, font, line height)
- [x] Multiple certifications don't overflow — compact bullet list, no page break inside block
- [x] Document title = `Sollicitatie – <Role> – <Organisation>` (dynamically injected)
- [x] GitHub Actions workflow: install Quarto + XeLaTeX, render, validate, upload PDF/JSON artifacts

### Milestone 2 — Correct Certifications in rxresu.me ✅ DONE (pending verification)
- [x] Audit and normalize certifications in `profiel.yml` — split into confirmed/unconfirmed/brief-badges
- [x] Map to rxresume JSON schema without manual edits (`sync_certifications.py`)
- [ ] Verify ~28 unconfirmed certs in `certificeringen_onbevestigd` and promote to `certificeringen_cv`

### Milestone 3 — Career Document for Chris
- [ ] `/career/career.qmd` with identity statement, career tracks, SWOT, ENFP-T strengths
- [ ] Deep research extraction: patterns from past CVs, signature capabilities, roles to avoid

### Milestone 4 — Job-Specific CV Generation ✅ DONE
- [x] Per-job config file (cv_config.yml per sollicitatie folder)
- [x] `generate_cv.py` filters/reorders projects, certifications, and skills per job
- [x] `validate_cv.py` validates rxresume JSON schema before import
- [x] `build_job.py` runs full pipeline: config → cv.json → validate → quarto render
- [x] `new_job.py` creates new application folder from template

### Milestone 5 — Application Dashboard
- [ ] Google Sheets tracking: vacancy, org, salary, dates, stage, outcome, CV/letter versions used
- [ ] Links to rendered artifacts per row

### Milestone 6 — Portfolio (socialchicken.net)
- [ ] Landing, About, Projects, Talks, CV download
- [ ] 5 flagship projects with impact summaries
- [ ] Linked to GitHub repos and generated CV

---

## Instructions for Claude

- **Always read `profiel.yml`** before editing any letter or CV — it is the single source of truth.
- **Letters must fit on 1 page** (A4). When writing or editing letter content, keep body concise.
- **Naming convention for application folders:** `YYYY-MM-DD_bedrijfsnaam_functie` (lowercase, underscores).
- **Do not edit rendered PDFs** — always edit the `.qmd` source and re-render.
- **When adding certifications**, update `profiel.yml` first, then ensure they map to the rxresume JSON schema.
- **Language:** letters are in Dutch (Nederlands). Code, configs, and file names are in English or Dutch depending on existing convention — match what's already there.
- **Do not over-engineer.** The goal is reproducible output, not complexity. Keep scripts and configs minimal.
- When creating a GitHub Actions workflow, install both Quarto and a full XeLaTeX distribution, and validate that PDFs are generated before uploading artifacts.
