from .models import Store
from rest_framework import filters
from django.db.models.expressions import RawSQL

class NearestNeighborFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        longitude = request.query_params.get("longitude", None)
        latitude = request.query_params.get("latitude", None)

        gcd_formula = "6371 * acos(least(greatest(\
        cos(radians(%s)) * cos(radians(latitude)) \
        * cos(radians(longitude) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(latitude)) \
        , -1), 1))"
        distance_raw_sql = RawSQL(
            gcd_formula,
            (latitude, longitude, latitude)
        )
        queryset = Store.objects.all() \
        .annotate(distance=distance_raw_sql) \
        .order_by('distance')
        queryset = queryset.filter(distance__lt=2000)
        return queryset