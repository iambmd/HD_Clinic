from django.conf import settings

from . import opening_hours


def clinic_info(request):
    return {
        'clinic': settings.CLINIC_INFO,
        'opening_hours': opening_hours.display_schedule(),
    }
