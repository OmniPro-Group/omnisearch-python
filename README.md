# omnisearch-python
Simple Python Client for OmniSearch.ai

## Example Usage
```python
import logging
from omnisearch.client import Client
from omnisearch import exceptions
from scripts.colour_json import print_json_in_colour

logger = logging.getLogger(__name__)

key = "<your key>"
host = "https://<your server>.omnisearch.ai/api"
version = "v1"
omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

try:
    records_response = omnisearch_client.records(record_type="post", page=1, page_size=20)
    print_json_in_colour(records_response, colour=True)
except exceptions.OmniSearchError:
    logger.error("Error calling /records")
```

## CLI Examples
Set up your environment:
```shell
export PYTHONPATH=$PWD:$PWD/scripts 
export OMNISEARCH_API_SERVER=https://<your server>.omnisearch.ai/api
export OMNISEARCH_API_VERSION=v1
export OMNISEARCH_API_KEY=<your api key>
```

The cli will look in your environment for the detail of the api host, api version and api key if not provided as options:
```shell
python scripts/cli.py hello --host $OMNISEARCH_API_SERVER --version $OMNISEARCH_API_VERSION --key $OMNISEARCH_API_KEY --colour
# or 
python scripts/hello.py hello --colour
```

### Hello
```shell
python scripts/cli.py hello --colour
```

### Languages
```shell
python scripts/cli.py languages --colour
```

### Records
```shell
python scripts/cli.py records --record_type post --colour

# Create post using generated data
python scripts/cli.py create-records --colour \
    --record_type post --name "Post 1" -r title "Post 1" \
    --properties data/post_properties.json \
    --data data/post_data.json \
    --generate data/post_chance.json

python scripts/cli.py get-record --colour --record_id record-2870f4dfd87b4393a7481e6a60182ffd 

python scripts/cli.py update-record --colour --record_id record-2870f4dfd87b4393a7481e6a60182ffd \
    --name "Post 1" -r title "Post 1" \
    --properties data/post_properties.json \
    --data data/post_data.json \
    --generate data/post_chance.json

python scripts/cli.py delete-record --colour --record_id record-2870f4dfd87b4393a7481e6a60182ffd
````

### Record Objects
```shell
python scripts/cli.py create-record-objects --colour \
    --record_id record-a66a83e05da94ba9a0f5f5798a4b611c \
    --generate data/post_chance.json \
    --objects data/post_objects.json

python scripts/cli.py delete-record-objects --colour \
    --record_id record-a66a83e05da94ba9a0f5f5798a4b611c 

python scripts/cli.py get-record-objects --colour \
    --record_id record-a66a83e05da94ba9a0f5f5798a4b611c

python scripts/cli.py get-record-objects-by-type --colour \
    --record_id record-a66a83e05da94ba9a0f5f5798a4b611c \
    --object_type content

python scripts/cli.py update-record-objects-by-type --colour \
    --record_id record-a66a83e05da94ba9a0f5f5798a4b611c \
    --object_type content \
    --generate data/post_chance.json \
    --objects data/post_objects.json

python scripts/cli.py get-record-objects-by-type-content --colour \
    --record_id record-a66a83e05da94ba9a0f5f5798a4b611c \
    --object_type content

python scripts/cli.py get-record-objects-by-type-transcript --colour \
    --record_id record-a66a83e05da94ba9a0f5f5798a4b611c \
    --object_type video
```

### Schema
```shell
python scripts/cli.py schema --record_type post --colour

python scripts/cli.py schema --record_type post --colour --query "CPD" \
    --disable_autocorrect --sort_by_count

python scripts/cli.py schema --record_type post --colour \
    --filters '[["categories" "HasIntersectionWith", "Tax"]]'
    
python scripts/cli.py schema --record_type post --colour --object_types content
```

### Search
```shell
python scripts/cli.py search --colour --record_type post \
    --sort_field slug --sort_order descending --detailed
```
