from datetime import date, time, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import AppointmentForm
from .models import Appointment, Article, ContactMessage, Doctor, Service


def next_weekday(target):
    """The next upcoming date whose weekday() == target (never today)."""
    day = timezone.localdate() + timedelta(days=1)
    while day.weekday() != target:
        day += timedelta(days=1)
    return day


def appointment_payload(preferred_date, preferred_time):
    return {
        'full_name': 'Nguyễn Văn A',
        'phone': '+84915572887',
        'email': 'patient@example.com',
        'preferred_date': preferred_date.isoformat(),
        'preferred_time': preferred_time.strftime('%H:%M'),
        'branch': Appointment.Branch.MAIN,
    }


class PageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Service.objects.create(
            title_en='Sinusitis', title_vi='Viêm Xoang',
            description_en='Sinus care.', description_vi='Chăm sóc xoang.',
            icon='bi-wind', category=Service.Category.NOSE,
        )
        Doctor.objects.create(
            name='Dr. Test', specialty='ENT', bio_en='Bio.', bio_vi='Tiểu sử.',
        )
        cls.article = Article.objects.create(
            title_en='Hearing Loss', title_vi='Mất Thính Lực',
            content_en='Content here.', content_vi='Nội dung.',
            slug='hearing-loss',
        )

    def test_public_pages_render(self):
        for name in ['home', 'about', 'services', 'news', 'appointment', 'contact', 'location']:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(f'clinic:{name}')).status_code, 200)

    def test_article_detail_renders(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hearing Loss')

    def test_missing_article_returns_404(self):
        self.assertEqual(self.client.get('/news/does-not-exist/').status_code, 404)


class FormSubmissionTests(TestCase):
    def test_appointment_submission_is_saved(self):
        # Saturday morning window: 08:30 – 11:30
        payload = appointment_payload(next_weekday(5), time(9, 30))
        response = self.client.post(reverse('clinic:appointment'), payload)
        self.assertRedirects(response, reverse('clinic:appointment'))
        self.assertEqual(Appointment.objects.count(), 1)

    def test_contact_submission_is_saved(self):
        response = self.client.post(reverse('clinic:contact'), {
            'name': 'Test Patient',
            'phone': '+84915572887',
            'email': 'patient@example.com',
            'message': 'Do you treat tinnitus?',
        })
        self.assertRedirects(response, reverse('clinic:contact'))
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_invalid_appointment_is_rejected(self):
        response = self.client.post(reverse('clinic:appointment'), {'full_name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), 0)


class OpeningHoursTests(TestCase):
    """Booking is restricted to today-or-later, inside published opening hours.

    Weekdays  17:30 – 20:00
    Weekends  08:30 – 11:30 and 13:30 – 17:30
    """

    def assert_accepted(self, preferred_date, preferred_time):
        form = AppointmentForm(data=appointment_payload(preferred_date, preferred_time))
        self.assertTrue(form.is_valid(), form.errors.as_json())

    def assert_rejected(self, preferred_date, preferred_time, field):
        form = AppointmentForm(data=appointment_payload(preferred_date, preferred_time))
        self.assertFalse(form.is_valid())
        self.assertIn(field, form.errors)

    def test_past_date_is_rejected(self):
        yesterday = timezone.localdate() - timedelta(days=1)
        self.assert_rejected(yesterday, time(18, 0), 'preferred_date')

    def test_weekday_evening_window_is_accepted(self):
        monday = next_weekday(0)
        self.assert_accepted(monday, time(17, 30))
        self.assert_accepted(monday, time(18, 45))
        self.assert_accepted(monday, time(20, 0))

    def test_weekday_outside_evening_window_is_rejected(self):
        monday = next_weekday(0)
        for bad_time in [time(9, 0), time(17, 29), time(20, 1), time(13, 0)]:
            with self.subTest(time=bad_time):
                self.assert_rejected(monday, bad_time, 'preferred_time')

    def test_weekend_windows_are_accepted(self):
        for weekday in (5, 6):
            day = next_weekday(weekday)
            for good_time in [time(8, 30), time(11, 30), time(13, 30), time(17, 30)]:
                with self.subTest(weekday=weekday, time=good_time):
                    self.assert_accepted(day, good_time)

    def test_weekend_lunch_gap_is_rejected(self):
        saturday = next_weekday(5)
        for bad_time in [time(12, 0), time(11, 31), time(13, 29)]:
            with self.subTest(time=bad_time):
                self.assert_rejected(saturday, bad_time, 'preferred_time')

    def test_weekend_outside_hours_is_rejected(self):
        sunday = next_weekday(6)
        for bad_time in [time(7, 0), time(8, 29), time(17, 31), time(19, 0)]:
            with self.subTest(time=bad_time):
                self.assert_rejected(sunday, bad_time, 'preferred_time')

    def test_weekday_evening_is_closed_on_weekend_schedule(self):
        """19:00 is open Mon–Fri but closed on Saturday."""
        self.assert_accepted(next_weekday(0), time(19, 0))
        self.assert_rejected(next_weekday(5), time(19, 0), 'preferred_time')

    def test_date_input_blocks_past_dates_in_browser(self):
        form = AppointmentForm()
        self.assertEqual(
            form.fields['preferred_date'].widget.attrs['min'],
            timezone.localdate().isoformat(),
        )


class ApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Service.objects.create(
            title_en='Tinnitus', title_vi='Ù Tai',
            description_en='Ringing.', description_vi='Tiếng ù.',
            icon='bi-soundwave', category=Service.Category.EAR,
        )

    def test_service_list_endpoint(self):
        response = self.client.get('/api/services/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_appointment_create_endpoint(self):
        payload = appointment_payload(next_weekday(5), time(9, 30))
        response = self.client.post('/api/appointments/', payload)
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_appointment_api_rejects_past_date(self):
        payload = appointment_payload(timezone.localdate() - timedelta(days=1), time(18, 0))
        response = self.client.post('/api/appointments/', payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('preferred_date', response.json())
        self.assertEqual(Appointment.objects.count(), 0)

    def test_appointment_api_rejects_time_outside_opening_hours(self):
        payload = appointment_payload(next_weekday(0), time(9, 0))
        response = self.client.post('/api/appointments/', payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('preferred_time', response.json())
        self.assertEqual(Appointment.objects.count(), 0)

    def test_contact_create_endpoint(self):
        response = self.client.post('/api/contact/', {
            'name': 'API Patient',
            'phone': '+84915572887',
            'email': 'api@example.com',
            'message': 'Hello',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactMessage.objects.count(), 1)


class BilingualTests(TestCase):
    def test_localized_property_follows_active_language(self):
        service = Service.objects.create(
            title_en='Tonsillitis', title_vi='Viêm Amidan',
            description_en='EN desc.', description_vi='VI desc.',
            icon='bi-shield-plus', category=Service.Category.THROAT,
        )
        with self.settings(LANGUAGE_CODE='en'):
            self.assertEqual(service.title, 'Tonsillitis')
        from django.utils import translation

        with translation.override('vi'):
            self.assertEqual(service.title, 'Viêm Amidan')
