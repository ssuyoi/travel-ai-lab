import argparse
import json
import os
import time

import anthropic
from anthropic.types.beta import BetaMessage
from dotenv import load_dotenv
from tour_api_client import RAW_DIR, log_latency

MODEL = "claude-sonnet-5-5"
SYSTEM_PROMPT = "너는 여행 안내 문구를 쓰는 편집자다. 3문장 이내, 존댓말로 적는다."

load_dotenv()
LLM_API_KEY = os.getenv("LLM_API_KEY")
if not LLM_API_KEY:
    raise RuntimeError("LLM API 키가 설정되지 않았습니다.")


def load_overview(content_id: str) -> str:
    path = RAW_DIR / "detail_common" / f"{content_id}.json"
    if not path.exists():
        raise SystemExit(
            f"{path} 파일이 없습니다. 먼저 실행: "
            f"uv run python scripts/fetch_tour_detail.py {content_id}"
        )

    with path.open("r", encoding="utf-8") as f:
        detail = json.load(f)

    overview = (detail.get("overview") or "").strip()
    if not overview:
        raise SystemExit(
            f"contentid={content_id}: overview가 비어 있어 요약할 수 없습니다."
        )
    return overview


def call_llm(client: anthropic.Anthropic, overview: str) -> BetaMessage:
    status_code, result_code = None, None  # 응답을 못 받은 경우의 기본값
    start = time.perf_counter()
    try:
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=1024,
            output_config={"effort": "low"},
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"다음 장소 설명을 3문장으로 요약해줘.\n\n{overview}",
                }
            ],
            # 안전 분류기가 거절(refusal)하면 서버가 다른 모델로 다시 시도한다
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
        status_code, result_code = 200, response.stop_reason
        return response
    except anthropic.APIStatusError as e:
        status_code = e.status_code
        if e.status_code == 401:
            print("[401 Unauthorized] LLM API 키를 확인하세요.")
        elif e.status_code == 429:
            print(
                "[429 Too Many Requests] 호출 한도를 초과했습니다. 잠시 후 다시 시도하세요."
            )
        elif e.status_code >= 500:
            print(f"[{e.status_code} Server Error] LLM 서버가 정상 응답하지 않습니다.")
        else:
            print(f"[{e.status_code}] LLM API 요청이 실패했습니다.")
        raise
    except anthropic.APIConnectionError:
        print("[연결 오류] 네트워크 또는 요청 설정을 확인하세요.")
        raise
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        log_latency("claude.messages", status_code, result_code, elapsed_ms)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("content_id", type=str, help="요약할 contentid")
    args = parser.parse_args()

    overview = load_overview(args.content_id)

    # 측정값에 SDK 자동 재시도 시간이 섞이지 않도록 재시도를 끈다
    client = anthropic.Anthropic(api_key=LLM_API_KEY, max_retries=0)
    response = call_llm(client, overview)

    if response.stop_reason != "end_turn":
        print(f"[LLM] 비정상 종료: stop_reason={response.stop_reason}")

    summary = next((b.text for b in response.content if b.type == "text"), None)
    if summary is None:
        raise SystemExit("응답에 텍스트가 없습니다.")

    print(summary)
    print(
        f"(model={response.model}, "
        f"input={response.usage.input_tokens}, output={response.usage.output_tokens} tokens)"
    )


if __name__ == "__main__":
    main()
