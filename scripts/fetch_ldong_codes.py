from __future__ import annotations

import csv
from datetime import datetime
import os
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "tour_api"
LOG_DIR = ROOT / "logs"
BASE_URL = "https://apis.data.go.kr/B551011/KorService2"
LATENCY_CSV = LOG_DIR / "latency.csv"

LATENCY_FIELDS = ["timestamp", "operation", "status_code", "result_code", "elapsed_ms"]
CODE_FIELDS = ["lDongRegnCd", "lDongRegnNm", "lDongSignguCd", "lDongSignguNm"]

load_dotenv()
DATA_KEY = os.getenv("TOUR_API_KEY")
if not DATA_KEY:
    raise RuntimeError("TOUR API 키가 설정되지 않았습니다.")


def call_api(client: httpx.Client, operation: str, params: dict) -> dict:
    start = time.perf_counter()

    try:
        resp = client.get(f"{BASE_URL}/{operation}", params=params)
    except httpx.RequestError as e:
        log_latency(operation, None, None, (time.perf_counter() - start) * 1000)
        raise

    elapsed_ms = (time.perf_counter() - start) * 1000

    # HTTP 실패
    if not resp.is_success:
        status_code = resp.status_code
        log_latency(operation, status_code, None, elapsed_ms)
        if status_code == 401:
            print("[401 Unauthorized] 인증정보가 잘못되었습니다.")
        elif status_code == 429:
            print("[429 Too Many Requests] 요청 횟수를 초과했습니다. 잠시 후 다시 시도해주세요.")
        elif status_code >= 500:
            print("[Server Error] 서버가 정상 응답하지 않습니다. 잠시 후 다시 시도해주세요.")
        else:
            print(f"[{status_code}] 요청이 실패했습니다.")
        resp.raise_for_status()

    # HTTP 성공, 본문 타입 확인
    try:
        data = resp.json()
        result_code = data["response"]["header"]["resultCode"]
    except (ValueError, KeyError):
        data, result_code = None, "NON_JSON"
        print("반환 타입이 JSON이 아닙니다.")
    log_latency(operation, resp.status_code, result_code, elapsed_ms)

    # API 실패
    if data is None or result_code != "0000":
        print(f"[API Error] status={resp.status_code}, result code={result_code}")
        raise RuntimeError(f"{operation} 실패: resultCode={result_code}")

    return data


def log_latency(operation: str, status_code: int|None, result_code: str|None, elapsed_ms: float) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    is_new = not LATENCY_CSV.exists()
    with LATENCY_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LATENCY_FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "operation": operation,
            "status_code": status_code,
            "result_code": result_code,
            "elapsed_ms": round(elapsed_ms, 1),
        })


def fetch_ldong_codes(client: httpx.Client) -> list[dict]:
    page_no = 1

    rows: list[dict] = []

    while True:
        params = {
            "numOfRows":1000,
            "pageNo":page_no,
            "MobileOS":"ETC",
            "MobileApp":"TravelAI",
            "serviceKey":DATA_KEY,
            "_type":"json",
            "lDongListYn":"Y",
        }
        data = call_api(client, "ldongCode2", params)
        body = data["response"]["body"]

        items = body["items"]
        if not items:
            break
        item = items["item"]
        rows.extend(item)

        if len(rows) >= body["totalCount"]:
            break
        page_no += 1

    return rows


def save_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CODE_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    with httpx.Client(timeout=10.0) as client:   # Client 재사용 (실험·측정 항목과 연결)
        rows = fetch_ldong_codes(client)
    save_csv(rows, RAW_DIR / "ldong_codes.csv")
    print(f"{len(rows)}건 저장")


if __name__ == "__main__":
    main()