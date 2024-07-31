# class NoCacheMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#         response['Pragma'] = 'no-cache'
#         response['Expires'] = '0'
#         return response


# Define a middleware class named NoCacheMiddleware.
# Middleware is a way to process requests globally before they reach the view or after the view has processed them.
class NoCacheMiddleware:
    # The __init__ method is called when the middleware is instantiated.
    # get_response is a callable that takes a request and returns a response.
    def __init__(self, get_response):
        self.get_response = get_response  # Store the get_response callable for later use.

    # The __call__ method is called for each request.
    # It processes the request and modifies the response to disable caching.
    def __call__(self, request):
        # Call the get_response callable to get the response for the current request.
        response = self.get_response(request)

        # Add headers to the response to disable caching.
        # 'Cache-Control' header tells the browser not to cache the page.
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        # 'Pragma' header is included for backward compatibility with HTTP/1.0 caches.
        response['Pragma'] = 'no-cache'
        # 'Expires' header is set to '0' to indicate that the content is already expired.
        response['Expires'] = '0'

        # Return the modified response.
        return response
