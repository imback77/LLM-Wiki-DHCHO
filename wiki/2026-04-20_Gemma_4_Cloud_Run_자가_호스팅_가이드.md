---
type: summary
created: 2026-04-21
updated: 2026-04-21
sources: ["raw/videos/2026-04-20_Self host Gemma 4 Deploy LLMs on Cloud Run GPUs_Google Cloud Tech.md"]
tags: [Gemma4, GoogleCloud, CloudRun, Ollama, vLLM, Deployment, Infra]
---

# 구글 클라우드(Cloud Run) 기반 Gemma 4 자가 호스팅 가이드

Google Cloud Run(GPU) 환경에서 오픈 모델인 [[Gemma]]를 직접 호스팅하고 배포하기 위한 두 가지 핵심 전략(Ollama vs vLLM)과 실전 파이프라인을 다룹니다.

## 🚀 배포 전략 비교: Ollama vs vLLM

| 특성 | **Ollama (이미지 내장형)** | **vLLM (스토리지 마운트형)** |
| :--- | :--- | :--- |
| **적합한 환경** | 개발, PoC, 로컬 테스트 | 프로덕션(Production), 대규모 서비스 |
| **모델 저장소** | Docker 컨테이너 이미지 내부 | Google Cloud Storage (GCS) |
| **장점** | 초기 구동(Cold Start) 속도 우수 | 메모리 효율(Page Attention), 유지보수 용이 |
| **업대이트** | 컨테이너 이미지 전체 재빌드 필요 | GCS 버킷 내 가중치 파일만 교체 가능 |

## 🛠️ 실전 배포 파이프라인

### 1. Ollama 방식 (사전 패키징)
- **과정**: Ollama 서버 설치 ➔ `Ollama Pull gemma4` ➔ 모델이 포함된 Docker 이미지 빌드 ➔ Artifact Registry 푸시 ➔ Cloud Run GPU 배포.
- **인사이트**: 모델 가중치가 이미지에 포함되어 있어 배포 직후 즉각적인 서비스가 가능합니다.

### 2. vLLM + GCS Fuse 방식 (유연한 확장)
- **과정**: Hugging Face 가중치를 GCS 버킷에 업로드 ➔ vLLM 코어 엔진만 담긴 경량 Docker 이미지 빌드 ➔ Cloud Run 배포 ➔ **GCS Fuse**를 통해 버킷을 로컬 폴더로 마운트하여 모델 로드.
- **인사이트**: **GCS Fuse**를 활용하면 수십 GB의 모델 가중치를 컨테이너 이미지에 넣지 않고도 로컬 파일처럼 접근할 수 있어 배포 유연성이 극대화됩니다.

## 💡 에이전틱 시스템의 4가지 기둥
이 튜토리얼에서는 성공적인 [[Agentic AI (에이전틱 AI)]] 관리를 위해 다음 4가지를 강조합니다:
1. **비용/용량 최적화**: 사용량에 따라 GPU 자원을 할당하는 Serverless(Cloud Run) 활용.
2. **모델 전략**: 보안이 중요한 데이터는 오픈 모델(Gemma)로 처리.
3. **확장성 있는 서빙**: vLLM 등의 고성능 인퍼런스 엔진 사용.
4. **관측 가능성(Observability)**: 모델 응답 속도 및 자원 소모 실시간 모니터링.

## 🔗 연관 지식
- [[Gemma 4 (젬마 4)]] - 최신 오픈소스 모델 엔티티
- [[2026-04-20_Gemma_4_Cloud_Run_자가_호스팅_가이드]] - 구글의 서버리스 컨테이너 서비스
- [[AI 인프라 레이스]] - 기업의 독자적 호스팅 환경 구축 트렌드
- [[Ollama]] / [[vLLM]]

---
> 출처: [[Gemma|Google Cloud Tech 핸즈온 튜토리얼 (2026-04-20)]]
