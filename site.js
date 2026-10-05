/* Carola Page · Paisajismo — interacciones del sitio
   Todo es progresivo: sin JavaScript la página se ve y funciona igual,
   solo sin animaciones. */
(function () {
  "use strict";
  var quieto = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // que cada página arranque donde corresponde y no donde quedó la vez anterior
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";

  /* ---------- scroll suave (Lenis) ----------
     Le da inercia al scroll: la página sigue corriendo un poco después de
     soltar la rueda, en vez de frenar en seco. Misma configuración que usa
     Naetive. Si Lenis no cargó o el sistema pide menos movimiento, el scroll
     nativo funciona igual. */
  var lenis = null;
  if (!quieto && window.Lenis) {
    lenis = new window.Lenis({
      duration: 1.1,
      easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); },
      smoothWheel: true,
      wheelMultiplier: 1,
      anchors: { offset: -(parseInt(getComputedStyle(document.documentElement)
                 .getPropertyValue("--header-real"), 10) || 92) - 28 }
    });
    function latido(t) { lenis.raf(t); requestAnimationFrame(latido); }
    requestAnimationFrame(latido);
    window.lenis = lenis;
  }

  /* ---------- cabecera del home sobre el hero ---------- */
  var header = document.getElementById("header");
  var hero = document.querySelector(".hero");
  if (header && hero && header.classList.contains("site-header--over")) {
    new IntersectionObserver(function (e) {
      header.classList.toggle("is-solid", !e[0].isIntersecting);
    }, { rootMargin: "-72px 0px 0px 0px" }).observe(hero);
  }

  /* ---------- alto real de la cabecera (para los saltos de ancla) ---------- */
  if (header) {
    var medir = function () {
      document.documentElement.style.setProperty("--header-real", header.offsetHeight + "px");
    };
    medir();
    addEventListener("resize", medir);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(medir);
  }

  /* ---------- filtros (Archivo, Noticias) ---------- */
  document.querySelectorAll(".filters").forEach(function (grupo) {
    var grid = document.getElementById(grupo.dataset.target || "archivo-grid");
    if (!grid) return;
    grupo.addEventListener("click", function (e) {
      var btn = e.target.closest("button");
      if (!btn) return;
      grupo.querySelectorAll("button").forEach(function (b) {
        b.setAttribute("aria-pressed", String(b === btn));
      });
      var f = btn.dataset.filter, visibles = 0;
      grid.querySelectorAll("[data-cat]").forEach(function (c) {
        c.hidden = f !== "todos" && c.dataset.cat !== f;
        if (!c.hidden) visibles++;
      });
      var vacio = grid.parentNode.querySelector(".grid-vacio");
      if (vacio) vacio.hidden = visibles > 0;
    });
  });

  /* ---------- titulares que caen línea por línea ---------- */
  function partirEnLineas(el) {
    var crudo = el.dataset.crudo;
    if (crudo === undefined) { crudo = el.innerHTML; el.dataset.crudo = crudo; }
    el.innerHTML = crudo;

    // 1. envolver cada palabra para poder medir en qué línea cae
    var frag = document.createDocumentFragment();
    Array.prototype.slice.call(el.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        n.textContent.split(/(\s+)/).forEach(function (tok) {
          if (!tok) return;
          if (/^\s+$/.test(tok)) { frag.appendChild(document.createTextNode(" ")); return; }
          var i = document.createElement("i");
          i.className = "pal"; i.textContent = tok;
          frag.appendChild(i);
        });
      } else {
        frag.appendChild(n.cloneNode(true));
      }
    });
    el.innerHTML = "";
    el.appendChild(frag);

    // 2. agrupar por posición vertical
    var lineas = [], ultimo = null;
    el.querySelectorAll("i.pal").forEach(function (p) {
      var top = Math.round(p.offsetTop);
      if (ultimo === null || Math.abs(top - ultimo) > 2) { lineas.push([]); ultimo = top; }
      lineas[lineas.length - 1].push(p);
    });
    if (!lineas.length) return false;

    // 3. rearmar con una máscara por línea
    el.innerHTML = "";
    lineas.forEach(function (palabras, i) {
      var linea = document.createElement("span");
      linea.className = "linea";
      var dentro = document.createElement("span");
      dentro.style.transitionDelay = (i * 0.085).toFixed(3) + "s";
      palabras.forEach(function (p, j) {
        dentro.appendChild(document.createTextNode(j ? " " : ""));
        dentro.appendChild(document.createTextNode(p.textContent));
      });
      linea.appendChild(dentro);
      el.appendChild(linea);
    });
    return true;
  }

  var revelables = Array.prototype.slice.call(document.querySelectorAll("[data-revelar]"));
  if (revelables.length && !quieto) {
    var mirón = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); mirón.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.1 });

    var armar = function () {
      revelables.forEach(function (el) {
        try {
          if (partirEnLineas(el)) el.classList.add("revelar");
          else el.classList.remove("revelar");
        } catch (err) {
          el.classList.remove("revelar");                 // ante la duda, texto visible
          if (el.dataset.crudo !== undefined) el.innerHTML = el.dataset.crudo;
        }
      });
      revelables.forEach(function (el) {
        if (el.getBoundingClientRect().top < innerHeight * 0.9) el.classList.add("is-in");
        else mirón.observe(el);
      });
    };

    if (document.fonts && document.fonts.ready) document.fonts.ready.then(armar);
    else armar();

    var reloj;
    addEventListener("resize", function () {
      clearTimeout(reloj);
      reloj = setTimeout(function () {
        revelables.forEach(function (el) { el.classList.remove("is-in"); });
        armar();
      }, 250);
    });
  }

})();

/* ---- carrusel del header del home ----------------------------------- */
(function () {
  var fotos = document.querySelectorAll(".hero-img");
  if (fotos.length < 2) return;
  var pie = document.querySelector(".hero-caption");
  var prev = document.querySelector(".hero-flecha--prev");
  var sig = document.querySelector(".hero-flecha--next");
  var puntos = document.querySelectorAll(".hero-punto");
  var i = 0;

  function mostrar(n) {
    i = (n + fotos.length) % fotos.length;
    for (var k = 0; k < fotos.length; k++) {
      fotos[k].classList.toggle("is-activa", k === i);
      fotos[k].setAttribute("aria-hidden", k === i ? "false" : "true");
    }
    for (var j = 0; j < puntos.length; j++) {
      puntos[j].classList.toggle("is-activo", j === i);
      puntos[j].setAttribute("aria-selected", j === i ? "true" : "false");
    }
    if (pie && fotos[i].dataset.pie) pie.textContent = fotos[i].dataset.pie;
  }

  if (prev) prev.addEventListener("click", function () { mostrar(i - 1); });
  if (sig) sig.addEventListener("click", function () { mostrar(i + 1); });

  for (var p = 0; p < puntos.length; p++) {
    (function (n) {
      puntos[n].addEventListener("click", function () { mostrar(n); });
    })(p);
  }

  // flechas del teclado, solo mientras el header está a la vista
  document.addEventListener("keydown", function (e) {
    if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
    var h = document.querySelector(".hero");
    if (!h || h.getBoundingClientRect().bottom < 120) return;
    mostrar(e.key === "ArrowLeft" ? i - 1 : i + 1);
  });

  mostrar(0);
})();
