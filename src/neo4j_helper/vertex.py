from dataclasses import dataclass
from typing import TextIO, Iterable, Optional

import numpy as np

from word2vec_model import Word2VecModel


@dataclass(frozen=True)
class Vertex:
    etymdb_id: int
    language: str
    field: int
    lexeme: str
    meaning: Optional[str] = None
    embedding: Optional[np.ndarray] = None

    def to_neo4j_dict(self) -> dict:
        fields = {
            "etymdb_id:ID": self.etymdb_id,
            "language": self.language,
            "field:int": self.field,
            "lexeme": self.lexeme,
        }

        if self.meaning is not None:
            fields["meaning"] = self.meaning

        if self.embedding is not None:
            fields["embedding:double[]"] = "\t".join(str(x) for x in self.embedding)

        return fields


def _get_language(language_code: str, code_to_lang: dict[str, str]) -> str:
    try:
        return code_to_lang[language_code]
    except KeyError:
        return "Unknown"


def _get_embedding(word: str, model: Word2VecModel) -> Optional[np.ndarray]:
    try:
        return model.get_vector(word)
    except KeyError:
        return None


def parse_vertices(fp: TextIO, code_to_lang: dict[str, str], model: Word2VecModel) -> Iterable[Vertex]:
    for row in fp:
        entries = [e for e in row.rstrip("\n").split("\t") if e != ""]

        match len(entries):
            case 5:
                idx, language_code, field, lexeme, meaning = entries
            case 4:
                idx, language_code, field, lexeme = entries
                meaning = None
            case _:
                continue

        language = _get_language(language_code, code_to_lang)
        embedding = _get_embedding(lexeme, model)

        yield Vertex(
            etymdb_id=int(idx),
            language=language,
            field=int(field),
            lexeme=lexeme,
            meaning=meaning,
            embedding=embedding,
        )
