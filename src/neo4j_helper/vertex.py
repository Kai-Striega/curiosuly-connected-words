from dataclasses import dataclass
from typing import TextIO, Iterable, Optional


@dataclass(frozen=True)
class Vertex:
    etymdb_id: int
    language: str
    field: int
    lexeme: str
    meaning: Optional[str] = None

    def to_neo4j_dict(self) -> dict:
        fields = {
            "etymdb_id:ID": self.etymdb_id,
            "language": self.language,
            "field:int": self.field,
            "lexeme": self.lexeme,
        }

        if self.meaning is not None:
            fields["meaning"] = self.meaning

        return fields


def _get_language(language_code: str, code_to_lang: dict[str, str]) -> str:
    try:
        return code_to_lang[language_code]
    except KeyError:
        return "Unknown"


def parse_vertices(fp: TextIO, code_to_lang: dict[str, str]) -> Iterable[Vertex]:
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
        yield Vertex(
            etymdb_id=int(idx),
            language=language,
            field=int(field),
            lexeme=lexeme,
            meaning=meaning,
        )
