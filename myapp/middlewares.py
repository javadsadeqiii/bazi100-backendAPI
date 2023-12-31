from django.http import HttpResponseForbidden

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization')
        fixed_token = "Ek.R@{S-,F?6k:]r0lFT@3q1qi=bv7Zlj/4VT7{oD+xw-HOw8tv3.pV+OGXufkb#J!):1{*qcP@a#6iK8jVgar-2PCep=tWfQ7+v}mQY;pUC7.h-.I/W|!mrp[Hm"

        if not self._is_valid_token(token, fixed_token):
            return HttpResponseForbidden('شما اجازه دسترسی ندارید')

        response = self.get_response(request)
        return response

    def _is_valid_token(self, token, fixed_token):
        return token == f"Bearer {fixed_token}"