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
    # 구름 뒤 태양 (흐린 날 자외선) — 흰 채움으로 구름이 해를 가리게 겹쳐 그림
    "cloudsun": ('<g fill="#ffffff" stroke="' + TEAL_D + '" stroke-width="13" '
                 'stroke-linecap="round" stroke-linejoin="round">'
                 '<line x1="993" y1="212" x2="993" y2="186"/>'
                 '<line x1="938" y1="235" x2="920" y2="217"/>'
                 '<line x1="1048" y1="235" x2="1066" y2="217"/>'
                 '<line x1="1071" y1="290" x2="1088" y2="290"/>'
                 '<line x1="1048" y1="345" x2="1066" y2="363"/>'
                 '<circle cx="993" cy="290" r="62"/>'
                 '<path d="M985 347 h-12 A76 76 0 1 0 899.5 442 h85.5 a47.5 47.5 0 0 0 0 -95 Z"/>'
                 '</g>'),
    # 입가 (침독) — 미소 + 물방울
    "mouth": ic('<path d="M855 300 q100 90 200 0"/>'
                '<path d="M905 250 l0 0"/>'
                '<circle cx="900" cy="255" r="8" fill="'+TEAL_D+'" stroke="none"/>'
                '<circle cx="1010" cy="255" r="8" fill="'+TEAL_D+'" stroke="none"/>'
                '<path d="M955 380 c-18 24 -18 40 0 52 c18 -12 18 -28 0 -52 Z" fill="'+TEAL+'" stroke="none"/>'),
    # 방 + 물방울 (실내 습도)
    "humid": ic('<path d="M835 315 l120 -105 l120 105 v120 a22 22 0 0 1 -22 22 h-196 a22 22 0 0 1 -22 -22 Z"/>'
                '<path d="M955 305 c-30 42 -42 58 -42 74 a42 42 0 0 0 84 0 c0 -16 -12 -32 -42 -74 Z" fill="'+TEAL+'" stroke="none"/>'),
    # 몸통 + 발진 점 (몸에 난 발진)
    "body": ic('<circle cx="955" cy="212" r="42"/>'
               '<rect x="898" y="268" width="114" height="146" rx="40"/>'
               '<path d="M898 296 l-44 56"/>'
               '<path d="M1012 296 l44 56"/>'
               '<path d="M925 414 l0 44"/>'
               '<path d="M985 414 l0 44"/>'
               '<circle cx="930" cy="308" r="8" fill="'+TEAL+'" stroke="none"/>'
               '<circle cx="978" cy="330" r="8" fill="'+TEAL+'" stroke="none"/>'
               '<circle cx="945" cy="360" r="8" fill="'+TEAL+'" stroke="none"/>'
               '<circle cx="988" cy="382" r="8" fill="'+TEAL+'" stroke="none"/>'),
    # 두피 + 떨어지는 딱지 조각 (지루성 두피)
    "scalp": ic('<circle cx="955" cy="338" r="108"/>'
                '<path d="M847 330 q108 -90 216 0"/>'
                '<rect x="876" y="200" width="26" height="26" rx="7" fill="'+TEAL+'" stroke="none"/>'
                '<rect x="940" y="182" width="30" height="30" rx="8" fill="'+TEAL+'" stroke="none"/>'
                '<rect x="1008" y="204" width="24" height="24" rx="7" fill="'+TEAL+'" stroke="none"/>'),
    # 화장품 용기 + 시계 (유통기한·개봉 후 사용기간) — 시계는 흰 채움으로 용기 위에 겹침
    "expiry": ('<g fill="none" stroke="' + TEAL_D + '" stroke-width="13" '
               'stroke-linecap="round" stroke-linejoin="round">'
               '<rect x="862" y="240" width="118" height="175" rx="26"/>'
               '<path d="M896 240 v-26 a13 13 0 0 1 13 -13 h24 a13 13 0 0 1 13 13 v26"/>'
               '<line x1="892" y1="292" x2="950" y2="292"/>'
               '<circle cx="1000" cy="355" r="54" fill="#ffffff"/>'
               '<path d="M1000 320 v35 h26"/>'
               '</g>'),
    # 해 + 아래 피부 면 (햇빛 화상) — 해가 피부를 내리쬐는 구도
    "sunburn": ic('<circle cx="955" cy="272" r="52"/>'
                  '<line x1="955" y1="206" x2="955" y2="185"/>'
                  '<line x1="1002" y1="225" x2="1017" y2="211"/>'
                  '<line x1="1021" y1="272" x2="1042" y2="272"/>'
                  '<line x1="908" y1="225" x2="893" y2="211"/>'
                  '<line x1="889" y1="272" x2="868" y2="272"/>'
                  '<line x1="908" y1="319" x2="893" y2="333"/>'
                  '<line x1="1002" y1="319" x2="1017" y2="333"/>'
                  '<line x1="955" y1="338" x2="955" y2="356"/>'
                  '<rect x="858" y="380" width="194" height="64" rx="26"/>'
                  '<circle cx="905" cy="408" r="11" fill="'+TEAL+'" stroke="none"/>'
                  '<circle cx="955" cy="422" r="11" fill="'+TEAL+'" stroke="none"/>'
                  '<circle cx="1008" cy="404" r="11" fill="'+TEAL+'" stroke="none"/>'),
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
    ("세라마이드-아기-피부-역할", "보습 가이드", "세라마이드가", "왜 중요할까?", "왜 중요할까?", "drop"),
    ("아기-화장품-피해야-할-성분", "성분 가이드", "이 성분,", "피해야 할까?", "피해야 할까?", "list"),
    ("아기-실내-습도-관리", "환경 가이드", "아기 방 습도,", "몇 %가 맞을까?", "몇 %가 맞을까?", "humid"),
    ("아기-자외선-물리-차단", "외출 가이드", "아기 햇빛 차단,", "무엇으로 막을까?", "무엇으로 막을까?", "sun"),
    ("아기-열꽃-두드러기-구분", "증상 판정", "갑자기 난 발진,", "열꽃일까 두드러기?", "열꽃일까 두드러기?", "body"),
    ("목욕-후-3분-보습-이유", "보습 가이드", "목욕 후 보습,", "왜 3분일까?", "왜 3분일까?", "drop"),
    ("무향-화장품-아기", "성분 가이드", "아기 화장품,", "무향이 나을까?", "무향이 나을까?", "list"),
    ("아기-옷-몇-겹", "환경 가이드", "아기 옷,", "몇 겹이 맞을까?", "몇 겹이 맞을까?", "thermo"),
    ("흐린-날-자외선", "자외선 가이드", "흐린 날에도", "선크림 발라야 할까?", "선크림 발라야 할까?", "cloudsun"),
    ("아기-두피-노란-딱지", "증상 판정", "아기 두피 노란 딱지,", "왜 생길까?", "왜 생길까?", "scalp"),
    ("아기-보습제-유통기한-보관", "보습 가이드", "아기 보습제,", "언제까지 쓸까?", "언제까지 쓸까?", "expiry"),
    ("페녹시에탄올-아기-안전성", "성분 가이드", "페녹시에탄올,", "안전한 걸까?", "안전한 걸까?", "list"),
    ("아기-여름-땀-관리", "환경 가이드", "아기 땀띠,", "어떻게 예방할까?", "어떻게 예방할까?", "thermo"),
    ("아기-자외선-화상-대처", "대처 가이드", "아기 햇빛 화상,", "지금 뭘 해야 할까?", "지금 뭘 해야 할까?", "sunburn"),
    ("아기-살-접힌-곳-빨감", "증상 판정", "살 접힌 곳이 빨개요,", "간찰진일까?", "간찰진일까?", "body"),
    ("아토피-가족력-신생아-보습", "보습 가이드", "아토피 가족력이라면,", "첫 4주에 뭘 할까?", "첫 4주에 뭘 할까?", "drop"),
    ("천연-화장품-저자극-오해", "성분 가이드", "천연·유기농이면,", "저자극일까?", "저자극일까?", "list"),
    ("아기-수영장-목욕탕-시기", "목욕 가이드", "아기 수영장·목욕탕,", "언제부터 갈까?", "언제부터 갈까?", "thermo"),
    ("유모차-외출-자외선", "외출 가이드", "유모차 외출,", "햇빛은 어떻게 피할까?", "어떻게 피할까?", "sun"),
    ("아기-손발-각질-벗겨짐", "증상 판정", "손발이 자꾸 벗겨져요,", "각질일까 습진일까?", "각질일까 습진일까?", "body"),
    ("보습해도-건조한-아기", "보습 가이드", "보습해도 건조하다면,", "무엇을 놓쳤을까?", "무엇을 놓쳤을까?", "drop"),
    ("전성분-표기-순서-1퍼센트-룰", "성분 가이드", "전성분 순서,", "앞일수록 많을까?", "앞일수록 많을까?", "list"),
    ("신생아-첫-통목욕-체크리스트", "목욕 가이드", "신생아 통목욕,", "언제부터 할까?", "언제부터 할까?", "thermo"),
    ("아기-피부-타입-자외선-민감도", "자외선 가이드", "우리 아기 피부,", "얼마나 민감할까?", "얼마나 민감할까?", "sun"),
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
