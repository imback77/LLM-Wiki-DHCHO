---
type: video-note
title: "Self host Gemma 4: Deploy LLMs on Cloud Run GPUs"
url: http://youtu.be/njWyDHKYeVA
channel: Google Cloud Tech
published: 2026-04-19
created: 2026-04-20
description: Google Cloud Run(GPU) 환경에서 Ollama와 vLLM을 활용하여 오픈 모델인 Gemma 4를 직접 호스팅하고 배포하는 방법을 다루는 핸즈온 튜토리얼
tags:
  - raw/videos
wiki_status: 미처리
---
---

## 핵심 요약
Google Cloud Run(GPU)을 활용하여 오픈 모델인 Gemma 4를 직접 호스팅(Self-hosting)하는 두 가지 방식(Ollama, vLLM)을 비교하고 직접 배포하는 실습 가이드입니다. Ollama는 모델을 컨테이너 이미지에 직접 구워 빠른 초기 구동(Cold start)과 로컬 개발에 유리하며, vLLM은 모델 가중치를 GCS(Google Cloud Storage)에 저장하고 GCS Fuse로 마운트하여 메모리 효율성(Page Attention)과 대규모 프로덕션 서비스에 적합함을 설명합니다.

---

## 주요 내용 (타임스탬프)
- [00:00:30] 엔드투엔드 에이전트 시스템 관리의 4가지 기둥: 비용/용량 최적화, 모델 전략(Open vs Closed), 확장성 있는 서빙, 보안/안전성 및 모니터링 (Observability)
- [00:01:23] **오픈 모델(Gemma) 사용의 이점:** 온프레미스/격리 환경 구축 가능(보안), 도메인 특화 데이터 파인튜닝, 인프라 기반의 예측 가능한 비용 구조
- [00:04:32] **Ollama vs vLLM 비교:** Ollama는 설치가 쉽고 다중 GPU를 지원해 개발/PoC에 적합하며, vLLM은 Page Attention과 동적 배치를 지원해 메모리 효율성이 뛰어나 프로덕션(Production) 환경에 적합함
- [00:05:33] **Ollama 기반 배포 파이프라인:** Ollama에서 모델(Gemma 4)을 Pull -> Docker 이미지 빌드(모델 내장) -> Artifact Registry 푸시 -> Cloud Run 배포
- [00:25:49] **vLLM 기반 배포 파이프라인:** Hugging Face에서 모델 가중치를 GCS로 다운로드 -> vLLM 코드만 있는 가벼운 Docker 이미지 빌드 -> Cloud Run 배포 -> GCS Fuse를 통해 버킷을 로컬 폴더로 마운트하여 모델 로드

---

## 나의 생각·코멘트
오픈 모델을 서비스 환경에 올릴 때 단순히 컨테이너에 다 때려 넣는 방식(Ollama)과 클라우드 스토리지를 마운트해서 코어 엔진만 가볍게 배포하는 방식(vLLM + GCS Fuse)의 차이를 명확히 알 수 있었다. 특히 vLLM 방식은 이미지를 다시 빌드하지 않고 GCS 버킷의 가중치 파일만 교체해도 모델 업데이트가 가능하다는 점이 프로덕션 환경에서 매우 큰 장점으로 작용할 것 같다. 향후 LLM Wiki에 연동할 자체 AI 에이전트를 구축할 때 이 배포 전략을 참고하면 좋을 것 같다.

## 관련 키워드
[[Cloud Run]], [[Gemma 4]], [[Ollama]], [[vLLM]], [[GCS Fuse]], [[LLM 배포]], [[AI 에이전트]]