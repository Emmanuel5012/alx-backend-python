import logging
from datetime import datetime

# Configure the logger
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

# Create a file handler to log to a file
file_handler = logging.FileHandler('requests.log')
file_handler.setLevel(logging.INFO)

# Create a log formatter
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """
    Middleware to log request details including timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user information (if authenticated)
        user = request.user if request.user.is_authenticated else 'Anonymous'

        # Get the timestamp and log the request
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - User: {user} - Path: {request.path}"

        # Log the request to the file
        logger.info(log_message)

        # Call the next middleware or view
        response = self.get_response(request)

        return response
