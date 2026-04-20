---
type: "concept"
created: 2026-04-19
updated: 2026-04-19
tags: ["ai-tech", "retrieval", "context-window"]
---

# RAG (Retrieval-Augmented Generation)

## 정의
검색 증강 생성(Retrieval-Augmented Generation)은 LLM이 사전에 학습된 데이터에만 의존하지 않고, 외부 데이터베이스에서 신뢰할 수 있는 정보를 검색하여 이를 기반으로 답변을 생성하는 기술입니다.

## 유형 및 구현
- **Naive RAG**: 단순히 질문과 유사한 조각을 찾아 모델에 입력.
- **Advanced RAG**: 쿼리 재구성, 하이브리드 검색, 재정렬(Re-ranking) 등을 포함.
- **Native Implementation**: [[Claude Projects]]와 같이 서비스 제공자가 시스템 레벨에서 자동으로 RAG를 가동하는 형태.

## 위키와의 차이점
- **RAG**: 질문 시점에 파편화된 정보를 찾아옴 (동적, 일회성).
- **[[LLM Wiki]]**: 소스 추가 시점에 지식을 종합하여 연결 구조를 만듦 ([[지식 복리 (Knowledge Compounding)]] 중심).

## 관련 페이지
- [[Claude Projects]]
- [[지식 복리 (Knowledge Compounding)]]
- [[LLM Wiki]]
