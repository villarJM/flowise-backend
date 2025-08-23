from flask import jsonify

def create_response(message: str, status_code: int, data: dict | None = None):
  response = {
    "message": message,
    "status": status_code
  }
  if data is not None:
    response["data"] = data
  return jsonify(response), status_code