/* ③ Juegos. Datos: fichas.js (FICHAS, automático) y datos.js (JUEGOS, redactado y verificado).
   Los dos los genera scripts/generar_juegos.py. */
(function () {
  "use strict";
  var FICHAS = (window.FICHAS && window.FICHAS.temas) || [];
  var CUR = (window.JUEGOS && window.JUEGOS.temas) || [];
  var RONDA = { quien: 10, mitos: 10, situaciones: 8, secuencias: 5, parejas: 5 };
  var NOMBRES = { pasapalabra: "Pasapalabra", quien: "¿Quién soy?", mitos: "¿Mito o realidad?",
    situaciones: "Situaciones al volante", secuencias: "Secuencias", parejas: "Parejas de cifras" };

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }
  function md(s) { return esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>"); }
  function sinTildes(s) { return String(s).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); }
  function ref(p) {
    return p ? ' <span class="ref" tabindex="0" data-tooltip="Manual Permiso B (DGT, LF), p. ' + esc(p) + '">p.' + esc(p) + "</span>" : "";
  }
  function barajar(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var x = a[i]; a[i] = a[j]; a[j] = x; }
    return a;
  }
  function etiqueta(t) {
    return '<span class="ju-tema-etiqueta" style="--c:' + t.color + '">' + esc(t.titulo) + "</span>";
  }
  function enlaceTema(t) { return '<a href="../' + esc(t.archivo) + '">Ver el tema →</a>'; }

  /* Palabra principal de un término: sin paréntesis ni códigos de señal («R-1 Ceda el paso» → «Ceda el paso») */
  function principal(t) { return t.replace(/\s*\(.*?\)\s*/g, " ").replace(/^[A-Z]-\d+[a-z]?\s+/, "").trim(); }
  function normal(s) {
    return sinTildes(String(s).replace(/ñ/gi, "#")).replace(/#/g, "ñ").replace(/[^a-z0-9ñ ]+/g, " ").replace(/^\s*(el|la|los|las|un|una)\s+/, "").replace(/\s+/g, " ").trim();
  }
  /* Tapa el término en su definición (sin tener en cuenta tildes ni mayúsculas) */
  function tapar(def, termino) {
    var out = def;
    var palabras = principal(termino).split(/\s+/).filter(function (w) { return w.length >= 4; });
    palabras.concat([principal(termino)]).forEach(function (w) {
      var patron = w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
        .replace(/[aá]/gi, "[aá]").replace(/[eé]/gi, "[eé]").replace(/[ií]/gi, "[ií]")
        .replace(/[oó]/gi, "[oó]").replace(/[uúü]/gi, "[uúü]");
      out = out.replace(new RegExp("(?<!\\p{L})" + patron + "(?!\\p{L})", "giu"), "……");
    });
    return out;
  }

  function temasElegidos(lista) {
    var id = $("ju-tema").value;
    return lista.filter(function (t) { return !id || t.id === id; });
  }
  function pool(lista, campo) {
    var out = [];
    temasElegidos(lista).forEach(function (t) { (t[campo] || []).forEach(function (x) { out.push({ x: x, tema: t }); }); });
    return out;
  }

  /* ---------- Marco común ---------- */
  var estado = null;
  var panel;

  function abrir(juego) {
    $("ju-menu").hidden = true;
    panel.hidden = false;
    estado = { juego: juego, aciertos: 0, total: 0, fallos: [] };
    ({ pasapalabra: pasapalabra, quien: quien, mitos: mitos, situaciones: situaciones,
       secuencias: secuencias, parejas: parejas })[juego]();
    panel.scrollIntoView({ block: "start" });
  }
  function volver() {
    panel.hidden = true;
    panel.innerHTML = "";
    $("ju-menu").hidden = false;
    estado = null;
  }
  function barra(extra) {
    return '<div class="ju-barra"><h2>' + NOMBRES[estado.juego] + '</h2><span class="ju-marcador" data-marcador>' +
      (extra || marcador()) + '</span></div>';
  }
  function marcador() { return estado.aciertos + " de " + estado.total + " bien"; }
  function actualizarMarcador() { var m = panel.querySelector("[data-marcador]"); if (m) m.textContent = marcador(); }
  function vacio(que) {
    panel.innerHTML = barra(" ") + "<p>Este tema todavía no tiene " + que + '. Elige «Todos los temas» u otro tema.</p>' +
      '<div class="ju-botones"><button type="button" class="ju-boton" data-volver>← Elegir otro juego</button></div>';
  }
  function resumen(textoFallos) {
    var h = barra() + '<div class="ju-resumen"><p class="ju-pista">Has acertado ' + estado.aciertos + " de " + estado.total + ".</p>";
    if (estado.fallos.length) {
      h += "<p>" + (textoFallos || "Para repasar:") + "</p><ul>" + estado.fallos.map(function (f) { return "<li>" + f + "</li>"; }).join("") + "</ul>";
    } else if (estado.total) {
      h += "<p>¡Todo bien! 🎉</p>";
    }
    h += '</div><div class="ju-botones"><button type="button" class="ju-boton ju-boton--primario" data-otra>Jugar otra vez</button>' +
      '<button type="button" class="ju-boton" data-volver>← Elegir otro juego</button></div>';
    panel.innerHTML = h;
  }
  function feedback(ok, titulo, cuerpo, p, tema) {
    return '<div class="ju-feedback ' + (ok ? "ok" : "mal") + '"><p><b>' + (ok ? "✔ ¡Bien! " : "✘ No. ") + titulo + "</b></p>" +
      "<p>" + cuerpo + ref(p) + "</p><p>" + enlaceTema(tema) + "</p></div>";
  }
  function botonSiguiente(ultima) {
    return '<div class="ju-botones"><button type="button" class="ju-boton ju-boton--primario" data-siguiente>' +
      (ultima ? "Ver resultado" : "Siguiente →") + "</button></div>";
  }

  /* ---------- Preguntas de una en una (¿Quién soy?, mitos, situaciones) ---------- */
  function preguntas(lista, pintar) {
    estado.lista = lista;
    estado.i = 0;
    estado.siguiente = function () {
      estado.i++;
      if (estado.i >= estado.lista.length) resumen(); else pintar(estado.lista[estado.i]);
    };
    pintar(lista[0]);
  }
  function opcionesHtml(opciones) {
    return '<ul class="opciones">' + opciones.map(function (o, i) {
      return '<li><button type="button" data-op="' + i + '"><span class="letra">' + "abc"[i] + ")</span><span>" + esc(o) + "</span></button></li>";
    }).join("") + "</ul>";
  }
  function corregirOpciones(elegida, correcta) {
    panel.querySelectorAll("[data-op]").forEach(function (b) {
      b.disabled = true;
      if (+b.dataset.op === correcta) b.classList.add("correcta");
      else if (+b.dataset.op === elegida) b.classList.add("incorrecta");
    });
  }

  function quien() {
    var todos = pool(FICHAS, "defs");
    if (todos.length < 3) return vacio("definiciones");
    var lista = barajar(todos).slice(0, RONDA.quien);
    preguntas(lista, function (q) {
      var mismo = todos.filter(function (o) { return o.tema.id === q.tema.id && normal(principal(o.x.t)) !== normal(principal(q.x.t)); });
      var otros = todos.filter(function (o) { return o.tema.id !== q.tema.id; });
      var distractores = barajar(mismo).concat(barajar(otros)).slice(0, 2);
      var ops = barajar([q].concat(distractores));
      var correcta = ops.indexOf(q);
      panel.innerHTML = barra() + etiqueta(q.tema) + '<p class="muted">Pregunta ' + (estado.i + 1) + " de " + estado.lista.length + '</p>' +
        '<p class="ju-pista">«' + esc(tapar(q.x.d, q.x.t)) + "»</p><p>¿Quién soy?</p>" +
        opcionesHtml(ops.map(function (o) { return o.x.t; })) + '<div data-fb></div>';
      estado.responder = function (i) {
        var ok = i === correcta;
        estado.total++;
        if (ok) estado.aciertos++; else estado.fallos.push("<b>" + esc(q.x.t) + "</b>: " + esc(q.x.d) + ref(q.x.p));
        corregirOpciones(i, correcta);
        panel.querySelector("[data-fb]").innerHTML = feedback(ok, "Es «" + esc(q.x.t) + "».", esc(q.x.d), q.x.p, q.tema) +
          botonSiguiente(estado.i === estado.lista.length - 1);
        actualizarMarcador();
      };
    });
  }

  function mitos() {
    var todos = pool(CUR, "mitos");
    if (!todos.length) return vacio("frases de ¿Mito o realidad?");
    preguntas(barajar(todos).slice(0, RONDA.mitos), function (q) {
      panel.innerHTML = barra() + etiqueta(q.tema) + '<p class="muted">Frase ' + (estado.i + 1) + " de " + estado.lista.length + '</p>' +
        '<p class="ju-pista">«' + esc(q.x.f) + '»</p><div class="ju-dos"><button type="button" data-mr="0">🤔 Mito</button>' +
        '<button type="button" data-mr="1">✅ Realidad</button></div><div data-fb></div>';
      estado.responder = function (i) {
        var ok = (i === 1) === q.x.r;
        estado.total++;
        if (ok) estado.aciertos++; else estado.fallos.push("«" + esc(q.x.f) + "» → <b>" + (q.x.r ? "Realidad" : "Mito") + "</b>" + ref(q.x.p));
        panel.querySelectorAll("[data-mr]").forEach(function (b) {
          b.disabled = true;
          if ((b.dataset.mr === "1") === q.x.r) b.classList.add("correcta"); else if (+b.dataset.mr === i) b.classList.add("incorrecta");
        });
        panel.querySelector("[data-fb]").innerHTML = feedback(ok, q.x.r ? "Es realidad." : "Es un mito.", esc(q.x.e), q.x.p, q.tema) +
          botonSiguiente(estado.i === estado.lista.length - 1);
        actualizarMarcador();
      };
    });
  }

  function situaciones() {
    var todos = pool(CUR, "situaciones");
    if (!todos.length) return vacio("situaciones");
    preguntas(barajar(todos).slice(0, RONDA.situaciones), function (q) {
      var orden = barajar([0, 1, 2]);
      var correcta = orden.indexOf(q.x.c);
      panel.innerHTML = barra() + etiqueta(q.tema) + '<p class="muted">Situación ' + (estado.i + 1) + " de " + estado.lista.length + '</p>' +
        '<p class="ju-pista">' + esc(q.x.s) + "</p>" + opcionesHtml(orden.map(function (k) { return q.x.o[k]; })) + '<div data-fb></div>';
      estado.responder = function (i) {
        var ok = i === correcta;
        estado.total++;
        if (ok) estado.aciertos++; else estado.fallos.push(esc(q.x.s) + " → <b>" + esc(q.x.o[q.x.c]) + "</b>" + ref(q.x.p));
        corregirOpciones(i, correcta);
        panel.querySelector("[data-fb]").innerHTML = feedback(ok, "", esc(q.x.e), q.x.p, q.tema) +
          botonSiguiente(estado.i === estado.lista.length - 1);
        actualizarMarcador();
      };
    });
  }

  /* ---------- Pasapalabra ---------- */
  var LETRAS = "ABCDEFGHIJLMNÑOPQRSTUVZ".split("");
  function pasapalabra() {
    /* Solo términos cortos (hasta 3 palabras) y que no sean parejas («LDW y LKA») */
    var todos = pool(FICHAS, "defs").filter(function (o) {
      var t = principal(o.x.t);
      return !/\s(y|e|frente a)\s/.test(t) && t.split(/\s+/).length <= 3;
    });
    if (todos.length < 3) return vacio("definiciones");
    var usados = {};
    var rosco = [];
    LETRAS.forEach(function (L) {
      var l = L.toLowerCase();
      function libre(o) { return !usados[o.x.t]; }
      var empieza = barajar(todos.filter(function (o) { return libre(o) && normal(principal(o.x.t)).charAt(0) === l; }));
      var contiene = barajar(todos.filter(function (o) { return libre(o) && normal(principal(o.x.t)).indexOf(l) > 0; }));
      var o = empieza[0] || contiene[0];
      if (!o) return;
      usados[o.x.t] = true;
      rosco.push({ L: L, modo: empieza[0] ? "Empieza por" : "Contiene la", o: o, estado: "" });
    });
    estado.rosco = rosco;
    estado.total = rosco.length;
    estado.pend = rosco.map(function (_, i) { return i; });
    pintarRosco();
  }
  function pintarRosco(fb) {
    var r = estado.rosco;
    if (!estado.pend.length) {
      estado.fallos = r.filter(function (x) { return x.estado === "fallo"; }).map(function (x) {
        return "<b>" + x.L + ": " + esc(x.o.x.t) + "</b> — " + esc(x.o.x.d) + ref(x.o.x.p);
      });
      return resumen("Las que fallaste:");
    }
    var i = estado.pend[0];
    var q = r[i];
    panel.innerHTML = barra(estado.aciertos + " bien · " + estado.pend.length + " por responder") +
      '<ol class="ju-rosco" aria-label="Letras">' + r.map(function (x, k) {
        return '<li class="' + x.estado + (k === i ? " actual" : "") + '" aria-label="' + x.L + (x.estado ? " " + (x.estado === "acierto" ? "bien" : "mal") : "") + '">' + x.L + "</li>";
      }).join("") + "</ol>" + (fb || "") + etiqueta(q.o.tema) +
      '<p class="ju-pista">' + q.modo + " <b>" + q.L + "</b>: «" + esc(tapar(q.o.x.d, q.o.x.t)) + '»</p>' +
      '<form class="ju-respuesta" data-pasa><label class="sr-only" for="ju-palabra">Tu respuesta</label>' +
      '<input id="ju-palabra" autocomplete="off" autocapitalize="off" placeholder="Escribe la palabra">' +
      '<button type="submit" class="ju-boton ju-boton--primario">Comprobar</button>' +
      '<button type="button" class="ju-boton" data-pasapalabra>Pasapalabra</button></form>' +
      '<div class="ju-botones"><button type="button" class="ju-boton" data-rendirse>Terminar</button></div>';
    var inp = $("ju-palabra");
    if (inp && estado.enfocar) inp.focus();
  }
  function comprobarPalabra(texto) {
    var i = estado.pend.shift();
    var q = estado.rosco[i];
    var buena = normal(principal(q.o.x.t));
    var ok = normal(texto) === buena || normal(texto) === normal(q.o.x.t);
    q.estado = ok ? "acierto" : "fallo";
    if (ok) estado.aciertos++;
    estado.enfocar = true;
    pintarRosco('<div class="ju-feedback ' + (ok ? "ok" : "mal") + '"><p><b>' + (ok ? "✔ ¡Bien! " : "✘ No. ") + q.L + ": " +
      esc(q.o.x.t) + "</b>" + ref(q.o.x.p) + "</p></div>");
  }

  /* ---------- Secuencias ---------- */
  function secuencias() {
    var todos = pool(CUR, "secuencias");
    if (!todos.length) return vacio("secuencias");
    preguntas(barajar(todos).slice(0, RONDA.secuencias), function (q) {
      var pasos = q.x.pasos.map(function (p, k) { return { p: p, k: k }; });
      var mezcla = barajar(pasos);
      while (mezcla.every(function (m, k) { return m.k === k; })) mezcla = barajar(pasos);
      estado.elegidos = [];
      function pintar() {
        var hecho = estado.elegidos.length === pasos.length;
        var h = barra() + etiqueta(q.tema) + '<p class="muted">Secuencia ' + (estado.i + 1) + " de " + estado.lista.length + "</p>" +
          '<p class="ju-pista">' + esc(q.x.t) + "</p><p>Toca los pasos en orden:</p>" +
          '<ul class="ju-pasos">' + mezcla.map(function (m) {
            return '<li><button type="button" data-paso="' + m.k + '"' + (estado.elegidos.indexOf(m.k) >= 0 ? " disabled" : "") + ">" + esc(m.p) + "</button></li>";
          }).join("") + "</ul>";
        if (estado.elegidos.length) {
          h += '<p><b>Tu orden:</b></p><ol class="ju-orden">' + estado.elegidos.map(function (k, pos) {
            return '<li class="' + (hecho ? (k === pos ? "ok" : "mal") : "") + '">' + esc(q.x.pasos[k]) + "</li>";
          }).join("") + "</ol>";
        }
        if (!hecho) {
          h += estado.elegidos.length ? '<div class="ju-botones"><button type="button" class="ju-boton" data-deshacer>↶ Deshacer</button></div>' : "";
        } else {
          var ok = estado.elegidos.every(function (k, pos) { return k === pos; });
          h += feedback(ok, ok ? "Orden correcto." : "El orden correcto es:",
            ok ? "" : "<ol>" + q.x.pasos.map(function (p) { return "<li>" + esc(p) + "</li>"; }).join("") + "</ol>", q.x.p, q.tema) +
            botonSiguiente(estado.i === estado.lista.length - 1);
        }
        panel.innerHTML = h;
      }
      estado.pintarSec = pintar;
      estado.elegir = function (k) {
        estado.elegidos.push(k);
        if (estado.elegidos.length === pasos.length) {
          var ok = estado.elegidos.every(function (x, pos) { return x === pos; });
          estado.total++;
          if (ok) estado.aciertos++; else estado.fallos.push(esc(q.x.t) + ref(q.x.p));
        }
        pintar();
      };
      pintar();
    });
  }

  /* ---------- Parejas de cifras ---------- */
  function parejas() {
    var temas = temasElegidos(FICHAS).filter(function (t) { return t.cifras.length >= 3; });
    if (!temas.length) return vacio("cifras");
    var t = temas[Math.floor(Math.random() * temas.length)];
    var vistos = {};
    var filas = barajar(t.cifras).filter(function (c) {
      var k = normal(c.v);
      if (vistos[k]) return false;
      vistos[k] = true;
      return true;
    }).slice(0, RONDA.parejas);
    estado.par = { tema: t, filas: filas, izq: barajar(filas.map(function (_, i) { return i; })),
      der: barajar(filas.map(function (_, i) { return i; })), hechos: {}, sel: null, errores: 0 };
    pintarParejas();
  }
  function pintarParejas() {
    var e = estado.par;
    var n = Object.keys(e.hechos).length;
    if (n === e.filas.length) {
      estado.total = e.filas.length;
      estado.aciertos = Math.max(0, e.filas.length - e.errores);
      estado.fallos = [];
      panel.innerHTML = barra(e.errores + " errores") + etiqueta(e.tema) + '<p class="ju-pista">¡Hecho! Has unido las ' + n +
        " parejas con " + e.errores + " error" + (e.errores === 1 ? "" : "es") + ".</p><ul>" + e.filas.map(function (f) {
          return "<li>" + md(f.c) + ": <b>" + md(f.v) + "</b>" + ref(f.p) + "</li>";
        }).join("") + "</ul><p>" + enlaceTema(e.tema) + '</p><div class="ju-botones"><button type="button" class="ju-boton ju-boton--primario" data-otra>Otra ronda</button>' +
        '<button type="button" class="ju-boton" data-volver>← Elegir otro juego</button></div>';
      return;
    }
    function boton(lado, i, texto) {
      var cls = e.hechos[i] ? "hecho" : (e.sel && e.sel.lado === lado && e.sel.i === i ? "elegido" : "");
      return '<button type="button" class="' + cls + '" data-lado="' + lado + '" data-i="' + i + '"' + (e.hechos[i] ? " disabled" : "") + ">" + md(texto) + "</button>";
    }
    panel.innerHTML = barra(n + " de " + e.filas.length + " parejas · " + e.errores + " errores") + etiqueta(e.tema) +
      "<p>Toca un dato y después su número.</p>" +
      '<div class="ju-parejas"><div class="ju-col" aria-label="Datos">' + e.izq.map(function (i) { return boton("c", i, e.filas[i].c); }).join("") +
      '</div><div class="ju-col" aria-label="Números">' + e.der.map(function (i) { return boton("v", i, e.filas[i].v); }).join("") + "</div></div>";
  }
  function tocarPareja(lado, i) {
    var e = estado.par;
    if (!e.sel || e.sel.lado === lado) { e.sel = { lado: lado, i: i }; return pintarParejas(); }
    var otro = e.sel;
    e.sel = null;
    if (otro.i === i) { e.hechos[i] = true; return pintarParejas(); }
    e.errores++;
    pintarParejas();
    [[otro.lado, otro.i], [lado, i]].forEach(function (x) {
      var b = panel.querySelector('[data-lado="' + x[0] + '"][data-i="' + x[1] + '"]');
      if (b) b.classList.add("error");
    });
  }

  /* ---------- Arranque y eventos ---------- */
  function iniciar() {
    panel = $("ju-juego");
    FICHAS.forEach(function (t) {
      var o = document.createElement("option");
      o.value = t.id; o.textContent = t.titulo;
      $("ju-tema").appendChild(o);
    });
    $("ju-menu").addEventListener("click", function (e) {
      var c = e.target.closest("[data-juego]");
      if (c) abrir(c.dataset.juego);
    });
    $("ju-tema").addEventListener("change", function () { if (estado) abrir(estado.juego); });
    panel.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b || b.disabled) return;
      if (b.hasAttribute("data-volver")) return volver();
      if (b.hasAttribute("data-otra")) return abrir(estado.juego);
      if (b.hasAttribute("data-siguiente")) return estado.siguiente();
      if (b.dataset.op !== undefined) return estado.responder(+b.dataset.op);
      if (b.dataset.mr !== undefined) return estado.responder(+b.dataset.mr);
      if (b.dataset.paso !== undefined) return estado.elegir(+b.dataset.paso);
      if (b.hasAttribute("data-deshacer")) { estado.elegidos.pop(); return estado.pintarSec(); }
      if (b.dataset.lado) return tocarPareja(b.dataset.lado, +b.dataset.i);
      if (b.hasAttribute("data-pasapalabra")) { estado.pend.push(estado.pend.shift()); estado.enfocar = true; return pintarRosco(); }
      if (b.hasAttribute("data-rendirse")) {
        estado.pend.forEach(function (i) { estado.rosco[i].estado = "fallo"; });
        estado.pend = [];
        return pintarRosco();
      }
    });
    panel.addEventListener("submit", function (e) {
      if (!e.target.hasAttribute("data-pasa")) return;
      e.preventDefault();
      var v = $("ju-palabra").value.trim();
      if (v) comprobarPalabra(v);
    });
    var pedido = (location.hash || "").slice(1);
    if (NOMBRES[pedido]) abrir(pedido);
  }
  iniciar();
})();
