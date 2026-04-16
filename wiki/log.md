---
type: log
created: 2026-04-16
---

# 📝 위키 활동 로그 (Wiki Log)

> 이 파일은 위키의 모든 활동을 시간순으로 기록합니다 (append-only).
> AI는 ingest, query, lint 등 모든 작업 후 이곳에 기록합니다.
> 검색 팁: `## [` 으로 시작하는 줄을 찾으면 모든 엔트리를 볼 수 있습니다.

---

## [2026-04-16] init | 위키 초기화
- **작업**: LLM Wiki 시스템 초기 세팅
- **내용**: Karpathy의 LLM Wiki 패턴을 참고하여 후니님 맞춤형 위키 구조 생성
- **생성된 구조**:
  - `raw/` — articles, notes, conversations, courses, research, assets
  - `wiki/` — AI가 컴파일하는 위키 (index.md, log.md)
  - `output/` — blog, reports, lectures, misc
- **참고**: [Karpathy LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## [2026-04-16] update | raw/videos/ 폴더 추가
- **작업**: 유튜브·영상 학습 노트 전용 폴더 신설
- **내용**: `raw/videos/ANTIGRAVITY.md` 생성 (노트 템플릿 포함)
- **이유**: 후니님이 AI·투자·경제 유튜브를 주요 학습 소스로 활용하므로 별도 분류

## [2026-04-16] ingest | 카파시의 LLM Wiki로 나만의 AI 세컨드 브레인 만들기
- **소스**: `raw/videos/_카파시의 LLM Wiki...브레인 트리니티.md`
- **채널**: 브레인 트리니티 (Brain Trinity)
- **생성된 페이지** (4개):
  - `wiki/요약_2026-04-16_카파시의 LLM Wiki로 나만의 AI 세컨드 브레인 만들기.md`
  - `wiki/LLM Wiki 패턴.md`
  - `wiki/AI 세컨드 브레인.md`
  - `wiki/Andrej Karpathy.md`
- **후니님 맥락**:
  - 수집 이유: LLM Wiki 세팅 방법을 참고하기 위해 (현재 이 볼트 구축에 직접 활용 중)
  - Claude Code 기반 영상이지만 Antigravity로 동일 구조 구현
  - 다음 목표: Graphify 세팅 완료 → 나만의 기록 저장소 운영 시작

## [2026-04-16] ingest | 미소스(Claude Mythos)가 무서운 이유
- **소스**: `raw/articles/_4월15일 27년간 숨어있던 문제...미소스.md`
- **타입**: article | 출처: AI타임스
- **생성된 페이지** (4개):
  - `wiki/요약_2026-04-16_미소스(Claude Mythos)가 무서운 이유.md`
  - `wiki/Claude Mythos.md`
  - `wiki/AI 사이버보안.md`
  - `wiki/제로데이 취약점.md`
- **핵심**: AI가 27년된 OpenBSD 버그를 이틀 만에 발견. 제로데이 공격 시간 847일→20시간으로 급감. AI의 공격/방어 비대칭성 심화.

## [2026-04-16] ingest | 시민개발자 구씨 LLM Wiki 튜토리얼 & 깃허브
- **소스**: `raw/videos/_안쓰면 손해!...시민개발자 구씨.md`, `raw/courses/_yt-assets...README.md at main.md`
- **타입**: video / course (GitHub) | 출처: 유튜브 / GitHub
- **생성된 페이지** (3개):
  - `wiki/요약_2026-04-16_시민개발자 구씨의 클로드코드 LLM Wiki 정리.md`
  - `wiki/요약_2026-04-16_시민개발자 구씨 LLM Wiki GitHub Repo.md`
  - `wiki/시민개발자 구씨.md`
- **핵심**: 카파시의 LLM Wiki 아이디어를 대중이 실전에서 구현할 수 있도록 만든 실무 강의 영상 및 실습 파일.

## [2026-04-16] fetch + ingest | AI 업계 동향 10개 기사 (4개 사이트)
- **소스**: `raw/articles/2026-04-16_*.md` (10개)
- **출처**: The Rundown AI(4) · Anthropic(2) · Google DeepMind(2) · AI Magazine(2)
- **생성된 페이지** (13개):
  - 요약 10개 (OpenAI, AI리테일, Perplexity, Meta, Glasswing, LTBT, Gemma4, SIMA2, OpenAI UK, Andy Jassy)
  - 신규 엔티티 3개: `Perplexity.md`, `Meta Superintelligence Labs.md`, `Google DeepMind.md`
- **핵심 이슈**: OpenAI GPT-5.4-Cyber vs Mythos 전략 대비 / Meta AGI 참전 / Gemma 4 오픈소스 / Project Glasswing 보안 대연합
- **후니님 follow-up 메모**:
  - Gemini Chrome 자동화 실습 → raw/notes 추가 예정
  - Perplexity 에이전트 + Notion 자동화 → raw/notes 추가 예정
  - 한국 AI 규제 현황 → raw/research 추가 예정
  - Gemma 4 로컬 활용 방법 탐구 예정
