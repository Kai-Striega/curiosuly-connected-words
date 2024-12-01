# curiously-connected-words
Find curiously connected words

## Setup

```shell
docker run \
  --publish=7474:7474 \
  --publish=7687:7687 \
  --volume=$HOME/neo4j/data:/data \ 
  neo4j
```

### Getting the data into Neo4j
```shell
export DATA_DIR /home/kai/Projects/curiously-connected-words/data/neo4j_import_data
```
```shell
docker run --interactive --tty --rm \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    --volume=$DATA_DIR:/import \
    neo4j \
    neo4j-admin database import full \
    --nodes=/import/vertex/full.csv \
    --nodes=/import/vertex/with_embedding.csv \
    --nodes=/import/vertex/with_meaning.csv \
    --nodes=/import/vertex/small.csv \
    --relationships=/import/relationships.csv \
    neo4j
```