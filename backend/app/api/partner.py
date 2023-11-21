import hashlib
import hmac
import json

from django.utils import timezone
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.tasks import update_rx_status
from utils.datetime import get_unix_datetime

EXAMPLE_PARTNER_SIGNING_KEY = 'thisIsNotSecure!'


class BasePartnerView(APIView):
    # Request will come from 3rd party application
    # Authentication is based off of an API key
    permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        self.data = None
        super().__init__(**kwargs)
        
    def initial(self, request, *args, **kwargs):
        if not self.is_authenticated_request(request):
            raise exceptions.PermissionDenied(
                detail='Invalid request signature',
                code=status.HTTP_403_FORBIDDEN
            )
        
        self.data = json.loads(request.data['_raw_data'])
        super().initial(request, *args, **kwargs)
        
        # Note: If there are common data attributes shared by child classes, we could
        # parse the data here. For now, we'll stick with self.data
    
    @staticmethod
    def is_authenticated_request(request):
        """This is adapted from Slack's webhook implementation
        """
        timestamp = int(request.headers['X-Partner-Request-Timestamp'])
        current_timestamp = get_unix_datetime(timezone.now())
        if abs(current_timestamp - timestamp) > 60 * 5:
            # The request timestamp is more than five minutes from local time.
            # It could be a replay attack, so let's ignore it.
            return
        
        sig_basestring = 'v0:' + str(timestamp) + ':' + request.data['_raw_data']
        signature = 'v0=' + hmac.new(
            key=EXAMPLE_PARTNER_SIGNING_KEY.encode('utf-8'),
            msg=sig_basestring.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        partner_signature = request.headers['X-Partner-Signature']
        return hmac.compare_digest(signature, partner_signature)
    
    @staticmethod
    def get_authenticated_request_headers(rx_fill_data: dict):
        """This is a utility method for testing locally. Generate request headers
        and add them to an API utility like Postman or add to a Django test
        """
        current_timestamp = get_unix_datetime(timezone.now())
        sig_basestring = 'v0:' + str(current_timestamp) + ':' + json.dumps(rx_fill_data)
        signature = 'v0=' + hmac.new(
            key=EXAMPLE_PARTNER_SIGNING_KEY.encode('utf-8'),
            msg=sig_basestring.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        return {
            'X-Partner-Request-Timestamp': current_timestamp,
            'X-Partner-Signature': signature
        }
    
    
class RxFillView(BasePartnerView):
    
    def put(self, request):
        # This is asynchronous and results are stored in database
        # Here we acknowledge receipt of the rx fill update and we
        # can poll (e.g. flower) the results to make sure it is successful
        update_rx_status.delay(self.data)
        return Response(status=status.HTTP_200_OK)
