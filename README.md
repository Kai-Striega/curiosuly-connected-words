# curiously-connected-words
Find curiously connected words

## Setup

### Getting the data into Neo4j

```shell
poetry run python src/neo4j_helper dump-relationships-as-csv data/EtymDB/data/split_etymdb/ data
```

```shell
poetry run python src/neo4j_helper dump-vertices-as-csv data/EtymDB/data/split_etymdb/ data
```

```shell
docker run --interactive --tty --rm \
  --publish=7474:7474 \
  --publish=7687:7687 \
  --volume=$HOME/neo4j/data:/data \
  --volume=$HOME/neo4j/import:/import \
  neo4j \
  neo4j-admin database import full \
  --nodes=/import/vertex/full.csv \
  --nodes=/import/vertex/with_embedding.csv \
  --nodes=/import/vertex/with_meaning.csv \
  --nodes=/import/vertex/small.csv \
  --relationships=/import/relationships.csv \
  --multiline-fields=true \
  --array-delimiter "\t"
```

### Using Neo4j

```shell
docker run \
  --publish=7474:7474 \
  --publish=7687:7687 \
  --volume=$HOME/neo4j/data:/data \
  neo4j
```

# Draft Queries:

Get all matches, ordered by similarity:

```
MATCH (target: Lexeme) -[:INHERITS_FROM|BORROWS_FROM|der *]-> (root: Lexeme) <-[:INHERITS_FROM|BORROWS_FROM|der *]- (connected: Lexeme)
WHERE
    target.language = 'English'
    AND connected.language = 'English'
    AND target.lexeme <> connected.lexeme
RETURN DISTINCT target.lexeme AS src, connected.lexeme AS word, vector.similarity.cosine(target.embedding, connected.embedding) AS similarity
ORDER BY similarity
```

Get all matches for a specific word:
```
MATCH (target: Lexeme) -[:INHERITS_FROM|BORROWS_FROM|der *]-> (root: Lexeme) <-[:INHERITS_FROM|BORROWS_FROM|der *]- (connected: Lexeme)
WHERE
    target.lexeme = 'poison'
    AND target.language = 'English'
    AND connected.language = 'English'
    AND target.lexeme <> connected.lexeme
RETURN DISTINCT target.lexeme AS src, connected.lexeme AS word, vector.similarity.cosine(target.embedding, connected.embedding) AS similarity
ORDER BY similarity
```

Get all paths for a specific word:

Some fun words to try:

* poison
* coronal

```
MATCH p = ALL SHORTEST (target: Lexeme) -[:INHERITS_FROM|BORROWS_FROM|der *]-> (root: Lexeme) <-[:INHERITS_FROM|BORROWS_FROM|der *]- (connected: Lexeme)
WHERE
    target.lexeme = 'poison'
    AND target.language = 'English'
    AND connected.language = 'English'
    AND target.lexeme <> connected.lexeme
RETURN DISTINCT [n in nodes(p)]
```