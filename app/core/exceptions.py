from werkzeug.exceptions import HTTPException

from app.core.utils.response_utils import create_response


class APIException(Exception):
    """Base API exception."""
    code = 500
    description = "An error occurred"

    def __init__(self, description=None, code=None):
        if description:
            self.description = description
        if code:
            self.code = code
        super().__init__(self.description)

class NotFoundException(APIException):
    """Resource not found exception."""
    code = 404
    description = "Resource not found"

class ValidationError(APIException):
    """Validation error exception."""
    code = 400
    description = "Validation error"

class AuthenticationError(APIException):
    """Authentication error exception."""
    code = 401
    description = "Authentication error"

class AuthorizationError(APIException):
    """Authorization error exception."""
    code = 403
    description = "Authorization error"

def register_error_handlers(app):
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        app.logger.error(f"API error: {error.description}")
        return create_response(error.description, error.code)

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        app.logger.error(f"HTTP error: {error.description}")
        return create_response(error.description, error.code)

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        app.logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        return create_response("An unexpected error occurred", 500)
