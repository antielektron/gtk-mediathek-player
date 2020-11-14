import requests
import json

import datetime as dt


class MediathekViewWebAnswer(object):
    def __init__(self, answer_json: str):

        def get_field(field: str):
            if field in answer_json:
                return answer_json[field]
            return None

        self._raw = answer_json

        self._channel = get_field('channel')
        self._topic = get_field('topic')
        self._title = get_field('title')
        self._description = get_field('description')
        self._timestamp = get_field('timestamp')
        self._duration = get_field('duration')
        self._size = get_field('size')
        self._url_website = get_field('url_website')
        self._url_subtitle = get_field('url_subtitle')
        self._filmlisteTimestamp = get_field('filmlisteTimestamp')
        self._id = get_field('id')
        self._url_video = get_field('url_video')
        self._url_video_low = get_field('url_video_low')
        self._url_video_hd = get_field('url_video_hd')

    def get_best_vid_url(self) -> str:
        if self._url_video_hd is not None:
            return self._url_video_hd

        if self._url_video is not None:
            return self._url_video

        if self._url_video_low is not None:
            return self._url_video_low

        return None

    def get_lowest_vid_url(self) -> str:
        if self._url_video_low is not None:
            return self._url_video_low

        if self._url_video is not None:
            return self._url_video

        if self._url_video_hd is not None:
            return self._url_video_hd

        return None

    def get_id(self):
        return self._id

    def get_site(self):
        return self._url_website

    def get_title(self):
        return self._title

    def get_channel(self):
        return self._channel

    def get_topic(self):
        return self._topic

    def get_description(self):
        return self._description
    
    def get_timestamp(self) -> dt.datetime:
        if self._timestamp is None:
            return None
        return dt.datetime.utcfromtimestamp(int(self._timestamp))
    
    def get_duration(self):
        return self._duration


class MediathekViewWebRequest(object):
    @staticmethod
    def from_serialization(
        d: dict,
        request_url="https://mediathekviewweb.de/api/query"
    ) -> 'MediathekViewWebRequest':

        json_query = d['queries'][0]
        sort_by = d['sortBy']
        sort_order = d['sortOrder']
        future = d['future']
        offset = d['offset']
        size = d['size']

        query = json_query['query']
        fields = json_query['fields']

        search_channel = "channel" in fields
        search_topic = "topic" in fields
        search_title = "title" in fields

        return MediathekViewWebRequest(
            query=query,
            search_title=search_title,
            search_channel=search_channel,
            search_topic=search_topic,
            sort_by=sort_by,
            sort_order=sort_order,
            future=future,
            size=size,
            offset=offset,
            request_url=request_url
        )

    @staticmethod
    def from_json(
        js: str,
        request_url="https://mediathekviewweb.de/api/query"
    ) -> 'MediathekViewWebRequest':
        return MediathekViewWebRequest.from_serialization(
            d=json.loads(js),
            request_url=request_url
        )

    def __init__(self,
                 query: str,
                 search_title: bool = True,
                 search_channel: bool = False,
                 search_topic: bool = False,
                 sort_by: str = 'timestamp',
                 sort_order: str = 'desc',
                 future: bool = False,
                 size: int = 10,
                 offset: int = 0,
                 request_url="https://mediathekviewweb.de/api/query"):

        assert search_title or search_channel or search_topic
        assert sort_order == 'desc' or sort_order == 'asc'

        self._query = query
        self._fields = []
        if search_title:
            self._fields.append("title")
        if search_channel:
            self._fields.append("channel")
        if search_topic:
            self._fields.append("topic")

        self._sort_by = sort_by
        self._sort_order = sort_order
        self._future = future
        self._size = size
        self._offset = offset
        self._request_url = request_url

    def serialize(self):
        query = {
            'queries': [
                {
                    'fields': self._fields,
                    'query': self._query
                }
            ],

            'sortBy': self._sort_by,
            'sortOrder': self._sort_order,
            'future': self._future,
            'offset': self._offset,
            'size': self._size
        }
        return query

    def to_json(self):
        return json.dumps(self.serialize())

    def perform_request(self):
        headers = {'Content-type': 'text/plain'}
        req = requests.post(self._request_url,
                            data=self.to_json(), headers=headers)

        if not req.ok:
            return None

        answer = json.loads(req.text)

        if 'result' in answer:
            result = answer['result']

            if 'results' in result:
                results = result['results']
                return [MediathekViewWebAnswer(i) for i in results]

        return None
