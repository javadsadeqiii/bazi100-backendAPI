from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response



class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        
        if token != 'g:oa6Ek/-0w-j-gwdH,II,ABIEv*Z+sI6Lw1qc-}4\zco.b0,82W"FCH3o.)jC7;jv"VQlr@*k:DWhlRfeW?(McktEi[V?{!OmyBhllwAQ.t+)9xoY4O2!ZM8F3tT,6.AA;ZO-K3A#f,9\pr:M43}J|M=SDiFjOK\X|R:8DKxW*:cI4]*}61\(IgwaK#':
            return Response({'error':'شما مجاز به دسترسی نیستید'})
        return None
    
    
    