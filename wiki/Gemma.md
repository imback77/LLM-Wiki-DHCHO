---
type: entity
name: Gemma
tags: [google, open-source, llm, sllm]
---

# 💎 Gemma

## 📋 소개 (Overview)
Gemma는 구글과 구글 딥마인드([[Google DeepMind]])가 개발한 오픈소스 대규모 언어 모델(LLM) 시리즈입니다. 구글의 플래그십 모델인 제미나이([[Gemini]])를 개발하는 데 사용된 동일한 기술과 아키텍처를 기반으로 제작되었습니다.

---

## 🚀 주요 버전 및 특징

### Gemma 4 (2026 출시)
최근 출시된 최신 버전으로, 경량화된 가중치에도 불구하고 논리 추론 및 수학 능력에서 이전 세대 대비 비약적인 향상을 보였습니다. 특히 로컬 호스팅 및 서버리스 환경 배포에 최적화되어 있습니다.

### 배포 및 운영 전략
- **Ollama**: 로컬 실행 및 모델 내장 Docker 이미지 배포에 적합.
- **vLLM + GCS Fuse**: 대규모 프로덕션 환경에서 모델 가중치를 외부 스토리지(GCS)에 두고 동적으로 로드하여 효율성 극대화.
- **상세 가이드**: [[2026-04-19_PwC_AI_Performance_Gap_Study]]

---

## 🔗 관련 페이지
- [[Gemini]]
- [[Google DeepMind]]
- [[2026-04-19_PwC_AI_Performance_Gap_Study]]
- [[AI 인프라 레이스]]
