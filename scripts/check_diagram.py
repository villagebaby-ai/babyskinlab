#!/usr/bin/env python3
"""다이어그램 모바일 검증 (IMAGE_GUIDE v2 규격).

usage: python scripts/check_diagram.py {slug}
       python scripts/check_diagram.py --all
"""
import glob
import re
import sys

MOBILE_SCALE = 327 / 1200  # 모바일 figure 폭 327px 기준
MIN_FONT = 36              # viewBox 기준 하한
MIN_PX = 10.0              # 모바일 실제 픽셀 하한
MAX_WORDS = 15
WATERMARK = 'babyskinlab.com'


def check(path):
    with open(path, 'r', encoding='utf-8') as f:
        svg = f.read()

    texts = re.findall(r'<text[^>]*font-size="(\d+)"[^>]*>([^<]*)</text>', svg)
    if not texts:
        return False, ['<text> 요소를 찾지 못했습니다 (font-size 속성 순서 확인)']

    problems = []
    words = 0
    for fs_raw, content in texts:
        fs = int(fs_raw)
        content = content.strip()
        if content == WATERMARK:
            continue
        px = fs * MOBILE_SCALE
        if fs < MIN_FONT or px < MIN_PX:
            problems.append(f'폰트 미달: "{content}" {fs}px → 모바일 {px:.1f}px (하한 {MIN_FONT}px / {MIN_PX}px)')
        # 숫자만 있는 건 단어로 세지 않음
        if not re.fullmatch(r'[\d.%]+', content):
            words += len(content.split())

    if words > MAX_WORDS:
        problems.append(f'단어 과다: {words}개 (상한 {MAX_WORDS}개) — 텍스트를 줄이고 도형으로 표현하세요')

    if '<title>' in svg or re.search(r'font-size="(8[0-9]|9[0-9]|1[0-9]{2})"[^>]*>[가-힣]{6,}', svg):
        problems.append('SVG 안에 제목·문장이 있는 것으로 보입니다 — 제목은 figcaption의 몫입니다')

    return len(problems) == 0, problems


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # 소스는 img-src (폰트 임베드 전 클린 SVG). 하위호환으로 public/diagrams도 탐색.
    arg = sys.argv[1]
    if arg == '--all':
        paths = sorted(glob.glob('img-src/*-[12].svg')) or sorted(glob.glob('public/diagrams/*.svg'))
    else:
        paths = sorted(glob.glob(f'img-src/{arg}-[12].svg')) or sorted(glob.glob(f'public/diagrams/{arg}-*.svg'))

    if not paths:
        print(f'대상 파일 없음: {arg}')
        sys.exit(1)

    all_ok = True
    for p in paths:
        ok, problems = check(p)
        name = p.replace('\\', '/').split('/')[-1]
        if ok:
            print(f'PASS  {name}')
        else:
            all_ok = False
            print(f'FAIL  {name}')
            for pr in problems:
                print(f'      - {pr}')

    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()
