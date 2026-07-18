#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""img-src/*.svg → 배포 이미지 생성
   - {slug}-1.svg, {slug}-2.svg (다이어그램): Pretendard 임베드 → public/diagrams/
   - {slug}-hero.svg           (대표 이미지): Pretendard 임베드 → PNG → public/og/{slug}.png (1200x630)

   usage: python scripts/build_images.py
"""
import os, sys, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "img-src")
DIAG = os.path.join(ROOT, "public", "diagrams")
OG = os.path.join(ROOT, "public", "og")
EMBED = os.path.join(ROOT, "scripts", "embed_font.py")
RASTER = os.path.join(ROOT, "scripts", "svg_to_png.mjs")

os.makedirs(DIAG, exist_ok=True)
os.makedirs(OG, exist_ok=True)

def run(cmd):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    if r.returncode != 0:
        print("ERROR:", " ".join(cmd)); print(r.stdout); print(r.stderr); sys.exit(1)
    return (r.stdout or "").strip()

def main():
    files = sorted(f for f in os.listdir(SRC) if f.endswith(".svg"))
    for f in files:
        src = os.path.join(SRC, f)
        if f.endswith("-hero.svg"):
            slug = f[:-len("-hero.svg")]
            tmp = os.path.join(tempfile.gettempdir(), f)
            print(run([sys.executable, EMBED, src, tmp]))
            out = os.path.join(OG, f"{slug}.png")
            print(run(["node", RASTER, tmp, out, "1200", "630"]))
        else:
            out = os.path.join(DIAG, f)
            print(run([sys.executable, EMBED, src, out]))
    print("done.")

if __name__ == "__main__":
    main()
