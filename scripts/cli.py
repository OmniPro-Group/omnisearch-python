"""
OmniSearch.ai cli

export OMNISEARCH_API_SERVER=https://<your server>.omnisearch.ai/api
export OMNISEARCH_API_VERSION=v1
export OMNISEARCH_API_KEY=<your api key>
python scripts/cli.py hello --colour
"""
import functools
import logging
from collections import OrderedDict
import json
import string
from datetime import datetime
from typing import Optional
import click
from portabletext_html import PortableTextRenderer
from portabletext_html.types import Block

from omnisearch.client import Client
from omnisearch import exceptions
from scripts.colour_json import print_json_in_colour
from scripts.chance_extension import chance_dictionary

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("nose").setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


def common_params(func):
    @click.option("--host", envvar='OMNISEARCH_API_SERVER', help="OmniSearch Host.", type=str)
    @click.option(
        "--version", envvar='OMNISEARCH_API_VERSION', help="OmniSearch API Version.", required=False, type=str, default="v1"
    )
    @click.option("--key", envvar='OMNISEARCH_API_KEY', help="OmniSearch API Key.", type=str)
    @click.option("--colour", is_flag=True, show_default=True, default=False, help="Print json output in colour.")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class NaturalOrderGroup(click.Group):
    """Command group trying to list subcommands in the order they were added.

    Make sure you initialize the `self.commands` with OrderedDict instance.

    With decorator, use::

        @click.group(cls=NaturalOrderGroup, commands=OrderedDict())
    """

    def list_commands(self, ctx):
        """List command names as they are in commands dict.

        If the dict is OrderedDict, it will preserve the order commands
        were added.
        """
        return self.commands.keys()


@click.group(cls=NaturalOrderGroup, commands=OrderedDict())
def cli():
    pass


@cli.command()
@common_params
def hello(
    host,
    version,
    key,
    colour,
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        hello_response = omnisearch_client.hello()
        print_json_in_colour(hello_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /hello")


@cli.command()
@common_params
def get_languages(
    host,
    version,
    key,
    colour,
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        languages_response = omnisearch_client.languages()
        print_json_in_colour(languages_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /languages")


@cli.command()
@common_params
@click.option("--record_type", help="OmniSearch Record Type.", type=str)
@click.option("--page", help="OmniSearch Page Number.", type=int, default=0)
@click.option("--page_size", help="OmniSearch Page Size.", type=int, default=10)
def get_records(
    host,
    version,
    key,
    colour,
    record_type,
    page,
    page_size,
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        records_response = omnisearch_client.records(record_type=record_type, page=page, page_size=page_size)
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /records")


@cli.command()
@common_params
@click.option("--record_type", help="OmniSearch Record Type.", type=str)
@click.option("--name", help="OmniSearch Record Name.", type=str)
@click.option("--hidden", is_flag=True, show_default=True, default=False, help="OmniSearch Record is hidden.")
@click.option('--replacement', '-r', type=(str, str), multiple=True,
              help="Key/Value replacements in properties or data.")
@click.option("--generate", type=click.Path(exists=True), help="Generate data.")
@click.option("--properties", type=click.Path(exists=True), required=True, help="Properties json file")
@click.option("--data", type=click.Path(exists=True), required=False, help="Data json file")
def create_records(
    host,
    version,
    key,
    colour,
    record_type,
    name,
    hidden,
    replacement,
    generate,
    properties,
    data,
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    properties_json, data_json = get_data(generate, replacement, properties, data)

    try:
        records_response = omnisearch_client.create_records(
            record_type=record_type,
            name=name,
            properties=properties_json,
            data=data_json,
            hidden=hidden
        )
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /records")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
def get_record(
    host,
    version,
    key,
    colour,
    record_id,
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        records_response = omnisearch_client.record(record_id=record_id)
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /record/{uid}")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
@click.option("--name", help="OmniSearch Record Name.", type=str)
@click.option("--hidden", is_flag=True, show_default=True, default=False, help="OmniSearch Record is hidden.")
@click.option('--replacement', '-r', type=(str, str), multiple=True,
              help="Key/Value replacements in properties or data.")
@click.option("--generate", type=click.Path(exists=True), help="Generate data.")
@click.option("--properties", type=click.Path(exists=True), required=True, help="Properties json file")
@click.option("--data", type=click.Path(exists=True), required=False, help="Data json file")
def update_record(
    host,
    version,
    key,
    colour,
    record_id,
    name,
    hidden,
    replacement,
    generate,
    properties,
    data,
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    properties_json, data_json = get_data(generate, replacement, properties, data)

    try:
        records_response = omnisearch_client.update_record(
            record_id=record_id,
            name=name,
            properties=properties_json,
            data=data_json,
            hidden=hidden
        )
        if "modified" in records_response and not records_response["modified"]:
            raise exceptions.OmniSearchError
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /record/{uid}")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
def delete_record(
    host,
    version,
    key,
    colour,
    record_id,
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        records_response = omnisearch_client.delete_record(record_id=record_id)
        if records_response and "message" in records_response and records_response["message"].lower() != "record deleted":
            raise exceptions.OmniSearchError

        if records_response:
            print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /record/{uid}")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
def get_record_objects(
    host,
    version,
    key,
    colour,
    record_id,
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        records_response = omnisearch_client.record_objects(record_id=record_id)
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /record/{uid}/objects")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
@click.option('--replacement', '-r', type=(str, str), multiple=True,
              help="Key/Value replacements in properties or data.")
@click.option("--generate", type=click.Path(exists=True), help="Generate data.")
@click.option("--objects", type=click.Path(exists=True), required=True, help="Properties objects file")
def create_record_objects(
    host,
    version,
    key,
    colour,
    record_id,
    replacement,
    generate,
    objects
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    objects_json, _ = get_data(generate, replacement, objects, None)

    objects_json = convert_portable_text(objects_json)

    logger.info(objects_json)

    try:
        records_response = omnisearch_client.create_record_objects(record_id=record_id, objects=objects_json)
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /record/{uid}/objects")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
def delete_record_objects(
    host,
    version,
    key,
    colour,
    record_id,
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        records_response = omnisearch_client.delete_record_objects(record_id=record_id)
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /record/{uid}/objects")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
@click.option("--object_type", help="OmniSearch Object Type.", type=str)
def get_record_objects_by_type(
    host, version, key, colour,
    record_id,
    object_type
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        records_response = omnisearch_client.record_objects_type(record_id=record_id, object_type=object_type)
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /records/{uid}/objects/{type}")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
@click.option("--object_type", help="OmniSearch Object Type.", type=str)
@click.option('--replacement', '-r', type=(str, str), multiple=True,
              help="Key/Value replacements in properties or data.")
@click.option("--generate", type=click.Path(exists=True), help="Generate data.")
@click.option("--objects", type=click.Path(exists=True), required=True, help="Properties objects file")
def update_record_objects_by_type(
    host, version, key, colour,
    record_id, object_type,
    replacement, generate, objects
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    objects_json, _ = get_data(generate, replacement, objects, None)

    objects_json = convert_portable_text(objects_json)

    logger.info(objects_json[object_type])

    try:
        records_response = omnisearch_client.update_record_objects_type(
            record_id=record_id, object_type=object_type, data=objects_json[object_type]
        )
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /records/{uid}/objects/{type}")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
@click.option("--object_type", help="OmniSearch Object Type.", type=str)
def delete_record_objects_by_type(
    host, version, key, colour,
    record_id, object_type
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        records_response = omnisearch_client.delete_record_objects_type(
            record_id=record_id, object_type=object_type
        )
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /records/{uid}/objects/{type}")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
@click.option("--object_type", help="OmniSearch Object Type.", type=str)
def get_record_objects_by_type_content(
    host, version, key, colour,
    record_id, object_type
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        records_response = omnisearch_client.record_type_content(
            record_id=record_id, object_type=object_type
        )
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /records/{uid}/objects/{type}/content")


@cli.command()
@common_params
@click.option("--record_id", help="OmniSearch Record ID.", type=str)
@click.option("--object_type", help="OmniSearch Object Type.", type=str)
def get_record_objects_by_type_transcript(
    host, version, key, colour,
    record_id, object_type
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        records_response = omnisearch_client.record_type_transcript(
            record_id=record_id, object_type=object_type
        )
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /records/{uid}/objects/{type}/transcript")


@cli.command()
@common_params
@click.option("--record_type", help="OmniSearch Record Type.", type=str)
@click.option("--query", help="OmniSearch Query.", type=str)
@click.option("--record_ids", help="OmniSearch Record IDs.", type=list, default=None)
@click.option("--object_types", help="OmniSearch Object Types.", type=list, default=None)
@click.option("--filters", help="OmniSearch Filters.", type=str, default=None)
@click.option("--hidden", is_flag=True, show_default=True, default=False, help="Show hidden records.")
@click.option("--disable_autocorrect", is_flag=True, show_default=True, default=False, help="Autocorrect query.")
@click.option("--excluded_properties", help="Specify a list of properties that you want to exclude from the schema.",
              type=list, default=None)
@click.option("--aggregate_properties",
              help="Specify a list of properties that should be aggregated when generating the schema.",
              type=list, default=None)
@click.option("--sort_by_count", is_flag=True, show_default=True, default=False, help="Sort by counts.")
def schema(
    host, version, key, colour,
    record_type, query, record_ids, object_types, filters,
    hidden,
    disable_autocorrect,
    excluded_properties,
    aggregate_properties,
    sort_by_count,
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    if filters:
        filters = json.loads(filters)

    try:
        records_response = omnisearch_client.record_schema(
            record_type=record_type,
            query=query,
            record_ids=record_ids,
            object_types=object_types,
            filters=filters,
            include_hidden=hidden,
            disable_autocorrect=disable_autocorrect,
            excluded_properties=excluded_properties,
            aggregate_properties=aggregate_properties,
            sort_by_count=sort_by_count
        )
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /schema/{record_type}")


@cli.command()
@common_params
@click.option("--record_type", help="OmniSearch Record Type.", type=str)
@click.option("--query", help="OmniSearch Query.", type=str)
@click.option("--record_ids", help="OmniSearch Record IDs.", type=list, default=None)
@click.option("--object_types", help="OmniSearch Object Types.", type=list, default=None)
@click.option("--filters", help="OmniSearch Filters.", type=list, default=None)
@click.option("--hidden", is_flag=True, show_default=True, default=False, help="Show hidden records.")
@click.option("--disable_autocorrect", is_flag=True, show_default=True, default=False, help="Autocorrect query.")
@click.option("--sort_field", help="Sort by field.", type=str, default=None)
@click.option("--sort_order", help="Sort order.",
              type=click.Choice(['ascending', 'descending'], case_sensitive=False),
              default="ascending")
@click.option("--detailed", is_flag=True, show_default=True, default=False, help="Detailed.")
@click.option("--page", help="OmniSearch Page Number.", type=int, default=1)
@click.option("--page_size", help="OmniSearch Page Size.", type=int, default=10)
def search(
    host, version, key, colour,
    record_type,
    query, record_ids, object_types, filters,
    hidden,
    disable_autocorrect,
    sort_field,
    sort_order,
    detailed,
    page=1,
    page_size=10
):
    omnisearch_client = Client(logger=logger, api_key=key, api_host=host, api_version=version)

    try:
        records_response = omnisearch_client.search(
            record_type=record_type,
            query=query,
            record_ids=record_ids,
            object_types=object_types,
            filters=filters,
            sort_by=f"{sort_field}:{sort_order}" if sort_field else None,
            include_hidden=hidden,
            disable_autocorrect=disable_autocorrect,
            detailed=detailed,
            page=page,
            page_size=page_size
        )
        print_json_in_colour(records_response, colour=colour)
    except exceptions.OmniSearchError:
        logger.error("Error calling /search/{record_type}")


def get_data(generate, replacement, properties, data):
    generated_values = {}
    if generate:
        with open(generate, 'r') as f:
            generate_json = json.load(f)

            generate_formatted = {}
            for k, v in generate_json.items():
                generate_formatted[k] = (v["type"], v["options"])

            generated_values = chance_dictionary(generate_formatted)

            for k, v in generated_values.items():
                if type(v) == datetime:
                    generated_values[k] = v.strftime("%Y-%m-%d %H:%M")

    for r in replacement:
        generated_values[r[0]] = r[1]

    logger.info(generated_values)

    with open(properties, 'r') as f:
        properties_str = f.read()
        properties_template_text = string.Template(properties_str)
        properties_str = properties_template_text.safe_substitute(generated_values)
        properties_json = json.loads(properties_str)

    data_json = {}
    if data:
        with open(data, 'r') as f:
            data_str = f.read()
            data_template_text = string.Template(data_str)
            data_str = data_template_text.safe_substitute(generated_values)
            data_json = json.loads(data_str)

    return properties_json, data_json


def youtube_serializer(node: dict, context: Optional[Block], list_item: bool):
    return f'<div><ReactPlayer url="{node["url"]}" /></div>'


def convert_portable_text(objects_json):
    for k, v in objects_json.items():
        if v["type"] == "portable_text":
            blocks_json = json.loads(v["content"])
            objects_json[k]["content"] = ""
            for block in blocks_json:
                renderer = PortableTextRenderer(
                    block, custom_serializers={'youtube': youtube_serializer})
                objects_json[k]["content"] += renderer.render()
        if "type" in v:
            del v["type"]
    return objects_json


if __name__ == '__main__':
    cli()
