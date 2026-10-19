# 🛠️ Lab Console 설계

Lab Console은 프롬프트·데이터셋·평가 결과를 **버전으로 관리**하고, 버전끼리 지표를 비교해 **채택 여부를 결정**하는 사내 LLMOps 도구입니다.
『LLMOps를 활용한 LLM 엔지니어링』(박슬기, 위키북스)의 LLMOps 도구 구성을 참고하되, 프레임워크 없이 Lab의 인터페이스 위에 만듭니다.

## 버전별 기능

| 버전 | 기능 | 로드맵 단계 (Notion 주차) |
| --- | --- | --- |
| **v1** | `ops` 스키마 · 데이터셋 등록 · 평가 실행 기록(run manifest) · 평가 worker · 검색 지표 결과 비교 화면 | 2. 검색 (W05 백엔드 · W07 API·worker·화면) |
| **v2** | 프롬프트 버저닝 · Playground · RAG 평가자(faithfulness · context precision) · 토큰·지연·비용 분석 | 3. RAG (W08) |
| **v3** | 합성 데이터셋 생성 → 사람 검수 · CI 품질 게이트 · 운영 대시보드(사용량 · 성능 · injection 탐지) · Langfuse 비교 | 5. 평가·운영 (W12–W13) |

## 구성

```
Next.js (apps/web)  ──HTTP──▶  FastAPI /ops/* (apps/api)  ──▶  PostgreSQL ops 스키마
   화면만 담당                    버전·데이터셋·평가 로직             ▲
                                   │ 평가 실행 요청 (job 등록)        │ 결과 저장
                                   └──────────▶  Eval Worker (apps/worker)
```

- **프론트엔드는 바이브코딩으로 만듭니다.** 이 Lab의 학습 대상은 백엔드·평가·운영이고, 화면은 AI 코딩 도구로 생성합니다.
- 그래서 **모든 로직은 FastAPI에** 두고, 프론트엔드는 API를 호출해 보여주기만 합니다.
- **API 계약이 기준입니다.** FastAPI의 OpenAPI 스키마에서 TypeScript 타입을 생성(`openapi-typescript`)해 프론트엔드가 그 타입만 쓰게 합니다. 프론트 코드 리뷰는 "계약대로 호출하는가"만 봅니다.
- 오래 걸리는 평가는 **worker가 실행**하고(PostgreSQL job 큐, `FOR UPDATE SKIP LOCKED`), 화면은 실행 요청 · 진행 상태 조회 · 결과 비교만 합니다.

## 저장소 (PostgreSQL `ops` 스키마)

서비스 데이터와 같은 DB에 스키마를 따로 둡니다.

| 테이블 | 담는 것 |
| --- | --- |
| `prompts` · `prompt_versions` | 프롬프트 이름, 버전별 템플릿·파라미터·작성 메모 |
| `datasets` · `dataset_items` | 평가셋 버전, 문항(질문 · 정답 문서 ID · 기대 답변 · 유형 · 출처: 수작업/합성) |
| `eval_jobs` | 평가 실행 요청 큐 (상태 · 시작/종료 시각 · 오류) |
| `eval_runs` | 한 번의 평가 실행 + **run manifest**(프롬프트·데이터셋·인덱스·임베딩·모델 버전, git commit) |
| `eval_results` | 문항별 출력 · 지표 점수 · 토큰 · 지연 · 비용 · 실패 태그 |

> run manifest가 있어야 "이 점수가 어떤 조합에서 나왔는가"를 언제든 재현할 수 있습니다.

## 이후

직접 만든 뒤에는 같은 기능을 Langfuse 등 실무 도구와 비교해 실험 노트로 남깁니다.
