# parcels/views.py
import re
import random
import string
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TrackingNumber
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache

class NextTrackingNumberView(APIView):
    """
    API endpoint to generate a unique tracking number.
    
    The API accepts the following query parameters:
    - `origin_country_id`: The order's origin country code in ISO 3166-1 alpha-2 format (e.g., "MY").
    - `destination_country_id`: The order's destination country code in ISO 3166-1 alpha-2 format (e.g., "ID").
    - `weight`: The order's weight in kilograms, up to three decimal places (e.g., "1.234").
    - `created_at`: The order's creation timestamp in RFC 3339 format (e.g., "2018-11-20T19:29:32+08:00").
    - `customer_id`: The customer's UUID (e.g., "de619854-b59b-425e-9db4-943979e1bd49").
    - `customer_name`: The customer's name (e.g., "RedBox Logistics").
    - `customer_slug`: The customer's name in slug-case/kebab-case (e.g., "redbox-logistics").
    
    Returns a response with the generated tracking number and the current timestamp.
    """
    
    def get(self, request):
        # Extract query parameters
        origin_country_id = request.query_params.get('origin_country_id')
        destination_country_id = request.query_params.get('destination_country_id')
        weight = request.query_params.get('weight')
        created_at = request.query_params.get('created_at', timezone.now().strftime("%Y-%m-%dT%H:%M:%S%z"))
        customer_id = request.query_params.get('customer_id')
        customer_name = request.query_params.get('customer_name')
        customer_slug = request.query_params.get('customer_slug')

        # Validate query parameters
        error_messages = []
        
        if not origin_country_id:
            error_messages.append('Missing origin_country_id')
        if not destination_country_id:
            error_messages.append('Missing destination_country_id')
        if not weight:
            error_messages.append('Missing weight')
        if not created_at:
            error_messages.append('Missing created_at')
        if not customer_id:
            error_messages.append('Missing customer_id')
        if not customer_name:
            error_messages.append('Missing customer_name')
        if not customer_slug:
            error_messages.append('Missing customer_slug')
        
        if error_messages:
            return Response({'error': 'Missing required query parameters: ' + ', '.join(error_messages)}, status=400)
        
        # Validate created_at timestamp
        try:
            datetime.datetime.fromisoformat(created_at)
        except ValueError:
            return Response({'error': 'Invalid created_at timestamp'}, status=400)
        
        # Validate weight
        try:
            float(weight)
        except ValueError:
            return Response({'error': 'Invalid weight'}, status=400)
        
        # Generate tracking number based on parameters
        tracking_number = self.generate_unique_tracking_number(origin_country_id, destination_country_id, weight, created_at, customer_id, customer_name, customer_slug)
        
        # Check if the tracking number is cached
        cached_tracking_number = cache.get(tracking_number)

        if cached_tracking_number:
            return Response({'tracking_number': cached_tracking_number, 'created_at': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")})

        # Store the tracking number in the database
        TrackingNumber.objects.create(tracking_number=tracking_number)

        # Prepare response
        response_data = {
            'tracking_number': tracking_number,
            'created_at': created_at,
            'origin_country_id': origin_country_id,
            'destination_country_id': destination_country_id,
            'weight': weight,
            'customer_id': customer_id,
            'customer_name': customer_name,
            'customer_slug': customer_slug
        }
        return Response(response_data)
    
    @transaction.atomic
    def generate_unique_tracking_number(self, origin_country_id, destination_country_id, weight, created_at, customer_id, customer_name, customer_slug):
        """
        Generate a unique tracking number matching ^[A-Z0-9]{1,16}$.

        Parameters:
        origin_country_id (int): The ID of the origin country.
        destination_country_id (int): The ID of the destination country.
        weight (float): The weight of the shipment.
        customer_id (int): The ID of the customer.
        customer_name (str): The name of the customer.
        customer_slug (str): The slug of the customer.

        Returns:
        str: A unique tracking number.
        """
        # Create a hash of the parameters to ensure uniqueness
        params_hash = hash((origin_country_id, destination_country_id, weight, created_at, customer_id, customer_name, customer_slug))
        tracking_number_prefix = str(params_hash)[:8]  # Take the first 8 characters of the hash

        # Generate a random alphanumeric tracking number
        tracking_number_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        # Combine the prefix and suffix to create the tracking number
        tracking_number = f"{tracking_number_prefix}{tracking_number_suffix}"
        # Ensure the number is unique
        while self.is_valid_tracking_number(tracking_number) and TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
            # Regenerate the suffix if the tracking number already exists
            tracking_number_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            tracking_number = f"{tracking_number_prefix}{tracking_number_suffix}"

        return tracking_number

    def is_valid_tracking_number(self, tracking_number):
        # Validate the tracking number against the regex pattern
        pattern = r"^[A-Z0-9]{1,16}$"
        return bool(re.match(pattern, tracking_number))
