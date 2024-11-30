import csv
from dataclasses import dataclass, fields
from pathlib import Path

import click

from vertex import Vertex, parse_vertices
from relationship import Relationship, parse_relationships
from code_to_langs import WIKI_CODE_TO_LANG

@click.group()
def cli():
    pass

@cli.command()
@click.argument("etymdb-path", type=click.Path(exists=True))
@click.argument("outdir", type=click.Path(exists=True))
def dump_vertices_as_csv(etymdb_path: str, outdir: str):
    etymdb_vertices_path = Path(etymdb_path) / "etymdb_values.csv"
    full_vertices_path = Path(".") / outdir / "full_vertices.csv"
    part_vertices_path = Path(".") / outdir / "part_vertices.csv"
    full_headers = ["etymdb_id:ID", "language", "field:int", "lexeme", "meaning", ":LABEL"]
    part_headers = ["etymdb_id:ID", "language", "field:int", "lexeme", ":LABEL"]
    full_csv_writer = csv.DictWriter(full_vertices_path.open("w+"), full_headers)
    part_csv_writer = csv.DictWriter(part_vertices_path.open("w+"), part_headers)

    full_csv_writer.writeheader()
    part_csv_writer.writeheader()
    with open(etymdb_vertices_path) as fp:
        for vertex in parse_vertices(fp, WIKI_CODE_TO_LANG):
            row_values = vertex.to_neo4j_dict() | {":LABEL": "Lexeme"}
            if vertex.meaning is None:
                part_csv_writer.writerow(row_values)
            else:
                full_csv_writer.writerow(row_values)


@cli.command()
@click.argument("etymdb-path", type=click.Path(exists=True))
@click.argument("outdir", type=click.Path(exists=True))
def dump_relationships_as_csv(etymdb_path: str, outdir: str):
    etymdb_edges_path = Path(etymdb_path) / "etymdb_links_info.csv"
    edge_path = Path(".") / outdir / "relationships.csv"
    headers = [":START_ID", ":END_ID", ":TYPE"]
    csv_writer = csv.DictWriter(edge_path.open("w+"), headers)
    csv_writer.writeheader()
    with open(etymdb_edges_path) as fp:
        for relationship in parse_relationships(fp):
            csv_writer.writerow(relationship.to_neo4j_dict())


if __name__ == "__main__":
    cli()