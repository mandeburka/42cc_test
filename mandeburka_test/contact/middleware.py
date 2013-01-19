from mandeburka_test.contact.models import Request


class ContactMiddleware(object):
    def process_request(self, request):
        r = Request(method=request.method, path=request.path)
        r.save()
