/* ② Guía «lo esencial». Lee window.ESENCIAL (datos.js, generado por scripts/generar_esencial.py). */
(function () {
  "use strict";
  var DATOS = (window.ESENCIAL || { temas: [] }).temas;
  var CLAVE = "esencial-sabidos";
  var sabidos = {};
  try { (JSON.parse(localStorage.getItem(CLAVE) || "[]") || []).forEach(function (k) { sabidos[k] = true; }); } catch (e) { /* sin almacenamiento */ }

  function guardar() {
    try { localStorage.setItem(CLAVE, JSON.stringify(Object.keys(sabidos))); } catch (e) { /* sin almacenamiento */ }
  }
  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }
  function md(s) { return esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>"); }
  function sinTildes(s) { return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); }
  function ref(p) {
    if (!p) return "";
    return ' <span class="ref" tabindex="0" data-tooltip="Manual Permiso B (DGT, LF), p. ' + esc(p) + '">p.' + esc(p) + "</span>";
  }

  /* Resalta q en el HTML de un texto, sin tener en cuenta tildes ni mayúsculas */
  function resaltar(html, q) {
    if (!q) return html;
    return html.replace(/(<[^>]+>)|([^<]+)/g, function (_, tag, txt) {
      if (tag) return tag;
      var n = "", mapa = [];
      for (var i = 0; i < txt.length; i++) {
        var c = sinTildes(txt[i]);
        for (var j = 0; j < c.length; j++) { n += c[j]; mapa.push(i); }
      }
      var out = "", ult = 0, pos = n.indexOf(q);
      while (pos >= 0 && q.length) {
        var a = mapa[pos], b = mapa[pos + q.length - 1] + 1;
        out += txt.slice(ult, a) + "<mark>" + txt.slice(a, b) + "</mark>";
        ult = b;
        pos = n.indexOf(q, pos + q.length);
      }
      return out + txt.slice(ult);
    });
  }

  function terminoMapa(linea) {
    var m = linea.match(/\*\*(.+?)\*\*/);
    return m ? m[1] : linea.split(" — ")[0];
  }

  function item(id, tipo, t, d, p, extra) {
    var marcado = sabidos[id] ? " checked" : "";
    return '<li class="es-item' + (sabidos[id] ? " sabido" : "") + '" data-id="' + id + '" data-tipo="' + tipo + '">' +
      '<input type="checkbox" aria-label="Ya me lo sé: ' + esc(t) + '"' + marcado + ">" +
      "<div><b data-buscar>" + esc(t) + '</b><span class="es-def" data-buscar>' + md(d) + ref(p) + "</span>" + (extra || "") + "</div></li>";
  }

  function htmlTema(t) {
    var h = '<details class="es-tema" id="es-' + t.id + '" style="--c:' + t.color + '" data-tema="' + t.id + '">' +
      "<summary><h2>" + esc(t.titulo) + '</h2><span class="es-tema__prog" data-prog></span>' +
      "<p>" + md(t.frase) + '</p><div class="es-barra"><span data-barra></span></div></summary><div class="es-tema__cuerpo">';

    h += '<div data-bloque="memorizar"><h3>🔴 Memorizar sí o sí</h3><ul class="es-lista">';
    t.memorizar.forEach(function (m, i) { h += item(t.id + "-m-" + i, "memorizar", m.t, m.d, m.p); });
    h += "</ul></div>";

    h += '<div data-bloque="dominar"><h3>🟠 Importante entender</h3><ul class="es-lista">';
    t.dominar.forEach(function (d, i) {
      var cubre = (d.cubre || []).map(function (n) { return t.mapa[n - 1] ? terminoMapa(t.mapa[n - 1]) : ""; }).filter(Boolean);
      var extra = cubre.length ? "<small>Del mapa del tema: " + esc(cubre.join(" · ")) + "</small>" : "";
      h += item(t.id + "-d-" + i, "dominar", d.t, d.d, d.p, extra);
    });
    h += "</ul></div>";

    h += '<div data-bloque="extra">';
    t.tablas.forEach(function (tb) {
      h += '<h3>📋 ' + md(tb.titulo) + '</h3><div class="tabla-wrap"><table><thead><tr>' +
        tb.cab.map(function (c) { return '<th scope="col">' + md(c) + "</th>"; }).join("") + "</tr></thead><tbody>" +
        tb.filas.map(function (f) { return "<tr>" + f.map(function (c) { return '<td data-buscar>' + md(c) + "</td>"; }).join("") + "</tr>"; }).join("") +
        "</tbody></table></div>";
    });
    if (t.cifras.length) {
      h += '<h3>🔢 Cifras clave</h3><div class="tabla-wrap"><table><thead><tr><th scope="col">Dato</th><th scope="col">Valor</th><th scope="col">Pág.</th></tr></thead><tbody>' +
        t.cifras.map(function (c) { return '<tr><td data-buscar>' + md(c.c) + '</td><td data-buscar><b>' + md(c.v) + "</b></td><td>" + esc(c.p) + "</td></tr>"; }).join("") +
        "</tbody></table></div>";
    }
    if (t.trampas.length) {
      h += '<h3>⚠️ Trampas de examen</h3><ul class="es-lista">' +
        t.trampas.map(function (x) { return '<li class="es-item es-trampa" style="grid-template-columns:1fr"><div><b>' + md(x.t) + '</b><span data-buscar>' + md(x.d) + "</span></div></li>"; }).join("") + "</ul>";
    }
    if (t.mnemo.length) {
      h += '<h3>🧠 Para recordarlo</h3><ul class="es-lista">' +
        t.mnemo.map(function (x) { return '<li class="es-item es-mnemo" style="grid-template-columns:1fr"><div><span data-buscar>' + md(x.r) + "</span> <small>(" + esc(x.base) + ")</small></div></li>"; }).join("") + "</ul>";
    }
    if (t.conexiones.length) {
      h += '<h3>🔗 Conexiones</h3><ul class="es-conex">' +
        t.conexiones.map(function (c) {
          var o = DATOS.filter(function (x) { return x.id === c.id; })[0];
          return '<li><a href="#es-' + c.id + '" data-ir="' + c.id + '">' + esc(o ? o.titulo.split(". ")[0] : c.id) + ": " + esc(c.por) + "</a></li>";
        }).join("") + "</ul>";
    }
    h += "</div>";
    h += '<p class="es-tema__enlace"><a href="../' + esc(t.archivo) + '">Ver el tema completo →</a></p></div></details>';
    return h;
  }

  function pintarTemas() {
    $("vista-temas").innerHTML = DATOS.map(htmlTema).join("");
    actualizarProgreso();
  }

  function pintarGlosario() {
    var todos = [];
    DATOS.forEach(function (t) { t.memorizar.forEach(function (m) { todos.push({ t: m.t, d: m.d, p: m.p, tema: t }); }); });
    todos.sort(function (a, b) { return a.t.localeCompare(b.t, "es"); });
    var grupos = {};
    todos.forEach(function (x) { var l = sinTildes(x.t)[0].toUpperCase(); (grupos[l] = grupos[l] || []).push(x); });
    var letras = Object.keys(grupos).sort();
    var h = '<nav class="es-letras" aria-label="Letras">' + letras.map(function (l) { return '<a href="#gl-' + l + '">' + l + "</a>"; }).join("") + "</nav>";
    letras.forEach(function (l) {
      h += '<h2 id="gl-' + l + '">' + l + '</h2><dl class="es-glosario">';
      grupos[l].forEach(function (x) {
        h += '<div data-glosa><dt>' + esc(x.t) + '</dt><dd><span class="es-def" data-buscar>' + md(x.d) + ref(x.p) + '</span> <small>· <a href="#es-' + x.tema.id + '" data-ir="' + x.tema.id + '">' + esc(x.tema.titulo.split(". ")[0]) + "</a></small></dd></div>";
      });
      h += "</dl>";
    });
    $("vista-glosario").innerHTML = h;
  }

  function actualizarProgreso() {
    var total = 0, hechos = 0;
    DATOS.forEach(function (t) {
      var n = t.memorizar.length + t.dominar.length, s = 0;
      t.memorizar.forEach(function (_, i) { if (sabidos[t.id + "-m-" + i]) s++; });
      t.dominar.forEach(function (_, i) { if (sabidos[t.id + "-d-" + i]) s++; });
      total += n; hechos += s;
      var el = $("es-" + t.id);
      if (el) {
        el.querySelector("[data-prog]").textContent = s + " de " + n;
        el.querySelector("[data-barra]").style.width = (n ? Math.round(100 * s / n) : 0) + "%";
      }
    });
    var pct = total ? Math.round(100 * hechos / total) : 0;
    $("es-progreso").innerHTML = '<div class="progreso__barra" role="progressbar" aria-valuemin="0" aria-valuemax="' + total +
      '" aria-valuenow="' + hechos + '" aria-label="Lo que ya te sabes"><span style="width:' + pct + '%"></span></div>' +
      "<p>Ya te sabes " + hechos + " de " + total + " puntos (" + pct + " %)</p>";
  }

  /* Filtros: búsqueda, tema y «Solo 🔴» */
  var originales = new WeakMap();
  function filtrar() {
    var q = sinTildes($("es-buscar").value.trim());
    var tema = $("es-tema").value;
    var soloRojo = $("es-solo-rojo").checked;
    var visibles = 0;
    document.querySelectorAll("[data-buscar]").forEach(function (el) {
      if (!originales.has(el)) originales.set(el, el.innerHTML);
      el.innerHTML = resaltar(originales.get(el), q);
    });
    document.querySelectorAll(".es-tema").forEach(function (sec) {
      var okTema = !tema || sec.dataset.tema === tema;
      var hayAlgo = false;
      sec.querySelectorAll(".es-item, tbody tr").forEach(function (it) {
        var tipo = it.dataset.tipo;
        var visiblePorTipo = !soloRojo || tipo === "memorizar";
        var coincide = !q || sinTildes(it.textContent).indexOf(q) >= 0;
        var ver = visiblePorTipo && coincide;
        it.hidden = !ver;
        if (ver && (tipo === "memorizar" || tipo === "dominar" || !soloRojo)) hayAlgo = true;
      });
      sec.querySelector('[data-bloque="dominar"]').hidden = soloRojo;
      sec.querySelector('[data-bloque="extra"]').hidden = soloRojo;
      sec.hidden = !okTema || (q && !hayAlgo);
      if (!sec.hidden) visibles++;
      if (q && !sec.hidden) sec.open = true;
    });
    document.querySelectorAll("[data-glosa]").forEach(function (g) {
      g.hidden = q && sinTildes(g.textContent).indexOf(q) < 0;
    });
    $("es-resultado").textContent = q ? (visibles ? visibles + " temas con «" + $("es-buscar").value.trim() + "»" : "No hay resultados") : "";
  }

  function iniciar() {
    if (!DATOS.length) { $("vista-temas").innerHTML = "<p>No hay datos. Ejecuta scripts/generar_esencial.py.</p>"; return; }
    DATOS.forEach(function (t) {
      var o = document.createElement("option");
      o.value = t.id; o.textContent = t.titulo;
      $("es-tema").appendChild(o);
    });
    pintarTemas();
    pintarGlosario();
    var primero = document.querySelector(".es-tema");
    if (primero) primero.open = true;

    document.addEventListener("change", function (e) {
      var li = e.target.closest(".es-item");
      if (li && e.target.type === "checkbox") {
        if (e.target.checked) sabidos[li.dataset.id] = true; else delete sabidos[li.dataset.id];
        li.classList.toggle("sabido", e.target.checked);
        guardar();
        actualizarProgreso();
      }
    });
    document.addEventListener("click", function (e) {
      var def = e.target.closest(".tapar .es-def");
      if (def) def.classList.toggle("visto");
      var ir = e.target.closest("[data-ir]");
      if (ir) {
        mostrarVista("temas");
        var d = $("es-" + ir.dataset.ir);
        if (d) { d.hidden = false; d.open = true; }
      }
    });
    $("es-buscar").addEventListener("input", filtrar);
    $("es-tema").addEventListener("change", function () {
      filtrar();
      var d = $("es-" + this.value);
      if (d) d.open = true;
    });
    $("es-solo-rojo").addEventListener("change", filtrar);
    $("es-tapar").addEventListener("change", function () {
      document.querySelector("main").classList.toggle("tapar", this.checked);
      document.querySelectorAll(".es-def.visto").forEach(function (d) { d.classList.remove("visto"); });
    });
    $("es-imprimir").addEventListener("click", function () { window.print(); });
    var abiertos = [];
    window.addEventListener("beforeprint", function () {
      abiertos = [];
      document.querySelectorAll(".es-tema:not([open])").forEach(function (d) { d.open = true; abiertos.push(d); });
    });
    window.addEventListener("afterprint", function () { abiertos.forEach(function (d) { d.open = false; }); });
    $("tab-temas").addEventListener("click", function () { mostrarVista("temas"); });
    $("tab-glosario").addEventListener("click", function () { mostrarVista("glosario"); });
  }

  function mostrarVista(v) {
    $("vista-temas").hidden = v !== "temas";
    $("vista-glosario").hidden = v !== "glosario";
    $("tab-temas").setAttribute("aria-selected", v === "temas");
    $("tab-glosario").setAttribute("aria-selected", v === "glosario");
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar);
  else iniciar();
})();
