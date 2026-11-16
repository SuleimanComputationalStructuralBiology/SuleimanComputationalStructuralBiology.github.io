<p align="center">
  <a href="https://suleimancomputationalstructuralbiology.github.io/">
    <img src="assets/logo.svg" alt="Suleiman Computational Structural Biology Logo" width="680"/>
  </a>
</p>

<p align="center">
  <strong>Public Web Portal for the Suleiman Computational Structural Biology Laboratory</strong>
</p>

<p align="center">
  <a href="https://suleimancomputationalstructuralbiology.github.io/"><img src="https://img.shields.io/badge/Public_Portal-Live_Site-0284c7?style=flat-square" alt="Live Site"/></a>
  <a href="https://github.com/SuleimanComputationalStructuralBiology"><img src="https://img.shields.io/badge/Organization-GitHub-334155?style=flat-square" alt="Organization"/></a>
  <a href="https://github.com/SuleimanComputationalStructuralBiology/SuleimanComputationalStructuralBiology"><img src="https://img.shields.io/badge/Core_Repository-Private-991b1b?style=flat-square" alt="Backend Repo"/></a>
  <a href="mailto:suleyman.hacizade1@gmail.com?subject=Access%20Request%20-%20SuleimanComputationalStructuralBiology%20Private%20Data"><img src="https://img.shields.io/badge/Access_Inquiries-suleyman.hacizade1%40gmail.com-047857?style=flat-square" alt="Request Access"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-15803d?style=flat-square" alt="License: MIT"/></a>
</p>

---

## Overview

This repository hosts the public frontend presentation portal and interactive 3D structural biology explorer for the [SuleimanComputationalStructuralBiology](https://github.com/SuleimanComputationalStructuralBiology) organization, deployed via GitHub Pages at:

**[https://suleimancomputationalstructuralbiology.github.io/](https://suleimancomputationalstructuralbiology.github.io/)**

The site presents research outputs, mathematical formulations, high-resolution figures, interactive macromolecular models, and an interlinked 48-note structural biology knowledge base developed by **Suleiman Hajizadeh** at the Institute of Molecular Biology (IMB).

> **Private Data and Access Policy:** The raw datasets, full multiple sequence alignments (MSAs), complete AlphaFold2 scoring tensors, docking trajectories, manuscript drafts, and backend source pipelines housed in `SuleimanComputationalStructuralBiology` are private. Researchers and academic reviewers wishing to request access should contact: **[suleyman.hacizade1@gmail.com](mailto:suleyman.hacizade1@gmail.com?subject=Access%20Request%20-%20SuleimanComputationalStructuralBiology%20Private%20Data)**.

---

## Architecture and File Organization

```
SuleimanComputationalStructuralBiology.github.io/
├── index.html               # Semantic HTML5 single-page application
├── css/
│   └── style.css            # Responsive stylesheet with dark/light themes
├── js/
│   ├── app.js               # Application coordinator, 3Dmol viewer, wiki reader
│   └── charts.js            # Canvas-based charts (pLDDT tracks and PAE heatmaps)
├── data/
│   ├── site.json            # Build metadata, synchronization timestamps, counts
│   ├── projects.json        # Project metadata, metrics, and structural summaries
│   ├── wiki.json            # 48 interlinked notes (entities, concepts, syntheses)
│   ├── curriculum.json      # Structural Bioinformatics MSc curriculum syllabus
│   └── tracks/
│       ├── akt1.json        # AKT1 per-residue pLDDT, binned PAE matrix, sequence
│       └── stn7-stn8.json   # STN7/STN8 chain pLDDT, heterodimer PAE, hydropathy
├── structures/
│   ├── AKT1_AF2_rank001.pdb                # Top-ranked AKT1 AlphaFold2 model
│   └── STN7_STN8_AF2multimer_rank001.pdb  # Top-ranked STN7-STN8 AF2-multimer model
├── research/                # Static deep pages for search engine indexing
├── methods/                 # Mathematical and biophysical formulations
├── knowledge/               # Structural biology knowledge base directory
├── gallery/                 # Publication figure gallery
├── curriculum/              # Academic curriculum syllabus
├── about/                   # Laboratory leadership and access governance
├── sitemap.xml              # XML sitemap covering all canonical URLs
├── sitemap-images.xml       # Image sitemap indexing all publication figures
└── robots.txt               # Crawler instructions and sitemap directives
```

### Interactive Features
* **Interactive 3D Structure Viewer (3Dmol.js)**:
  - Client-side WebGL rendering of **AKT1** (monomer) and **STN7-STN8** (heterodimer complex).
  - Visualization styles: Cartoon, Molecular Surface + Cartoon, Sticks, and Spheres.
  - Color palettes: pLDDT confidence spectrum, Chain distinction, Secondary Structure, and N-to-C spectrum.
* **Synchronized 2D Confidence and Error Tracks**:
  - Canvas-based per-residue pLDDT line chart with AlphaFold confidence intervals (>=90 Very High, 70-90 Confident, 50-70 Low, <50 Disordered).
  - Selecting any residue on the pLDDT track centers the 3D viewer directly on that Cα coordinate.
  - Predicted Aligned Error (PAE) heatmap with live coordinate readout in Angstroms.
* **Publication Figure Gallery**:
  - 30 high-resolution scientific figures categorized by project and analytical type.
  - Modal lightbox viewer with keyboard accessibility (Escape / light-dismiss).
* **Structural Biology Knowledge Base**:
  - 48 interlinked articles covering biological targets, biophysical concepts, syntheses, and primary literature.
  - Real-time search across titles, aliases, tags, and content.
  - Interactive reader modal rendering Markdown, sanitized HTML, LaTeX mathematical notation (KaTeX), and internal cross-references.

---

## Separation of Concerns: Core Repository vs Public Portal

| Concern | SuleimanComputationalStructuralBiology (Private Core) | SuleimanComputationalStructuralBiology.github.io (Public) |
|---|---|---|
| **Purpose** | Computation, raw data, pipeline execution, manuscripts | Web presentation, 3D visualization, figure access |
| **Data** | Full AlphaFold MSAs (.a3m), trajectory files, raw PDBQTs | Lightweight PDB models, downsampled JSON tracks |
| **Figures** | Full-resolution raw figure outputs | Web-optimized PNGs |
| **Manuscripts** | Working LaTeX and Markdown drafts | Published findings, metrics, and summaries |
| **Synchronization**| Runs `site_export/export_site_data.py` | Receives generated data and assets |

---

## Local Development and Preview

The portal is built as a static application and runs without package managers or build steps:

```bash
git clone https://github.com/SuleimanComputationalStructuralBiology/SuleimanComputationalStructuralBiology.github.io.git
cd SuleimanComputationalStructuralBiology.github.io
python3 -m http.server 8080
```
Open `http://localhost:8080` in your browser.

---

## License

This public presentation platform and its curated assets are released under the [MIT License](LICENSE).
Raw structural coordinates, pipeline code, and manuscript drafts in the private core repository remain restricted.

**Author:** Suleiman Hajizadeh  
**Affiliation:** Institute of Molecular Biology (IMB), Azerbaijan  
**Contact:** suleyman.hacizade1@gmail.com
