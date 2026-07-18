import sharp from 'sharp';
const [inp, outp, w, h] = process.argv.slice(2);
const buf = await sharp(inp, { density: 300 })
  .resize(parseInt(w), parseInt(h), { fit: 'fill' })
  .png()
  .toBuffer();
const fs = await import('node:fs');
fs.writeFileSync(outp, buf);
console.log(`[png] ${outp} ${w}x${h} ${(buf.length/1024).toFixed(0)}KB`);
