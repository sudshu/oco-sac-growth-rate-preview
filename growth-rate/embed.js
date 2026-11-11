/* OCO-SAC CO2 growth-rate dashboard: the script for a page that embeds it (decision 104).
   Put the dashboard in an iframe with the data-oco-sac-embed attribute, then this script once anywhere on the page:

     <iframe src="https://DASHBOARD-HOST/growth-rate/?embed=1" data-oco-sac-embed
             title="Whole-atmosphere CO2 growth rate from satellite observations"
             style="display:block;width:100%;height:2400px;border:0"></iframe>
     <script src="https://DASHBOARD-HOST/growth-rate/embed.js"></script>

   It sizes each such iframe to the dashboard's height, again whenever that changes (Methods or a table opened, a new
   width), so the dashboard never scrolls inside its frame. It scrolls this page when a link inside the dashboard points
   further down it, and it tells the dashboard which part of the frame is in view, so the dashboard's picture preview and
   tooltips open there. Optional: data-oco-sac-offset="80" on the iframe if this page has a fixed header 80 px tall.
   It reads nothing from this page but the frame's position and the window's height, and sets only the frame's height
   and this page's scroll position. Messages are checked against the frame's own window and origin. Plain ES5. */
(function () {
  "use strict";
  var FROM = "oco-sac-growth-rate", TO = "oco-sac-growth-rate-host", frames = [];

  function originOf(src) {
    try { return new URL(src, location.href).origin; }
    catch (e) { var a = document.createElement("a"); a.href = src; return a.protocol + "//" + a.host; }
  }
  function offset(f) { return Math.max(0, parseFloat(f.el.getAttribute("data-oco-sac-offset")) || 0); }
  function tell(f) {   // the part of the frame in this window, below a fixed header, in the frame's own coordinates
    var w = f.el.contentWindow; if (!w || !f.live) return;   // not before the dashboard is in the frame
    var r = f.el.getBoundingClientRect(), off = offset(f);
    try {
      w.postMessage({ source: TO, v: 1, type: "viewport", top: off - (r.top + f.el.clientTop),
                      height: (window.innerHeight || document.documentElement.clientHeight) - off }, f.origin);
    } catch (e) {}
  }
  function find() {
    var els = document.querySelectorAll("iframe[data-oco-sac-embed]");
    for (var i = 0; i < els.length; i++) {
      var known = false;
      for (var j = 0; j < frames.length; j++) if (frames[j].el === els[i]) known = true;
      if (known) continue;
      // live: the frame has loaded or spoken (the dashboard repeats its height until this script answers, so a frame
      // that loaded before this script ran is found too)
      var f = { el: els[i], origin: originOf(els[i].getAttribute("src") || ""), live: false };
      frames.push(f);
      els[i].addEventListener("load", (function (f) { return function () { f.origin = originOf(f.el.getAttribute("src") || ""); f.live = true; tell(f); }; })(f));
    }
  }
  function handle(e, d) {
    for (var i = 0; i < frames.length; i++) {
      var f = frames[i];
      if (e.source !== f.el.contentWindow || e.origin !== f.origin) continue;
      f.live = true;
      if (d.type === "height") {
        var h = Math.ceil(+d.height);
        if (h > 0 && h < 200000) f.el.style.height = Math.max(h, 150) + "px";
      } else if (d.type === "scroll") {
        var t = +d.top, r = f.el.getBoundingClientRect();
        if (isFinite(t)) window.scrollTo(0, Math.max(0, (window.pageYOffset || document.documentElement.scrollTop || 0) + r.top + f.el.clientTop + t - offset(f)));
      }
      tell(f);
      return true;
    }
    return false;
  }
  window.addEventListener("message", function (e) {
    var d = e.data;
    if (!d || typeof d !== "object" || d.source !== FROM) return;
    if (!handle(e, d)) { find(); handle(e, d); }   // a frame added after this script ran
  });
  var queued = false;
  function tellAll() { queued = false; for (var i = 0; i < frames.length; i++) tell(frames[i]); }
  function moved() {   // once a frame
    if (queued) return;
    queued = true;
    if (window.requestAnimationFrame) window.requestAnimationFrame(tellAll); else setTimeout(tellAll, 16);
  }
  window.addEventListener("scroll", moved, { passive: true });
  window.addEventListener("resize", moved);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", find); else find();
})();
