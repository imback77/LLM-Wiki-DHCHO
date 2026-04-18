---
type: log
created: 2026-04-16
updated: 2026-04-18
tags: ["auto-fixed"]
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

## [2026-04-16] ingest | Claude 실전 가이드 & 프로젝트 관리 & 스킬 구축
- **소스**: `raw/videos/_클로드 초보...`, `raw/research/_프로젝트...`, `raw/courses/_The-Complete-Guide...`
- **타입**: video / research / course
- **생성된 페이지** (5개):
  - 요약 3개 (실전 가이드, 프로젝트 관리, 스킬 구축)
  - 신규 개념 2개: `Claude Projects.md`, `AI 스킬 자산화.md`
- **핵심**: Claude 3.5 Sonnet 활용 기법, 프로젝트 지식 기반 관리법, 그리고 워크플로우를 '스킬'로 자산화하는 에이전트 설계 전략.
- **후니님 맥락**: "AI 업황 및 도구 정보 자동 연결" 규칙에 따라 사후 질문 없이 자동 반영함.

## [2026-04-16] ingest | 그린코끼리 AI 클로드 초보자 가이드
- **소스**: `raw/videos/_클로드 초보자 가이드...그린코끼리 AI.md`
- **타입**: video-note
- **생성된 페이지** (1개):
  - `wiki/요약_2026-04-16_그린코끼리 AI 클로드 초보자 가이드.md`
- **핵심**: 클로드의 기초 기능을 마스터하여 프로젝트와 스킬 단계로 넘어가기 위한 토대를 마련함.
- **후니님 맥락**: 후니님이 직접 남긴 "클로드 사용의 마스터 필수 영상"이라는 메모를 반영하여 자동 인제스트함.

## [2026-04-17] ingest | AI 업계 동향 수집 및 신규 지식망 구성 (4건)
- **소스**: `raw/articles/2026-04-17_*.md` (4건)
- **타입**: article
- **생성 및 갱신된 페이지** (9개):
  - 요약 4개: Anthropic, OpenAI, Google DeepMind, The Rundown AI Briefs
  - 신규 엔티티/개념 5개: `Claude Opus 4.7.md`, `GPT-Rosalind.md`, `피지컬 AI.md`, `AI 바이오 혁신과 투자 기회.md`, `AI 윤리와 의식.md`
- **핵심**: 유저의 각 4개 아티클별 코멘트·인사이트를 기반으로 물리적 AI 도래, 바이오 제약 혁신 투자, 기계 의식, 방어용 AI 모델 활용 등의 연결 지점을 위키에 구조화함.
- **후니님 맥락**: "제약 신규개발 바이오 기회, 피지컬 AI 패러다임 전환, AI 윤리 및 의식 발달 등"의 주요 인사이트를 즉각적으로 위키 내 개별 지식 노드로 치환함.

## [2026-04-17] ingest | Claude 기반 코딩 디자인 & AI 자동화 투자 봇 구축
- **소스**: `raw/videos/_Claude Code Design...`, `raw/videos/_Claude Just Changed the Stock Market...`
- **타입**: video-note
- **생성된 페이지** (5개):
  - 요약 2개: `요약_2026-04-17_Claude Code Design just became UNSTOPPABLE.md`, `요약_2026-04-17_Claude Just Changed the Stock Market Forever.md`
  - 신규 개념/엔티티 3개: `코드 기반 디자인.md`, `Firecrawl.md`, `AI 투자 자동화.md`, `휠 전략 (Wheel Strategy).md`
- **핵심**: 코드 기반 디자인 패러다임 전환 및 Firecrawl MCP 활용. 트레이딩 API(Alpaca)와 Claude 연동을 통한 기관급 투자 전략 개인화.
- **후니님 맥락**: 최근 관심사인 디자인 시스템 파이프라인(AI 스킬 자산화 연계)과 AI를 활용한 시장 모니터링/수익 창출 모델(투자 자동화) 지식을 확보함.

## [2026-04-18] ingest | 협업형 AI로의 전환
- **소스**: raw/articles/2026-04-18_협업형 AI로의 전환.md
- **타입**: article
- **생성된 페이지** (2개): `wiki/요약_2026-04-18_협업형 AI로의 전환.md`, `wiki/협업형 AI.md`
- **후니님 맥락**: 단발성 텍스트 처리를 넘어 진정한 비즈니스 파트너(디지털 동료)로서의 AI를 인식함. 세컨드 브레인을 통해 나만의 AI 파트너를 키우겠다는 방향성을 재고.

## [2026-04-18] ingest | AI 업계 동향 잔여 기사 4건 일괄 처리
- **소스**: raw/articles/2026-04-18_AI 인프라와 물리적 한계.md 외 3건
- **타입**: article
- **생성된 페이지** (8개): 요약 4건, 신규 개념 4건 (AI 인프라 레이스, AI 파일럿 트랩, 위험 임계점, 하이브리드 양자-AI)
- **후니님 맥락**: 새롭게 떠오르는 투자 트렌드(AI 인프라 레이스, 양자 컴퓨팅 융합)와 AI 도입 리스크(파일럿 트랩)를 투자 및 자기주도적 1인 기업 창업 관점에서 연결 및 저장함.

## [2026-04-18] ingest | AI 비디오 노트 잔여분 3건 일괄 처리
- **소스**: raw/videos/_I Built An Entire AI Trading Team... 등 3건
- **타입**: video-note
- **생성된 페이지** (8개): 요약 3건, 신규 개념 5건 (AI 투자 팀, 자동화 투자 분석, 코드 기반 UI 생성, AI 디자인 자동화, Claude 커스텀 인스트럭션)
- **후니님 맥락**: 클로드와 에이전틱 AI를 실질적인 아웃풋(트레이딩 봇, 웹디자인 결과물, 생산성 파이프라인)으로 연결하여 1인 기업 역량을 확장.

## [2026-04-18] lint | 정기 점검
- **총 페이지**: 102개
- **발견된 문제**: 깨진 링크 33 / 고아 페이지 0 / index 누락 13 / frontmatter 문제 2
- **자동 수정**: 48건 (스텁 33건 생성, index.md 13건 등록, frontmatter 2건 갱신)
- **후니님 확인 필요**: 0건
- **추천 ingest 주제**: 신규 자동 생성된 33개의 개념(Stub) 페이지들에 대해 관련 아티클이나 노트를 fetch하여 살을 붙일 것을 권장함.

## [2026-04-18] research | AI 인프라 전력망 수혜주
- **소스**: `raw/articles/2026-04-18_AI 인프라 전력망 관련 국내 종목.md`
- **타입**: sector (투자 인프라 섹터 분석)
- **생성된 페이지**: `wiki/2026-04-18_AI 인프라 전력망 수혜주.md`
- **핵심**: AI 인프라 사이클의 근본적 병목인 '전력 시설'의 수급 불균형 심화를 통해, 단순 테마가 아니라 실질적 수주잔고 급증을 보이는 전력 장비 기업(LS일렉트릭, HD현대일렉트릭 등)들의 구조적 성장을 다룸.
