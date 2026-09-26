// Render the tracker HTML to an A4 PDF and a side-by-side PNG preview, and check nothing overflows.
// Usage: NODE_PATH=$(npm root -g) node render.js tracker.html out.pdf preview.png
const path = require('path');
const { chromium } = require(path.join(process.env.NODE_PATH || '', 'playwright'));
const [src, pdf, png] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto('file://' + path.resolve(src));
  await p.evaluate(() => document.fonts.ready);
  const gaps = await p.evaluate(() => [...document.querySelectorAll('.page')].map(pg =>
    Math.round(pg.getBoundingClientRect().bottom - pg.querySelector('.foot').getBoundingClientRect().bottom)));
  const bad = gaps.map((g, i) => [i + 1, g]).filter(([, g]) => g < 30);
  if (bad.length) console.log('OVERFLOW on pages', bad.map(x => x[0]).join(', '), '- shorten the first move or next moves');
  await p.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
  if (png) {
    await p.setViewportSize({ width: 794 * gaps.length, height: 1123 });
    await p.addStyleTag({ content: 'body{display:flex}.page{flex:none}' });
    await p.screenshot({ path: png });
  }
  console.log('pages', gaps.length, bad.length ? 'CHECK LAYOUT' : 'ok');
  await b.close();
})();
