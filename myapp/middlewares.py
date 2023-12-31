from django.http import HttpResponseForbidden
class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.fixed_token = "Ek.R@{S-,F?6k:]r0lFT@3q1qi=bv7Zlj/4VT7{oD+xw-HOw8tv3.pV+OGXufkb#J!):1{*qcP@a#6iK8jVgar-2PCep=tWfQ7+v}mQY;pUC7.h-.I/W|!mrp[Hm"

    def __call__(self, request):
        token = request.headers.get('Authorization')

        if not self._is_valid_token(token):
            return HttpResponseForbidden('شما اجازه دسترسی ندارید')

        response = self.get_response(request)
        return response

    def _is_valid_token(self, token):
        # Remove 'Bearer ' prefix if it exists in the received token
        if token and token.startswith('Bearer '):
            token = token.split('Bearer ')[1]

        return token == self.fixed_token   