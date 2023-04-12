from flask import Flask, request, Response
from marshmallow import ValidationError

from utils import execute_query
from models import BatchRequestSchema

app = Flask(__name__)


@app.route("/perform_query/", methods=['POST'])
def perform_query() -> Response:
    data = request.json

    try:
        data = BatchRequestSchema().load(data)
    except ValidationError as error:
        return app.response_class(error.messages, status=400)

    result = None
    for query in data['queries']:
        result = execute_query(
            file_name=data['file_name'],
            cmd=query['cmd'],
            value=query['value'],
            data=result
        )
    if not result:
        return app.response_class('', status=200)
    return app.response_class('\n'.join(result), status=200)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
