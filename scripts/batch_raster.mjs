import sharp from 'sharp';
import fs from 'node:fs';
import os from 'node:os';
const outDir = process.argv[2];
const tmp = os.tmpdir();
const files = fs.readdirSync(tmp).filter(f=>f.startsWith('emb_')&&f.endsWith('.svg'));
for (const f of files) {
  const slug = f.replace(/^emb_/,'').replace(/\.svg$/,'');
  const buf = await sharp(tmp+'/'+f,{density:200}).resize(1600,840,{fit:'fill'}).png().toBuffer();
  fs.writeFileSync(outDir+'/'+slug+'.png', buf);
  console.log('png', slug, (buf.length/1024).toFixed(0)+'KB');
}
console.log('DONE', files.length);
