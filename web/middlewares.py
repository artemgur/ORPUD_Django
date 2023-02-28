import re

from web.models import PageVisitCount


class PageVisitCounterMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        url = request.path
        # Id censoring
        url = re.sub(r'((?<=/)|^)\d+((?=/)|$)', 'X', url)
        visit_count = PageVisitCount.objects.filter(url=url).first()
        if visit_count:
            visit_count.visit_count += 1
        else:
            visit_count = PageVisitCount(url=url, visit_count=1)
        visit_count.save()

        return response
