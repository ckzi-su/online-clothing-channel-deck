(function () {
  const slides = Array.from(document.querySelectorAll(".slide"));
  const page = document.getElementById("page");
  const themeButtons = Array.from(document.querySelectorAll("[data-theme-set]"));
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const hasAnime = typeof window.anime !== "undefined";
  let current = 0;

  function fit() {
    const scale = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    document.documentElement.style.setProperty("--scale", String(scale));
  }

  function byId(id) {
    return document.getElementById(id);
  }

  function scope(id, selector) {
    const root = byId(id);
    return root ? Array.from(root.querySelectorAll(selector)) : [];
  }

  function animateCounter(element, target, decimals, delay) {
    if (!element) return;
    const proxy = { value: 0 };
    anime({
      targets: proxy,
      value: target,
      duration: 1100,
      delay: delay || 0,
      easing: "easeOutQuart",
      update: function () {
        element.textContent = proxy.value.toFixed(decimals) + "%";
      }
    });
  }

  function drawLine(id, delay) {
    const line = byId(id);
    if (!line) return 0;
    const length = line.getTotalLength();
    line.style.strokeDasharray = String(length);
    line.style.strokeDashoffset = String(length);
    anime({
      targets: line,
      strokeDashoffset: [length, 0],
      duration: 1400,
      delay: delay || 0,
      easing: "easeInOutQuart"
    });
    return length;
  }

  function hideLine(id) {
    const line = byId(id);
    if (!line) return;
    const length = line.getTotalLength();
    line.style.strokeDasharray = String(length);
    line.style.strokeDashoffset = String(length);
  }

  const init = {
    S00: function () {
      anime.set(["#coverTitle", "#coverLead", "#coverMeta", ".cover-foot"], {
        opacity: 0,
        translateY: 22
      });
    },
    S01: function () {
      anime.set(scope("S01", ".rank-bar"), { scaleX: 0 });
    },
    S02: function () {
      anime.set(scope("S02", ".caution-card"), { opacity: 0, translateY: 18 });
      anime.set(scope("S02", ".method-banner"), { opacity: 0, translateY: 10 });
    },
    S03: function () {
      hideLine("trendLine");
      anime.set("#trendArea", { opacity: 0 });
      anime.set(".trend-dot", { opacity: 0, scale: 0 });
      anime.set("#trendCallout", { opacity: 0, translateY: 8 });
      const counter = byId("trendCounter");
      if (counter) counter.textContent = "0.00%";
    },
    S04: function () {
      hideLine("onlineLine");
      hideLine("omniLine");
      anime.set(".dot-a, .dot-b", { opacity: 0, scale: 0 });
      anime.set("#slopeLabels text", { opacity: 0 });
      const online = byId("onlineCounter");
      const omni = byId("omniCounter");
      if (online) online.textContent = "0.00%";
      if (omni) omni.textContent = "0.00%";
      const fill = byId("shareFill");
      if (fill) fill.style.width = "42.42%";
    },
    S05: function () {
      anime.set(scope("S05", ".share-omni"), { scaleY: 0 });
      anime.set(scope("S05", ".share-value, .share-month"), { opacity: 0 });
    },
    S06: function () {
      anime.set(scope("S06", ".side-stack .mini-stat, .side-stack .beginner"), {
        opacity: 0,
        translateY: 14
      });
    },
    S07: function () {
      anime.set(scope("S07", ".contrib-seg"), { scaleX: 0 });
      anime.set(scope("S07", ".contrib-legend"), { opacity: 0 });
    },
    S08: function () {
      const image = byId("categoryChart");
      if (image) image.style.clipPath = "inset(0 100% 0 0)";
      anime.set("#categoryCallout", { opacity: 0, translateY: 8 });
    },
    S09: function () {
      anime.set(scope("S09", ".scatter-dot, .scatter-fashion"), { scale: 0, opacity: 0 });
      anime.set(scope("S09", ".scatter-label"), { opacity: 0 });
      anime.set(scope("S09", ".scatter-avg"), { opacity: 0 });
    },
    S10: function () {
      anime.set(scope("S10", ".caution-card"), { opacity: 0, translateY: 18 });
      anime.set(scope("S10", ".hypothesis-note"), { opacity: 0, translateY: 8 });
    },
    S11: function () {
      anime.set(scope("S11", ".journey-step"), { opacity: 0, translateY: 18 });
      anime.set(scope("S11", ".journey-arrow"), { opacity: 0 });
      anime.set(scope("S11", ".hypothesis-note"), { opacity: 0, translateY: 8 });
    },
    S12: function () {
      anime.set(scope("S12", ".trust-node"), { opacity: 0, scale: 0.94 });
      anime.set(scope("S12", ".trust-arrow"), { opacity: 0 });
      anime.set(scope("S12", ".hypothesis-note"), { opacity: 0, translateY: 8 });
    },
    S13: function () {
      anime.set(scope("S13", ".versus-card"), { opacity: 0, translateY: 18 });
      anime.set(scope("S13", ".hypothesis-note"), { opacity: 0, translateY: 8 });
    },
    S14: function () {
      anime.set(scope("S14", ".caution-card"), { opacity: 0, translateY: 18 });
      anime.set(scope("S14", ".hypothesis-note"), { opacity: 0, translateY: 8 });
    },
    S15: function () {
      anime.set(scope("S15", ".caution-card"), { opacity: 0, translateY: 18 });
      anime.set(scope("S15", ".closing"), { opacity: 0, translateY: 10 });
    },
    S16: function () {
      anime.set(scope("S16", ".takeaway"), { opacity: 0, translateY: 18 });
      anime.set(scope("S16", ".closing"), { opacity: 0, translateY: 10 });
    },
    S17: function () {
      anime.set(scope("S17", ".ref-item, .ref-note, .qna"), { opacity: 0, translateY: 10 });
    }
  };

  const play = {
    S00: function () {
      anime.timeline({ easing: "easeOutExpo" })
        .add({ targets: "#coverTitle", opacity: [0, 1], translateY: [22, 0], duration: 750 })
        .add({ targets: "#coverLead", opacity: [0, 1], translateY: [22, 0], duration: 650 }, "-=520")
        .add({ targets: "#coverMeta", opacity: [0, 1], translateY: [22, 0], duration: 550 }, "-=420")
        .add({ targets: ".cover-foot", opacity: [0, 1], translateY: [22, 0], duration: 500 }, "-=380");
    },
    S01: function () {
      anime({
        targets: scope("S01", ".rank-bar"),
        scaleX: [0, 1],
        delay: anime.stagger(80, { start: 120 }),
        duration: 700,
        easing: "easeOutQuart"
      });
    },
    S02: function () {
      anime({
        targets: scope("S02", ".caution-card"),
        opacity: [0, 1],
        translateY: [18, 0],
        delay: anime.stagger(110, { start: 100 }),
        duration: 600,
        easing: "easeOutExpo"
      });
      anime({
        targets: scope("S02", ".method-banner"),
        opacity: [0, 1],
        translateY: [10, 0],
        delay: 520,
        duration: 520
      });
    },
    S03: function () {
      drawLine("trendLine");
      anime({ targets: "#trendArea", opacity: [0, 0.12], duration: 900, delay: 350, easing: "easeOutQuad" });
      anime({
        targets: ".trend-dot",
        scale: [0, 1],
        opacity: [0, 1],
        delay: anime.stagger(105, { start: 620 }),
        duration: 420,
        easing: "easeOutBack"
      });
      animateCounter(byId("trendCounter"), -34.38, 2, 500);
      anime({ targets: "#trendCallout", opacity: [0, 1], translateY: [8, 0], delay: 1100, duration: 420 });
    },
    S04: function () {
      drawLine("onlineLine", 0);
      drawLine("omniLine", 130);
      anime({
        targets: ".dot-a, .dot-b",
        scale: [0, 1],
        opacity: [0, 1],
        delay: anime.stagger(75, { start: 650 }),
        duration: 380,
        easing: "easeOutBack"
      });
      anime({
        targets: "#slopeLabels text",
        opacity: [0, 1],
        translateY: [6, 0],
        delay: anime.stagger(120, { start: 1050 }),
        duration: 400
      });
      animateCounter(byId("onlineCounter"), -37.94, 2, 550);
      animateCounter(byId("omniCounter"), -29.53, 2, 750);
      anime({
        targets: "#shareFill",
        width: ["42.42%", "45.55%"],
        duration: 1200,
        delay: 900,
        easing: "easeOutQuart"
      });
    },
    S05: function () {
      anime({
        targets: scope("S05", ".share-omni"),
        scaleY: [0, 1],
        delay: anime.stagger(110, { start: 180 }),
        duration: 760,
        easing: "easeOutQuart"
      });
      anime({
        targets: scope("S05", ".share-value, .share-month"),
        opacity: [0, 1],
        translateY: [6, 0],
        delay: anime.stagger(60, { start: 300 }),
        duration: 420
      });
    },
    S06: function () {
      anime({
        targets: scope("S06", ".side-stack .mini-stat, .side-stack .beginner"),
        opacity: [0, 1],
        translateY: [14, 0],
        delay: anime.stagger(110, { start: 150 }),
        duration: 520,
        easing: "easeOutExpo"
      });
      const video = byId("phaseVideo");
      if (video && !reduceMotion) {
        video.currentTime = 0;
        const promise = video.play();
        if (promise && promise.catch) promise.catch(function () {});
      }
    },
    S07: function () {
      anime({
        targets: scope("S07", ".contrib-seg.a"),
        scaleX: [0, 1],
        duration: 760,
        delay: 150,
        easing: "easeOutQuart"
      });
      anime({
        targets: scope("S07", ".contrib-seg.b"),
        scaleX: [0, 1],
        duration: 560,
        delay: 760,
        easing: "easeOutQuart"
      });
      anime({
        targets: scope("S07", ".contrib-legend"),
        opacity: [0, 1],
        translateY: [8, 0],
        delay: 900,
        duration: 420
      });
    },
    S08: function () {
      const image = byId("categoryChart");
      if (image) {
        anime({
          targets: image,
          clipPath: ["inset(0 100% 0 0)", "inset(0 0% 0 0)"],
          duration: 1350,
          easing: "easeInOutQuart"
        });
      }
      anime({ targets: "#categoryCallout", opacity: [0, 1], translateY: [8, 0], delay: 950, duration: 420 });
    },
    S09: function () {
      anime({
        targets: scope("S09", ".scatter-dot, .scatter-fashion"),
        scale: [0, 1],
        opacity: function (el) {
          return el.classList.contains("scatter-fashion") ? 1 : 0.32;
        },
        delay: anime.stagger(80, { start: 250 }),
        duration: 560,
        easing: "easeOutBack"
      });
      anime({
        targets: scope("S09", ".scatter-label"),
        opacity: [0, 1],
        translateY: [5, 0],
        delay: anime.stagger(60, { start: 800 }),
        duration: 380
      });
      anime({ targets: scope("S09", ".scatter-avg"), opacity: [0, 0.45], duration: 600, delay: 100 });
    },
    S10: function () {
      anime({
        targets: scope("S10", ".caution-card"),
        opacity: [0, 1],
        translateY: [18, 0],
        delay: anime.stagger(110, { start: 100 }),
        duration: 620,
        easing: "easeOutExpo"
      });
      anime({ targets: scope("S10", ".hypothesis-note"), opacity: [0, 1], translateY: [8, 0], delay: 640, duration: 420 });
    },
    S11: function () {
      anime({
        targets: scope("S11", ".journey-step"),
        opacity: [0, 1],
        translateY: [18, 0],
        delay: anime.stagger(100, { start: 100 }),
        duration: 600,
        easing: "easeOutExpo"
      });
      anime({ targets: scope("S11", ".journey-arrow"), opacity: [0, 1], delay: anime.stagger(100, { start: 220 }), duration: 300 });
      anime({ targets: scope("S11", ".hypothesis-note"), opacity: [0, 1], translateY: [8, 0], delay: 700, duration: 420 });
    },
    S12: function () {
      anime({
        targets: scope("S12", ".trust-node"),
        opacity: [0, 1],
        scale: [0.94, 1],
        delay: anime.stagger(130, { start: 100 }),
        duration: 620,
        easing: "easeOutBack"
      });
      anime({ targets: scope("S12", ".trust-arrow"), opacity: [0, 1], delay: anime.stagger(130, { start: 240 }), duration: 300 });
      anime({ targets: scope("S12", ".hypothesis-note"), opacity: [0, 1], translateY: [8, 0], delay: 720, duration: 420 });
    },
    S13: function () {
      anime({
        targets: scope("S13", ".versus-card"),
        opacity: [0, 1],
        translateY: [18, 0],
        delay: anime.stagger(120, { start: 100 }),
        duration: 620,
        easing: "easeOutExpo"
      });
      anime({ targets: scope("S13", ".hypothesis-note"), opacity: [0, 1], translateY: [8, 0], delay: 640, duration: 420 });
    },
    S14: function () {
      anime({
        targets: scope("S14", ".caution-card"),
        opacity: [0, 1],
        translateY: [18, 0],
        delay: anime.stagger(120, { start: 130 }),
        duration: 620,
        easing: "easeOutExpo"
      });
      anime({ targets: scope("S14", ".hypothesis-note"), opacity: [0, 1], translateY: [8, 0], delay: 700, duration: 420 });
    },
    S15: function () {
      anime({
        targets: scope("S15", ".caution-card"),
        opacity: [0, 1],
        translateY: [18, 0],
        delay: anime.stagger(120, { start: 100 }),
        duration: 620,
        easing: "easeOutExpo"
      });
      anime({ targets: scope("S15", ".closing"), opacity: [0, 1], translateY: [10, 0], delay: 600, duration: 520 });
    },
    S16: function () {
      anime({
        targets: scope("S16", ".takeaway"),
        opacity: [0, 1],
        translateY: [18, 0],
        delay: anime.stagger(120, { start: 100 }),
        duration: 620,
        easing: "easeOutExpo"
      });
      anime({ targets: scope("S16", ".closing"), opacity: [0, 1], translateY: [10, 0], delay: 640, duration: 520 });
    },
    S17: function () {
      anime({
        targets: scope("S17", ".ref-item"),
        opacity: [0, 1],
        translateY: [10, 0],
        delay: anime.stagger(120, { start: 100 }),
        duration: 520
      });
      anime({
        targets: scope("S17", ".ref-note, .qna"),
        opacity: [0, 1],
        translateY: [10, 0],
        delay: anime.stagger(140, { start: 450 }),
        duration: 520
      });
    }
  };

  function pauseVideo() {
    const video = byId("phaseVideo");
    if (video) video.pause();
  }

  function prepare(slide) {
    if (!hasAnime || reduceMotion) return;
    const id = slide.id;
    if (init[id]) init[id]();
  }

  function run(slide) {
    if (!hasAnime || reduceMotion) return;
    const id = slide.id;
    if (play[id]) play[id]();
  }

  function go(index, updateHash) {
    const next = Math.max(0, Math.min(slides.length - 1, index));
    pauseVideo();
    slides.forEach(function (slide, i) {
      slide.classList.toggle("active", i === next);
    });
    current = next;
    const slide = slides[current];
    page.textContent = current + 1 + " / " + slides.length;
    if (updateHash !== false) {
      history.replaceState(null, "", "#" + slide.id);
    }
    prepare(slide);
    window.setTimeout(function () {
      if (slides[current] === slide) run(slide);
    }, 70);
  }

  function replay() {
    const slide = slides[current];
    prepare(slide);
    window.setTimeout(function () {
      if (slides[current] === slide) run(slide);
    }, 40);
  }

  function setTheme(theme) {
    document.body.dataset.theme = theme;
    themeButtons.forEach(function (button) {
      const active = button.dataset.themeSet === theme;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    const chart = byId("categoryChart");
    if (chart) chart.src = "assets/charts/category_omni_" + theme + ".svg";
    const video = byId("phaseVideo");
    if (video) {
      const suffix = theme === "ppt" ? "_ppt" : "";
      const nextSrc = "assets/video/phase_reversal" + suffix + ".mp4";
      const nextPoster = "assets/video/phase_poster" + suffix + ".png";
      if (video.getAttribute("src") !== nextSrc) {
        video.pause();
        video.setAttribute("src", nextSrc);
        video.setAttribute("poster", nextPoster);
        video.load();
      }
    }
    try {
      localStorage.setItem("deck-theme", theme);
    } catch (error) {
      /* ignore storage errors */
    }
    replay();
  }

  function initialTheme() {
    const params = new URLSearchParams(window.location.search);
    const requested = params.get("theme");
    if (requested === "figma" || requested === "ppt") return requested;
    try {
      const stored = localStorage.getItem("deck-theme");
      if (stored === "figma" || stored === "ppt") return stored;
    } catch (error) {
      /* ignore storage errors */
    }
    return "figma";
  }

  themeButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      setTheme(button.dataset.themeSet);
    });
  });

  document.getElementById("replayBtn").addEventListener("click", replay);

  document.addEventListener("keydown", function (event) {
    if (event.key === "ArrowRight" || event.key === "PageDown" || event.key === " ") {
      event.preventDefault();
      go(current + 1);
    } else if (event.key === "ArrowLeft" || event.key === "PageUp") {
      event.preventDefault();
      go(current - 1);
    } else if (event.key === "Home") {
      event.preventDefault();
      go(0);
    } else if (event.key === "End") {
      event.preventDefault();
      go(slides.length - 1);
    } else if (event.key.toLowerCase() === "t") {
      const next = document.body.dataset.theme === "figma" ? "ppt" : "figma";
      setTheme(next);
    } else if (event.key.toLowerCase() === "r") {
      replay();
    }
  });

  window.addEventListener("resize", fit);
  fit();
  setTheme(initialTheme());

  const hash = window.location.hash.replace("#", "");
  const found = slides.findIndex(function (slide) {
    return slide.id === hash;
  });
  go(found >= 0 ? found : 0, false);
})();
