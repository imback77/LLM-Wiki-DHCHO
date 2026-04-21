---
type: "summary"
created: 2026-04-19
updated: 2026-04-19
sources: ["[[2026-04-16_Claude Code Design just became UNSTOPPABLE]]"]
tags: ["claude-code", "developer-productivity", "prompt-engineering", "workflow"]
---

# 2026-04-19_Matt_Pocock_Claude_Code_Skills

## 핵심 주장
- **프로세스 중심 개발**: AI 에이전트([[Claude Code]])의 품질은 단순 프롬프트가 아니라, 명확하고 엄격한 업무 프로세스(Workflow)에 의해 결정됨.
- **5단계 핵심 스킬**:
  1. **Grill me**: 요구사항의 모호함을 없애기 위해 AI가 반대로 사용자를 인터뷰하는 과정.
  2. **PRD 자동화**: 인터뷰 내용을 바탕으로 상세 제품 요구사항 정의서(PRD)를 작성.
  3. **이슈 분할**: PRD를 실행 가능한 아주 작은 단위(Vertical Slices)로 쪼개어 AI가 하나씩 정복하게 함.
  4. **TDD 강제**: 테스트 코드를 먼저 작성하게 하여 인터페이스의 설계를 견고히 함.
  5. **아키텍처 개선**: 서브 에이전트를 활용해 리팩토링 대안을 제안받고 코드 베이스를 개선.

## 언급된 엔티티
- [[Claude Code]]: 앤스로픽의 터미널 기반 AI 코딩 에이전트.
- **Matt Pocock**: TypeScript 전문가 및 AI 개발 워크플로우 인플루언서.

## 다루는 개념
- [[Grill me (프롬프트 기법)]]: AI에게 정보를 주는 대신, AI가 정보를 캐내도록 만드는 역발상 기법.
- **수직적 슬라이스 (Vertical Slices)**: 사용자에게 가치를 줄 수 있는 최소 단위의 기능을 끝까지(DB부터 UI까지) 구현하는 방식.
- [[TDD (Test-Driven Development, 테스트 주도 개발)]] (테스트 주도 개발): AI 에이전트의 환각을 방지하고 코드 품질을 보장하는 핵심 장치.

## 후니님의 맥락 메모
- "Grill me" 기법은 위키의 '지식 인제스트' 과정에도 적용 가능함. 내가 정보를 던져주기만 하는 게 아니라, AI가 내 위키의 맥락에 맞게 "이 지식은 [[Agentic AI (에이전틱 AI)]]와 어떤 관계인가요?"라고 질문하게 함으로써 지식의 밀도를 높일 수 있음.
- 복잡한 프로젝트를 작은 이슈로 쪼개는 것은 AI 에이전트가 긴 컨텍스트에서 길을 잃지 않게 하는 가장 실질적인 방법임.

## 후속 액션
- [ ] 현재 사용 중인 Agentic 워크플로우에 'Grill me' 단계 추가 검토.
- [ ] PRD에서 GitHub Issue로 자동 변환하는 프롬프트 템플릿 제작.
