"""Omnisearch.ai API Python Client"""
from omnisearch import apiclient, exceptions


class Client(apiclient.ApiClient):
    def __init__(
        self,
        logger,
        api_key,
        api_host=None,
        api_version="v1",
    ):
        super().__init__(logger=logger, api_key=api_key, api_host=api_host, api_version=api_version)

    def hello(self):
        """
        GET /hello

        :return:
        """
        url = "/hello"
        return self.request(method="GET", url=url)

    def languages(self):
        """
        GET /languages

        :return:
        """
        url = "/languages"
        return self.request(method="GET", url=url)

    def records(self, record_type, page=0, page_size=10):
        """
        GET /records

        :param record_type:
        :param page:
        :param page_size:
        :return:
        """
        url = "/records"

        params = {
            "type": record_type,
            "page": page,
            "page_size": page_size
        }

        try:
            self.request(method="GET", url=url, params=params)
        except exceptions.OmniSearchError:
            return None

    def create_records(self, record_type: str, name: str, properties: dict, data: dict, hidden: bool = False):
        """
        POST /records

        :param record_type: The type of the record (used to define the search domain by record type)
        :param name: The name of the record (used only for your reference)
        :param properties: Properties that are used to filter out the records when searching (JSON encoded dict); NOTE: All properties that you add here are going to be fully indexed. If you want to add additional data to the record that shouldn't be indexed (but should be returned with the record), add it into data.
        :param data: Data allows you to supply additional data that you want saved and associated with the record. The data itself won't be indexed and you can't search or filter by it, but it will be returned with the record.
        :param hidden: Set whether or not the record should be found when executing search queries
        :return:
        """
        url = "/records"

        data = {
            "type": record_type,
            "name": name,
            "properties": properties,
            "data": data,
            "hidden": hidden,
        }

        try:
            return self.request(method="POST", url=url, data=data)
        except exceptions.OmniSearchError:
            return None

    def record(self, record_id):
        """
        GET /records/{uid}

        :param record_id:
        :return:
        """
        url = f"/records/{record_id}"
        try:
            return self.request(method="GET", url=url)
        except exceptions.OmniSearchError:
            return None

    def update_record(self):
        """
        PATCH /records/{uid}

        :return:
        """
        pass

    def delete_record(self):
        """
        DELETE /records/{uid}

        :return:
        """
        pass

    def record_objects(self, record_id):
        """
        GET /records/{uid}/objects

        :param record_id:
        :return:
        """
        url = f"/records/{record_id}/objects"
        try:
            return self.request(method="GET", url=url)
        except exceptions.OmniSearchError:
            return None

    def create_objects(self, record_id, objects):
        """
        POST /records/{uid}/objects

        Creates objects for the document with the specified values. Objects are specified as a
        dictionary where the key is the object type and the value is the object data.

        Missing keys (object types) that currently exist will be removed. If you don't want to
        remove them, you can specify the object type's value as null to leave the current data.

        :param record_id:
        :param objects:
        :return:
        """
        url = f"/records/{record_id}/objects"

        data = {
                "objects": objects,
            }

        try:
            return self.request(method="POST", url=url, data=data)
        except exceptions.OmniSearchError:
            return None

    def delete_object(self):
        """
        DELETE /records/{uid}/objects

        :return:
        """
        pass

    def record_objects_type(self):
        """
        GET /records/{uid}/objects/{type}

        :return:
        """
        pass

    def update_record_objects_type(self):
        """
        PUT /records/{uid}/objects/{type}

        :return:
        """
        pass

    def delete_record_objects_type(self, record_id, record_type):
        """
        DELETE /records/{uid}/objects/{type}

        :param record_id:
        :param record_type:
        :return:
        """
        url = f"/records/{record_id}/objects/{record_type}"
        try:
            return self.request(method="DELETE", url=url)
        except exceptions.OmniSearchError:
            return None

    def record_content(self, record_id, object_type):
        """
        GET /records/{uid}/objects/{type}/content

        :param record_id:
        :param object_type:
        :return:
        """
        url = f"/records/{record_id}/objects/{object_type}/content"
        try:
            return self.request(method="GET", url=url)
        except exceptions.OmniSearchError:
            return None

    def record_transcript(self, record_id, object_type):
        """
        GET /records/{uid}/objects/{type}/transcript

        :param record_id:
        :param object_type:
        :return:
        """
        url = f"/records/{record_id}/objects/{object_type}/transcript"
        try:
            return self.request(method="GET", url=url)
        except exceptions.OmniSearchError:
            return None

    def record_schema(
            self, record_type, query="", record_ids=None, object_types=None, filters=None,
            include_hidden=False, disable_autocorrect=False,
            excluded_properties=None, aggregate_properties=None,
            sort_by_count=False,
    ):
        """
        GET /schema/{record_type}

        filters format: [[key, comparison, value], [key, comparison, value], ...]
          key specifies the property name,
          comparison specifies the filter type, example: ["price", "equalto", 5];
          available filter types:
             EqualTo, NotEqualTo, LessThan, GreaterThan, LessThanOrEqualTo,
             GreaterThanOrEqualTo, Contains, StartsWith, EndsWith, IsIn, HasIntersectionWith

        :param record_type: record type
        :param query: search query
        :param record_ids: specify a list of record UIDs that you want to be searched; if not specified, all available
        records will be searched; JSON-encoded list of strings
        :param object_types: specify a list of object types that you want to be searched; if not specified, all
        available object types will be searched; JSON-encoded list of strings
        :param filters:
        :param include_hidden: set whether or not the search results should include hidden records; if not specified,
        hidden records aren't included
        :param disable_autocorrect: use this flag to disable autocorrection of the search query
        :param excluded_properties: specify a list of properties that you want to exclude from the schema
        (e.g. properties that you use for internal things as ID tracking); JSON-encoded list of strings
        :param aggregate_properties: specify a list of properties that should be aggregated when generating the schema;
        aggregated properties will have their inner values flattened out; e.g. a property that has a list
        value ([1, 2, 3]) would return the following schema [[1, 1], [2, 1], [3, 1]] instead of [[[1, 2, 3], 1]];
        JSON-encoded list of strings
        :param sort_by_count: if set to true the schema will be sorted by counts descending; otherwise it will be sorted
        by value ascending
        :return:
        """
        if aggregate_properties is None:
            aggregate_properties = []
        if excluded_properties is None:
            excluded_properties = []
        if filters is None:
            filters = []
        if object_types is None:
            object_types = []
        if record_ids is None:
            record_ids = []
        url = f"/schema/{record_type}"

        params = {
            "query": query,
            "record_uids": record_ids,
            "object_types": object_types,
            "filters": filters,
            "include_hidden": include_hidden,
            "disable_autocorrect": disable_autocorrect,
            "excluded_properties": excluded_properties,
            "aggregate_properties": aggregate_properties,
            "sort_by_count": sort_by_count,
        }

        try:
            return self.request(method="GET", url=url, params=params)
        except exceptions.OmniSearchError:
            return None

    def search(
            self, record_type, query="", record_ids=None, object_types=None, filters=None,
            include_hidden=False, disable_autocorrect=False, sort_by="",
            detailed=False, page=1, page_size=10):
        """
        GET /search/{record_type}
        GET /search/{record_type}/detailed

        filters format: [[key, comparison, value], [key, comparison, value], ...]
          key specifies the property name,
          comparison specifies the filter type, example: ["price", "equalto", 5];
          available filter types:
             EqualTo, NotEqualTo, LessThan, GreaterThan, LessThanOrEqualTo,
             GreaterThanOrEqualTo, Contains, StartsWith, EndsWith, IsIn, HasIntersectionWith

        sort by format: name:order
          name specifies which property should be used for sorting
          order is one of the following:
             ascending, descending,
             best_matches_first_then_ascending, best_matches_first_then_descending

        :param record_type:
        :param query:
        :param record_ids:
        :param object_types:
        :param filters:
        :param include_hidden:
        :param disable_autocorrect:
        :param sort_by:
        :param detailed:
        :param page:
        :param page_size:
        :return:
        """
        if filters is None:
            filters = []
        if object_types is None:
            object_types = []
        if record_ids is None:
            record_ids = []

        url = f"/search/{record_type}"
        if detailed:
            url += "/detailed"

        params = {
            "query": query,
            "record_uids": record_ids,
            "object_types": object_types,
            "filters": filters,
            "include_hidden": include_hidden,
            "disable_autocorrect": disable_autocorrect,
            "sort_by": sort_by,
            "page": page,
            "page_size": page_size
        }

        try:
            return self.request(method="GET", url=url, params=params)
        except exceptions.OmniSearchError:
            return None
