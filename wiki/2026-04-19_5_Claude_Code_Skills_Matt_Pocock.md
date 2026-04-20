---
type: summary
parent: [[Claude Code]]
source: [[raw/videos/2026-04-19_5 Claude Code skills I use every single day_Matt Pocock.md]]
tags: [agentic-coding, workflow, prd, tdd]
---

# 📝 요약: Claude Code 5대 실전 스킬 (Matt Pocock)

## 💡 핵심 컨셉
AI 에이전트(Claude Code)는 강력하지만, 명확한 **프로세스(Process)**와 **제약(Constraints)**이 없으면 비효율적인 코드를 생성하거나 길을 잃기 쉽습니다. Matt Pocock은 개발 전 과정에서 AI의 품질을 극대화하는 5가지 단계를 제안합니다.

---

## 🛠️ 5가지 핵심 스킬 (The 5 Skills)

### 1. "Grill me" (역질문 요청)
- **목적**: 요구사항의 모호함을 제거하고 의존성을 파악.
- **방법**: "코드를 짜기 전에, 내가 놓친 부분이나 구현에 필요한 상세 내용을 알 수 있도록 나에게 계속 질문해줘(Grill me)."
- **효과**: 사용자와 AI 간의 완벽한 상호 이해(Alignment) 도달.

### 2. "Write a PRD" (요구사항 정의서 작성)
- **목적**: 합의된 아이디어를 문서화하여 나침반으로 활용.
- **내용**: 기능 범위, 유저 스토리, 기술적 제약 사항 등을 상세히 기록.
- **효과**: 개발 도중 발생할 수 있는 '기능 비대(Scope Creep)' 방지.

### 3. "PRD to Issues" (이슈 분할)
- **목적**: 큰 작업을 관리 가능한 작은 단위로 쪼개기.
- **방법**: PRD를 바탕으로 독립적으로 실행 및 검증 가능한 **'수직적 슬라이스(Vertical slices)'** 이슈들로 분할.
- **효과**: AI가 한 번에 처리해야 할 컨텍스트 양을 줄여 정확도 향상.

### 4. "TDD (Test-Driven Development)" (테스트 주도 개발)
- **목적**: 인터페이스 설계 강제 및 코드 품질 보장.
- **방법**: Red-Green-Refactor 루프를 AI가 지키도록 지시. 테스트를 먼저 짜고, 그것을 통과하는 최소한의 코드를 작성.
- **효과**: 리팩토링이 용이하고 결함이 적은 견고한 코드베이스 구축.

### 5. "Improve Codebase Architecture" (아키텍처 개선)
- **목적**: 전체적인 구조적 완성도 향상.
- **방법**: 코드베이스를 분석하게 하고, 서브 에이전트들을 생성하여 "이 인터페이스를 개선할 3가지 대안을 제시해봐"라고 요청.
- **효과**: 단일 솔루션에 매몰되지 않고 최적의 설계 선택 가능.

---

## 🚀 인사이트: 나만의 위키 활용법
- **Agentic Coding**: 단순히 코드를 맡기는 것이 아니라, **'매니저'**로서 단계를 설계해야 함.
- **PRD 기반 워크플로우**: 이 위키에 새로운 툴을 추가할 때도 위 5단계(Grill -> PRD -> Issues -> TDD)를 적용하여 자동화 안정성을 높일 수 있음.

## 🔗 연결된 지식
- [[Claude Code]]
- [[Agentic Coding]]
- [[프롬프트 엔지니어링]]
- [[Matt Pocock]]
