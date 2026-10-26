/* Lightweight, dependency-free canvas charts for per-residue tracks. */
(function () {
  "use strict";

  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

  function setupCanvas(canvas, cssHeight) {
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth || canvas.parentElement.clientWidth;
    const h = cssHeight ?? (canvas.clientHeight || 180);
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx, w, h };
  }

  /** AlphaFold pLDDT palette */
  function plddtColor(v) {
    if (v >= 90) return "#0053d6";
    if (v >= 70) return "#65cbf3";
    if (v >= 50) return "#ffdb13";
    return "#ff7d45";
  }

  /**
   * Line chart.
   * opts: { series:[{label, values, color}], yMin, yMax, plddtBands, height,
   *         segments:[{start,end,label}], onHover(i, seriesIdx), onClick(i), yTicks }
   */
  function lineChart(canvas, opts) {
    const height = opts.height || 180;
    const pad = { l: 34, r: 8, t: 10, b: 22 };
    let hoverX = null;

    function draw() {
      const { ctx, w, h } = setupCanvas(canvas, height);
      const iw = w - pad.l - pad.r, ih = h - pad.t - pad.b;
      const n = Math.max(...opts.series.map((s) => s.values.length));
      const yMin = opts.yMin ?? Math.min(...opts.series.flatMap((s) => s.values));
      const yMax = opts.yMax ?? Math.max(...opts.series.flatMap((s) => s.values));
      const X = (i) => pad.l + (n <= 1 ? 0 : (i / (n - 1)) * iw);
      const Y = (v) => pad.t + ih - ((v - yMin) / (yMax - yMin || 1)) * ih;
      const text = css("--muted"), grid = css("--border");

      ctx.clearRect(0, 0, w, h);
      if (opts.plddtBands) {
        [[90, 100, "#0053d6"], [70, 90, "#65cbf3"], [50, 70, "#ffdb13"], [0, 50, "#ff7d45"]].forEach(([a, b, c]) => {
          ctx.fillStyle = c + "1f";
          ctx.fillRect(pad.l, Y(b), iw, Y(a) - Y(b));
        });
      }
      // segments (e.g. chain A / chain B)
      (opts.segments || []).forEach((s, k) => {
        if (k > 0) {
          ctx.strokeStyle = text; ctx.setLineDash([4, 4]);
          ctx.beginPath(); ctx.moveTo(X(s.start), pad.t); ctx.lineTo(X(s.start), pad.t + ih); ctx.stroke();
          ctx.setLineDash([]);
        }
        ctx.fillStyle = text; ctx.font = "600 10px system-ui, sans-serif";
        ctx.fillText(s.label, X(s.start) + 4, pad.t + 11);
      });
      // axes + ticks
      ctx.strokeStyle = grid; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, pad.t + ih); ctx.lineTo(pad.l + iw, pad.t + ih); ctx.stroke();
      ctx.fillStyle = text; ctx.font = "10px system-ui, sans-serif"; ctx.textAlign = "right";
      (opts.yTicks || [yMin, (yMin + yMax) / 2, yMax]).forEach((t) => {
        ctx.fillText(+t.toFixed(1), pad.l - 5, Y(t) + 3);
      });
      ctx.textAlign = "center";
      const step = Math.pow(10, Math.floor(Math.log10(Math.max(n, 10)))) / (n > 600 ? 1 : 2);
      for (let i = step; i < n; i += step) ctx.fillText(i, X(i - 1), h - 6);
      ctx.textAlign = "left";

      // series
      opts.series.forEach((s) => {
        ctx.lineWidth = 1.6;
        if (s.color === "plddt") {
          for (let i = 1; i < s.values.length; i++) {
            ctx.strokeStyle = plddtColor((s.values[i] + s.values[i - 1]) / 2);
            ctx.beginPath(); ctx.moveTo(X(i - 1), Y(s.values[i - 1])); ctx.lineTo(X(i), Y(s.values[i])); ctx.stroke();
          }
        } else {
          ctx.strokeStyle = s.color;
          ctx.beginPath();
          s.values.forEach((v, i) => (i ? ctx.lineTo(X(i), Y(v)) : ctx.moveTo(X(i), Y(v))));
          ctx.stroke();
        }
      });
      // reference line
      if (opts.refLine != null) {
        ctx.strokeStyle = css("--accent-3"); ctx.setLineDash([5, 4]);
        ctx.beginPath(); ctx.moveTo(pad.l, Y(opts.refLine)); ctx.lineTo(pad.l + iw, Y(opts.refLine)); ctx.stroke();
        ctx.setLineDash([]);
      }
      // legend
      if (opts.legend) {
        let lx = pad.l + 8;
        opts.series.forEach((s) => {
          ctx.fillStyle = s.color; ctx.fillRect(lx, pad.t + 4, 10, 3);
          ctx.fillStyle = text; ctx.fillText(s.label, lx + 14, pad.t + 9);
          lx += ctx.measureText(s.label).width + 34;
        });
      }
      // hover cursor
      if (hoverX != null) {
        ctx.strokeStyle = css("--text"); ctx.globalAlpha = .5;
        ctx.beginPath(); ctx.moveTo(X(hoverX), pad.t); ctx.lineTo(X(hoverX), pad.t + ih); ctx.stroke();
        ctx.globalAlpha = 1;
      }
      canvas._idx = (clientX) => {
        const r = canvas.getBoundingClientRect();
        const i = Math.round(((clientX - r.left - pad.l) / iw) * (n - 1));
        return Math.max(0, Math.min(n - 1, i));
      };
    }

    canvas.onpointermove = (e) => {
      hoverX = canvas._idx(e.clientX); draw();
      opts.onHover && opts.onHover(hoverX);
    };
    canvas.onpointerleave = () => { hoverX = null; draw(); opts.onLeave && opts.onLeave(); };
    canvas.onclick = (e) => opts.onClick && opts.onClick(canvas._idx(e.clientX));
    draw();
    return { redraw: draw };
  }

  /** PAE heat map (AlphaFold green palette). */
  function heatmap(canvas, matrix, opts = {}) {
    const n = matrix.length;
    const max = opts.max || Math.max(...matrix.flat());
    function color(v) {
      const t = Math.min(1, v / max);
      // dark green -> light green -> white
      const stops = [[11, 107, 58], [111, 207, 151], [255, 255, 255]];
      const s = t < .5 ? 0 : 1, f = t < .5 ? t / .5 : (t - .5) / .5;
      const a = stops[s], b = stops[s + 1];
      return [0, 1, 2].map((k) => Math.round(a[k] + (b[k] - a[k]) * f));
    }
    function draw() {
      const size = Math.min(canvas.clientWidth || 300, 340);
      canvas.style.width = size + "px";
      const { ctx } = setupCanvas(canvas, size);
      const off = document.createElement("canvas");
      off.width = n; off.height = n;
      const octx = off.getContext("2d");
      const img = octx.createImageData(n, n);
      for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
        const [r, g, b] = color(matrix[i][j]);
        const p = (i * n + j) * 4;
        img.data[p] = r; img.data[p + 1] = g; img.data[p + 2] = b; img.data[p + 3] = 255;
      }
      octx.putImageData(img, 0, 0);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(off, 0, 0, size, size);
      (opts.boundaries || []).forEach((bnd) => {
        const x = (bnd / n) * size;
        ctx.strokeStyle = "rgba(0,0,0,.65)"; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, size); ctx.moveTo(0, x); ctx.lineTo(size, x); ctx.stroke();
      });
      canvas.onpointermove = (e) => {
        const r = canvas.getBoundingClientRect();
        const j = Math.floor(((e.clientX - r.left) / r.width) * n);
        const i = Math.floor(((e.clientY - r.top) / r.height) * n);
        if (i >= 0 && j >= 0 && i < n && j < n) opts.onHover && opts.onHover(i, j, matrix[i][j]);
      };
    }
    draw();
    return { redraw: draw };
  }

  window.CSBCharts = { lineChart, heatmap, plddtColor };
})();
