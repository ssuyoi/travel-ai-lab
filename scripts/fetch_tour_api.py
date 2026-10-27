from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
from tour_api_client import RAW_DIR, call_api, save_csv

JEJU_REGN_CODE = "50"
JEJU_SIGNGU_CODE = "110"

RESPONSE_FIELDS = [
    "contentid",
    "title",
    "contenttypeid",
    "addr1",
    "addr2",
    "lDongRegnCd",
    "lDongSignguCd",
    "mapx",
    "mapy",
    "lclsSystm1",
    "lclsSystm2",
    "lclsSystm3",
    "createdtime",
    "modifiedtime",
]

kst_now = datetime.now(ZoneInfo("Asia/Seoul"))
filename = f"area_based_list_{kst_now.date().isoformat()}.csv"


def fetch_tour_api(client: httpx.Client) -> list[dict]:
    page_no = 1

    rows: list[dict] = []

    while True:
        params = {
            "numOfRows": 100,
            "pageNo": page_no,
            "lDongRegnCd": JEJU_REGN_CODE,
            "lDongSignguCd": JEJU_SIGNGU_CODE,
            "arrange": "A",  # 제목순 정렬
            "contentTypeId": "12",  # 관광지만
        }
        data = call_api(client, "areaBasedList2", params)
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
    with httpx.Client(timeout=10.0) as client:
        rows = fetch_tour_api(client)
    save_csv(rows, RAW_DIR / filename, RESPONSE_FIELDS)
    print(f"{len(rows)}건 저장")


if __name__ == "__main__":
    main()
