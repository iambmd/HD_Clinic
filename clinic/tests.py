from datetime import date, time

from django.test import TestCase
from django.urls import reverse

from .models import Appointment, Article, ContactMessage, Doctor, Service


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
        response = self.client.post(reverse('clinic:appointment'), {
            'full_name': 'Nguyễn Văn A',
            'phone': '+84915572887',
            'email': 'patient@example.com',
            'preferred_date': '2026-08-01',
            'preferred_time': '09:30',
            'branch': Appointment.Branch.MAIN,
        })
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
        response = self.client.post('/api/appointments/', {
            'full_name': 'API Patient',
            'phone': '+84915572887',
            'email': 'api@example.com',
            'preferred_date': str(date(2026, 8, 1)),
            'preferred_time': str(time(9, 30)),
            'branch': Appointment.Branch.MAIN,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Appointment.objects.count(), 1)

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
