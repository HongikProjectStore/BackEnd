
import django_filters
from .models import Product
# from rest_framework import filters

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point    

# class NearestNeighborFilterBackend(filters.BaseFilterBackend):
#     """
#     Filter that only allows users to see their own objects.
#     """
#     def filter_queryset(self, request, queryset, view):
#         longitude = request.query_params.get("longitude", None)
#         latitude = request.query_params.get("latitude", None)

#         ref_location = Point(longitude, latitude, srid=4326)
#         queryset = Store.objects.filter(location__dwithin=(ref_location, 0.02)). \
#             filter(location__distance_lte=(ref_location, D(m=2000))). \
#             annotate(distance=Distance('location', ref_location)).order_by('distance')

#         return queryset
