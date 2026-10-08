/* Menú común del ciclo de estudio: ① Índice · ② Guía · ③ Juegos · ④ Examen.
   Calcula las rutas desde la ubicación de este mismo script (…/js/menu.js),
   así funciona igual publicado que abierto con doble clic (file://).
   También gestiona el botón 🌓 de modo claro/oscuro. */
(function () {
  "use strict";

  // Aplica el tema guardado lo antes posible (evita el parpadeo)
  try {
    var guardado = localStorage.getItem("tema");
    if (guardado === "light" || guardado === "dark") {
      document.documentElement.setAttribute("data-theme", guardado);
    }
  } catch (e) { /* almacenamiento no disponible */ }

  var script = document.currentScript ||
    document.querySelector('script[src$="js/menu.js"]');
  var raiz = script.src.replace(/js\/menu\.js(\?.*)?$/, "");
  window.GUIA_RAIZ = raiz;

  var PASOS = [
    { id: "indice", num: "①", texto: "Índice", ruta: "index.html" },
    { id: "guia", num: "②", texto: "Guía", ruta: "esencial/index.html" },
    { id: "juegos", num: "③", texto: "Juegos", ruta: "juegos/index.html" },
    { id: "examen", num: "④", texto: "Examen", ruta: "simulador/index.html" }
  ];

  function pasoActual() {
    var s = document.body.getAttribute("data-seccion");
    if (s) return s;
    var rel = location.href.split("#")[0].split("?")[0].replace(raiz, "");
    if (rel.indexOf("esencial/") === 0) return "guia";
    if (rel.indexOf("juegos/") === 0) return "juegos";
    if (rel.indexOf("simulador/") === 0) return "examen";
    return "indice";
  }

  function temaEfectivo() {
    var t = document.documentElement.getAttribute("data-theme");
    if (t) return t;
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function construir() {
    if (document.querySelector(".ciclo")) return;
    var actual = pasoActual();
    var nav = document.createElement("nav");
    nav.className = "ciclo";
    nav.setAttribute("aria-label", "Pasos para estudiar");

    var html = '<button id="btn-indice" class="btn-icono" type="button" aria-label="Abrir el índice de temas" aria-expanded="false" aria-controls="sidebar-index">☰</button>' +
      '<a class="ciclo__marca" href="' + raiz + 'index.html">Manual <span>Permiso B</span></a><ol class="ciclo__pasos">';
    PASOS.forEach(function (p) {
      html += '<li><a class="ciclo__paso" href="' + raiz + p.ruta + '"' +
        (p.id === actual ? ' aria-current="page"' : "") + '>' +
        '<span class="ciclo__num" aria-hidden="true">' + p.num + '</span>' +
        '<span>' + p.texto + '</span></a></li>';
    });
    html += '</ol><button id="btn-tema" class="btn-icono" type="button" aria-label="Cambiar entre modo claro y oscuro">🌓</button>';
    nav.innerHTML = html;
    document.body.insertBefore(nav, document.body.firstChild);

    var salto = document.createElement("a");
    salto.className = "skip-link";
    salto.href = "#contenido";
    salto.textContent = "Saltar al contenido";
    document.body.insertBefore(salto, nav);

    document.getElementById("btn-tema").addEventListener("click", function () {
      var nuevo = temaEfectivo() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", nuevo);
      try { localStorage.setItem("tema", nuevo); } catch (e) { /* sin almacenamiento */ }
    });

    // El botón ☰ solo tiene sentido si la página tiene panel lateral
    var btnIndice = document.getElementById("btn-indice");
    if (!document.getElementById("sidebar-index")) {
      btnIndice.remove();
    } else {
      btnIndice.addEventListener("click", function () {
        var abierto = document.body.classList.toggle("indice-abierto");
        btnIndice.setAttribute("aria-expanded", abierto ? "true" : "false");
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && document.body.classList.contains("indice-abierto")) {
          document.body.classList.remove("indice-abierto");
          btnIndice.setAttribute("aria-expanded", "false");
          btnIndice.focus();
        }
      });
      // Tocar fuera del panel lo cierra
      document.addEventListener("click", function (e) {
        if (document.body.classList.contains("indice-abierto") &&
            !e.target.closest("#sidebar-index") && !e.target.closest("#btn-indice")) {
          document.body.classList.remove("indice-abierto");
          btnIndice.setAttribute("aria-expanded", "false");
        }
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", construir);
  } else {
    construir();
  }
})();
