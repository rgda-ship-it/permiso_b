/* Interacción de las páginas de tema.
   - Examen tipo: .quiz-question con <ol class="opciones"> de 3 botones (a, b, c);
     la correcta lleva data-correct="true". Al responder se marca y se muestra
     la .justificacion. Si existe [data-marcador], cuenta aciertos.
   - Referencias .ref: se pueden enfocar con teclado o al tocar (muestran el tooltip).
   - Al imprimir se abren todos los desplegables. */
(function () {
  "use strict";
  var LETRAS = ["a", "b", "c"];

  function prepararExamen() {
    var preguntas = document.querySelectorAll(".quiz-question");
    if (!preguntas.length) return;
    var marcador = document.querySelector("[data-marcador]");
    var aciertos = 0, respondidas = 0;

    function pintarMarcador() {
      if (!marcador) return;
      marcador.classList.add("marcador");
      marcador.textContent = "Aciertos: " + aciertos + " de " + respondidas +
        " respondidas (" + preguntas.length + " en total)";
    }

    preguntas.forEach(function (q) {
      var botones = q.querySelectorAll(".opciones button");
      botones.forEach(function (b, i) {
        if (!b.querySelector(".letra")) {
          var letra = document.createElement("span");
          letra.className = "letra";
          letra.textContent = (LETRAS[i] || i + 1) + ")";
          b.insertBefore(letra, b.firstChild);
        }
        b.type = "button";
        b.addEventListener("click", function () {
          if (q.classList.contains("respondida")) return;
          q.classList.add("respondida");
          respondidas++;
          var bien = b.getAttribute("data-correct") === "true";
          if (bien) aciertos++;
          botones.forEach(function (o) {
            o.disabled = true;
            if (o.getAttribute("data-correct") === "true") o.classList.add("correcta");
          });
          if (!bien) b.classList.add("incorrecta");
          var j = q.querySelector(".justificacion");
          if (j) {
            j.setAttribute("role", "status");
            j.insertAdjacentHTML("afterbegin", "<p><b>" + (bien ? "✅ ¡Correcto!" : "❌ No es correcta.") + "</b></p>");
          }
          pintarMarcador();
        });
      });
    });
    pintarMarcador();
  }

  function prepararReferencias() {
    document.querySelectorAll(".ref").forEach(function (r) {
      if (!r.hasAttribute("tabindex")) r.setAttribute("tabindex", "0");
      if (r.dataset.tooltip && !r.hasAttribute("aria-label")) {
        r.setAttribute("aria-label", "Libro, " + r.textContent.trim() + ": " + r.dataset.tooltip);
      }
    });
  }

  function prepararImpresion() {
    var abiertos = [];
    window.addEventListener("beforeprint", function () {
      abiertos = [];
      document.querySelectorAll("details:not([open])").forEach(function (d) {
        d.setAttribute("open", "");
        abiertos.push(d);
      });
    });
    window.addEventListener("afterprint", function () {
      abiertos.forEach(function (d) { d.removeAttribute("open"); });
    });
  }

  function iniciar() {
    prepararExamen();
    prepararReferencias();
    prepararImpresion();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();
