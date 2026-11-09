import json

from fetch_tour_detail_batch import DETAIL_DIR
from tour_api_client import RAW_DIR

DOCS_PATH = RAW_DIR / "baseline_docs.jsonl"


def build_doc(item: dict) -> dict:
    text = f"{item['title']}\n{item['addr1']}\n{item['overview']}"
    return {"contentid": item["contentid"], "title": item["title"], "text": text}


def load_details() -> list[dict]:
    details = []
    for path in sorted(DETAIL_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as f:
            details.append(json.load(f))
    return details


def main() -> None:
    docs = [build_doc(item) for item in load_details() if item.get("overview")]

    with DOCS_PATH.open("w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(f"문서 {len(docs)}개 저장: {DOCS_PATH}")


if __name__ == "__main__":
    main()
