from robyn import Response, jsonify


def api_result(message: str = "", data: dict | str | None = None, code: int = 200):
    return Response(
        code,
        {"Content-Type": "application/json"},
        jsonify(
            {
                "message": message,
                "data": data,
            }
        ),
    )
