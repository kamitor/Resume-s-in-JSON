# Resume's in JSON & Sollicitatiebrieven

CV-data (Reactive Resume formaat) en Quarto-gebaseerde sollicitatiebrieven voor
Christiaan Verhoef.

---

## To do

Milestone 1: First acceptable Results: 

- Format the quarto template so that the letters come out on one page each time.
- Format the quarto template in such a way that multipule certifications don't drop off the page (new line)
- The title of the document should be the job application that we're applying but creatively applied.
- Use Github Runners to automate the flow and make sure documents are renderd correctly every time. 

Milestone 2: 
https://rxresu.me/ - Now with the correct certifications; add all the onces from profile.yml

Milestone 3: A carreer for chris
A quarto document listing where chris is going, a personality profile, a swot matrix, extracting deep research for chris. 


Milestone 4: A new CV for every job:

- intergrate rxresume into workflow - create a unique CV for everyapplication.
- Format the CV to a working version of JSON. 

Milestone 5: 

- Create a dashboard for an overview of job applications that are to be done, overview of applications from the dashboard already created @: https://docs.google.com/spreadsheets/d/11DrcD_TH4VPhlmNaySlJ8uMBQTYM6Ahf6LWjojqNhO4/edit?gid=0#gid=0

Milestone 4: A portfolio for chris
Using socialchicken.net to create a cool website for chris that serves as his portfolio. 

# Career OS Roadmap – Christiaan Verhoef

## Where You Are Going

You are building a **Career Operating System**.

Not just CVs.
Not just letters.
Not just a portfolio.

You are building a reproducible system that:

- Standardizes your identity
- Automates tailored applications
- Aligns your ENFP-T strengths with strategic positioning
- Turns complexity into structured output
- Reduces emotional burnout from job searching
- Signals seniority through systems thinking

You are moving from:

> Capable but scattered generalist  
to  
> System-driven innovation leader with proof infrastructure

---
# Expanded Task List (Based on Your Original Milestones)

Below is your original structure — expanded, clarified, and broken into smaller executable steps — without changing your direction.

---

# Milestone 1 — First Acceptable Results

## 1. Format the Quarto template so letters always fit on one page

### Layout Lockdown
- [ ] Set paper size to A4
- [ ] Lock margins (explicit values, not defaults)
- [ ] Fix font family
- [ ] Fix base font size
- [ ] Fix line height
- [ ] Remove unpredictable spacing blocks

### Structural Constraints
- [ ] Define max number of paragraphs in letter body
- [ ] Define max bullet count if used
- [ ] Ensure no extra vertical spacing between sections
- [ ] Remove widow/orphan page breaks

### Overflow Protection
- [ ] Add fallback smaller font size option
- [ ] Add controlled paragraph trimming strategy
- [ ] Test with long vacancy titles
- [ ] Test with long organization names

### Validation
- [ ] Render 5 different test vacancies
- [ ] Confirm output is always exactly 1 page

---

## 2. Format certifications so multiple certifications don’t drop off page

### Data Structure
- [ ] Ensure certifications are structured in `profile.yml`
- [ ] Remove hard line breaks inside certification titles

### Rendering Control
- [ ] Convert certifications to compact bullet list
- [ ] Ensure text wrapping is enabled
- [ ] Reduce spacing between certification lines
- [ ] Prevent page break inside certification block

### Edge Case Testing
- [ ] Test with 3 certifications
- [ ] Test with 10 certifications
- [ ] Test with long certification names

---

## 3. Title of document = job application creatively applied

### Dynamic Title Injection
- [ ] Extract vacancy title from job config
- [ ] Extract organization name
- [ ] Apply naming pattern:
  - `Sollicitatie – <Role> – <Organisation>`

### Creative Layer
- [ ] Add optional subtitle logic:
  - Based on role type
  - Based on keywords (AI, ESG, Education, etc.)
- [ ] Ensure subtitle does not break layout

### Consistency
- [ ] Ensure title works in both PDF and JSON metadata
- [ ] Test with long titles

---

## 4. Use GitHub Runners to automate rendering

### Basic Automation
- [ ] Create `.github/workflows/build.yml`
- [ ] Install Quarto in workflow
- [ ] Install Python dependencies
- [ ] Run render command

### Validation
- [ ] Check JSON validity
- [ ] Check PDF exists
- [ ] Fail build if rendering fails

### Artifact Management
- [ ] Upload rendered CV
- [ ] Upload rendered letter
- [ ] Upload JSON

---

# Milestone 2 — rxresu.me (Correct Certifications)  (To be done by Chris Manually)

## 1. Sync Certifications from profile.yml

- [ ] Audit certifications in profile.yml
- [ ] Remove duplicates
- [ ] Normalize naming format
- [ ] Add missing certifications

## 2. Update rxresume JSON

- [ ] Map profile.yml certifications to rxresume schema


---

# Milestone 3 — A Career for Chris

## 1. Create Career Quarto Document

- [ ] Create `/career/career.qmd`
- [ ] Define professional identity statement
- [ ] Define 3 main career tracks
- [ ] Define value proposition per track

## 2. Personality Profile

- [ ] Write ENFP-T strengths in professional framing
- [ ] Write ENFP-T risks and mitigation strategies
- [ ] Align strengths with role types

## 3. SWOT Matrix

- [ ] Strengths (technical, strategic, ecosystem)
- [ ] Weaknesses (focus, over-extension)
- [ ] Opportunities (AI infrastructure, ESG regulation)
- [ ] Threats (market saturation, mispositioning)

## 4. Deep Research Extraction

- [ ] Extract patterns from past CVs
- [ ] Extract recurring themes from chats
- [ ] Identify signature capabilities
- [ ] Identify roles to avoid

---

# Milestone 4 — New CV for Every Job
 https://github.com/AmruthPillai/Reactive-Resume

## 1. Integrate rxresume into Workflow

- [ ] Create job configuration file:
  - Role
  - Organization
  - Emphasis tags
  - Tone
- [ ] Script filters projects by relevance
- [ ] Script filters certifications by relevance
- [ ] Reorder skills per job

## 2. Generate Unique CV JSON

- [ ] Create base JSON template
- [ ] Apply job-specific overrides
- [ ] Validate output JSON
- [ ] Ensure compatibility with rxresu.me

## 3. Render Job-Specific Outputs

- [ ] CV PDF
- [ ] Letter PDF
- [ ] JSON export


---

# Milestone 5 — Dashboard Overview

## 1. Define Application Tracking Structure

Columns:
- Vacancy Title
- Organization
- Location
- Salary
- Closing Date
- Applied?
- Interview Stage
- Outcome
- CV Version Used
- Letter Version Used

## 2. Sync With Generated Files

- [ ] Link dashboard rows to application folders
- [ ] Add link to rendered artifacts
- [ ] Add status flags (urgent, waiting, rejected, offer)

## 3. Automation

- [ ] Optional script to export Google Sheet CSV
- [ ] Optional script to validate missing artifacts

---

# Milestone 6 — Portfolio for Chris (socialchicken.net)

## 1. Structure Website

- [ ] Landing page
- [ ] About
- [ ] Projects
- [ ] Talks / Education
- [ ] Download CV

## 2. Content Preparation

- [ ] Extract 5 flagship projects
- [ ] Write impact-focused summaries
- [ ] Add visual proof where possible

## 3. Integration

- [ ] Link to generated CV
- [ ] Link to GitHub repositories
- [ ] Link to case studies

## 4. Deployment

- [ ] Configure hosting on socialchicken.net
- [ ] Ensure SSL
- [ ] Test mobile layout

---

# Final Outcome

You will have:

- A stable Quarto letter template
- A structured certification system
- Automated GitHub rendering
- Job-specific CV generation
- Application tracking dashboard
- A live portfolio site

All aligned, structured, and reproducible.

## Structuur

```
Resume-s-in-JSON/
├── _quarto.yml                          # Quarto project config
├── profiel.yml                          # Persoonlijke gegevens (auto-geladen)
│
├── _stijl/
│   ├── brief-modern.tex                 # Modern template (header + icoontjes)
│   └── brief-klassiek.tex              # Klassiek formeel template
│
├── sollicitaties/
│   ├── _template/                       # Startpunt voor nieuwe sollicitaties
│   │   ├── brief.qmd                    # Brief template (kopiëren!)
│   │   └── vacature.md                  # Vacature notities template
│   │
│   └── YYYY-MM-DD_bedrijf_functie/      # Één map per sollicitatie
│       ├── brief.qmd                    # De brief
│       ├── vacature.md                  # Vacature notities & status
│       └── brief.pdf                    # Gegenereerde PDF (na render)
│
└── christiaan-verhoef_*.json            # CV data (Reactive Resume export)
```

---

## Nieuwe sollicitatie starten

**1. Kopieer de template-map:**
```bash
cp -r sollicitaties/_template/ sollicitaties/2026-03-15_bedrijfsnaam_functie/
```

**2. Vul `vacature.md` in** — noteer de bedrijfsgegevens, vereisten en contactpersoon.

**3. Pas `brief.qmd` aan:**
- Vul de YAML frontmatter in (bedrijf, functie, datum, aanhef, enz.)
- Schrijf de brief in het markdown-gedeelte
- Kies je template: `brief-modern.tex` of `brief-klassiek.tex`
- Pas optioneel de `certificeringen` lijst aan voor deze functie

**4. Genereer de PDF:**
```bash
quarto render sollicitaties/2026-03-15_bedrijfsnaam_functie/brief.qmd
```

De PDF staat daarna in dezelfde map als `brief.pdf`.

---

## Templates

### `brief-modern.tex`
- Header met naam en headline
- Contactgegevens met icoontjes (telefoon, email, website, locatie)
- Certificeringen als kleurgebadges onder de header
- Accentkleur aanpasbaar in het `.tex` bestand (`\definecolor{accent}{HTML}{1A5276}`)

### `brief-klassiek.tex`
- Traditionele zakelijke brief layout
- Afzender rechtsboven, geadresseerde links
- Geen icoontjes, maximaal formeel

---

## Persoonlijke gegevens aanpassen

Bewerk `profiel.yml` voor wijzigingen in contactgegevens of de standaard
certificeringenlijst. Deze worden automatisch in alle brieven geladen.

---

## Vereisten

- [Quarto](https://quarto.org) >= 1.4
- XeLaTeX (onderdeel van TeX Live): `sudo apt install texlive-xetex`
- LaTeX pakketten: `fontawesome5`, `xcolor`, `fontspec` (in TeX Live aanwezig)
