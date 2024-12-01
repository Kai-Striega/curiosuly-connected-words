# curiously-connected-words
Find curiously connected words

## Setup

### Getting the data into Neo4j

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