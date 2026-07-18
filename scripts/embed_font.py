#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SVG 안의 <text>에 쓰인 글자만 Pretendard에서 서브셋해 @font-face(base64)로 임베드한다.
   결과 SVG는 웹(img)·sharp 래스터라이즈 어디서나 Pretendard로 렌더된다.

   usage: python scripts/embed_font.py <in.svg> <out.svg>

   준비물(최초 1회, scripts/fonts/ 는 gitignore):
     pip install fonttools brotli
     for w in Bold ExtraBold SemiBold; do
       curl -sL -o scripts/fonts/Pretendard-$w.woff2 \
         "https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/woff2/Pretendard-$w.woff2"
     done
"""
import sys, re, io, base64
from fontTools import subset
from fontTools.ttLib import TTFont

FONT_DIR = __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0] + "/fonts"
WEIGHTS = {  # css weight -> woff2 파일
    600: "Pretendard-SemiBold.woff2",
    700: "Pretendard-Bold.woff2",
    800: "Pretendard-ExtraBold.woff2",
}
# 항상 포함할 기본 글자 (숫자·영문·기호·단위)
BASE = set(" .,·:/%~–—()°C℃±+-×#0123456789"
           "abcdefghijklmnopqrstuvwxyz"
           "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
           "babyskinlab.com")

def collect_chars(svg_text):
    chars = set(BASE)
    for m in re.findall(r"<text[^>]*>(.*?)</text>", svg_text, re.S):
        # 태그 제거
        t = re.sub(r"<[^>]+>", "", m)
        chars.update(t)
    chars.discard("\n"); chars.discard("\t")
    return chars

def subset_b64(font_path, unicodes):
    font = TTFont(font_path)
    opt = subset.Options()
    opt.flavor = "woff2"
    opt.desubroutinize = True
    opt.layout_features = ["*"]
    opt.name_IDs = []
    opt.notdef_outline = True
    opt.recalc_bounds = True
    sub = subset.Subsetter(options=opt)
    sub.populate(unicodes=[ord(c) for c in unicodes])
    sub.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode("ascii")

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, "r", encoding="utf-8") as f:
        svg = f.read()
    chars = collect_chars(svg)
    faces = []
    for weight, fname in WEIGHTS.items():
        b64 = subset_b64(FONT_DIR + "/" + fname, chars)
        faces.append(
            "@font-face{font-family:'Pretendard';font-style:normal;"
            f"font-weight:{weight};font-display:block;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
    style = "<style>" + "".join(faces) + "</style>"
    # 첫 <svg ...> 여는 태그 바로 뒤에 삽입
    out = re.sub(r"(<svg\b[^>]*>)", r"\1" + style, svg, count=1)
    with open(outp, "w", encoding="utf-8") as f:
        f.write(out)
    total_kb = len(out.encode("utf-8")) / 1024
    print(f"[embed] {inp} -> {outp}  ({len(chars)} glyphs, {total_kb:.0f}KB)")

if __name__ == "__main__":
    main()
