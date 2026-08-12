/* ============================================================
   Pixel Cafe Scene — embeddable canvas animation
   Two coders facing each other at a table, laptops, coffee, cat.

   USAGE in your existing template:
   1. Add a container element:
        <div id="pixel-cafe" style="width:480px;"></div>

   2. Include this script (as a module or regular script):
        <script src="pixel-cafe-scene.js"></script>

   3. Initialize it:
        PixelCafeScene.init('pixel-cafe');

      Optional second arg for sizing/options:
        PixelCafeScene.init('pixel-cafe', { width: 480, scale: 3 });
   ============================================================ */

(function (global) {
  const PAL = {
    bg1: '#2a1f33', bg2: '#231a2b',
    floor: '#3a2a40',
    table: '#6b4226', tableTop: '#7d4f30', tableLeg: '#4a2e16',
    laptopBody: '#cfcfcf', laptopScreen: '#7ee8c4', laptopDark: '#2b2b2b',
    skin1: '#e8b48a', skin2: '#a9714f',
    hair1: '#3b2a20', hair2: '#caa472',
    shirt1: '#e76f51', shirt2: '#457b9d',
    cupBody: '#fdfdfd', coffee: '#6f4518', steam: 'rgba(255,255,255,0.55)',
    cat: '#d9a066', catEye: '#111111',
    star: '#fff7d6'
  };

  function lerp(a, b, f) { return a + (b - a) * f; }

  function createScene(canvas, opts) {
    const ctx = canvas.getContext('2d');
    ctx.imageSmoothingEnabled = false;

    const W = 200, H = 120; // internal pixel-art resolution
    canvas.width = W;
    canvas.height = H;

    function px(x, y, w, h, color) {
      ctx.fillStyle = color;
      ctx.fillRect(Math.round(x), Math.round(y), w, h);
    }

    function drawBackground(t) {
      for (let y = 0; y < H; y++) {
        const f = y / H;
        const r = lerp(42, 26, f), g = lerp(31, 20, f), b = lerp(51, 32, f);
        ctx.fillStyle = `rgb(${r},${g},${b})`;
        ctx.fillRect(0, y, W, 1);
      }
      // stars
      for (let i = 0; i < 10; i++) {
        const sx = (i * 41) % W;
        const sy = (i * 17) % 30 + 3;
        const tw = 0.5 + 0.5 * Math.sin(t / 400 + i);
        ctx.globalAlpha = 0.3 + 0.5 * tw;
        px(sx, sy, 1, 1, PAL.star);
        ctx.globalAlpha = 1;
      }
      // floor
      px(0, H - 28, W, 28, PAL.floor);
      for (let x = 0; x < W; x += 14) px(x, H - 28, 1, 28, 'rgba(0,0,0,0.12)');
    }

    function drawTable(cx, y) {
      // round-ish table seen from the side, centered at cx
      px(cx - 34, y, 68, 6, PAL.tableTop);
      px(cx - 34, y + 6, 68, 4, PAL.table);
      px(cx - 30, y + 10, 4, 14, PAL.tableLeg);
      px(cx + 26, y + 10, 4, 14, PAL.tableLeg);
    }

    function drawLaptop(x, y, t, idx, facingRight) {
      px(x, y, 22, 3, PAL.laptopBody);
      const bob = Math.sin(t / 500 + idx) * 0.5;
      px(x + 2, y - 14 + bob, 18, 14, PAL.laptopDark);
      px(x + 3, y - 13 + bob, 16, 12, PAL.laptopScreen);
      ctx.globalAlpha = 0.5 + 0.3 * Math.sin(t / 150 + idx);
      px(x + 5, y - 10 + bob, 8, 1, '#0e3b2e');
      px(x + 5, y - 7 + bob, 11, 1, '#0e3b2e');
      ctx.globalAlpha = 1;
    }

    // person sitting, can face left or right (mirrors arm placement)
    function drawPerson(x, y, skin, hair, shirt, t, idx, typing, faceRight) {
      const typeOff = typing ? (Math.sin(t / 120 + idx * 2) > 0 ? 0 : 1) : 0;
      const dir = faceRight ? 1 : -1;

      px(x - 6, y - 2, 12, 12, shirt); // torso
      px(x - 8, y - 2, 2, 9, shirt);   // back arm
      px(x + 6, y - 2, 2, 9, shirt);   // front arm
      px(x - 7 * dir + (faceRight ? 5 : -7), y + 5, 3, 4, skin); // back hand
      px(x + (faceRight ? -1 : -1), y + 5 - typeOff, 3, 4, skin); // front hand (typing)

      // head
      px(x - 5, y - 12, 10, 10, skin);
      // hair
      px(x - 6, y - 14, 12, 4, hair);
      px(x - 6, y - 10, 2, 6, hair);
      px(x + 4, y - 10, 2, 6, hair);
      // face dot
      const eyeX = faceRight ? x : x - 2;
      px(eyeX, y - 8, 1, 1, '#2b2b2b');
    }

    function drawCup(x, y, t, phase) {
      px(x, y, 7, 6, PAL.cupBody);
      px(x + 1, y + 1, 5, 3, PAL.coffee);
      px(x + 7, y + 2, 2, 2, PAL.cupBody);
      for (let i = 0; i < 3; i++) {
        const cycle = (t / 30 + i * 20 + phase) % 26;
        const sy = y - 2 - cycle;
        const sx = x + 2 + i * 1.3 + Math.sin(t / 200 + i + phase) * 1.5;
        const alpha = 1 - cycle / 26;
        ctx.globalAlpha = Math.max(0, alpha * 0.6);
        px(sx, sy, 1, 2, PAL.steam);
        ctx.globalAlpha = 1;
      }
    }

    function drawCat(x, y, t, idx) {
      const tailWag = Math.sin(t / 250 + idx) * 1.6;
      px(x, y, 10, 5, PAL.cat);
      px(x - 2, y + 1, 3, 3, PAL.cat);
      px(x + 8, y - 3, 5, 5, PAL.cat);
      px(x + 8, y - 5, 2, 2, PAL.cat);
      px(x + 11, y - 5, 2, 2, PAL.cat);
      px(x - 3 + tailWag * 0.3, y - 1 + tailWag, 3, 3, PAL.cat);
      const blink = Math.sin(t / 700 + idx) > 0.85;
      if (!blink) {
        px(x + 10, y - 1, 1, 1, PAL.catEye);
        px(x + 12, y - 1, 1, 1, PAL.catEye);
      }
      const breathe = Math.sin(t / 400 + idx) * 0.5;
      px(x + 1, y + breathe, 6, 1, PAL.cat);
    }

    function draw(t) {
      ctx.clearRect(0, 0, W, H);

      const tableY = 70;
      const cx = W / 2;
      drawTable(cx, tableY);

      // left person, facing right (toward the table/other person)
      drawLaptop(cx - 30, tableY - 4, t, 0, true);
      drawPerson(cx - 30, tableY + 4, PAL.skin1, PAL.hair1, PAL.shirt1, t, 0, true, true);
      drawCup(cx - 44, tableY - 2, t, 0);

      // right person, facing left
      drawLaptop(cx + 8, tableY - 4, t, 1, false);
      drawPerson(cx + 30, tableY + 4, PAL.skin2, PAL.hair2, PAL.shirt2, t, 1, false, false);
      drawCup(cx + 38, tableY - 2, t, 9);

      // cat lounging under/beside the table
      drawCat(cx - 6, tableY + 24, t, 0);
    }

    let raf = null;
    let start = null;
    function loop(ts) {
      if (!start) start = ts;
      draw(ts - start);
      raf = requestAnimationFrame(loop);
    }
    raf = requestAnimationFrame(loop);

    return {
      stop() { if (raf) cancelAnimationFrame(raf); }
    };
  }

  function init(containerId, opts) {
    opts = opts || {};
    const container = typeof containerId === 'string'
      ? document.getElementById(containerId)
      : containerId;
    if (!container) {
      console.error('PixelCafeScene: container not found:', containerId);
      return null;
    }

    const canvas = document.createElement('canvas');
    canvas.style.width = (opts.width || '100%');
    canvas.style.height = 'auto';
    canvas.style.imageRendering = 'pixelated';
    canvas.style.display = 'block';
    canvas.style.borderRadius = opts.borderRadius || '8px';
    container.innerHTML = '';
    container.appendChild(canvas);

    return createScene(canvas, opts);
  }

  global.PixelCafeScene = { init };
})(window);
