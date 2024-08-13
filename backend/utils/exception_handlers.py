import json, traceback
from loguru import logger

CLIENT_ERRORS = range(400, 500)
SERVER_ERRORS = range(500, 600)

class ClientError(Exception):
    '''
    Exception raised for client-side errors.

    Attributes:
        message -- explanation of the error
        status_code -- HTTP status code representing the error
    '''

    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ServerError(Exception):
    '''
    Exception raised for server-side errors.

    Attributes:
        message -- explanation of the error
        status_code -- HTTP status code representing the error
    '''

    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def function_decorator(func):
    '''
    A decorator function to log exceptions.

    Usage:
    @function_decorator
    def my_function():
        # Your code here
    '''
    def wrapper(*args, **kwargs):
        try:
            logger.debug('START')
            logger.debug(f'{args=}, {kwargs=}')
            result = func(*args, **kwargs)
            logger.debug('FINISH')
            return result

        # Client errors that we catch
        except ClientError as e:
            logger.debug(f'{str(traceback.format_exc())}')
            logger.error(f'Exception encountered: {str(e)}')

            return {
                'statusCode': e.status_code,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': {'error': str(e)},
            }
        
        # Specific serverside errors that we catch
        except ServerError as e:
            logger.debug(f'{str(traceback.format_exc())}')
            logger.error(f'Exception encountered: {str(e)}')

            return {
                'statusCode': e.status_code,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': {'error': str(e)},
            }
        
        # Unhandled exceptions
        except Exception as e:
            logger.debug(f'{str(traceback.format_exc())}')
            logger.error(f'Exception encountered: {str(e)}, ')

            return {
                'statusCode': e.status_code,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': {'error': str(e)},
            }

    return wrapper