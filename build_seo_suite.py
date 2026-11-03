#!/usr/bin/env python3
"""
Enterprise / Senior Architect SEO Generator for Suleiman Computational Structural Biology.
Generates:
  1. robots.txt
  2. sitemap.xml (all canonical paths and data endpoints)
  3. sitemap-images.xml (Google Image Sitemap for all 30 publication figures)
  4. Pre-rendered semantic HTML subpages for all paths:
     - /research/index.html
     - /research/akt1/index.html
     - /research/stn7-stn8/index.html
     - /explorer/index.html
     - /gallery/index.html
     - /methods/index.html
     - /knowledge/index.html
     - /curriculum/index.html
     - /about/index.html
     - /404.html
  5. Injects Senior Architect JSON-LD Schema.org & Meta tags into /index.html
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime, timezone

SITE_URL = "https://suleimancomputationalstructuralbiology.github.io"
SITE_TITLE = "Suleiman Computational Structural Biology | AlphaFold2, Molecular Docking & Kinase Mechanics | IMB"
SITE_DESC = "Computational structural biology laboratory of Suleiman Hajizadeh (Institute of Molecular Biology, IMB). Deep-learning protein modeling (AlphaFold2/ColabFold), kinase structural mechanics, and automated molecular docking (AutoDock Vina) for AKT1 and STN7/STN8."
AUTHOR_NAME = "Suleiman Hajizadeh"
AUTHOR_EMAIL = "suleyman.hacizade1@gmail.com"
ORG_NAME = "Suleiman Computational Structural Biology"
ORG_INSTITUTE = "Institute of Molecular Biology (IMB)"
ORG_LOCATION = "Baku, Azerbaijan"
NOW_ISO = datetime.now(timezone.utc).strftime("%Y-%m-%d")

REPO_DIR = Path(__file__).resolve().parent

# Load data
with open(REPO_DIR / "data/projects.json", "r", encoding="utf-8") as f:
    PROJECTS = json.load(f)

with open(REPO_DIR / "data/wiki.json", "r", encoding="utf-8") as f:
    WIKI = json.load(f)

with open(REPO_DIR / "data/curriculum.json", "r", encoding="utf-8") as f:
    CURRICULUM = json.load(f)

def generate_robots_txt():
    content = f"""# robots.txt for Suleiman Computational Structural Biology
# Generated: {NOW_ISO}
# Website: {SITE_URL}/

User-agent: *
Allow: /
Allow: /research/
Allow: /research/akt1/
Allow: /research/stn7-stn8/
Allow: /explorer/
Allow: /gallery/
Allow: /methods/
Allow: /knowledge/
Allow: /curriculum/
Allow: /about/
Allow: /assets/
Allow: /data/
Allow: /structures/

# Host
Host: {SITE_URL}

# XML Sitemaps
Sitemap: {SITE_URL}/sitemap.xml
Sitemap: {SITE_URL}/sitemap-images.xml
"""
    with open(REPO_DIR / "robots.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Wrote robots.txt")

def generate_sitemap_xml():
    pages = [
        {"loc": f"{SITE_URL}/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": f"{SITE_URL}/research/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{SITE_URL}/research/akt1/", "priority": "0.9", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/research/stn7-stn8/", "priority": "0.9", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/explorer/", "priority": "0.85", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/gallery/", "priority": "0.85", "changefreq": "weekly"},
        {"loc": f"{SITE_URL}/methods/", "priority": "0.85", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/knowledge/", "priority": "0.85", "changefreq": "weekly"},
        {"loc": f"{SITE_URL}/curriculum/", "priority": "0.8", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/about/", "priority": "0.8", "changefreq": "monthly"},
        # Structural data files
        {"loc": f"{SITE_URL}/structures/AKT1_AF2_rank001.pdb", "priority": "0.7", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/structures/STN7_STN8_AF2multimer_rank001.pdb", "priority": "0.7", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/data/tracks/akt1.json", "priority": "0.6", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/data/tracks/stn7-stn8.json", "priority": "0.6", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/data/wiki.json", "priority": "0.6", "changefreq": "weekly"},
        {"loc": f"{SITE_URL}/data/projects.json", "priority": "0.6", "changefreq": "weekly"},
        {"loc": f"{SITE_URL}/data/curriculum.json", "priority": "0.6", "changefreq": "monthly"},
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    xml.append('        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    xml.append('        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">')
    
    for p in pages:
        xml.append('  <url>')
        xml.append(f'    <loc>{p["loc"]}</loc>')
        xml.append(f'    <lastmod>{NOW_ISO}</lastmod>')
        xml.append(f'    <changefreq>{p["changefreq"]}</changefreq>')
        xml.append(f'    <priority>{p["priority"]}</priority>')
        xml.append('  </url>')
    xml.append('</urlset>')

    with open(REPO_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml) + "\n")
    print(f"✓ Wrote sitemap.xml ({len(pages)} URLs)")

def generate_sitemap_images_xml():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    xml.append('        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')

    # Group figures by page URL
    fig_groups = [
        (f"{SITE_URL}/research/akt1/", PROJECTS[0]["figures"]),
        (f"{SITE_URL}/research/stn7-stn8/", PROJECTS[1]["figures"]),
        (f"{SITE_URL}/gallery/", PROJECTS[0]["figures"] + PROJECTS[1]["figures"]),
    ]

    for page_url, figs in fig_groups:
        xml.append('  <url>')
        xml.append(f'    <loc>{page_url}</loc>')
        for fig in figs:
            src = fig["src"]
            caption = fig["caption"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
            title = Path(src).stem.replace("_", " ").replace("-", " ")
            xml.append('    <image:image>')
            xml.append(f'      <image:loc>{SITE_URL}/{src}</image:loc>')
            xml.append(f'      <image:title>{title}</image:title>')
            xml.append(f'      <image:caption>{caption}</image:caption>')
            xml.append('    </image:image>')
        xml.append('  </url>')
    xml.append('</urlset>')

    with open(REPO_DIR / "sitemap-images.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml) + "\n")
    print("✓ Wrote sitemap-images.xml (30 publication figures mapped)")

def build_master_schema():
    faq = [
        {
            "@type": "Question",
            "name": "What is the structural biology focus of the Suleiman Computational Structural Biology lab?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "The laboratory bridges transcriptomics/WGCNA co-expression network analysis, deep learning macromolecular structure prediction (AlphaFold2, ColabFold v1.6.1, AF2-multimer), vector-algebraic structural analytics, and allosteric molecular docking (AutoDock Vina) to study human oncogenic hub kinases (AKT1) and photosynthetic chloroplast kinases (STN7 and STN8)."
            }
        },
        {
            "@type": "Question",
            "name": "What are the structural findings for the AKT1 hub kinase model?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "AKT1 was predicted using AlphaFold2 (mean pLDDT 65.61 with a catalytic core >= 90). Analysis revealed 573 long-range non-trivial C-alpha contacts (<= 8.0 A, |i-j| >= 6), and Ramachandran dihedral distribution showing 24.6% alpha-helix, 32.9% beta-strand, 3.1% left-handed/Gly, and 39.4% loops."
            }
        },
        {
            "@type": "Question",
            "name": "How is the STN7-STN8 chloroplast kinase heterodimer complex characterized?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "STN7 and STN8 thylakoid kinases from Arabidopsis thaliana share 36.1% sequence identity. The heterodimer was modeled with AlphaFold2-multimer v3 (ipTM 0.72, pTM 0.78, 2,179 contact pairs). SVD superposition revealed an RMSD of 3.76 A over 312 C-alpha atoms. Virtual screening of ATP, ADP, Staurosporine, K252a, SB216763, and Quercetin identified conserved active-site geometries."
            }
        },
        {
            "@type": "Question",
            "name": "How can researchers request access to the private core repository and raw datasets?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "All raw datasets, complete MSAs, AlphaFold scoring matrices, docking trajectories, and backend pipelines in SuleimanComputationalStructuralBiology are private. Researchers wishing to obtain access may apply via email to suleyman.hacizade1@gmail.com."
            }
        },
        {
            "@type": "Question",
            "name": "What academic curriculum does the laboratory provide for structural bioinformatics?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "The laboratory features a 9-module Master's level curriculum covering VMD visualization, stochastic thermodynamics, GROMACS molecular dynamics, MDAnalysis, PLUMED metadynamics, CP2K QM/MM, AlphaFold2/ColabFold modeling, AutoDock Vina docking, and RFdiffusion/ProteinMPNN de novo protein design."
            }
        }
    ]

    graph = [
        {
            "@type": "WebSite",
            "@id": f"{SITE_URL}/#website",
            "url": f"{SITE_URL}/",
            "name": ORG_NAME,
            "alternateName": ["SuleimanCSB", "Suleiman Structural Biology", "Suleiman Hajizadeh Structural Biology"],
            "description": SITE_DESC,
            "publisher": {
                "@id": f"{SITE_URL}/#organization"
            },
            "inLanguage": "en-US",
            "potentialAction": {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": f"{SITE_URL}/knowledge/?q={{search_term_string}}"
                },
                "query-input": "required name=search_term_string"
            }
        },
        {
            "@type": "Organization",
            "@id": f"{SITE_URL}/#organization",
            "name": ORG_NAME,
            "alternateName": "SuleimanCSB Laboratory",
            "url": f"{SITE_URL}/",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/assets/logo-emblem.png",
                "width": 512,
                "height": 512,
                "caption": "Suleiman Computational Structural Biology Emblem"
            },
            "image": f"{SITE_URL}/assets/og-image.png",
            "email": AUTHOR_EMAIL,
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Baku",
                "addressCountry": "Azerbaijan"
            },
            "founder": {
                "@id": f"{SITE_URL}/#author"
            },
            "member": [
                {"@id": f"{SITE_URL}/#author"}
            ],
            "parentOrganization": {
                "@type": "EducationalOrganization",
                "name": ORG_INSTITUTE,
                "alternateName": "IMB",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Baku",
                    "addressCountry": "Azerbaijan"
                }
            },
            "sameAs": [
                "https://github.com/SuleimanComputationalStructuralBiology",
                "https://github.com/SuleimanHajizadeh"
            ]
        },
        {
            "@type": "Person",
            "@id": f"{SITE_URL}/#author",
            "name": AUTHOR_NAME,
            "jobTitle": "Lead Structural Bioinformatician & Computational Biologist",
            "worksFor": {
                "@id": f"{SITE_URL}/#organization"
            },
            "affiliation": {
                "@type": "Organization",
                "name": ORG_INSTITUTE,
                "alternateName": "IMB"
            },
            "email": AUTHOR_EMAIL,
            "url": f"{SITE_URL}/about/",
            "sameAs": [
                "https://github.com/SuleimanHajizadeh",
                "https://github.com/SuleimanComputationalStructuralBiology"
            ],
            "knowsAbout": [
                "Computational Structural Biology",
                "AlphaFold2 & ColabFold",
                "Protein Structure Prediction",
                "Molecular Docking (AutoDock Vina)",
                "Kinase Structural Mechanics",
                "Triple-Negative Breast Cancer (TNBC)",
                "Photosystem II Regulation (STN7 & STN8)",
                "Ramachandran Dihedral Analysis",
                "Predicted Aligned Error (PAE)",
                "Local Distance Difference Test (pLDDT)",
                "Molecular Dynamics (GROMACS)",
                "Quantum Mechanics / Molecular Mechanics (QM/MM)"
            ]
        },
        {
            "@type": "ResearchProject",
            "@id": f"{SITE_URL}/research/akt1/#project",
            "name": "AKT1 Kinase Structural Modeling in Triple-Negative Breast Cancer",
            "alternateName": "AlphaFold2 AKT1 Structural Analytics",
            "url": f"{SITE_URL}/research/akt1/",
            "description": "De novo deep-learning structure prediction of the oncogenic hub kinase AKT1 (UniProt: P31749) using AlphaFold2 and ColabFold v1.6.1, with per-residue pLDDT confidence analysis, Ramachandran dihedral torsion calculations, and C-alpha contact map topology.",
            "funder": {
                "@id": f"{SITE_URL}/#organization"
            },
            "studySubject": {
                "@type": "BioChemEntity",
                "name": "RAC-alpha serine/threonine-protein kinase",
                "identifier": "P31749",
                "url": "https://www.uniprot.org/uniprotkb/P31749/entry"
            }
        },
        {
            "@type": "ResearchProject",
            "@id": f"{SITE_URL}/research/stn7-stn8/#project",
            "name": "STN7 and STN8 Chloroplast Thylakoid Kinases Complex & Molecular Docking",
            "alternateName": "STN7-STN8 AF2-Multimer Heterodimer & Virtual Screening",
            "url": f"{SITE_URL}/research/stn7-stn8/",
            "description": "Comparative structural, phylogenetic and complex modeling of Arabidopsis thaliana photosynthetic kinases STN7 (Q9S713) and STN8 (Q9LZV4) using AlphaFold2-multimer, SVD superposition, conserved kinase motif mapping, and high-throughput AutoDock Vina screening.",
            "funder": {
                "@id": f"{SITE_URL}/#organization"
            },
            "studySubject": [
                {
                    "@type": "BioChemEntity",
                    "name": "Serine/threonine-protein kinase STN7, chloroplastic",
                    "identifier": "Q9S713",
                    "url": "https://www.uniprot.org/uniprotkb/Q9S713/entry"
                },
                {
                    "@type": "BioChemEntity",
                    "name": "Serine/threonine-protein kinase STN8, chloroplastic",
                    "identifier": "Q9LZV4",
                    "url": "https://www.uniprot.org/uniprotkb/Q9LZV4/entry"
                }
            ]
        },
        {
            "@type": "Dataset",
            "@id": f"{SITE_URL}/structures/AKT1_AF2_rank001.pdb",
            "name": "AlphaFold2 AKT1 Structure Model & Confidence Tracks",
            "description": "Predicted 3D macromolecular coordinate file (PDB) and per-residue pLDDT confidence track for human AKT1 kinase.",
            "url": f"{SITE_URL}/structures/AKT1_AF2_rank001.pdb",
            "creator": {"@id": f"{SITE_URL}/#author"},
            "license": "https://opensource.org/licenses/MIT",
            "distribution": [
                {
                    "@type": "DataDownload",
                    "encodingFormat": "chemical/x-pdb",
                    "contentUrl": f"{SITE_URL}/structures/AKT1_AF2_rank001.pdb"
                },
                {
                    "@type": "DataDownload",
                    "encodingFormat": "application/json",
                    "contentUrl": f"{SITE_URL}/data/tracks/akt1.json"
                }
            ]
        },
        {
            "@type": "Dataset",
            "@id": f"{SITE_URL}/structures/STN7_STN8_AF2multimer_rank001.pdb",
            "name": "AlphaFold2-Multimer STN7-STN8 Heterodimer Complex Coordinates",
            "description": "Predicted 3D coordinate model (PDB) and inter-chain PAE error matrices for Arabidopsis STN7-STN8 heterodimer complex.",
            "url": f"{SITE_URL}/structures/STN7_STN8_AF2multimer_rank001.pdb",
            "creator": {"@id": f"{SITE_URL}/#author"},
            "license": "https://opensource.org/licenses/MIT",
            "distribution": [
                {
                    "@type": "DataDownload",
                    "encodingFormat": "chemical/x-pdb",
                    "contentUrl": f"{SITE_URL}/structures/STN7_STN8_AF2multimer_rank001.pdb"
                },
                {
                    "@type": "DataDownload",
                    "encodingFormat": "application/json",
                    "contentUrl": f"{SITE_URL}/data/tracks/stn7-stn8.json"
                }
            ]
        },
        {
            "@type": "Course",
            "@id": f"{SITE_URL}/curriculum/#course",
            "name": "Structural Bioinformatics (MSc Curriculum)",
            "description": "Comprehensive 9-module structural bioinformatics and biomolecular modeling curriculum covering molecular dynamics (GROMACS), enhanced sampling, QM/MM, AlphaFold2, and de novo protein design.",
            "provider": {"@id": f"{SITE_URL}/#organization"},
            "instructor": {"@type": "Person", "name": "Prof. Carlo Camilloni & Suleiman Hajizadeh"}
        },
        {
            "@type": "FAQPage",
            "@id": f"{SITE_URL}/#faq",
            "mainEntity": faq
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{SITE_URL}/#breadcrumbs",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "Research", "item": f"{SITE_URL}/research/"},
                {"@type": "ListItem", "position": 3, "name": "3D Explorer", "item": f"{SITE_URL}/explorer/"},
                {"@type": "ListItem", "position": 4, "name": "Figure Gallery", "item": f"{SITE_URL}/gallery/"},
                {"@type": "ListItem", "position": 5, "name": "Methods", "item": f"{SITE_URL}/methods/"},
                {"@type": "ListItem", "position": 6, "name": "Knowledge Base", "item": f"{SITE_URL}/knowledge/"},
                {"@type": "ListItem", "position": 7, "name": "Curriculum", "item": f"{SITE_URL}/curriculum/"},
                {"@type": "ListItem", "position": 8, "name": "About", "item": f"{SITE_URL}/about/"}
            ]
        }
    ]

    return {"@context": "https://schema.org", "@graph": graph}

def render_page_template(title, description, canonical_url, breadcrumbs, content_html, extra_head="", root_rel="../"):
    schema_breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": b["name"], "item": b["url"]}
            for i, b in enumerate(breadcrumbs)
        ]
    }

    bc_html = ' <span class="bc-sep">/</span> '.join(
        [f'<a href="{b["url"]}">{b["name"]}</a>' if i < len(breadcrumbs)-1 else f'<span>{b["name"]}</span>'
         for i, b in enumerate(breadcrumbs)]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="color-scheme" content="light dark" />
  <script>try{{document.querySelector('meta[name="color-scheme"]').content=localStorage.getItem("color-scheme")??"light dark"}}catch(e){{}}</script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="Computational Structural Biology, AlphaFold2, ColabFold, AF2-multimer, AKT1, STN7, STN8, pLDDT, PAE, Ramachandran, Molecular Docking, AutoDock Vina, Suleiman Hajizadeh, IMB, Institute of Molecular Biology" />
  <meta name="author" content="{AUTHOR_NAME}" />
  <meta name="creator" content="{AUTHOR_NAME}" />
  <meta name="publisher" content="{ORG_INSTITUTE}" />
  <meta name="theme-color" content="#0b1020" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <meta name="bingbot" content="index, follow, max-snippet:-1, max-image-preview:large" />

  <link rel="canonical" href="{canonical_url}" />
  <link rel="alternate" hreflang="en" href="{canonical_url}" />
  <link rel="alternate" hreflang="x-default" href="{canonical_url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="{ORG_NAME}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:image" content="{SITE_URL}/assets/og-image.png" />
  <meta property="og:image:secure_url" content="{SITE_URL}/assets/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{title}" />
  <meta property="og:locale" content="en_US" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="twitter:image" content="{SITE_URL}/assets/og-image.png" />
  <meta name="twitter:creator" content="@SuleimanHajizadeh" />
  <meta name="twitter:site" content="@SuleimanHajizadeh" />

  <!-- Academic Citations & Dublin Core -->
  <meta name="citation_title" content="{title}" />
  <meta name="citation_author" content="Hajizadeh, Suleiman" />
  <meta name="citation_publication_date" content="2026/04/01" />
  <meta name="citation_technical_report_institution" content="{ORG_INSTITUTE}" />
  <meta name="DC.title" content="{title}" />
  <meta name="DC.creator" content="{AUTHOR_NAME}" />
  <meta name="DC.description" content="{description}" />
  <meta name="DC.publisher" content="{ORG_INSTITUTE}" />
  <meta name="DC.language" content="en" />

  <link rel="icon" type="image/svg+xml" href="{root_rel}favicon.svg" />
  <link rel="apple-touch-icon" href="{root_rel}apple-touch-icon.png" />
  <link rel="manifest" href="{root_rel}manifest.json" />

  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous" />
  <link rel="stylesheet" href="{root_rel}css/style.css" />

  <script type="application/ld+json">
{json.dumps(schema_breadcrumbs, indent=2)}
  </script>
{extra_head}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="navbar">
    <div class="container navbar-inner">
      <a href="{root_rel}#top" class="brand" aria-label="Suleiman Computational Structural Biology — home">
        <img src="{root_rel}assets/logo-icon.svg" alt="SuleimanCSB Logo" width="36" height="36" />
        <span class="brand-text">Suleiman<span class="accent">CSB</span></span>
      </a>
      <nav aria-label="Main Navigation">
        <ul class="nav-links" id="navLinks">
          <li><a href="{root_rel}research/">Research</a></li>
          <li><a href="{root_rel}explorer/">3D Explorer</a></li>
          <li><a href="{root_rel}gallery/">Figures</a></li>
          <li><a href="{root_rel}methods/">Methods</a></li>
          <li><a href="{root_rel}knowledge/">Knowledge Base</a></li>
          <li><a href="{root_rel}curriculum/">Curriculum</a></li>
          <li><a href="{root_rel}about/">About</a></li>
        </ul>
      </nav>
      <div class="nav-actions">
        <button id="themeToggle" class="btn-icon" type="button" aria-label="Toggle theme">
          <svg class="icon-sun" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          <svg class="icon-moon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <a class="btn btn-primary btn-sm" href="https://github.com/SuleimanComputationalStructuralBiology" target="_blank" rel="noopener noreferrer">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.21 11.39.6.11.79-.26.79-.58v-2.23c-3.34.73-4.03-1.42-4.03-1.42-.55-1.39-1.33-1.76-1.33-1.76-1.09-.75.08-.73.08-.73 1.2.08 1.84 1.24 1.84 1.24 1.07 1.83 2.81 1.3 3.49 1 .11-.78.42-1.31.76-1.6-2.67-.31-5.47-1.34-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.65.24 2.87.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.62-5.48 5.92.43.37.82 1.1.82 2.22v3.29c0 .32.19.69.8.58C20.57 21.8 24 17.3 24 12c0-6.63-5.37-12-12-12z"/></svg>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </header>

  <main id="main">
    <div class="container" style="padding-top: 1.5rem;">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        {bc_html}
      </nav>
    </div>

    {content_html}
  </main>

  <footer class="footer">
    <div class="container footer-inner">
      <p>© 2026 {AUTHOR_NAME} · {ORG_NAME} ({ORG_INSTITUTE}) · 🔒 Private data access: <a href="mailto:{AUTHOR_EMAIL}">{AUTHOR_EMAIL}</a></p>
      <p class="muted"><a href="{root_rel}sitemap.xml">Sitemap XML</a> · <a href="{root_rel}sitemap-images.xml">Image Sitemap</a> · <a href="{root_rel}robots.txt">robots.txt</a></p>
    </div>
  </footer>

  <script src="{root_rel}js/app.js" defer></script>
</body>
</html>
"""

def generate_subpages():
    # 1. /research/index.html
    akt = PROJECTS[0]
    stn = PROJECTS[1]

    research_html = f"""
    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Research Portfolio</p>
          <h1>Computational Structural Biology Research Projects</h1>
          <p class="lead">Reproducible deep learning structure prediction, geometric analytics and allosteric virtual screening pipelines conducted at the {ORG_INSTITUTE}.</p>
        </header>

        <div class="access-notice" role="note">
          <span class="access-icon">🔒</span>
          <p>
            <strong>Private Data &amp; Core Repository Notice:</strong> All raw MSAs, full AlphaFold score matrices, molecular dynamics trajectories and docking workflows are securely stored in the private core repository. To request research access, please email <a href="mailto:{AUTHOR_EMAIL}?subject=Access%20Request%20-%20SuleimanComputationalStructuralBiology%20Private%20Data">{AUTHOR_EMAIL}</a>.
          </p>
        </div>

        <div class="project-grid" style="margin-top: 2rem;">
          <!-- AKT1 Card -->
          <article class="method-card" style="display: flex; flex-direction: column; gap: 1rem;">
            <div>
              <span class="pill" data-type="entity">Homo sapiens · P31749</span>
              <h2 style="margin: 0.5rem 0 0.2rem;"><a href="{SITE_URL}/research/akt1/" style="color: inherit; text-decoration: none;">{akt['title']}</a></h2>
              <p class="muted" style="margin: 0;">{akt['subtitle']}</p>
            </div>
            <p>{akt['summary']}</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; background: var(--surface-2); padding: 0.9rem; border-radius: 10px;">
              <div><strong>{akt['metrics'][0]['value']}</strong><br/><span class="muted" style="font-size: 0.75rem;">Residues</span></div>
              <div><strong>{akt['metrics'][1]['value']}</strong><br/><span class="muted" style="font-size: 0.75rem;">Mean pLDDT</span></div>
              <div><strong>{akt['metrics'][5]['value']}</strong><br/><span class="muted" style="font-size: 0.75rem;">Cα Contacts</span></div>
            </div>
            <div style="margin-top: auto; display: flex; gap: 0.75rem; flex-wrap: wrap;">
              <a href="{SITE_URL}/research/akt1/" class="btn btn-primary btn-sm">Read Full Project Dossier →</a>
              <a href="{SITE_URL}/#explorer" class="btn btn-ghost btn-sm">Inspect in 3D Viewer</a>
            </div>
          </article>

          <!-- STN7/STN8 Card -->
          <article class="method-card" style="display: flex; flex-direction: column; gap: 1rem;">
            <div>
              <span class="pill" data-type="entity">Arabidopsis thaliana · Q9S713 / Q9LZV4</span>
              <h2 style="margin: 0.5rem 0 0.2rem;"><a href="{SITE_URL}/research/stn7-stn8/" style="color: inherit; text-decoration: none;">{stn['title']}</a></h2>
              <p class="muted" style="margin: 0;">{stn['subtitle']}</p>
            </div>
            <p>{stn['summary']}</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; background: var(--surface-2); padding: 0.9rem; border-radius: 10px;">
              <div><strong>{stn['metrics'][2]['value']}</strong><br/><span class="muted" style="font-size: 0.75rem;">Kinase RMSD</span></div>
              <div><strong>{stn['metrics'][3]['value']}</strong><br/><span class="muted" style="font-size: 0.75rem;">AF2-multimer ipTM</span></div>
              <div><strong>{stn['metrics'][5]['value']}</strong><br/><span class="muted" style="font-size: 0.75rem;">Conserved MSA</span></div>
            </div>
            <div style="margin-top: auto; display: flex; gap: 0.75rem; flex-wrap: wrap;">
              <a href="{SITE_URL}/research/stn7-stn8/" class="btn btn-primary btn-sm">Read Full Project Dossier →</a>
              <a href="{SITE_URL}/#explorer" class="btn btn-ghost btn-sm">Inspect in 3D Viewer</a>
            </div>
          </article>
        </div>
      </div>
    </section>
    """
    p = REPO_DIR / "research/index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(render_page_template(
            title="Research Portfolio | Suleiman Computational Structural Biology",
            description="Deep learning protein structure modeling, kinase biophysics, and molecular docking projects for AKT1 and STN7/STN8 chloroplast kinases.",
            canonical_url=f"{SITE_URL}/research/",
            breadcrumbs=[{"name": "Home", "url": f"{SITE_URL}/"}, {"name": "Research", "url": f"{SITE_URL}/research/"}],
            content_html=research_html,
            root_rel="../"
        ))
    print("✓ Wrote /research/index.html")

    # 2. /research/akt1/index.html
    akt_figs_html = "".join([
        f"""
        <figure class="fig" style="cursor: default;">
          <img src="{SITE_URL}/{fig['src']}" alt="{fig['caption']}" loading="lazy" />
          <figcaption><strong>{fig['category'].upper()}</strong>: {fig['caption']}</figcaption>
        </figure>
        """ for fig in akt['figures']
    ])

    akt_html = f"""
    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Oncogenic Hub Kinase Modeling</p>
          <h1>{akt['title']}</h1>
          <p class="lead">{akt['subtitle']} — UniProt: <a href="https://www.uniprot.org/uniprotkb/P31749/entry" target="_blank" rel="noopener">P31749</a> (Homo sapiens)</p>
        </header>

        <div class="access-notice" role="note">
          <span class="access-icon">🔒</span>
          <p>
            <strong>Private Backend Access:</strong> Raw ColabFold scoring tensors, full MSA files (.a3m), and manuscript drafts are maintained in the private core repository. To request access, email <a href="mailto:{AUTHOR_EMAIL}?subject=Access%20Request%20-%20AKT1%20Raw%20Data">{AUTHOR_EMAIL}</a>.
          </p>
        </div>

        <article class="prose" style="max-width: 900px; margin-top: 2rem;">
          <h2>Project Overview &amp; Systems Biology Context</h2>
          <p>{akt['summary']}</p>

          <h2>Key Structural Findings</h2>
          <ul>
            {"".join(f"<li>{f}</li>" for f in akt['findings'])}
          </ul>

          <h2>Quantitative Metrics &amp; Benchmarks</h2>
          <table>
            <thead><tr><th>Metric</th><th>Value</th></tr></thead>
            <tbody>
              {"".join(f"<tr><td><strong>{m['label']}</strong></td><td>{m['value']}</td></tr>" for m in akt['metrics'])}
            </tbody>
          </table>

          <h2>Reproducible Computational Pipeline</h2>
          <ol>
            {"".join(f"<li>{step}</li>" for step in akt['pipeline'])}
          </ol>

          <h2>Published Structural Models &amp; Tracks</h2>
          <p>
            <a href="{SITE_URL}/structures/AKT1_AF2_rank001.pdb" download class="btn btn-ghost btn-sm">Download Top-Ranked PDB (AKT1_AF2_rank001.pdb)</a>
            <a href="{SITE_URL}/data/tracks/akt1.json" download class="btn btn-ghost btn-sm">Download Confidence Track JSON (akt1.json)</a>
            <a href="{SITE_URL}/#explorer" class="btn btn-primary btn-sm">Open in Interactive 3D Viewer</a>
          </p>

          <h2>Publication Figures &amp; Structural Topology</h2>
          <div class="gallery" style="margin-top: 1.5rem;">
            {akt_figs_html}
          </div>
        </article>
      </div>
    </section>
    """
    p = REPO_DIR / "research/akt1/index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(render_page_template(
            title="AKT1 Kinase Structural Modeling (TNBC Hub) | AlphaFold2 Analytics",
            description="AlphaFold2 modeling, Ramachandran dihedral torsion analysis, and C-alpha contact topology for the human oncogenic hub kinase AKT1 (P31749).",
            canonical_url=f"{SITE_URL}/research/akt1/",
            breadcrumbs=[
                {"name": "Home", "url": f"{SITE_URL}/"},
                {"name": "Research", "url": f"{SITE_URL}/research/"},
                {"name": "AKT1 Kinase", "url": f"{SITE_URL}/research/akt1/"}
            ],
            content_html=akt_html,
            root_rel="../../"
        ))
    print("✓ Wrote /research/akt1/index.html")

    # 3. /research/stn7-stn8/index.html
    stn_figs_html = "".join([
        f"""
        <figure class="fig" style="cursor: default;">
          <img src="{SITE_URL}/{fig['src']}" alt="{fig['caption']}" loading="lazy" />
          <figcaption><strong>{fig['category'].upper()}</strong>: {fig['caption']}</figcaption>
        </figure>
        """ for fig in stn['figures']
    ])

    stn_html = f"""
    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Photosynthetic Kinase Evolution &amp; Complex Modeling</p>
          <h1>{stn['title']}</h1>
          <p class="lead">{stn['subtitle']} — Arabidopsis thaliana (STN7: Q9S713, STN8: Q9LZV4)</p>
        </header>

        <div class="access-notice" role="note">
          <span class="access-icon">🔒</span>
          <p>
            <strong>Private Research Data Notice:</strong> Docking pose coordinates, full Vina configuration logs, and unreleased comparative manuscripts reside in the private core repository. For data access requests, please contact <a href="mailto:{AUTHOR_EMAIL}?subject=Access%20Request%20-%20STN7%20STN8%20Data">{AUTHOR_EMAIL}</a>.
          </p>
        </div>

        <article class="prose" style="max-width: 900px; margin-top: 2rem;">
          <h2>Project Overview &amp; Photosynthetic State Transitions</h2>
          <p>{stn['summary']}</p>

          <h2>Key Structural &amp; Evolutionary Discoveries</h2>
          <ul>
            {"".join(f"<li>{f}</li>" for f in stn['findings'])}
          </ul>

          <h2>Quantitative Metrics &amp; Complex Benchmarks</h2>
          <table>
            <thead><tr><th>Metric</th><th>Value</th><th>Note</th></tr></thead>
            <tbody>
              {"".join(f"<tr><td><strong>{m['label']}</strong></td><td>{m['value']}</td><td>{m.get('note', '')}</td></tr>" for m in stn['metrics'])}
            </tbody>
          </table>

          <h2>Screened Ligand Library (AutoDock Vina Virtual Screening)</h2>
          <table>
            <thead><tr><th>Ligand</th><th>PubChem CID</th><th>Molecular Weight</th><th>Biological Role</th></tr></thead>
            <tbody>
              {"".join(f"<tr><td><strong>{l['name']}</strong></td><td>{l['cid']}</td><td>{l['mw']} Da</td><td>{l['role']}</td></tr>" for l in stn['ligands'])}
            </tbody>
          </table>

          <h2>Structural Models &amp; Heterodimer Coordinates</h2>
          <p>
            <a href="{SITE_URL}/structures/STN7_STN8_AF2multimer_rank001.pdb" download class="btn btn-ghost btn-sm">Download Heterodimer Complex PDB (STN7_STN8_AF2multimer_rank001.pdb)</a>
            <a href="{SITE_URL}/data/tracks/stn7-stn8.json" download class="btn btn-ghost btn-sm">Download Complex Tracks JSON (stn7-stn8.json)</a>
            <a href="{SITE_URL}/#explorer" class="btn btn-primary btn-sm">Explore Complex in 3D Viewer</a>
          </p>

          <h2>Publication Figures &amp; Comparative Analytics</h2>
          <div class="gallery" style="margin-top: 1.5rem;">
            {stn_figs_html}
          </div>
        </article>
      </div>
    </section>
    """
    p = REPO_DIR / "research/stn7-stn8/index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(render_page_template(
            title="STN7 / STN8 Chloroplast Kinase Complex & Molecular Docking | AF2-Multimer",
            description="AlphaFold2-multimer heterodimer modeling, SVD structural alignment, phylogeny, and AutoDock Vina screening of chloroplast thylakoid kinases STN7 and STN8.",
            canonical_url=f"{SITE_URL}/research/stn7-stn8/",
            breadcrumbs=[
                {"name": "Home", "url": f"{SITE_URL}/"},
                {"name": "Research", "url": f"{SITE_URL}/research/"},
                {"name": "STN7/STN8 Kinases", "url": f"{SITE_URL}/research/stn7-stn8/"}
            ],
            content_html=stn_html,
            root_rel="../../"
        ))
    print("✓ Wrote /research/stn7-stn8/index.html")

    # 4. /explorer/index.html
    explorer_html = f"""
    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Interactive 3D Engine</p>
          <h1>Macromolecular 3D Structure &amp; Confidence Explorer</h1>
          <p class="lead">Client-side WebGL structure visualization powered by 3Dmol.js, synchronized with per-residue AlphaFold2 pLDDT confidence tracks and 2D Predicted Aligned Error (PAE) matrices.</p>
        </header>

        <div style="background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 2rem; margin-top: 1.5rem; text-align: center;">
          <h2>Launch Full Interactive 3D Session</h2>
          <p style="max-width: 650px; margin: 0 auto 1.5rem; color: var(--muted);">The full interactive explorer features real-time residue picking, cartoon/surface/stick representations, pLDDT and secondary structure color schemes, and linked PAE crosshairs.</p>
          <a href="{SITE_URL}/#explorer" class="btn btn-primary">Open 3D Explorer on Home Dashboard →</a>
        </div>

        <div style="margin-top: 3rem;">
          <h2>Pre-computed Structural Models Available</h2>
          <div class="project-grid" style="margin-top: 1rem;">
            <article class="method-card">
              <h3>AKT1 (Human Kinase Monomer)</h3>
              <p>Predicted with AlphaFold2 ColabFold v1.6.1. Highly confident kinase core with disordered terminal tails.</p>
              <a href="{SITE_URL}/structures/AKT1_AF2_rank001.pdb" download class="btn btn-ghost btn-sm">Download PDB (AKT1_AF2_rank001.pdb)</a>
            </article>
            <article class="method-card">
              <h3>STN7–STN8 (Chloroplast Kinase Heterodimer)</h3>
              <p>Predicted with AlphaFold2-multimer v3. Demonstrates extensive C-terminal domain interface contacts.</p>
              <a href="{SITE_URL}/structures/STN7_STN8_AF2multimer_rank001.pdb" download class="btn btn-ghost btn-sm">Download PDB (STN7_STN8_AF2multimer_rank001.pdb)</a>
            </article>
          </div>
        </div>
      </div>
    </section>
    """
    p = REPO_DIR / "explorer/index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(render_page_template(
            title="3D Molecular Structure & Confidence Explorer | 3Dmol.js & AlphaFold2",
            description="Interactive 3D WebGL protein structure explorer featuring AlphaFold2 models for AKT1 and STN7-STN8 with synchronized pLDDT and PAE tracks.",
            canonical_url=f"{SITE_URL}/explorer/",
            breadcrumbs=[{"name": "Home", "url": f"{SITE_URL}/"}, {"name": "3D Explorer", "url": f"{SITE_URL}/explorer/"}],
            content_html=explorer_html,
            root_rel="../"
        ))
    print("✓ Wrote /explorer/index.html")

    # 5. /gallery/index.html
    all_figs_html = "".join([
        f"""
        <figure class="fig" style="cursor: default;">
          <img src="{SITE_URL}/{fig['src']}" alt="{fig['caption']}" loading="lazy" />
          <figcaption>
            <span class="proj">{proj_id.upper()}</span>
            <strong>{fig['category'].upper()}</strong>: {fig['caption']}
          </figcaption>
        </figure>
        """
        for proj_id, p_obj in [("akt1", PROJECTS[0]), ("stn7-stn8", PROJECTS[1])]
        for fig in p_obj['figures']
    ])

    gallery_html = f"""
    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Publication Output</p>
          <h1>Publication-Grade Figure Gallery (30 High-Resolution Assets)</h1>
          <p class="lead">Complete collection of high-resolution scientific figures spanning AlphaFold confidence profiles, Ramachandran plots, contact topology, sequence evolution, and functional interaction networks.</p>
        </header>

        <div class="gallery" style="margin-top: 2rem;">
          {all_figs_html}
        </div>
      </div>
    </section>
    """
    p = REPO_DIR / "gallery/index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(render_page_template(
            title="Publication Figure Gallery | Suleiman Computational Structural Biology",
            description="30 high-resolution publication figures covering AlphaFold2 pLDDT, Ramachandran dihedral geometry, contact maps, phylogeny, and kinase networks.",
            canonical_url=f"{SITE_URL}/gallery/",
            breadcrumbs=[{"name": "Home", "url": f"{SITE_URL}/"}, {"name": "Figure Gallery", "url": f"{SITE_URL}/gallery/"}],
            content_html=gallery_html,
            root_rel="../"
        ))
    print("✓ Wrote /gallery/index.html")

    # 6. /methods/index.html
    methods_html = f"""
    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Mathematical &amp; Biophysical Foundations</p>
          <h1>Rigorous Mathematical Formulations &amp; Algorithms</h1>
          <p class="lead">Direct algebraic and geometric derivations implemented in Python rather than opaque GUI tools, demonstrating rigorous academic biophysics.</p>
        </header>

        <div class="method-grid" style="margin-top: 2rem;">
          <article class="method-card">
            <h3>1. Local Distance Difference Test (pLDDT)</h3>
            <p>Measures local structural agreement without global superposition over all Cα pairs within 15 Å:</p>
            <div class="math">$$\\text{{LDDT}}=\\frac{{1}}{{4|D|}}\\sum_{{(i,j)\\in D}}\\sum_{{t\\in\\{{0.5,1,2,4\\}}}}\\mathbb{{I}}\\big(|d^{{\\text{{pred}}}}_{{ij}}-d^{{\\text{{true}}}}_{{ij}}|\\le t\\big)$$</div>
          </article>

          <article class="method-card">
            <h3>2. Peptide Backbone Dihedrals (φ, ψ) via Vector Algebra</h3>
            <p>From four atom coordinates with bond vectors \\(\\mathbf v_1,\\mathbf v_2,\\mathbf v_3\\) and normal vectors \\(\\mathbf n_1=\\mathbf v_1\\times\\mathbf v_2\\), \\(\\mathbf n_2=\\mathbf v_2\\times\\mathbf v_3\\):</p>
            <div class="math">$$\\theta=\\operatorname{{atan2}}\\!\\Big(\\big(\\mathbf n_1\\times\\mathbf n_2\\big)\\cdot\\tfrac{{\\mathbf v_2}}{{\\lVert\\mathbf v_2\\rVert}},\\;\\mathbf n_1\\cdot\\mathbf n_2\\Big)$$</div>
          </article>

          <article class="method-card">
            <h3>3. Cα Pairwise Distance Matrix &amp; Non-Trivial Contact Topology</h3>
            <p>Euclidean distance matrix identifying physical tertiary contacts while eliminating trivial sequence neighbors:</p>
            <div class="math">$$D_{{ij}}=\\lVert\\mathbf r_i-\\mathbf r_j\\rVert_2,\\qquad D_{{ij}}\\le 8\\,\\text{{Å}}\\ \\wedge\\ |i-j|\\ge 6$$</div>
          </article>

          <article class="method-card">
            <h3>4. Predicted Aligned Error (PAE) Formulation</h3>
            <p>Expected position error of residue \\(j\\) when aligned on the local reference frame of residue \\(i\\):</p>
            <div class="math">$$\\text{{PAE}}_{{ij}}=\\mathbb E\\big[\\lVert\\mathbf x^{{\\text{{true}}}}_j-\\mathbf T_i\\,\\mathbf x^{{\\text{{pred}}}}_j\\rVert\\big]$$</div>
          </article>

          <article class="method-card">
            <h3>5. Kabsch Superposition &amp; RMSD via SVD</h3>
            <p>Optimal rotation matrix calculated from the Singular Value Decomposition (SVD) of covariance matrix \\(H=P^{{\\top}}Q=U\\Sigma V^{{\\top}}\\):</p>
            <div class="math">$$R=V\\,\\mathrm{{diag}}(1,1,\\det(VU^{{\\top}}))\\,U^{{\\top}},\\quad \\text{{RMSD}}=\\sqrt{{\\tfrac1N\\textstyle\\sum_i\\lVert R\\mathbf p_i-\\mathbf q_i\\rVert^2}}$$</div>
          </article>

          <article class="method-card">
            <h3>6. Shannon Information Entropy Conservation along MSA</h3>
            <p>Per-column entropy of multiple sequence alignment (H = 0 represents strict evolutionary invariance):</p>
            <div class="math">$$H_c=-\\sum_{{a}}p_{{a,c}}\\log_2 p_{{a,c}}$$</div>
          </article>
        </div>
      </div>
    </section>
    """
    p = REPO_DIR / "methods/index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(render_page_template(
            title="Mathematical Methods & Biophysical Algorithms | SuleimanCSB",
            description="Mathematical derivations for AlphaFold pLDDT, vector-algebraic Ramachandran dihedral torsion, PAE, Kabsch SVD RMSD, and Shannon conservation entropy.",
            canonical_url=f"{SITE_URL}/methods/",
            breadcrumbs=[{"name": "Home", "url": f"{SITE_URL}/"}, {"name": "Methods", "url": f"{SITE_URL}/methods/"}],
            content_html=methods_html,
            root_rel="../"
        ))
    print("✓ Wrote /methods/index.html")

    # 7. /knowledge/index.html (Semantic directory of all 47 wiki notes)
    notes_html = "".join([
        f"""
        <article class="note-card" style="cursor: default;">
          <span class="pill" data-type="{n['type']}">{n['type']}</span>
          <h3 style="margin: 0.3rem 0;"><a href="{SITE_URL}/#knowledge" style="color: inherit; text-decoration: none;">{n['title']}</a></h3>
          <p class="muted" style="margin: 0; font-size: 0.85rem;">{n['body'][:220].replace('#', '').strip()}…</p>
          <div style="margin-top: auto; display: flex; gap: 0.35rem; flex-wrap: wrap;">
            {"".join(f'<span class="muted" style="font-size: 0.72rem; background: var(--surface-2); padding: 0.15rem 0.45rem; border-radius: 4px;">#{t}</span>' for t in n.get('tags', [])[:3])}
          </div>
        </article>
        """ for n in WIKI
    ])

    knowledge_html = f"""
    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Compounding Knowledge Repository</p>
          <h1>Structural Biology Knowledge Base (47 Interlinked Notes)</h1>
          <p class="lead">An evolving, interlinked scientific wiki spanning biological entities, biophysical concepts, comprehensive syntheses and literature sources maintained alongside laboratory research.</p>
        </header>

        <p class="muted">Search and read any note in full interactive Markdown + LaTeX view on our <a href="{SITE_URL}/#knowledge">interactive Knowledge Base reader</a>.</p>

        <div class="kb-grid" style="margin-top: 2rem;">
          {notes_html}
        </div>
      </div>
    </section>
    """
    p = REPO_DIR / "knowledge/index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(render_page_template(
            title="Structural Biology Knowledge Base (47 Notes) | SuleimanCSB",
            description="Comprehensive interlinked knowledge base of entities (AKT1, STN7, STN8, LHCII), concepts (Cryo-EM, MSMs, PAE, pLDDT), and biophysical syntheses.",
            canonical_url=f"{SITE_URL}/knowledge/",
            breadcrumbs=[{"name": "Home", "url": f"{SITE_URL}/"}, {"name": "Knowledge Base", "url": f"{SITE_URL}/knowledge/"}],
            content_html=knowledge_html,
            root_rel="../"
        ))
    print("✓ Wrote /knowledge/index.html")

    # 8. /curriculum/index.html
    modules_html = "".join([
        f"""
        <li class="module">
          <span class="num">{m['n']}</span>
          <div>
            <h3 style="margin: 0 0 0.3rem;">{m['title']}</h3>
            <span class="muted">{m['tools']}</span>
          </div>
        </li>
        """ for m in CURRICULUM["modules"]
    ])

    curriculum_html = f"""
    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Academic Training Syllabus</p>
          <h1>{CURRICULUM['course']}</h1>
          <p class="lead">Comprehensive Master's level curriculum covering computational structural biology, molecular dynamics simulations, quantum mechanics, deep learning structure prediction, and de novo protein design.</p>
        </header>

        <p class="muted">Instructor: <strong>{CURRICULUM['instructor']}</strong> · License: {CURRICULUM['license']}</p>

        <ol class="module-grid" style="margin-top: 2rem;">
          {modules_html}
        </ol>
      </div>
    </section>
    """
    p = REPO_DIR / "curriculum/index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(render_page_template(
            title="Structural Bioinformatics MSc Curriculum | SuleimanCSB",
            description="9-module structural bioinformatics syllabus covering VMD, GROMACS molecular dynamics, PLUMED metadynamics, CP2K QM/MM, AlphaFold2, and RFdiffusion.",
            canonical_url=f"{SITE_URL}/curriculum/",
            breadcrumbs=[{"name": "Home", "url": f"{SITE_URL}/"}, {"name": "Curriculum", "url": f"{SITE_URL}/curriculum/"}],
            content_html=curriculum_html,
            root_rel="../"
        ))
    print("✓ Wrote /curriculum/index.html")

    # 9. /about/index.html
    about_html = f"""
    <section class="section">
      <div class="container about-grid">
        <div>
          <p class="eyebrow">Principal Investigator &amp; Lab Leadership</p>
          <h1>{AUTHOR_NAME}</h1>
          <p class="lead">Structural Bioinformatician at the <strong>{ORG_INSTITUTE}</strong>, Azerbaijan.</p>
          <p>
            Research focuses on the multi-scale continuum: <em>transcriptomics &rarr; co-expression network hubs (WGCNA) &rarr; deep learning protein structure prediction (AlphaFold2/ColabFold) &rarr; structural mechanics &rarr; virtual screening of allosteric chemical inhibitors</em>.
          </p>
          
          <div class="access-notice" role="note" style="margin-top: 1.5rem;">
            <span class="access-icon">🔒</span>
            <div>
              <strong>Strict Private Data &amp; Governance Policy:</strong>
              <p style="margin: 0.35rem 0 0;">
                All raw data, multi-sequence alignments, full AlphaFold scoring tensors, simulation trajectories and backend pipelines in <code>SuleimanComputationalStructuralBiology</code> are <strong>strictly private</strong>.
              </p>
              <p style="margin: 0.5rem 0 0;">
                To request research or academic reviewer access to the private repository and raw datasets, please send an inquiry to:
                <a href="mailto:{AUTHOR_EMAIL}?subject=Access%20Request%20-%20SuleimanComputationalStructuralBiology%20Private%20Data"><strong>{AUTHOR_EMAIL}</strong></a>
              </p>
            </div>
          </div>

          <div class="hero-cta" style="margin-top: 1.5rem;">
            <a class="btn btn-primary" href="mailto:{AUTHOR_EMAIL}?subject=Access%20Request%20-%20SuleimanComputationalStructuralBiology%20Private%20Data">Request Data Access ({AUTHOR_EMAIL})</a>
            <a class="btn btn-ghost" href="https://github.com/SuleimanHajizadeh" target="_blank" rel="noopener noreferrer">Personal GitHub Profile</a>
          </div>
        </div>

        <div class="arch-card">
          <h3>Laboratory Architecture</h3>
          <ul class="arch">
            <li>
              <span class="lock" aria-hidden="true">🔒</span>
              <div>
                <strong>SuleimanComputationalStructuralBiology (Private)</strong>
                <span class="muted">Private core repository — raw MSAs, full scoring matrices, molecular dynamics, manuscript drafts &amp; LLM wiki source.</span>
              </div>
            </li>
            <li>
              <span class="lock" aria-hidden="true">🌐</span>
              <div>
                <strong>SuleimanComputationalStructuralBiology.github.io (Public)</strong>
                <span class="muted">Public presentation portal — curated 3D models, downsampled JSON tracks, figure gallery &amp; searchable wiki.</span>
              </div>
            </li>
            <li>
              <span class="lock" aria-hidden="true">📩</span>
              <div>
                <strong>Data Access Contact</strong>
                <span class="muted"><a href="mailto:{AUTHOR_EMAIL}">{AUTHOR_EMAIL}</a></span>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </section>
    """
    p = REPO_DIR / "about/index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(render_page_template(
            title="About Suleiman Hajizadeh | Institute of Molecular Biology (IMB)",
            description="About Suleiman Hajizadeh, structural bioinformatician at the Institute of Molecular Biology (IMB), Azerbaijan, research methodologies, and private data access policy.",
            canonical_url=f"{SITE_URL}/about/",
            breadcrumbs=[{"name": "Home", "url": f"{SITE_URL}/"}, {"name": "About", "url": f"{SITE_URL}/about/"}],
            content_html=about_html,
            root_rel="../"
        ))
    print("✓ Wrote /about/index.html")

    # 10. /404.html
    notFound_html = f"""
    <section class="section" style="text-align: center; padding: 6rem 0;">
      <div class="container" style="max-width: 600px; margin: 0 auto;">
        <p class="eyebrow">404 Error</p>
        <h1>Page Not Found</h1>
        <p class="lead">The page or resource you requested does not exist or has been relocated.</p>
        <div style="margin: 2rem 0; display: flex; justify-content: center; gap: 0.75rem; flex-wrap: wrap;">
          <a href="{SITE_URL}/" class="btn btn-primary">Return to Home Portal</a>
          <a href="{SITE_URL}/research/" class="btn btn-ghost">View Research</a>
          <a href="{SITE_URL}/knowledge/" class="btn btn-ghost">Search Knowledge Base</a>
        </div>
        <p class="muted">Looking for private repository or research data access? Contact <a href="mailto:{AUTHOR_EMAIL}">{AUTHOR_EMAIL}</a>.</p>
      </div>
    </section>
    """
    p = REPO_DIR / "404.html"
    with open(p, "w", encoding="utf-8") as f:
        f.write(render_page_template(
            title="Page Not Found (404) | Suleiman Computational Structural Biology",
            description="404 Page Not Found — Return to Suleiman Computational Structural Biology laboratory portal.",
            canonical_url=f"{SITE_URL}/404.html",
            breadcrumbs=[{"name": "Home", "url": f"{SITE_URL}/"}, {"name": "404", "url": f"{SITE_URL}/404.html"}],
            content_html=notFound_html,
            root_rel="./"
        ))
    print("✓ Wrote /404.html")

def update_root_index_html():
    master_schema = build_master_schema()
    schema_json = json.dumps(master_schema, indent=2)

    index_path = REPO_DIR / "index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Build the rich SEO head snippet
    seo_head = f"""  <title>{SITE_TITLE}</title>
  <meta name="description" content="{SITE_DESC}" />
  <meta name="keywords" content="Computational Structural Biology, AlphaFold2, ColabFold, AF2-multimer, AKT1, STN7, STN8, pLDDT, PAE, Ramachandran, Molecular Docking, AutoDock Vina, Suleiman Hajizadeh, IMB, Institute of Molecular Biology, Azerbaijan, Kinase Mechanics, Structural Bioinformatics" />
  <meta name="author" content="{AUTHOR_NAME}" />
  <meta name="creator" content="{AUTHOR_NAME}" />
  <meta name="publisher" content="{ORG_INSTITUTE}" />
  <meta name="theme-color" content="#0b1020" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <meta name="bingbot" content="index, follow, max-snippet:-1, max-image-preview:large" />

  <link rel="canonical" href="{SITE_URL}/" />
  <link rel="alternate" hreflang="en" href="{SITE_URL}/" />
  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/" />

  <!-- Open Graph / Social Media -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{ORG_NAME}" />
  <meta property="og:title" content="{SITE_TITLE}" />
  <meta property="og:description" content="{SITE_DESC}" />
  <meta property="og:url" content="{SITE_URL}/" />
  <meta property="og:image" content="{SITE_URL}/assets/og-image.png" />
  <meta property="og:image:secure_url" content="{SITE_URL}/assets/og-image.png" />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="Suleiman Computational Structural Biology Laboratory" />
  <meta property="og:locale" content="en_US" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{SITE_TITLE}" />
  <meta name="twitter:description" content="{SITE_DESC}" />
  <meta name="twitter:image" content="{SITE_URL}/assets/og-image.png" />
  <meta name="twitter:creator" content="@SuleimanHajizadeh" />
  <meta name="twitter:site" content="@SuleimanHajizadeh" />

  <!-- Academic Citations & Dublin Core Metadata -->
  <meta name="citation_title" content="Deep Learning Macromolecular Structure Prediction, Kinase Structural Mechanics, and Automated Virtual Screening Pipelines" />
  <meta name="citation_author" content="Hajizadeh, Suleiman" />
  <meta name="citation_publication_date" content="2026/04/01" />
  <meta name="citation_technical_report_institution" content="{ORG_INSTITUTE}" />
  <meta name="citation_fulltext_html_url" content="{SITE_URL}/" />
  <meta name="DC.title" content="{SITE_TITLE}" />
  <meta name="DC.creator" content="{AUTHOR_NAME}" />
  <meta name="DC.description" content="{SITE_DESC}" />
  <meta name="DC.publisher" content="{ORG_INSTITUTE}" />
  <meta name="DC.language" content="en" />

  <!-- Enterprise JSON-LD Schema.org Knowledge Graph -->
  <script type="application/ld+json">
{schema_json}
  </script>"""

    # Replace <title>...</head> head meta block
    # Match from <title> to before </head>
    pattern = r'<title>.*?(?=\s*<link rel="icon")'
    new_content = re.sub(pattern, seo_head + "\n\n  ", content, flags=re.DOTALL)

    # In the footer, make sure sitemaps are referenced
    footer_pattern = r'(<p class="muted" id="buildInfo"></p>)'
    footer_replacement = r'\1\n      <p class="muted" style="margin-top: 0.4rem; font-size: 0.78rem;"><a href="sitemap.xml">Sitemap XML</a> · <a href="sitemap-images.xml">Image Sitemap</a> · <a href="robots.txt">robots.txt</a> · <a href="research/">Research</a> · <a href="methods/">Methods</a> · <a href="knowledge/">Knowledge Base</a></p>'
    if 'sitemap.xml' not in new_content:
        new_content = re.sub(footer_pattern, footer_replacement, new_content)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✓ Updated index.html with Senior Architect SEO head, metadata, and JSON-LD schema")

if __name__ == "__main__":
    generate_robots_txt()
    generate_sitemap_xml()
    generate_sitemap_images_xml()
    generate_subpages()
    update_root_index_html()
    print("All SEO architecture assets generated successfully!")
