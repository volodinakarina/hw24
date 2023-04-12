import os
import re
from typing import Optional, List, Generator, Any, Dict, Callable

from flask import abort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def read_file_by_chunks(path: str) -> Generator:
    """
    File descriptor as a generator
    """
    with open(path, 'r', encoding='utf-8') as f:
        buffer = []
        for line in f.readlines():
            buffer.append(line.strip())
        if len(buffer) == 10:
            yield buffer
            buffer = []
        if buffer:
            yield buffer


def execute_query(file_name: str, cmd: str, value: str, data: Optional[List[str]]) -> List[str]:

    if data is None:
        if not os.path.isfile(os.path.join(DATA_DIR, file_name)):
            abort(400)

        path = os.path.join(DATA_DIR, file_name)
        prep_data = []
        for chunk in read_file_by_chunks(path):
            prep_data += chunk
    else:
        prep_data = data

    func = CMD_TO_FUNC[cmd]
    try:
        return func(prep_data, value)
    except:
        abort(400)


def filter_data(data: List[str], value: str) -> List[str]:

    return list(filter(lambda text: value in text, data))


def map_data(data: List[str], value: str) -> List[str]:

    return list(map(lambda text: text.split(' ')[int(value)], data))


def unique_data(data: List[str], *args: Any, **kwargs: Any) -> List[str]:

    return list(set(data))


def sort_data(data: List[str], order: str) -> List[str]:

    return sorted(data, reverse=True if order == 'desc' else False)


def limit_data(data: List[str], limit: str | int) -> List[str]:

    limit = int(limit)
    if limit < 0:
        limit = 0
    return data[:limit]


def regex_data(data: List[str], regexp: str) -> List[str]:

    result = []
    for text in data:
        if found := re.search(regexp, text):
            result.append(found.group())
    return result


CMD_TO_FUNC: Dict[str, Callable] = {
    'filter': filter_data,
    'map': map_data,
    'unique': unique_data,
    'sort': sort_data,
    'limit': limit_data,
    'regex': regex_data,
}