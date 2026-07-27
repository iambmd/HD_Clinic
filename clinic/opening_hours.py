"""Single source of truth for when the clinic accepts appointments.

Used by the booking form, the REST API serializer and the templates that
display opening hours, so the three can never drift apart.
"""
from datetime import time

from django.utils import timezone
from django.utils.dates import WEEKDAYS
from django.utils.translation import gettext_lazy as _

WEEKNIGHT = ((time(17, 30), time(20, 0)),)
WEEKEND = ((time(8, 30), time(11, 30)), (time(13, 30), time(17, 30)))

# Keyed by Python's date.weekday(): Monday is 0, Sunday is 6.
SCHEDULE = {
    0: WEEKNIGHT,
    1: WEEKNIGHT,
    2: WEEKNIGHT,
    3: WEEKNIGHT,
    4: WEEKNIGHT,
    5: WEEKEND,
    6: WEEKEND,
}

# Grouped for display; each entry covers days that share the same hours.
DISPLAY_SCHEDULE = (
    (_('Monday – Friday'), WEEKNIGHT),
    (_('Saturday – Sunday'), WEEKEND),
)


def windows_for(value):
    """Opening windows for the weekday of `value`, or () when closed."""
    return SCHEDULE.get(value.weekday(), ())


def format_windows(windows):
    """Render windows as '17:30 – 20:00' or '08:30 – 11:30, 13:30 – 17:30'."""
    if not windows:
        return str(_('Closed'))
    return ', '.join(
        '%s – %s' % (start.strftime('%H:%M'), end.strftime('%H:%M'))
        for start, end in windows
    )


def display_schedule():
    """Template-friendly opening hours: [{'label': ..., 'hours': ...}, ...]."""
    return [
        {'label': label, 'hours': format_windows(windows)}
        for label, windows in DISPLAY_SCHEDULE
    ]


def slot_errors(preferred_date, preferred_time):
    """Validate a requested slot.

    Returns a {field_name: message} dict — empty when the slot is bookable.
    Callers raise their own exception type so this stays framework-neutral.
    """
    errors = {}
    if preferred_date is None:
        return errors

    today = timezone.localdate()
    if preferred_date < today:
        errors['preferred_date'] = _('Please choose today or a later date.')
        return errors

    windows = windows_for(preferred_date)
    day_name = WEEKDAYS[preferred_date.weekday()]

    if not windows:
        errors['preferred_date'] = _('The clinic is closed on %(day)s.') % {'day': day_name}
        return errors

    if preferred_time is None:
        return errors

    if not any(start <= preferred_time <= end for start, end in windows):
        errors['preferred_time'] = _(
            'The clinic is open %(hours)s on %(day)s. Please choose a time within those hours.'
        ) % {'hours': format_windows(windows), 'day': day_name}
        return errors

    if preferred_date == today and preferred_time <= timezone.localtime().time():
        errors['preferred_time'] = _(
            'That time has already passed today. Please choose a later time or another day.'
        )

    return errors
