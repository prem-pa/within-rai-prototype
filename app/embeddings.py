from __future__ import annotations

from typing import TypedDict

from FlagEmbedding import BGEM3FlagModel

_model: BGEM3FlagModel | None = None


def get_model() -> BGEM3FlagModel:
    global _model
    if _model is None:
        _model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
    return _model


class Embedding(TypedDict):
    dense: list[float]
    sparse: dict  # {"indices": list[int], "values": list[float]}


def embed(texts: list[str]) -> list[Embedding]:
    model = get_model()
    output = model.encode(
        texts,
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=False,
    )
    results: list[Embedding] = []
    for i in range(len(texts)):
        dense_vec = output["dense_vecs"][i].tolist()
        # lexical_weights is a dict {token_id: weight} per sample
        sparse_raw = output["lexical_weights"][i]
        indices = [int(k) for k in sparse_raw.keys()]
        values = [float(v) for v in sparse_raw.values()]
        results.append({"dense": dense_vec, "sparse": {"indices": indices, "values": values}})
    return results
