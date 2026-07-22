#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""글별 hero(대표) 이미지 SVG 생성 → img-src/{slug}-hero.svg
   1200x630 (OG 1.91:1 규격, 구글·네이버·카카오 섬네일 안 잘림).
   레이아웃: 좌측 질문형 헤드라인 + 우측 pale teal 패널 안 라인 아이콘.
   폰트 임베드·PNG 변환은 build_images.py가 수행.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "img-src")
os.makedirs(OUT, exist_ok=True)

TEAL = "#0ea5a4"; TEAL_D = "#0b8483"; INK = "#0f172a"; SOFT = "#64748b"
PALE = "#e6f7f7"; LINE = "#cbd5e1"

# ── 라인 아이콘 (오른쪽 패널 중심 cx=955 cy=315, 굵은 라운드 스트로크) ──
def ic(paths):
    return f'<g fill="none" stroke="{TEAL_D}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round">{paths}</g>'

ICONS = {
    # 얼굴 + 오돌토돌 점
    "face": ic('<circle cx="955" cy="315" r="130"/>'
               '<circle cx="915" cy="290" r="9" fill="'+TEAL_D+'" stroke="none"/>'
               '<circle cx="995" cy="290" r="9" fill="'+TEAL_D+'" stroke="none"/>'
               '<path d="M915 365 q40 30 80 0"/>'
               '<circle cx="885" cy="345" r="6" fill="'+TEAL+'" stroke="none"/>'
               '<circle cx="1025" cy="340" r="6" fill="'+TEAL+'" stroke="none"/>'
               '<circle cx="1010" cy="380" r="6" fill="'+TEAL+'" stroke="none"/>'),
    # 물방울 (보습)
    "drop": ic('<path d="M955 195 C 900 285 865 330 865 375 a90 90 0 0 0 180 0 c0 -45 -35 -90 -90 -180 Z"/>'
               '<path d="M905 380 a50 50 0 0 0 50 45"/>'),
    # 성분 목록
    "list": ic('<rect x="835" y="200" width="240" height="230" rx="20"/>'
               '<line x1="875" y1="255" x2="1035" y2="255"/>'
               '<line x1="875" y1="315" x2="1000" y2="315"/>'
               '<line x1="875" y1="375" x2="1035" y2="375"/>'
               '<circle cx="1055" cy="255" r="7" fill="'+TEAL+'" stroke="none"/>'),
    # 방패 + 체크 (차단·보호)
    "shield": ic('<path d="M955 190 l95 40 v95 c0 80 -55 130 -95 150 c-40 -20 -95 -70 -95 -150 v-95 Z"/>'
                 '<path d="M915 320 l28 30 l55 -65"/>'),
    # 온도계 (땀띠 환경)
    "thermo": ic('<path d="M930 200 a30 30 0 0 1 60 0 v150 a48 48 0 1 1 -60 0 Z"/>'
                 '<line x1="960" y1="250" x2="960" y2="380"/>'
                 '<circle cx="960" cy="405" r="26" fill="'+TEAL+'" stroke="none"/>'),
    # 체크리스트 (진료 전 준비)
    "clip": ic('<rect x="850" y="200" width="210" height="240" rx="20"/>'
               '<rect x="915" y="185" width="80" height="45" rx="14" fill="'+PALE+'"/>'
               '<path d="M885 285 l20 20 l35 -40"/>'
               '<line x1="960" y1="290" x2="1025" y2="290"/>'
               '<path d="M885 360 l20 20 l35 -40"/>'
               '<line x1="960" y1="365" x2="1025" y2="365"/>'),
    # 태양 (자외선)
    "sun": ic('<circle cx="955" cy="315" r="70"/>'
              '<line x1="955" y1="180" x2="955" y2="210"/>'
              '<line x1="955" y1="420" x2="955" y2="450"/>'
              '<line x1="820" y1="315" x2="850" y2="315"/>'
              '<line x1="1060" y1="315" x2="1090" y2="315"/>'
              '<line x1="865" y1="225" x2="885" y2="245"/>'
              '<line x1="1025" y1="385" x2="1045" y2="405"/>'
              '<line x1="1045" y1="225" x2="1025" y2="245"/>'
              '<line x1="885" y1="385" x2="865" y2="405"/>'),
    # 입가 (침독) — 미소 + 물방울
    "mouth": ic('<path d="M855 300 q100 90 200 0"/>'
                '<path d="M905 250 l0 0"/>'
                '<circle cx="900" cy="255" r="8" fill="'+TEAL_D+'" stroke="none"/>'
                '<circle cx="1010" cy="255" r="8" fill="'+TEAL_D+'" stroke="none"/>'
                '<path d="M955 380 c-18 24 -18 40 0 52 c18 -12 18 -28 0 -52 Z" fill="'+TEAL+'" stroke="none"/>'),
    # 기저귀
    "diaper": ic('<path d="M840 250 h230 l-25 90 a90 90 0 0 1 -180 0 Z"/>'
                 '<path d="M905 255 q50 40 100 0"/>'
                 '<circle cx="925" cy="315" r="6" fill="'+TEAL+'" stroke="none"/>'
                 '<circle cx="985" cy="325" r="6" fill="'+TEAL+'" stroke="none"/>'),
}

# ── center-safe 레이아웃 ──
# 네이버는 1:1 정사각으로 "중앙"을 크롭한다 (viewBox 1200x630 → 중앙 안전지대 x 285~915).
# 그래서 모든 핵심 요소(아이콘·헤드라인·배지)를 x=600 중심으로 세로 스택 → 구글(가로 전체)·
# 카카오(2:1)·네이버(1:1 중앙크롭) 어디서도 안 잘린다. 좌우 여백은 크롭돼도 무방한 흰 배경.
CX = 600
SAFE_L, SAFE_R = 285, 915  # 네이버 정사각 크롭 경계 (넘으면 잘림)

def _center_line(txt, y, size, em):
    """x=600 중앙정렬, em 부분만 teal 강조"""
    if em and em in txt:
        a, b = txt.split(em, 1)
        inner = f'{a}<tspan fill="{TEAL_D}">{em}</tspan>{b}'
    else:
        inner = txt
    return (f'<text x="{CX}" y="{y}" text-anchor="middle" '
            f'font-size="{size}" font-weight="800" fill="{INK}">{inner}</text>')

def hero(slug, badge, l1, l2, em, icon):
    icon_tf = f'<g transform="translate({CX},178) scale(0.6) translate(-955,-315)">{ICONS[icon]}</g>'
    bw = 56 + len(badge) * 30
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" font-family="Pretendard, sans-serif">
  <rect width="1200" height="630" fill="#ffffff"/>
  <circle cx="{CX}" cy="178" r="88" fill="{PALE}"/>
  {icon_tf}
  {_center_line(l1, 358, 60, em)}
  {_center_line(l2, 432, 60, em)}
  <rect x="{CX - bw//2}" y="470" rx="26" ry="26" width="{bw}" height="52" fill="none" stroke="{LINE}" stroke-width="3"/>
  <text x="{CX}" y="505" text-anchor="middle" font-size="30" font-weight="700" fill="{SOFT}">{badge}</text>
  <text x="{CX}" y="590" text-anchor="middle" font-size="26" font-weight="800" fill="{TEAL}" letter-spacing="1">Baby Skin Lab</text>
</svg>'''
    path = os.path.join(OUT, f"{slug}-hero.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("[hero]", slug)

# ── 글별 hero 정의 (질문형 헤드라인) ──
HEROES = [
    ("아기-로션-크림-연고-차이", "보습 가이드", "로션·크림·연고,", "뭐가 다를까?", "뭐가 다를까?", "drop"),
    ("아기-얼굴-오돌토돌-원인", "증상 판정", "아기 얼굴 오돌토돌,", "원인이 뭘까?", "원인이 뭘까?", "face"),
    ("아기-화장품-전성분-읽는-순서", "성분 가이드", "전성분표,", "어떻게 읽을까?", "어떻게 읽을까?", "list"),
    ("기저귀발진-3일-회복-루틴", "케어 루틴", "기저귀발진,", "3일 회복 루틴", "3일 회복 루틴", "diaper"),
    ("땀띠라면-24시간-환경-테스트", "증상 판정", "혹시 땀띠일까?", "24시간 확인법", "24시간 확인법", "thermo"),
    ("아토피-의심-진료-전-준비", "진료 준비", "아토피 의심,", "진료 전 준비", "진료 전 준비", "clip"),
    ("침독이라면-차단막-보습-루틴", "케어 루틴", "침독이라면,", "차단막 루틴", "차단막 루틴", "mouth"),
    ("태열이라면-시기별-케어", "케어 루틴", "태열이라면,", "시기별 케어", "시기별 케어", "shield"),
    ("신생아-목욕-온도-시간-빈도", "목욕 가이드", "신생아 목욕,", "몇 도·몇 분·몇 번?", "몇 도·몇 분·몇 번?", "thermo"),
    ("아기-자외선차단제-언제부터", "자외선 가이드", "아기 선크림,", "언제부터 발라요?", "언제부터 발라요?", "sun"),
    ("아기-볼-빨간-이유", "증상 판정", "볼이 빨개요,", "열일까 피부일까?", "열일까 피부일까?", "face"),
]

def default_hero():
    """사이트 기본 OG (툴·홈 등 hero 없는 페이지용) → img-src/default-hero.svg → /og/default.png
       center-safe 동일 규칙."""
    icon_tf = f'<g transform="translate({CX},170) scale(0.56) translate(-955,-315)">{ICONS["face"]}</g>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" font-family="Pretendard, sans-serif">
  <rect width="1200" height="630" fill="#ffffff"/>
  <circle cx="{CX}" cy="170" r="84" fill="{PALE}"/>
  {icon_tf}
  <text x="{CX}" y="345" text-anchor="middle" font-size="58" font-weight="800" fill="{INK}">우리 아기 피부,</text>
  <text x="{CX}" y="415" text-anchor="middle" font-size="58" font-weight="800" fill="{INK}"><tspan fill="{TEAL_D}">지금 어떤 상태</tspan>일까?</text>
  <text x="{CX}" y="480" text-anchor="middle" font-size="27" font-weight="600" fill="{SOFT}">증상 판정 · 케어 방향 · 성분 체크</text>
  <text x="{CX}" y="590" text-anchor="middle" font-size="26" font-weight="800" fill="{TEAL}" letter-spacing="1">Baby Skin Lab</text>
</svg>'''
    with open(os.path.join(OUT, "default-hero.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("[hero] default")

if __name__ == "__main__":
    for h in HEROES:
        hero(*h)
    default_hero()
    print(f"총 {len(HEROES)+1}개 hero 생성")
