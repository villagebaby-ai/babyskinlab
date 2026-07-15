import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import fs from 'node:fs';
import path from 'node:path';

// 가이드 URL → lastmod 매핑 (구글·네이버 SERP 날짜 노출 신호 — ruuve-guide에서 배운 것)
function buildLastmodMap() {
  const map = new Map();
  const dir = path.join(process.cwd(), 'src', 'content', 'guides');
  if (!fs.existsSync(dir)) return map;
  for (const file of fs.readdirSync(dir)) {
    if (!file.endsWith('.md')) continue;
    const txt = fs.readFileSync(path.join(dir, file), 'utf-8');
    const upd = txt.match(/^updatedAt:\s*(\S+)/m);
    const pub = txt.match(/^publishedAt:\s*(\S+)/m);
    const lastmod = (upd?.[1] || pub?.[1] || '').trim();
    if (!lastmod) continue;
    const slug = file.replace(/\.md$/, '');
    map.set(`https://babyskinlab.com/guides/${slug}/`, lastmod);
    map.set(`https://babyskinlab.com/guides/${encodeURIComponent(slug)}/`, lastmod);
  }
  return map;
}
const lastmodMap = buildLastmodMap();

// 가이드 slug → 다이어그램 이미지 목록 (sitemap image:image — 이미지 검색 색인 신호)
function buildDiagramMap() {
  const map = new Map();
  const dir = path.join(process.cwd(), 'public', 'diagrams');
  if (!fs.existsSync(dir)) return map;
  for (const file of fs.readdirSync(dir)) {
    if (!/\.(svg|webp|png)$/i.test(file)) continue;
    const slug = file.replace(/-\d+\.(svg|webp|png)$/i, '');
    if (!map.has(slug)) map.set(slug, []);
    map.get(slug).push(`https://babyskinlab.com/diagrams/${encodeURIComponent(file)}`);
  }
  return map;
}
const diagramMap = buildDiagramMap();

export default defineConfig({
  site: 'https://babyskinlab.com',
  trailingSlash: 'always',
  integrations: [
    sitemap({
      serialize(item) {
        const result = { ...item };
        let lm = lastmodMap.get(item.url);
        if (!lm) lm = lastmodMap.get(decodeURIComponent(item.url));
        if (lm) result.lastmod = `${lm}T00:00:00+09:00`;

        const m = decodeURIComponent(item.url).match(/\/guides\/([^\/]+)\/$/);
        if (m && diagramMap.has(m[1])) {
          result.img = diagramMap.get(m[1]).map((url) => ({ url }));
        }
        return result;
      },
    }),
  ],
  build: {
    format: 'directory',
  },
  // 초기 영문 slug → 한글 slug 301 redirect (2026-07-15 색인 전 전환, 잠깐 라이브됐던 URL 보호)
  // 룰: 한 번 라이브된 slug는 절대 redirect 없이 제거하지 않는다 (ruuve-guide 782편 404 사고 교훈)
  redirects: {
    '/tools/skin-symptom-checker/': '/tools/아기-피부-증상-진단기/',
    '/guides/if-taeyeol/': '/guides/태열이라면-시기별-케어/',
    '/guides/if-heat-rash/': '/guides/땀띠라면-24시간-환경-테스트/',
    '/guides/if-atopy-suspected/': '/guides/아토피-의심-진료-전-준비/',
    '/guides/if-drool-rash/': '/guides/침독이라면-차단막-보습-루틴/',
    '/guides/if-diaper-rash/': '/guides/기저귀발진-3일-회복-루틴/',
  },
});
