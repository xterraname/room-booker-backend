from rest_framework import pagination
from rest_framework.response import Response

def get_pagination(page_size=10):
    class CustomPagination(pagination.PageNumberPagination):
        def __init__(self) -> None:
            self.page_size = page_size
            super().__init__()

        def get_paginated_response(self, data):
            return Response({
                'page': self.page.number,
                'count': self.page.paginator.count,
                'page_size': self.page_size,
                'results': data
            })
    return CustomPagination

