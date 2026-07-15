# Baby Skin Lab — Claude 진입 가이드

`babyskinlab.com` — 아기 피부 상태를 판정하는 인터랙티브 도구 랩. Astro 5, GitHub Pages 자동 배포 (`villagebaby-ai/babyskinlab`, main push → 라이브). 운영: 빌리지베이비 (About에 투명 공개).

## 포지셔닝 (3사 구도 — 혼동 금지)

| 사이트 | 질문 | 포맷 |
|---|---|---|
| guide.ruuve.kr | "왜 피부가 이럴까" | 원인 설명 매거진 (네이버 담당) |
| **babyskinlab.com** | **"지금 어떤 상태? 뭘 해야 해?"** | **판정 도구 + 액션 카드 (Google 담당)** |

**ruuve-guide 콘텐츠 복제·번역·요약 재발행 절대 금지** (doorway 판정 리스크). 로직·지식은 참고하되 텍스트는 전부 신규 작성.

## 🔒 slug 영구 룰 (2026-07-15 확정 — 절대 위반 금지)

1. **slug는 한글** — `tools/아기-피부-증상-진단기`, `guides/태열이라면-시기별-케어` 형식. 한글 단어-하이픈, 30자 이내, 검색 자연 발화 패턴, "가이드/방법" 같은 일반어 제외.
2. **한 번 라이브된 slug는 절대 변경 금지.** 부득이 변경 시 astro.config.mjs `redirects`에 옛 slug → 새 slug 301 등록이 **동일 commit에서** 의무. (ruuve-guide에서 redirect 누락 782편 404 → 네이버 노출 -60% 사고의 재발 방지)
3. 신규 글 발행 전 slug 확정 검수 — 발행 후 후회하지 않을 slug인지 먼저 확인.

## 🔒 발행 헌법 (Google 페널티 재발 방지 — PLAN.md 7절)

1. **발행 페이스: 하루 1편 고정 (2026-07-15 사용자 결정).** 매일 오전 10시 cron 1편 — 하루 2편 이상 절대 금지 (폭증 패턴 방지). 캘린더는 CONTENT_PLAN.md, 30일 소진 시 GSC 데이터 보고 다음 30일 기획 (자동 연장 금지). 도구는 5종 완성(2026-07-15), 추가는 별도 승인.
2. 도구 우선 — "글 10편보다 도구 1개".
3. 상호 링크는 About의 운영사 소개 1곳만.
4. 주간 GSC 모니터링, 이상 신호 시 발행 중단.
5. 모든 판정 결과에 의료 면책 + 진료 신호 필수 (YMYL).
6. 제품 노출: 결과당 러베 예시 최대 1개, "예시" 표기, 의약품적 효능 표방 금지.

## 글 작성 룰 (ruuve CONTENT_WRITING_GUIDE 핵심 준수)

- 전부 존댓말 (`~요/~해요`), 이모지 금지, `**굵은 강조**` 남용 금지
- 숫자 범위는 `~` 대신 en-dash `–` (예: `1–3개월`) — `~` 두 번이면 취소선 렌더 사고
- 발행일은 실제 일자 (`publishedAt: 2026-07-15`), 미래 날짜 금지
- 본문에 "올해/최근/요즘" 시점 표현 금지
- References 2개 이상, DOI/PMID/공식 URL 하이퍼링크
- 내부 링크 2-4개, 콤마 명사구 나열 금지 (불릿으로)
- 영어 의학 표현 직역 금지 — 한국 부모 자연 표현 우선

## 구조

```
src/
  content/guides/{한글-slug}.md    # 근거 가이드 (frontmatter: title/description/publishedAt/relatedTool)
  pages/tools/{한글-slug}/index.astro   # 도구 (rule-based 판정 로직 인라인 JS)
  layouts/Base.astro               # 공통 레이아웃 (nav·footer·OG)
  styles/global.css                # 클리니컬 teal 랩 디자인 (#0EA5A4) — ruuve-guide 룩 재사용 금지
astro.config.mjs                   # sitemap lastmod + redirects
PLAN.md                            # 컨셉 기획서 (도구 5종 spec)
```

## 배포·검증

```bash
npm run build                                          # 로컬 검증
git push                                               # → GitHub Actions → 라이브
gh run list --repo villagebaby-ai/babyskinlab --limit 3
```

push 후 반드시 빌드 success 확인. 실패 시 --log-failed로 첫 에러 확인 후 fix.
