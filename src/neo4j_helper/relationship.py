from dataclasses import dataclass
from typing import TextIO, ClassVar, Iterable


@dataclass(frozen=True)
class Relationship:
    relation: str
    child: int
    parent: int

    def to_neo4j_dict(self) -> dict:
        return {
            ":TYPE": self.relation,
            ":START_ID": self.child,
            ":END_ID": self.parent,
        }


def parse_relationships(text: TextIO) -> Iterable[Relationship]:
    _relation_code_to_relation: dict[str, str] = {
        "inh": "INHERITS_FROM",
        "bor": "BORROWS_FROM",
        "cog": "COGNATE_TO",
        "der": "der",
        "der(s)": "der_s",
        "der(p)": "der_p",
        "cmpd+bor": "cmpd_bor",
    }

    for row in text.readlines():
        relation_code, child, parent = row.rstrip("\n").split("\t")
        yield Relationship(
            relation=_relation_code_to_relation[relation_code],
            child=int(child),
            parent=int(parent),
        )
