---
type: summary
created: 2026-04-20
updated: 2026-04-22
sources: ["raw/videos/2026-04-20_Self host Gemma 4 Deploy LLMs on Cloud Run GPUs_Google Cloud Tech.md"]
tags: ["tutorial", "gemma4", "cloud-run", "deployment"]
---

# Gemma 4: Cloud Run 자가 호스팅 가이드

Google Cloud Run(GPU) 환경에서 오픈 모델인 **[[Gemma 4 (젬마 4)]]**를 직접 호스팅하고 배포하는 전략을 정리한 기술 가이드입니다.

---

## 🏗️ 핵심 아키텍처 비교

이 가이드는 배포 환경의 목적에 따라 **[[Ollama]]**와 **[[vLLM]]** 두 가지 서빙 엔진 활용법을 제시합니다.

| 비교 항목 | **[[Ollama]]** | **[[vLLM]]** |
| :--- | :--- | :--- |
| **적합한 환경** | 개발, 시뮬레이션, PoC | 실제 서비스 생산(Production) |
| **모델 관리** | 컨테이너 이미지 내에 모델 가중치 포함 | GCS 버킷에 보관 후 GCS Fuse로 마운트 |
| **특징** | 설치 및 빌드가 매우 간단함 | Page Attention 기술로 메모리 효율 최적화 |
| **장점** | 초기 구동(Cold Start) 속도가 빠름 | 이미지 재빌드 없이 모델 가중치만 교체 가능 |

---

## 🛠️ 서빙 기술 핵심 요약

### 1. Ollama 기반 배포 (Quick & Simple)
- 모델을 Docker 이미지 빌드 단계에서 `pull`하여 내장하는 방식입니다.
- **아티팩트 레지스트리(Artifact Registry)**에 푸시 후 Cloud Run GPU 인스턴스에 즉시 배포 가능합니다.

### 2. vLLM + GCS Fuse 기반 배포 (Efficient & Scale)
- **[[vLLM]]** 엔진만 포함된 가벼운 이미지를 사용합니다.
- 모델 가중치는 GCS(Google Cloud Storage)에 저장하고, **GCS Fuse**를 통해 런타임 시 로컬 파일 시스템처럼 마운트하여 읽어옵니다.
- 동적 배치(Dynamic Batching)를 지원하여 다중 요청 처리 성능이 뛰어납니다.

---

## 💡 인사이트 (후니님의 맥락 메모)
오픈 모델을 서비스 환경에 올릴 때 엔진(Core)과 가중치(Weight)를 분리하여 관리하는 **vLLM + GCS Fuse** 방식이 실무적으로 훨씬 유연합니다. 모델 업데이트 시 대용량 이미지를 다시 빌드하고 푸시할 필요 없이 GCS 버킷의 파일만 교체하면 되기 때문입니다. 향후 위키용 자체 에이전트 구축 시 이 전략을 기본 채택할 예정입니다.

---

## 🔗 연관 지식
- [[Gemma 4 (젬마 4)]]
- [[Google Cloud]]
- [[Agentic AI (에이전틱 AI)]]
- [[Cloud Run]]
