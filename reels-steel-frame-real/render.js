// Renderiza index.html em quadros PNG e exporta os tempos de impacto (para o áudio).
// Uso: node render.js <pasta_de_quadros> [fps]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const out = process.argv[2], fps = +(process.argv[3] || 30);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'index.html') + '?render=1');
  await p.evaluate(() => window.READY);
  const info = await p.evaluate(() => ({ dur: DUR, hits: ITEMS.map(i => [i.t0 + i.dur, i.kind]) }));
  fs.writeFileSync(path.join(out, 'hits.json'), JSON.stringify(info));
  const canvas = await p.$('canvas');
  const n = Math.round(info.dur * fps);
  for (let f = 0; f < n; f++) {
    await p.evaluate(t => renderFrame(t), f / fps);
    await canvas.screenshot({ path: path.join(out, `f${String(f).padStart(4, '0')}.png`) });
  }
  await b.close();
})();
