# 🗺️ AI Engineering 기술 지도

LLM 애플리케이션을 구성하는 **개념별로**, 이 Lab에서 쓰는 기술과 **같은 역할을 하는 대안**을 정리한 문서입니다.
"이 기능은 보통 이런 도구들로 하는구나"를 파악하고, 공고나 글에서 처음 보는 이름이 어느 칸에 속하는지 찾는 용도로 씁니다.

| 표시 | 의미 |
| --- | --- |
| ✅ | 이 Lab에서 사용 |
| 🔍 | 비교 실험 후보 (실험 노트로 결과 기록) |
| 📚 | 직접 쓰지 않지만 개념·위치를 알아둘 것 |

> 도구는 빠르게 바뀝니다. 이름보다 **"이 칸이 해결하는 문제"** 를 기준으로 읽고, 도입 전에는 공식 문서로 현재 상태를 확인합니다.

---

## 1. 모델 호출 · 서빙

| 개념 | 하는 일 | 기술 |
| --- | --- | --- |
| **LLM API** | 상용 모델을 HTTP로 호출 | ✅ 상용 LLM API 1–2곳 · 📚 OpenAI · Anthropic · Google Gemini · Mistral |
| **로컬 실행** | 오픈 웨이트 모델을 내 PC에서 실행 | 🔍 Ollama · 📚 llama.cpp · LM Studio |
| **추론 서버** | GPU에서 여러 요청을 효율적으로 처리 (배칭·KV cache) | 📚 vLLM · SGLang · TGI · TensorRT-LLM |
| **모델 게이트웨이·라우팅** | 여러 공급자를 하나의 인터페이스로, 폴백·비용 제어 | ✅ 직접 구현 `LLMProvider` · 🔍 LiteLLM · 📚 OpenRouter · Portkey |
| **구조화 출력** | LLM 응답을 스키마에 맞는 JSON으로 | ✅ Pydantic + 공급자 structured output · 🔍 Instructor · 📚 Outlines |
| **프롬프트 캐싱** | 반복되는 프롬프트 앞부분 재사용으로 지연·비용 절감 | ✅ 공급자 기능 · 📚 응답 캐시(Redis) · semantic cache |

## 2. 데이터 수집 · 문서 처리

| 개념 | 하는 일 | 기술 |
| --- | --- | --- |
| **HTTP 수집** | 외부 API에서 데이터 가져오기 | ✅ httpx (+ asyncio) · 📚 requests · aiohttp |
| **문서 파싱** | PDF·HTML·오피스 문서를 텍스트·구조로 | 📚 PyMuPDF · Docling · Unstructured · BeautifulSoup |
| **데이터 검증** | 스키마·품질 규칙 확인 | ✅ Pydantic · 📚 Great Expectations · Pandera |
| **파이프라인 스케줄링** | 주기적 수집·재색인 자동화 | ✅ GitHub Actions(스케줄) · 📚 Airflow · Prefect · Dagster |
| **Chunking** | 문서를 검색 단위로 분할 | ✅ 직접 구현 · 📚 LangChain·LlamaIndex text splitter |

## 3. 검색 (Retrieval)

| 개념 | 하는 일 | 기술 |
| --- | --- | --- |
| **키워드 검색 (Lexical)** | 단어 일치 기반 검색, BM25 점수 | ✅ PostgreSQL FTS · 🔍 Elasticsearch/OpenSearch · 📚 rank_bm25 · Tantivy |
| **한국어 형태소 분석** | "애월읍에서" → "애월읍" 처럼 쪼개 키워드 검색 정확도 향상 | 🔍 Kiwi · nori(ES 플러그인) · 📚 MeCab-ko · Okt |
| **임베딩 모델** | 문장을 의미 벡터로 | 🔍 상용 임베딩 API · bge-m3 · KURE · 📚 multilingual-e5 · Cohere · Voyage · Jina |
| **벡터 저장·검색** | 비슷한 벡터를 빠르게 찾기 (ANN · HNSW) | ✅ pgvector · 📚 Qdrant · Milvus · Weaviate · Chroma · Pinecone · LanceDB · FAISS(라이브러리) |
| **하이브리드 결합** | 키워드 + 벡터 점수 합치기 | ✅ 직접 구현 (α 가중합 · RRF) · 📚 ES·Qdrant·Weaviate 내장 하이브리드 |
| **리랭킹** | 상위 후보를 더 정밀한 모델로 재정렬 | 🔍 bge-reranker 계열 cross-encoder · 📚 Cohere Rerank · Jina Reranker · ColBERT |
| **질의 변환** | 질문을 검색하기 좋게 바꾸기 | 🔍 query rewriting · 📚 HyDE · multi-query |
| **지식 그래프** | 엔티티 간 관계로 검색 (장소–지역–테마) | 📚 Neo4j · GraphRAG |

## 4. 생성 · 오케스트레이션 · Agent

| 개념 | 하는 일 | 기술 |
| --- | --- | --- |
| **RAG 프레임워크** | 검색 → 프롬프트 → 생성 흐름을 구성 | ✅ 직접 구현 · 📚 LlamaIndex · LangChain · Haystack |
| **Agent 오케스트레이션** | 상태·분기·반복이 있는 LLM 워크플로우 | ✅ 직접 구현 agent loop · 🔍 LangGraph · 📚 PydanticAI · OpenAI Agents SDK · Claude Agent SDK · CrewAI |
| **Tool calling** | LLM이 함수를 골라 호출 | ✅ 공급자 function calling |
| **도구 표준 프로토콜** | 도구·데이터 소스를 표준 방식으로 노출 | 🔍 MCP (Model Context Protocol) · 📚 A2A |
| **프롬프트 최적화** | 프롬프트·예시를 자동으로 개선 | 📚 DSPy |
| **Text-to-SQL** | 자연어 질문을 SQL로 | 🔍 직접 구현 (스키마 + few-shot) · 📚 Vanna |

## 5. 평가 (Evaluation)

| 개념 | 하는 일 | 기술 |
| --- | --- | --- |
| **검색 지표** | Recall@k · MRR · nDCG 계산 | ✅ 직접 구현 · 🔍 ranx · 📚 MTEB(임베딩 벤치마크) |
| **RAG 품질 지표** | Faithfulness · Answer relevancy · Context precision/recall | ✅ 직접 구현 judge · 🔍 Ragas · 📚 DeepEval · TruLens |
| **평가 하네스** | 테스트 케이스를 반복 실행·비교·리포트 | ✅ 직접 구현 eval runner + pytest · 🔍 promptfoo · 📚 Inspect · OpenAI Evals |
| **통계** | 신뢰구간 · 유의성 · 판정자 일치도 | ✅ scipy(`bootstrap`) · scikit-learn(`cohen_kappa_score`) |
| **Agent 벤치마크** | 도구 사용 신뢰성 측정 방식 참고 | 📚 τ-bench(pass^k) · BFCL(Berkeley Function Calling Leaderboard) |

## 6. 관측 · 운영 (LLMOps)

| 개념 | 하는 일 | 기술 |
| --- | --- | --- |
| **호출 로깅** | 모델·프롬프트 버전·토큰·지연·비용 기록 | ✅ 구조화 JSONL 로그 |
| **트레이싱** | 한 요청 안의 검색·LLM·도구 단계를 이어서 보기 | 🔍 OpenTelemetry · Langfuse · 📚 LangSmith · Arize Phoenix · Helicone |
| **프롬프트 관리** | 프롬프트 버전·배포·A/B | ✅ Lab Console (PostgreSQL `ops` 스키마) · 🔍 Langfuse · 📚 LangSmith prompt hub |
| **평가 데이터셋 관리** | 평가셋 버전·문항 관리, 합성 문항 생성·검수 | ✅ Lab Console · 🔍 Ragas testset generation · 📚 Langfuse datasets · LangSmith datasets |
| **실험 추적** | 실험 설정·결과 비교 | ✅ 실험 노트 + Console 평가 기록(run manifest) · 📚 MLflow · Weights & Biases |
| **부하 테스트** | 동시 요청에서의 처리량·지연 | 🔍 locust · k6 |
| **모니터링** | 지표 대시보드·알림 | 📚 Prometheus · Grafana |

## 7. 안전 (Safety · Guardrails)

| 개념 | 하는 일 | 기술 |
| --- | --- | --- |
| **입출력 검사** | 위험한 입력·출력 차단, 형식 강제 | ✅ 직접 구현 규칙 + 스키마 검증 · 📚 Guardrails AI · NeMo Guardrails |
| **안전 분류 모델** | 유해 콘텐츠·탈옥 시도 분류 | 📚 Llama Guard · 공급자 moderation API |
| **개인정보 탐지** | PII 탐지·마스킹 | 📚 Microsoft Presidio |
| **레드팀 테스트** | 공격 시나리오 자동 생성·실행 | 🔍 직접 만든 공격 셋 · 📚 promptfoo red teaming · garak |

## 8. 애플리케이션 · 인프라

| 개념 | 하는 일 | 기술 |
| --- | --- | --- |
| **API 서버** | 검색·질의응답 엔드포인트 | ✅ FastAPI · 📚 Flask · Spring Boot(Java/Kotlin 팀) |
| **데모 UI** | 빠른 채팅·검색 화면 | ✅ Streamlit · 📚 Gradio · Chainlit · Next.js + Vercel AI SDK |
| **스트리밍 전송** | 토큰을 실시간으로 화면에 | ✅ SSE · 📚 WebSocket |
| **컨테이너·배포** | 실행 환경 재현·배포 | ✅ Docker · Docker Compose · 📚 Kubernetes · Cloud Run · Fly.io |
| **CI/CD** | 테스트·린트·평가 자동 실행 | ✅ GitHub Actions · 📚 Argo CD |
| **개발 도구** | 패키지·린트·타입·테스트 | ✅ uv · Ruff · Pyright · pytest · pre-commit |

## 9. 모델 커스터마이징 (심화)

| 개념 | 하는 일 | 기술 |
| --- | --- | --- |
| **임베딩 파인튜닝** | 도메인 데이터로 검색 품질 개선 | 🔍 sentence-transformers 학습 |
| **LLM 파인튜닝** | 특정 형식·도메인에 맞게 모델 조정 | 📚 Hugging Face TRL · PEFT(LoRA) · Unsloth · 공급자 fine-tuning API |
| **양자화** | 모델을 작게·빠르게 | 📚 GGUF(llama.cpp) · bitsandbytes · AWQ · GPTQ |

---

## 고르는 기준

새 기술을 볼 때 이 Lab에서는 다음 순서로 판단합니다.

1. **어느 칸의 문제를 푸는가?** — 위 표에서 위치를 먼저 찾는다.
2. **지금 직접 구현으로 부족한가?** — 부족함을 지표로 보여줄 수 있을 때 도입을 검토한다.
3. **같은 평가셋으로 비교했는가?** — 도입 전후를 품질·지연·비용으로 비교하고 실험 노트로 남긴다.
4. **빼기 쉬운가?** — 인터페이스 뒤에 두어 나중에 교체할 수 있게 한다.
