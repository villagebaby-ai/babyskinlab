#!/usr/bin/env python3
"""영문 slug → 한글 slug 내부 링크 일괄 치환 (2026-07-15, 색인 전 1회성 마이그레이션)."""
import glob

MAP = {
    '/tools/skin-symptom-checker/': '/tools/아기-피부-증상-진단기/',
    '/guides/if-taeyeol/': '/guides/태열이라면-시기별-케어/',
    '/guides/if-heat-rash/': '/guides/땀띠라면-24시간-환경-테스트/',
    '/guides/if-atopy-suspected/': '/guides/아토피-의심-진료-전-준비/',
    '/guides/if-drool-rash/': '/guides/침독이라면-차단막-보습-루틴/',
    '/guides/if-diaper-rash/': '/guides/기저귀발진-3일-회복-루틴/',
}

targets = (
    glob.glob('src/**/*.astro', recursive=True)
    + glob.glob('src/**/*.md', recursive=True)
)

changed = 0
for fp in targets:
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()
    orig = text
    for old, new in MAP.items():
        text = text.replace(old, new)
    if text != orig:
        with open(fp, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        changed += 1
        print(f'updated: {fp}')

print(f'\n{changed} files updated')
