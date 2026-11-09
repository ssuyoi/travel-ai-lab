import json
from pathlib import Path

import numpy as np
from build_baseline_docs import DOCS_PATH
from dotenv import load_dotenv
from openai import OpenAI
from tour_api_client import ROOT

MODEL = "text-embedding-3-small"
EMBEDDINGS_PATH = ROOT / "data" / "processed" / "baseline_embeddings.npy"


def load_texts(path: Path) -> list[str]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line)["text"] for line in f]


def main() -> None:
    if EMBEDDINGS_PATH.exists():
        print(f"{EMBEDDINGS_PATH}가 이미 있습니다.")
        return

    load_dotenv()
    texts = load_texts(DOCS_PATH)

    client = OpenAI()
    response = client.embeddings.create(input=texts, model=MODEL)

    vectors = [item.embedding for item in response.data]
    embeddings = np.array(vectors, dtype=np.float32)
    EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.save(EMBEDDINGS_PATH, embeddings)

    print(f"shape={embeddings.shape}, 토큰={response.usage.total_tokens}")


if __name__ == "__main__":
    main()
