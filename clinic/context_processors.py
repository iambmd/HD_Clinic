from django.conf import settings


def clinic_info(request):
    return {'clinic': settings.CLINIC_INFO}
