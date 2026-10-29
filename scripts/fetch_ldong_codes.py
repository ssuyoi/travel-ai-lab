from __future__ import annotations

import httpx
from tour_api_client import RAW_DIR, call_api, save_csv

CODE_FIELDS = ["lDongRegnCd", "lDongRegnNm", "lDongSignguCd", "lDongSignguNm"]


def fetch_ldong_codes(client: httpx.Client) -> list[dict]:
    page_no = 1

    rows: list[dict] = []

    while True:
        params = {
            "numOfRows": 1000,
            "pageNo": page_no,
            "lDongListYn": "Y",
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


def main() -> None:
    with httpx.Client(timeout=10.0) as client:  # Client 재사용 (실험·측정 항목과 연결)
        rows = fetch_ldong_codes(client)
    save_csv(rows, RAW_DIR / "ldong_codes.csv", CODE_FIELDS)
    print(f"{len(rows)}건 저장")


if __name__ == "__main__":
    main()
