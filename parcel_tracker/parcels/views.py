# parcels/views.py
import random
import string
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TrackingNumber
from django.utils import timezone
from django.db import transaction



class NextTrackingNumberView(APIView):
    def get(self, request):
        # Extract query parameters
        origin_country_id = request.query_params.get('origin_country_id')
        destination_country_id = request.query_params.get('destination_country_id')
        weight = request.query_params.get('weight')
        created_at = request.query_params.get('created_at', timezone.now())
        customer_id = request.query_params.get('customer_id')
        customer_name = request.query_params.get('customer_name')
        customer_slug = request.query_params.get('customer_slug')

        # Generate a unique tracking number
        tracking_number = self.generate_unique_tracking_number()

        # Store the tracking number in the database
        TrackingNumber.objects.create(tracking_number=tracking_number)

        # Prepare response
        response_data = {
            'tracking_number': tracking_number,
            'created_at': created_at,
        }
        return Response(response_data)
    
    @transaction.atomic
    def generate_unique_tracking_number(self):
        """Generate a unique tracking number matching ^[A-Z0-9]{1,16}$"""
        while True:
            # Generate a random alphanumeric tracking number
            tracking_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

            # Ensure the number is unique
            if not TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
                return tracking_number
