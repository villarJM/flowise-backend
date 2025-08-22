from flask import jsonify

def create_response(message, status_code, data=None):
  response = {
    "message": message,
    "status": status_code
  }
  if data is not None:
    response["data"] = data
  return jsonify(response), status_code