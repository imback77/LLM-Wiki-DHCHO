---
type: "concept"
created: 2026-04-19
updated: 2026-04-19
tags: ["development", "qa", "ai-workflow"]
---

# TDD (Test-Driven Development, 테스트 주도 개발)

## 정의
실제 코드를 작성하기 전에 해당 코드가 통과해야 할 테스트 케이스를 먼저 작성하고, 그 테스트를 통과하기 위한 최소한의 코드를 작성한 뒤 리팩토링하는 소프트웨어 개발 방법론입니다.

## AI 에이전트 시대의 TDD
[[Agentic AI]]나 [[Claude Code]]와 같은 도구를 사용할 때 TDD는 선택이 아닌 필수적인 품질 보장 장치로 부상하고 있습니다.

### 이유
1. **환각(Hallucination) 방지**: AI가 작성한 코드가 의도대로 작동하는지 테스트를 통해 즉각 검증 가능.
2. **인터페이스 선설계**: 코드를 짜기 전 테스트를 먼저 짜게 함으로써 AI가 인터페이스의 사용성과 구조를 먼저 고민하게 만듦.
3. **자동 피드백 루프**: 테스트가 실패하면 AI는 에러 메시지를 보고 스스로 코드를 수정하는 'Self-healing' 프로세스를 수행할 수 있음.

## 관련 페이지
- [[Agentic AI]]
- [[Claude Code]]
- [[2026-04-19_Matt_Pocock_Claude_Code_Skills]]
