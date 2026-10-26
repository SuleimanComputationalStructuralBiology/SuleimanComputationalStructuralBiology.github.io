/* ==========================================================================
   Suleiman Computational Structural Biology — interactive application
   ========================================================================== */
(function () {
  "use strict";

  // ------------------------------------------------------------------------
  // State
  // ------------------------------------------------------------------------
  const state = {
    projects: [],
    wiki: [],
    curriculum: null,
    tracks: {},
    currentModel: "akt1",
    currentStyle: "cartoon",
    currentColor: "plddt",
    glviewer: null,
    pdbData: {},
    charts: {},
    activeProject: "akt1",
  };

  // ------------------------------------------------------------------------
  // Dark mode toggle (Modern Web Guidance: two-state toggle)
  // ------------------------------------------------------------------------
  function initDarkModeToggle() {
    const meta = document.querySelector('meta[name="color-scheme"]');
    const btn = document.getElementById("themeToggle");
    const mq = window.matchMedia("(prefers-color-scheme: dark)");

    function currentSystem() {
      return mq.matches ? "dark" : "light";
    }
    function currentRendered() {
      const stored = localStorage.getItem("color-scheme");
      return stored && stored !== "light dark" ? stored : currentSystem();
    }

    btn.addEventListener("click", () => {
      const target = currentRendered() === "dark" ? "light" : "dark";
      if (target === currentSystem()) {
        try { localStorage.removeItem("color-scheme"); } catch (e) {}
        meta.content = "light dark";
      } else {
        try { localStorage.setItem("color-scheme", target); } catch (e) {}
        meta.content = target;
      }
    });

    window.addEventListener("storage", (e) => {
      if (e.key === "color-scheme") meta.content = e.newValue ?? "light dark";
    });
  }

  // ------------------------------------------------------------------------
  // Light-dismiss dialog fallback (Safari <dialog closedby>)
  // ------------------------------------------------------------------------
  function initDialogFallbacks() {
    if (!("closedBy" in HTMLDialogElement.prototype)) {
      document.querySelectorAll("dialog").forEach((dlg) => {
        dlg.addEventListener("click", (event) => {
          if (event.target !== dlg) return;
          const rect = dlg.getBoundingClientRect();
          const inside =
            rect.top <= event.clientY &&
            event.clientY <= rect.top + rect.height &&
            rect.left <= event.clientX &&
            event.clientX <= rect.left + rect.width;
          if (!inside) dlg.close();
        });
      });
    }
  }

  // ------------------------------------------------------------------------
  // Mobile nav
  // ------------------------------------------------------------------------
  function initNav() {
    const menuBtn = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");
    menuBtn.addEventListener("click", () => {
      const open = navLinks.classList.toggle("is-open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
    navLinks.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => {
        navLinks.classList.remove("is-open");
        menuBtn.setAttribute("aria-expanded", "false");
      });
    });
  }

  // ------------------------------------------------------------------------
  // 3Dmol viewer
  // ------------------------------------------------------------------------
  const MODEL_META = {
    akt1: {
      pdb: "structures/AKT1_AF2_rank001.pdb",
      name: "AKT1 (AlphaFold2, rank 1)",
      trackKey: "akt1",
    },
    "stn7-stn8": {
      pdb: "structures/STN7_STN8_AF2multimer_rank001.pdb",
      name: "STN7–STN8 heterodimer (AF2-multimer v3, rank 1)",
      trackKey: "stn7-stn8",
    },
  };

  async function loadPdb(url) {
    if (state.pdbData[url]) return state.pdbData[url];
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status} fetching ${url}`);
    const text = await res.text();
    state.pdbData[url] = text;
    return text;
  }

  function plddtColorSpec(atom) {
    const b = atom.b;
    if (b >= 90) return 0x0053d6;
    if (b >= 70) return 0x65cbf3;
    if (b >= 50) return 0xffdb13;
    return 0xff7d45;
  }

  function apply3dStyle() {
    const v = state.glviewer;
    if (!v) return;
    v.removeAllSurfaces();
    const mode = state.currentStyle;
    const col = state.currentColor;

    let colorOpt = {};
    if (col === "plddt") {
      colorOpt = { colorfunc: plddtColorSpec };
    } else if (col === "chain") {
      colorOpt = {
        colorfunc: (a) => (a.chain === "B" ? 0x8b7bff : 0x2ee6c9),
      };
    } else if (col === "ss") {
      colorOpt = {
        colorfunc: (a) => {
          if (a.ss === "h") return 0xff6b8b;
          if (a.ss === "s") return 0xffdb13;
          return 0x65cbf3;
        },
      };
    } else if (col === "spectrum") {
      colorOpt = { color: "spectrum" };
    }

    if (mode === "cartoon") {
      v.setStyle({}, { cartoon: colorOpt });
    } else if (mode === "surface") {
      v.setStyle({}, { cartoon: colorOpt });
      v.addSurface($3Dmol.SurfaceType.MS, { opacity: 0.55, ...colorOpt });
    } else if (mode === "stick") {
      v.setStyle({}, { stick: { radius: 0.25, ...colorOpt } });
    } else if (mode === "sphere") {
      v.setStyle({}, { sphere: { scale: 0.3, ...colorOpt } });
    }
    v.render();
  }

  async function setModel(key) {
    state.currentModel = key;
    const status = document.getElementById("viewerStatus");
    const meta = MODEL_META[key];
    status.textContent = `Loading ${meta.name}…`;

    document.querySelectorAll(".seg-btn[data-model]").forEach((b) => {
      const match = b.dataset.model === key;
      b.classList.toggle("is-active", match);
      b.setAttribute("aria-pressed", String(match));
    });
    document.getElementById("downloadPdb").href = meta.pdb;

    try {
      const pdb = await loadPdb(meta.pdb);
      const host = document.getElementById("viewer3d");

      if (!state.glviewer) {
        state.glviewer = $3Dmol.createViewer(host, {
          backgroundColor: "transparent",
          antialias: true,
        });
      }
      const v = state.glviewer;
      v.clear();
      v.addModel(pdb, "pdb");
      v.zoomTo();
      apply3dStyle();
      v.render();
      status.textContent = meta.name;

      // Residue hover/click picking
      v.setHoverable(
        {},
        true,
        (atom) => {
          if (!atom) return;
          const chain = atom.chain ? ` Chain ${atom.chain}` : "";
          status.textContent = `${atom.resn} ${atom.resi}${chain} · pLDDT ${atom.b.toFixed(1)}`;
        },
        () => {
          status.textContent = meta.name;
        }
      );

      // Render corresponding tracks
      renderTracksForModel(key);
    } catch (err) {
      console.error(err);
      status.textContent = `Error loading model: ${err.message}`;
    }
  }

  function highlightResidueIn3D(resi, chain) {
    const v = state.glviewer;
    if (!v) return;
    const sel = { resi: resi };
    if (chain) sel.chain = chain;
    v.center(sel, 400);
  }

  function initExplorerControls() {
    document.querySelectorAll(".seg-btn[data-model]").forEach((btn) => {
      btn.addEventListener("click", () => setModel(btn.dataset.model));
    });
    document.getElementById("styleSelect").addEventListener("change", (e) => {
      state.currentStyle = e.target.value;
      apply3dStyle();
    });
    document.getElementById("colorSelect").addEventListener("change", (e) => {
      state.currentColor = e.target.value;
      apply3dStyle();
    });
    document.getElementById("spinToggle").addEventListener("change", (e) => {
      if (!state.glviewer) return;
      state.glviewer.spin(e.target.checked);
    });
    document.getElementById("resetView").addEventListener("click", () => {
      if (!state.glviewer) return;
      state.glviewer.zoomTo();
      state.glviewer.render();
    });
    window.addEventListener("resize", () => {
      if (state.glviewer) state.glviewer.resize();
    });
  }

  // ------------------------------------------------------------------------
  // Tracks (pLDDT & PAE charts)
  // ------------------------------------------------------------------------
  async function loadTrackData(key) {
    if (state.tracks[key]) return state.tracks[key];
    const res = await fetch(`data/tracks/${key}.json`);
    if (!res.ok) throw new Error(`HTTP ${res.status} loading track ${key}`);
    const data = await res.json();
    state.tracks[key] = data;
    return data;
  }

  async function renderTracksForModel(key) {
    const track = await loadTrackData(key);
    const plddtCanvas = document.getElementById("plddtChart");
    const paeCanvas = document.getElementById("paeChart");
    const resReadout = document.getElementById("residueReadout");
    const paeReadout = document.getElementById("paeReadout");
    const paeMax = document.getElementById("paeMax");

    if (key === "akt1") {
      paeMax.textContent = `${Math.round(track.max_pae || 31)} Å`;
      // pLDDT
      CSBCharts.lineChart(plddtCanvas, {
        series: [{ label: "pLDDT", values: track.plddt, color: "plddt" }],
        yMin: 0,
        yMax: 100,
        yTicks: [0, 50, 70, 90, 100],
        plddtBands: true,
        height: 180,
        onHover: (i) => {
          const v = track.plddt[i];
          const aa = track.sequence ? track.sequence[i] || "" : "";
          let tier = "Disordered (<50)";
          if (v >= 90) tier = "Very High (≥90)";
          else if (v >= 70) tier = "Confident (70–90)";
          else if (v >= 50) tier = "Low (50–70)";
          resReadout.textContent = `Residue ${i + 1} ${aa} · pLDDT ${v.toFixed(1)} (${tier})`;
        },
        onLeave: () => {
          resReadout.textContent = "hover the track";
        },
        onClick: (i) => {
          highlightResidueIn3D(i + 1, "A");
        },
      });

      // PAE
      CSBCharts.heatmap(paeCanvas, track.pae, {
        max: track.max_pae || 31,
        onHover: (i, j, v) => {
          const step = track.pae_bin || 1;
          const ri = i * step + 1, rj = j * step + 1;
          paeReadout.textContent = `Aligned ${ri} · Scored ${rj} · ${v.toFixed(1)} Å`;
        },
      });
    } else {
      // STN7/STN8 complex
      const plddtA = track.chains.A;
      const plddtB = track.chains.B;
      const combined = plddtA.concat(plddtB);
      paeMax.textContent = `${Math.round(track.max_pae || 30)} Å`;

      CSBCharts.lineChart(plddtCanvas, {
        series: [{ label: "pLDDT", values: combined, color: "plddt" }],
        yMin: 0,
        yMax: 100,
        yTicks: [0, 50, 70, 90, 100],
        plddtBands: true,
        height: 180,
        segments: [
          { start: 0, label: `Chain A: STN7 (1–${plddtA.length})` },
          { start: plddtA.length, label: `Chain B: STN8 (1–${plddtB.length})` },
        ],
        onHover: (i) => {
          const v = combined[i];
          const isA = i < plddtA.length;
          const chain = isA ? "A (STN7)" : "B (STN8)";
          const resi = isA ? i + 1 : i - plddtA.length + 1;
          resReadout.textContent = `Chain ${chain} Residue ${resi} · pLDDT ${v.toFixed(1)}`;
        },
        onLeave: () => {
          resReadout.textContent = "hover the track";
        },
        onClick: (i) => {
          const isA = i < plddtA.length;
          const chain = isA ? "A" : "B";
          const resi = isA ? i + 1 : i - plddtA.length + 1;
          highlightResidueIn3D(resi, chain);
        },
      });

      // Heterodimer PAE
      const bnd = Math.round(plddtA.length / (track.pae_bin || 5));
      CSBCharts.heatmap(paeCanvas, track.pae, {
        max: track.max_pae || 30,
        boundaries: [bnd],
        onHover: (i, j, v) => {
          const step = track.pae_bin || 1;
          const ri = i * step + 1, rj = j * step + 1;
          const cA = ri <= plddtA.length ? "A" : "B";
          const cB = rj <= plddtA.length ? "A" : "B";
          paeReadout.textContent = `Frame ${cA}:${ri} · Target ${cB}:${rj} · ${v.toFixed(1)} Å`;
        },
      });
    }
  }

  // ------------------------------------------------------------------------
  // Projects rendering & detail drawer
  // ------------------------------------------------------------------------
  function renderProjects(projects) {
    const grid = document.getElementById("projectCards");
    grid.innerHTML = projects
      .map(
        (p) => `
      <article class="project-card ${p.id === state.activeProject ? "is-active" : ""}" data-project="${p.id}" tabindex="0" role="button" aria-pressed="${p.id === state.activeProject}">
        <span class="status">${p.status}</span>
        <img src="${p.figures[0].src}" alt="${p.title}" loading="lazy" width="400" height="200" />
        <div class="body">
          <p class="eyebrow">${p.organism}</p>
          <h3>${p.title}</h3>
          <p class="muted">${p.subtitle}</p>
          <div class="tags">
            ${p.tags.slice(0, 4).map((t) => `<span class="tag">${t}</span>`).join("")}
          </div>
        </div>
      </article>
    `
      )
      .join("");

    grid.querySelectorAll(".project-card").forEach((card) => {
      const select = () => {
        state.activeProject = card.dataset.project;
        grid.querySelectorAll(".project-card").forEach((c) => {
          const match = c.dataset.project === state.activeProject;
          c.classList.toggle("is-active", match);
          c.setAttribute("aria-pressed", String(match));
        });
        renderProjectDetail(projects.find((p) => p.id === state.activeProject));
      };
      card.addEventListener("click", select);
      card.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          select();
        }
      });
    });

    renderProjectDetail(projects.find((p) => p.id === state.activeProject));
  }

  function renderProjectDetail(p) {
    const host = document.getElementById("projectDetails");
    if (!p) {
      host.innerHTML = "";
      return;
    }

    const uniprotLinks = p.targets
      .map((t) => `<a href="https://www.uniprot.org/uniprot/${t.uniprot}" target="_blank" rel="noopener noreferrer">${t.name} · ${t.uniprot} ↗</a>`)
      .join(" ");

    const metricsHtml = p.metrics
      .map(
        (m) => `
      <div class="metric">
        <div class="v">${m.value}</div>
        <div class="l">${m.label}</div>
        ${m.note ? `<div class="n">${m.note}</div>` : ""}
      </div>
    `
      )
      .join("");

    const pipelineHtml = `
      <ol class="pipeline">
        ${p.pipeline.map((step) => `<li>${step}</li>`).join("")}
      </ol>
    `;

    const findingsHtml = `
      <ul class="findings">
        ${p.findings.map((f) => `<li>${f}</li>`).join("")}
      </ul>
    `;

    // Project-specific additions
    let extrasHtml = "";
    if (p.id === "stn7-stn8" && p.domains) {
      const domainColors = {
        transit_peptide: "#ff7d45",
        transmembrane_anchor: "#ffdb13",
        kinase_domain: "#2ee6c9",
        activation_loop: "#8b7bff",
        c_terminal_tail: "#65cbf3",
      };
      const domainBars = ["STN7", "STN8"]
        .map((prot) => {
          const bnds = p.domains[prot];
          const total = prot === "STN7" ? 565 : 517;
          const spans = Object.entries(bnds)
            .map(([name, [start, end]]) => {
              const pct = (((end - start + 1) / total) * 100).toFixed(1);
              const col = domainColors[name] || "#888";
              return `<span style="width:${pct}%;background:${col}" title="${name}: ${start}–${end} (${pct}%)">${name.replace(/_/g, " ")}</span>`;
            })
            .join("");
          return `
          <div style="margin-bottom:1rem">
            <strong>${prot} domain architecture</strong>
            <div class="domain-bar">${spans}</div>
          </div>
        `;
        })
        .join("");

      // Catalytic motifs table
      const motifRows = Object.entries(p.motifs)
        .flatMap(([protKey, mdict]) => {
          const pName = protKey.split("_")[0];
          return Object.entries(mdict).flatMap(([mName, hits]) =>
            hits.map(
              (h) => `
            <tr>
              <td><strong>${pName}</strong></td>
              <td>${mName}</td>
              <td class="mono">${h.sequence}</td>
              <td class="mono">${h.start}–${h.end}</td>
            </tr>
          `
            )
          );
        })
        .join("");

      // Ligands table
      const ligandRows = (p.ligands || [])
        .map(
          (l) => `
        <tr>
          <td><strong>${l.name}</strong></td>
          <td class="mono">${l.cid}</td>
          <td>${l.mw}</td>
          <td>${l.role}</td>
          <td><span class="pill" style="--pc:#2ee6c9">PDBQT Ready</span></td>
        </tr>
      `
        )
        .join("");

      extrasHtml = `
        <div class="two-col">
          <div>
            <h3>Domain Architecture &amp; Conservation</h3>
            ${domainBars}
            <h3>Conserved Catalytic Kinase Motifs</h3>
            <div class="table-wrap">
              <table>
                <thead><tr><th>Protein</th><th>Motif</th><th>Sequence</th><th>Residues</th></tr></thead>
                <tbody>${motifRows}</tbody>
              </table>
            </div>
          </div>
          <div>
            <h3>Docking Ligand Screening Library (AutoDock Vina)</h3>
            <p class="muted">Receptors prepared with signal transit peptide truncation; ligands parameterized to PDBQT format.</p>
            <div class="table-wrap">
              <table>
                <thead><tr><th>Ligand</th><th>CID</th><th>MW</th><th>Role / Mechanism</th><th>Status</th></tr></thead>
                <tbody>${ligandRows}</tbody>
              </table>
            </div>
          </div>
        </div>
      `;
    }

    host.innerHTML = `
      <div class="detail">
        <div class="detail-head">
          <div>
            <p class="eyebrow">${p.organism}</p>
            <h2>${p.title}</h2>
            <p class="muted">${p.summary}</p>
          </div>
          <div class="uniprot">${uniprotLinks}</div>
        </div>
        ${pipelineHtml}
        <div class="metrics">${metricsHtml}</div>
        <h3>Key Empirical &amp; Structural Findings</h3>
        ${findingsHtml}
        ${extrasHtml}
      </div>
    `;
  }

  // ------------------------------------------------------------------------
  // Figure gallery & lightbox
  // ------------------------------------------------------------------------
  function renderGallery(projects) {
    const allFigs = projects.flatMap((p) =>
      p.figures.map((f) => ({ ...f, project: p.title, projId: p.id }))
    );
    const filterContainer = document.getElementById("galleryFilters");
    const grid = document.getElementById("galleryGrid");
    const lightbox = document.getElementById("lightbox");
    const lbImg = document.getElementById("lightboxImg");
    const lbCap = document.getElementById("lightboxCaption");

    const categories = ["all", "akt1", "stn7-stn8", "structure", "confidence", "complex", "evolution", "motifs", "network"];
    const labels = {
      all: "All figures (30)",
      akt1: "AKT1",
      "stn7-stn8": "STN7 / STN8",
      structure: "3D Structure",
      confidence: "Confidence & PAE",
      complex: "Heterodimer Complex",
      evolution: "Phylogeny & MSA",
      motifs: "Kinase Motifs",
      network: "Interaction Networks",
    };

    filterContainer.innerHTML = categories
      .map(
        (cat, i) =>
          `<button type="button" class="chip" data-cat="${cat}" aria-pressed="${i === 0}">${labels[cat] || cat}</button>`
      )
      .join("");

    function showCategory(cat) {
      filterContainer.querySelectorAll(".chip").forEach((btn) => {
        btn.setAttribute("aria-pressed", String(btn.dataset.cat === cat));
      });
      const list =
        cat === "all"
          ? allFigs
          : cat === "akt1" || cat === "stn7-stn8"
          ? allFigs.filter((f) => f.projId === cat)
          : allFigs.filter((f) => f.category === cat);

      grid.innerHTML = list
        .map(
          (f) => `
        <figure class="fig" tabindex="0" role="button" data-src="${f.src}" data-caption="${f.caption} — ${f.project}">
          <img src="${f.src}" alt="${f.caption}" loading="lazy" width="400" height="300" />
          <figcaption>
            <span class="proj">${f.project}</span>
            ${f.caption}
          </figcaption>
        </figure>
      `
        )
        .join("");

      grid.querySelectorAll(".fig").forEach((fig) => {
        const open = () => {
          lbImg.src = fig.dataset.src;
          lbImg.alt = fig.dataset.caption;
          lbCap.textContent = fig.dataset.caption;
          lightbox.showModal();
        };
        fig.addEventListener("click", open);
        fig.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            open();
          }
        });
      });
    }

    filterContainer.querySelectorAll(".chip").forEach((btn) => {
      btn.addEventListener("click", () => showCategory(btn.dataset.cat));
    });
    showCategory("all");
  }

  // ------------------------------------------------------------------------
  // Knowledge Base (Wiki) & Reader Dialog
  // ------------------------------------------------------------------------
  function renderKnowledgeBase(notes) {
    const grid = document.getElementById("kbGrid");
    const search = document.getElementById("kbSearch");
    const filterContainer = document.getElementById("kbFilters");
    const countEl = document.getElementById("kbCount");
    const reader = document.getElementById("noteReader");
    const titleEl = document.getElementById("noteTitle");
    const typeEl = document.getElementById("noteType");
    const tagsEl = document.getElementById("noteTags");
    const bodyEl = document.getElementById("noteBody");

    const types = ["all", "entity", "concept", "synthesis", "source"];
    const labels = {
      all: "All",
      entity: "Entities",
      concept: "Concepts",
      synthesis: "Syntheses",
      source: "Sources",
    };
    let activeType = "all";

    filterContainer.innerHTML = types
      .map(
        (t, i) =>
          `<button type="button" class="chip" data-type="${t}" aria-pressed="${i === 0}">${labels[t]}</button>`
      )
      .join("");

    function update() {
      const q = search.value.trim().toLowerCase();
      const filtered = notes.filter((n) => {
        if (activeType !== "all" && n.type !== activeType) return false;
        if (!q) return true;
        return (
          n.title.toLowerCase().includes(q) ||
          n.id.toLowerCase().includes(q) ||
          (n.aliases || []).some((a) => a.toLowerCase().includes(q)) ||
          (n.tags || []).some((t) => t.toLowerCase().includes(q)) ||
          n.body.toLowerCase().includes(q)
        );
      });

      countEl.textContent = `Showing ${filtered.length} of ${notes.length} notes`;

      grid.innerHTML = filtered
        .map(
          (n) => `
        <article class="note-card" tabindex="0" role="button" data-id="${n.id}">
          <span class="pill" data-type="${n.type}">${n.type}</span>
          <h3>${n.title}</h3>
          <p>${n.body.replace(/[#*`_\[\]]/g, "").slice(0, 180)}…</p>
          <div class="tags">
            ${(n.tags || []).slice(0, 3).map((t) => `<span class="tag">${t}</span>`).join("")}
          </div>
        </article>
      `
        )
        .join("");

      grid.querySelectorAll(".note-card").forEach((card) => {
        const open = () => openNote(card.dataset.id);
        card.addEventListener("click", open);
        card.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            open();
          }
        });
      });
    }

    function openNote(id) {
      const note = notes.find((n) => n.id === id);
      if (!note) return;
      titleEl.textContent = note.title;
      typeEl.textContent = note.type;
      typeEl.dataset.type = note.type;
      tagsEl.innerHTML = (note.tags || []).map((t) => `<span class="tag">${t}</span>`).join("");

      // Render markdown
      let rawMd = note.body;
      // Convert wikilinks [[Target|Label]] or [[Target]]
      rawMd = rawMd.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (m, target, label) => {
        const text = label || target;
        const exists = notes.some((n) => n.id === target || (n.aliases || []).includes(target));
        return `<a href="#note" class="wikilink ${exists ? "" : "missing"}" data-note="${target}">${text}</a>`;
      });

      const dirty = marked.parse(rawMd);
      bodyEl.innerHTML = DOMPurify.sanitize(dirty, {
        ADD_TAGS: ["annotation"],
        ADD_ATTR: ["data-note"],
      });

      // Render KaTeX math inside the reader
      if (window.renderMathInElement) {
        renderMathInElement(bodyEl, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "\\[", right: "\\]", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\(", right: "\\)", display: false },
          ],
          throwOnError: false,
        });
      }

      // Attach click to internal wikilinks
      bodyEl.querySelectorAll("a.wikilink").forEach((link) => {
        link.addEventListener("click", (e) => {
          e.preventDefault();
          const target = link.dataset.note;
          const match = notes.find((n) => n.id === target || (n.aliases || []).includes(target));
          if (match) openNote(match.id);
        });
      });

      reader.showModal();
    }

    search.addEventListener("input", update);
    filterContainer.querySelectorAll(".chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        activeType = btn.dataset.type;
        filterContainer.querySelectorAll(".chip").forEach((b) => {
          b.setAttribute("aria-pressed", String(b.dataset.type === activeType));
        });
        update();
      });
    });

    update();
  }

  // ------------------------------------------------------------------------
  // Curriculum
  // ------------------------------------------------------------------------
  function renderCurriculum(c) {
    if (!c) return;
    document.getElementById("curriculumSub").textContent = `${c.course} · ${c.instructor}`;
    const grid = document.getElementById("moduleGrid");
    grid.innerHTML = c.modules
      .map(
        (m) => `
      <li class="module">
        <span class="num">${m.n}</span>
        <h3>${m.title}</h3>
        <span>${m.tools}</span>
      </li>
    `
      )
      .join("");
  }

  // ------------------------------------------------------------------------
  // Initialize app
  // ------------------------------------------------------------------------
  async function init() {
    initDarkModeToggle();
    initDialogFallbacks();
    initNav();
    initExplorerControls();

    // Render static equations in the Methods section
    if (window.renderMathInElement) {
      renderMathInElement(document.getElementById("methods"), {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "\\[", right: "\\]", display: true },
          { left: "$", right: "$", display: false },
          { left: "\\(", right: "\\)", display: false },
        ],
        throwOnError: false,
      });
    }

    try {
      const [projects, wiki, curriculum, site] = await Promise.all([
        fetch("data/projects.json").then((r) => r.json()),
        fetch("data/wiki.json").then((r) => r.json()),
        fetch("data/curriculum.json").then((r) => r.json()),
        fetch("data/site.json").then((r) => r.json()),
      ]);

      state.projects = projects;
      state.wiki = wiki;
      state.curriculum = curriculum;

      // Update hero stats
      if (site.counts) {
        document.querySelectorAll("[data-stat]").forEach((el) => {
          const k = el.dataset.stat;
          if (site.counts[k] != null) el.textContent = site.counts[k];
        });
      }
      document.getElementById("buildInfo").textContent = `Built ${site.generated.slice(0, 10)} · commit ${site.backend_commit} (private core)`;

      renderProjects(projects);
      renderGallery(projects);
      renderKnowledgeBase(wiki);
      renderCurriculum(curriculum);

      // Start 3D model
      await setModel("akt1");
    } catch (err) {
      console.error("Initialization error:", err);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
