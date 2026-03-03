# Resume's in JSON & Sollicitatiebrieven

CV-data (Reactive Resume formaat) en Quarto-gebaseerde sollicitatiebrieven voor
Christiaan Verhoef.

---

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
