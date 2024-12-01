import csv
from collections import defaultdict
from pathlib import Path

import click

from vertex import parse_vertices
from relationship import parse_relationships
from code_to_langs import WIKI_CODE_TO_LANG
from word2vec_model import load_gensim_model

CSV_HEADER_FILENAMES = {
    frozenset(["etymdb_id:ID", "language", "field:int", "lexeme", ":LABEL"]): "small",
    frozenset(["etymdb_id:ID", "language", "field:int", "lexeme", "meaning", ":LABEL"]): "with_meaning",
    frozenset(["etymdb_id:ID", "language", "field:int", "lexeme", "embedding:double[]", ":LABEL"]): "with_embedding",
    frozenset(["etymdb_id:ID", "language", "field:int", "lexeme", "meaning", "embedding:double[]", ":LABEL"]): "full",
}

MODEL = load_gensim_model("glove-twitter-200")


@click.group()
def cli():
    pass

@cli.command()
@click.argument("etymdb-path", type=click.Path(exists=True))
@click.argument("outdir", type=click.Path(exists=True))
def dump_vertices_as_csv(etymdb_path: str, outdir: str):
    etymdb_vertices_path = Path(etymdb_path) / "etymdb_values.csv"

    csv_vertex_groups = defaultdict(list)
    with open(etymdb_vertices_path) as fp:
        for vertex in parse_vertices(fp, WIKI_CODE_TO_LANG, MODEL):
            row_values = vertex.to_neo4j_dict() | {":LABEL": "Lexeme"}
            row_key = frozenset(row_values.keys())
            csv_vertex_groups[row_key].append(row_values)

    for header, file_suffix in CSV_HEADER_FILENAMES.items():
        filename = Path(outdir) / "neo4j_import_data"/ "vertex" / f"{file_suffix}.csv"

        if not filename.exists():
            filename.parent.mkdir(parents=True, exist_ok=True)

        with open(filename, "w+") as fp:
            csv_writer = csv.DictWriter(fp, header)
            csv_writer.writeheader()

            for row_values in csv_vertex_groups[header]:
                csv_writer.writerow(row_values)




@cli.command()
@click.argument("etymdb-path", type=click.Path(exists=True))
@click.argument("outdir", type=click.Path(exists=True))
def dump_relationships_as_csv(etymdb_path: str, outdir: str):
    etymdb_edges_path = Path(etymdb_path) / "etymdb_links_info.csv"
    edge_path = Path(".") / outdir / "neo4j_import_data" / "relationships.csv"
    headers = [":START_ID", ":END_ID", ":TYPE"]

    if not edge_path.exists():
        edge_path.parent.mkdir(parents=True, exist_ok=True)

    csv_writer = csv.DictWriter(edge_path.open("w+"), headers)
    csv_writer.writeheader()
    with open(etymdb_edges_path) as fp:
        for relationship in parse_relationships(fp):

            if relationship.parent > 0 and relationship.child > 0:
                csv_writer.writerow(relationship.to_neo4j_dict())


if __name__ == "__main__":
    cli()