<p align="center">
  <a href="https://suleimancomputationalstructuralbiology.github.io/">
    <img src="assets/logo.svg" alt="Suleiman Computational Structural Biology Logo" width="680"/>
  </a>
</p>

<p align="center">
  <strong>The Official Public Web Portal for the SuleimanComputationalStructuralBiology Organization</strong>
</p>

<p align="center">
  <a href="https://suleimancomputationalstructuralbiology.github.io/"><img src="https://img.shields.io/badge/Live_Portal-suleimancomputationalstructuralbiology.github.io-00f2fe?style=flat-square&logo=google-chrome&logoColor=white" alt="Live Site"/></a>
  <a href="https://github.com/SuleimanComputationalStructuralBiology"><img src="https://img.shields.io/badge/Organization-SuleimanComputationalStructuralBiology-7209b7?style=flat-square&logo=github&logoColor=white" alt="Organization"/></a>
  <a href="https://github.com/SuleimanComputationalStructuralBiology/SuleimanComputationalStructuralBiology"><img src="https://img.shields.io/badge/Private_Core_Repo-SuleimanComputationalStructuralBiology-darkred?style=flat-square&logo=lock&logoColor=white" alt="Backend Repo"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License: MIT"/></a>
</p>

---

## 🌐 Overview

This repository hosts the **public frontend presentation portal and interactive 3D structural biology explorer** for the [SuleimanComputationalStructuralBiology](https://github.com/SuleimanComputationalStructuralBiology) organization, deployed via GitHub Pages at:

👉 **[https://suleimancomputationalstructuralbiology.github.io/](https://suleimancomputationalstructuralbiology.github.io/)**

It showcases the research outputs, mathematical derivations, publication figures, interactive macromolecular models, and an interlinked 48-note structural biology knowledge base developed by **Suleiman Hajizadeh**.

---

## ✨ Features & Architecture

```
SuleimanComputationalStructuralBiology.github.io/
├── index.html               # Semantic HTML5 single-page application
├── css/
│   └── style.css            # Modern CSS: light-dark(), color-scheme meta, fluid typography
├── js/
│   ├── app.js               # Application coordinator, 3Dmol viewer, wiki reader, router
│   └── charts.js            # Zero-dependency canvas charts (pLDDT line track & PAE heatmap)
├── data/
│   ├── site.json            # Build metadata, sync timestamp & project counts
│   ├── projects.json        # Curated project metadata, metrics & domain models
│   ├── wiki.json            # 48 interlinked notes (entities, concepts, syntheses, sources)
│   ├── curriculum.json      # Structural Bioinformatics MSc curriculum syllabus
│   └── tracks/
│       ├── akt1.json        # AKT1 per-residue pLDDT, binned PAE matrix, sequence
│       └── stn7-stn8.json   # STN7/STN8 chain pLDDT, heterodimer PAE, hydropathy, entropy
├── structures/
│   ├── AKT1_AF2_rank001.pdb                # Top-ranked AKT1 AlphaFold2 model
│   └── STN7_STN8_AF2multimer_rank001.pdb  # Top-ranked STN7-STN8 AF2-multimer model
└── assets/
    ├── logo.svg, logo-icon.svg, og-image.png, favicon.*, manifest.json
    └── figures/
        ├── akt1/            # 8 publication-quality figures (PyMOL, pLDDT, Ramachandran, Contact Map)
        └── stn7-stn8/       # 22 publication figures (complex, domain maps, phylogeny, MSA, networks)
```

### 🔬 Interactive Capabilities
* **Interactive 3D Structure Viewer (3Dmol.js)**:
  - Real-time client-side WebGL rendering of **AKT1** (monomer) and **STN7–STN8** (heterodimer complex).
  - Multiple representation modes: **Cartoon**, **Molecular Surface + Cartoon**, **Sticks**, and **Spheres**.
  - Dynamic colouring schemes: **pLDDT confidence spectrum** (AlphaFold blue-to-orange palette), **Chain** (Chain A vs Chain B), **Secondary Structure**, and **N→C Spectrum**.
  - Interactive residue hover picking and click-to-center.
* **Synchronized 2D Confidence & Error Tracks**:
  - Pure Canvas-based per-residue **pLDDT line chart** with AlphaFold confidence bands ($\ge 90$ Very High, $70\text{--}90$ Confident, $50\text{--}70$ Low, $< 50$ Disordered).
  - Clicking any residue on the pLDDT track centers the 3D viewer directly on that C$\alpha$ coordinate!
  - Downsampled **Predicted Aligned Error (PAE) heatmap** with live $(\text{aligned}, \text{scored})$ coordinate readout in Ångströms.
* **Publication Figure Gallery**:
  - 30 high-resolution figures categorized by project and analysis type (Structure, Confidence, Heterodimer Complex, Evolution, Kinase Motifs, Networks).
  - Modal lightbox viewer with keyboard accessibility (`Esc` / light-dismiss).
* **Compounding Knowledge Base (LLM Wiki)**:
  - 48 interlinked notes compiled from primary literature, AlphaFold runs, and biophysical mechanics.
  - Real-time fuzzy search across titles, aliases, tags, and note content.
  - Interactive reader modal that renders GitHub Flavored Markdown (`marked`), sanitizes input (`DOMPurify`), renders LaTeX math formulas (`KaTeX`), and resolves `[[wikilinks]]` into seamless in-dialog note navigation.
* **Accessible Two-State Dark/Light Theme**:
  - Implements the modern web pattern for `<meta name="color-scheme">` synchronised with CSS `light-dark()` variables and instant flash-of-unstyled-content (FOUC) prevention.
  - Respects OS system preference by default and persists manual user adjustments.

---

## 🔒 Separation of Concerns: Private Backend vs Public Frontend

| Concern | 🔒 SuleimanComputationalStructuralBiology (Private Core) | 🌐 SuleimanComputationalStructuralBiology.github.io (Public) |
|---|---|---|
| **Purpose** | Heavy computation, raw data, pipelines, manuscripts | Clean, interactive web presentation |
| **Data** | Full AlphaFold `.a3m` MSAs, multi-gigabyte simulation trajectories, raw PDBQTs | Lightweight PDB models, downsampled JSON tracks |
| **Figures** | Full 6000x6000px raw exports | Web-optimized PNGs ($\le 1800\text{px}$) |
| **Manuscripts** | Unreleased LaTeX/Markdown drafts | Published findings & summary tables |
| **Syncing** | Runs `site_export/export_site_data.py` | Receives generated `data/` and `assets/` |

---

## 🛠️ Local Development & Preview

Because the portal is built as a pure static web application, no Node.js compilation or bundler is required:

```bash
# Clone the repository
git clone https://github.com/SuleimanComputationalStructuralBiology/SuleimanComputationalStructuralBiology.github.io.git
cd SuleimanComputationalStructuralBiology.github.io

# Start a local HTTP server
python3 -m http.server 8080
```
Open [http://localhost:8080](http://localhost:8080) in your browser.

---

## 📄 License

This public presentation platform and its curated assets are released under the [MIT License](LICENSE).
Raw structural coordinates, pipeline code, and manuscripts in the private backend are protected under their respective laboratory copyrights.

**Author:** [Suleiman Hajizadeh](https://github.com/SuleimanHajizadeh)  
📧 suleyman.hacizade1@gmail.com
