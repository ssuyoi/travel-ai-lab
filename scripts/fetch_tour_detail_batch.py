import argparse
import csv
import json
import os
from pathlib import Path

import httpx
from fetch_tour_detail import fetch_tour_detail, save_json
from tour_api_client import RAW_DIR

CONTENT_PATH = RAW_DIR / "area_based_list_2026-10-27.csv"


def load_or_fetch_detail(client: httpx.Client, content_id: str) -> dict:
    file = RAW_DIR / "detail_common" / f"{content_id}.json"

    if os.path.exists(file):
        with file.open(encoding="utf-8") as f:
            return json.load(f)

    item = fetch_tour_detail(client, content_id)
    save_json(item, file)
    print(f"{content_id} 상세 정보 저장")
    return item


def load_content_ids(path: Path) -> list[str]:
    with path.open(encoding="utf-8") as f:
        return [row["contentid"] for row in csv.DictReader(f)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("count", type=int, help="조회할 관광지 갯수")
    args = parser.parse_args()
    max_count = args.count
    count = 0
    failures: list[tuple[str, str]] = []

    content_ids = load_content_ids(CONTENT_PATH)

    with httpx.Client(timeout=10.0) as client:
        for content_id in content_ids:
            try:
                item = load_or_fetch_detail(client, content_id)
            except (ValueError, RuntimeError, httpx.RequestError) as e:
                print(f"{content_id} 실패: {e}")
                failures.append((content_id, str(e)))
                continue

            if item.get("overview"):
                count += 1

            if count >= max_count:
                break

    print(f"관광지 상세정보 {count}개 저장, 실패 {len(failures)}건")


if __name__ == "__main__":
    main()
