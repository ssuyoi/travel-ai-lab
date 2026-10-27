import argparse
import json
from pathlib import Path

import httpx
from tour_api_client import RAW_DIR, call_api


def fetch_tour_detail(client: httpx.Client, content_id: str) -> dict:
    params = {"contentId": content_id}
    data = call_api(client, "detailCommon2", params)
    items = data["response"]["body"]["items"]

    if not items:
        raise ValueError(f"contentId={content_id}에 해당하는 상세 정보가 없습니다.")

    item = items["item"][0]
    return item


def save_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("content_id", type=str, help="조회할 contentid")
    args = parser.parse_args()

    with httpx.Client(timeout=10.0) as client:
        content_id = args.content_id
        item = fetch_tour_detail(client, content_id)
    save_json(item, RAW_DIR / "detail_common" / f"{content_id}.json")
    print(f"{content_id} 상세 정보 저장")


if __name__ == "__main__":
    main()
