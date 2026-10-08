/* Navegación del temario. Única fuente del orden y los títulos en la web
   (copiados exactamente de Temario.txt).
   - Panel lateral con todos los temas (#sidebar-index)
   - Anterior / siguiente al pie (#page-nav)
   - Índice «En esta página» con resaltado al desplazarse (#toc)
   - Portada: índice del temario (#indice-temario) y progreso (#progreso)
   Cada página de tema solo lleva <body data-temario="T3"> y los contenedores vacíos.
   Al terminar un tema: cambiar su estado a "listo". */
(function () {
  "use strict";

  var TEMARIO = [
    { id: "T1", numero: 1, titulo: "Tema 1. Definiciones", archivo: "tema01/definiciones.html", estado: "listo" },
    { id: "T2", numero: 2, titulo: "Tema 2. Documentación", archivo: "tema02/documentacion.html", estado: "pendiente" },
    { id: "T3", numero: 3, titulo: "Tema 3. El estado del conductor", archivo: "tema03/estado-del-conductor.html", estado: "listo" },
    { id: "T4", numero: 4, titulo: "Tema 4. Obligaciones de conductores y peatones", archivo: "tema04/obligaciones-conductores-peatones.html", estado: "pendiente" },
    { id: "T5", numero: 5, titulo: "Tema 5. Dispositivos de seguridad en el vehículo", archivo: "tema05/dispositivos-de-seguridad.html", estado: "pendiente" },
    { id: "T6", numero: 6, titulo: "Tema 6. Elementos del vehículo y normas para usarlos", archivo: "tema06/elementos-del-vehiculo.html", estado: "pendiente" },
    { id: "T7", numero: 7, titulo: "Tema 7. Sistema de luces de los vehículos", archivo: "tema07/sistema-de-luces.html", estado: "pendiente" },
    { id: "T8", numero: 8, titulo: "Tema 8. Señales de circulación", archivo: "tema08/senales-de-circulacion.html", estado: "pendiente" },
    { id: "T9", numero: 9, titulo: "Tema 9. La vía", archivo: "tema09/la-via.html", estado: "pendiente" },
    { id: "T10", numero: 10, titulo: "Tema 10. Velocidad y distancias", archivo: "tema10/velocidad-y-distancias.html", estado: "pendiente" },
    { id: "T11", numero: 11, titulo: "Tema 11. Maniobras", archivo: "tema11/maniobras.html", estado: "pendiente" },
    { id: "T12", numero: 12, titulo: "Tema 12. Normas de preferencia para circular", archivo: "tema12/normas-de-preferencia.html", estado: "pendiente" },
    { id: "T13", numero: 13, titulo: "Tema 13. Transportar personas y cargas", archivo: "tema13/transportar-personas-y-cargas.html", estado: "pendiente" },
    { id: "T14", numero: 14, titulo: "Tema 14. Conducir de forma segura", archivo: "tema14/conducir-de-forma-segura.html", estado: "pendiente" },
    { id: "T15", numero: 15, titulo: "Tema 15. Mecánica y mantenimiento del vehículo", archivo: "tema15/mecanica-y-mantenimiento.html", estado: "pendiente" },
    { id: "T16", numero: 16, titulo: "Tema 16. Accidentes de tráfico", archivo: "tema16/accidentes-de-trafico.html", estado: "pendiente" },
    { id: "T17", numero: 17, titulo: "Tema 17. Conducción preventiva y eficiente", archivo: "tema17/conduccion-preventiva-y-eficiente.html", estado: "pendiente" },
    { id: "ANEXO", numero: 18, titulo: "Anexo puntos. El permiso de conducir por puntos", archivo: "anexo/permiso-por-puntos.html", estado: "pendiente" }
  ];
  window.TEMARIO = TEMARIO;

  // Color de cada tema = color de su cabecera en el libro (igual que en style.css)
  var COLORES = {
    T1: "#248ec5", T2: "#009ee3", T3: "#00b2c3", T4: "#008784", T5: "#7fb289", T6: "#a9d19a",
    T7: "#d2db5c", T8: "#dabe3b", T9: "#f3c05c", T10: "#f3997a", T11: "#e09197", T12: "#eb5f84",
    T13: "#e5007d", T14: "#c35b9e", T15: "#9184be", T16: "#738fb3", T17: "#476eac", ANEXO: "#023d83"
  };
  var ETIQUETA_ESTADO = { listo: "Listo", pendiente: "Pendiente", "sin fuente": "Sin fuente" };

  var script = document.currentScript || document.querySelector('script[src$="js/temario-nav.js"]');
  var raiz = script.src.replace(/js\/temario-nav\.js(\?.*)?$/, "");

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function disponible(t) { return t.estado === "listo"; }
  function partes(t) {
    // «Tema 3. El estado del conductor» → ["Tema 3", "El estado del conductor"]
    var i = t.titulo.indexOf(". ");
    return [t.titulo.slice(0, i), t.titulo.slice(i + 2)];
  }

  function cargarMenu() {
    if (document.querySelector('script[src$="js/menu.js"]')) return;
    var s = document.createElement("script");
    s.src = raiz + "js/menu.js";
    document.head.appendChild(s);
  }

  function panelLateral(actualId) {
    var aside = document.getElementById("sidebar-index");
    if (!aside) return;
    var html = '<p class="sidebar__titulo">Temario</p><ol>';
    TEMARIO.forEach(function (t) {
      var p = partes(t);
      var estilo = ' style="--c:' + COLORES[t.id] + '"';
      if (disponible(t)) {
        html += '<li><a href="' + raiz + t.archivo + '"' + estilo +
          (t.id === actualId ? ' aria-current="page"' : "") + '><span><b>' + esc(p[0]) + '.</b> ' + esc(p[1]) + '</span></a></li>';
      } else {
        html += '<li><span class="pendiente"' + estilo + '><span><b>' + esc(p[0]) + '.</b> ' + esc(p[1]) +
          '<small>' + esc(ETIQUETA_ESTADO[t.estado] || t.estado) + '</small></span></span></li>';
      }
    });
    aside.setAttribute("aria-label", "Índice de temas");
    aside.innerHTML = html + "</ol>";
  }

  function anteriorSiguiente(actualId) {
    var nav = document.getElementById("page-nav");
    if (!nav) return;
    var i = TEMARIO.findIndex(function (t) { return t.id === actualId; });
    if (i < 0) return;
    // salta a los temas disponibles más cercanos
    var ant = null, sig = null, k;
    for (k = i - 1; k >= 0; k--) if (disponible(TEMARIO[k])) { ant = TEMARIO[k]; break; }
    for (k = i + 1; k < TEMARIO.length; k++) if (disponible(TEMARIO[k])) { sig = TEMARIO[k]; break; }
    var html = "";
    if (ant) html += '<a class="anterior" href="' + raiz + ant.archivo + '"><small>← Anterior</small>' + esc(ant.titulo) + "</a>";
    if (sig) html += '<a class="siguiente" href="' + raiz + sig.archivo + '"><small>Siguiente →</small>' + esc(sig.titulo) + "</a>";
    if (!ant && !sig) html = '<a class="anterior" href="' + raiz + 'index.html"><small>← Volver</small>Índice de temas</a>';
    nav.setAttribute("aria-label", "Tema anterior y siguiente");
    nav.className = "page-nav";
    nav.innerHTML = html;
  }

  function slug(s) {
    return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase()
      .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60);
  }

  function enEstaPagina() {
    var cont = document.getElementById("toc");
    if (!cont) return;
    var main = document.getElementById("contenido") || document.body;
    // h2 y h3, y los h4 de subapartado (hijos directos de una .fase; no los de las tarjetas)
    var hs = Array.prototype.slice.call(main.querySelectorAll("h2, h3, .fase > h4"));
    if (hs.length < 2) { cont.remove(); return; }
    var usados = {};
    var html = '<details open><summary>En esta página</summary><ol>';
    hs.forEach(function (h) {
      if (!h.id) {
        var base = slug(h.textContent) || "seccion", id = base, n = 2;
        while (usados[id] || document.getElementById(id)) id = base + "-" + n++;
        h.id = id;
      }
      usados[h.id] = true;
      html += '<li class="' + h.tagName.toLowerCase() + '"><a href="#' + h.id + '">' + esc(h.textContent.trim()) + "</a></li>";
    });
    cont.className = "toc";
    cont.setAttribute("aria-label", "En esta página");
    cont.innerHTML = html + "</ol></details>";
    // En móvil empieza plegado para no tapar el contenido
    if (window.matchMedia && matchMedia("(max-width: 760px)").matches) {
      cont.querySelector("details").removeAttribute("open");
    }

    if (!("IntersectionObserver" in window)) return;
    var enlaces = {};
    cont.querySelectorAll("a").forEach(function (a) { enlaces[a.getAttribute("href").slice(1)] = a; });
    var visibles = {};
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) { visibles[e.target.id] = e.isIntersecting; });
      var activo = null;
      for (var j = 0; j < hs.length; j++) { if (visibles[hs[j].id]) { activo = hs[j].id; break; } }
      if (!activo) return;
      Object.keys(enlaces).forEach(function (id) { enlaces[id].classList.toggle("activo", id === activo); });
    }, { rootMargin: "-60px 0px -60% 0px" });
    hs.forEach(function (h) { obs.observe(h); });
  }

  function portada() {
    var lista = document.getElementById("indice-temario");
    if (lista) {
      var html = "";
      TEMARIO.forEach(function (t) {
        var p = partes(t);
        var estado = '<span class="estado estado--' + slug(t.estado) + '">' + esc(ETIQUETA_ESTADO[t.estado] || t.estado) + "</span>";
        var dentro = '<span><b>' + esc(p[0]) + '.</b> ' + esc(p[1]) + "</span>" + estado;
        var estilo = ' style="--c:' + COLORES[t.id] + '"';
        html += disponible(t)
          ? '<li><a href="' + raiz + t.archivo + '"' + estilo + ">" + dentro + "</a></li>"
          : '<li><span class="pendiente"' + estilo + ">" + dentro + "</span></li>";
      });
      lista.className = "indice-temario";
      lista.innerHTML = html;
    }
    var prog = document.getElementById("progreso");
    if (prog) {
      var listos = TEMARIO.filter(disponible).length, total = TEMARIO.length;
      var pct = Math.round(100 * listos / total);
      prog.className = "progreso";
      prog.innerHTML = '<div class="progreso__barra" role="progressbar" aria-valuemin="0" aria-valuemax="' + total +
        '" aria-valuenow="' + listos + '" aria-label="Temas listos"><span style="width:' + pct + '%"></span></div>' +
        "<p>" + listos + " de " + total + " temas listos para estudiar</p>";
    }
  }

  function iniciar() {
    var actual = document.body.getAttribute("data-temario");
    panelLateral(actual);
    anteriorSiguiente(actual);
    enEstaPagina();
    portada();
    cargarMenu();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();
