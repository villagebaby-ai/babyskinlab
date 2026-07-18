#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""전체 hero 일괄 재생성 (최적화판).
   개별 embed_font는 파일마다 대용량 CJK 폰트 3종을 재서브셋해 느리다.
   여기선 모든 hero의 글자 합집합으로 '1회만' 서브셋 → 모든 SVG에 동일 @font-face 임베드.
   래스터는 embed된 SVG를 그대로 sharp(별도 node)가 처리하도록 /tmp에 남긴다.
"""
import os, re, io, base64, glob
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "img-src")
FONT_DIR = os.path.join(ROOT, "scripts", "fonts")
TMP = os.environ.get("TEMP", "/tmp")
WEIGHTS = {600: "Pretendard-SemiBold.woff2", 700: "Pretendard-Bold.woff2", 800: "Pretendard-ExtraBold.woff2"}
BASE = set(" .,·:/%~–—()°C℃±+-×#0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZbabyskinlab.com")

def collect(svg):
    chars = set()
    for m in re.findall(r"<text[^>]*>(.*?)</text>", svg, re.S):
        chars.update(re.sub(r"<[^>]+>", "", m))
    return chars

def main():
    files = sorted(glob.glob(os.path.join(SRC, "*-hero.svg")))
    union = set(BASE)
    contents = {}
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            svg = fh.read()
        contents[f] = svg
        union |= collect(svg)
    union.discard("\n"); union.discard("\t")

    # 합집합으로 3 weight 1회 서브셋
    faces = []
    for weight, fname in WEIGHTS.items():
        font = TTFont(os.path.join(FONT_DIR, fname))
        opt = subset.Options(); opt.flavor = "woff2"; opt.desubroutinize = True
        opt.layout_features = ["*"]; opt.name_IDs = []
        sub = subset.Subsetter(options=opt)
        sub.populate(unicodes=[ord(c) for c in union])
        sub.subset(font)
        buf = io.BytesIO(); font.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        faces.append(f"@font-face{{font-family:'Pretendard';font-style:normal;font-weight:{weight};"
                     f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    style = "<style>" + "".join(faces) + "</style>"
    print(f"[subset] {len(union)} glyphs (1회, {len(style)//1024}KB)")

    for f, svg in contents.items():
        slug = os.path.basename(f)[:-len("-hero.svg")]
        out = re.sub(r"(<svg\b[^>]*>)", r"\1" + style, svg, count=1)
        with open(os.path.join(TMP, f"emb_{slug}.svg"), "w", encoding="utf-8") as fh:
            fh.write(out)
        print("[emb]", slug)

if __name__ == "__main__":
    main()
