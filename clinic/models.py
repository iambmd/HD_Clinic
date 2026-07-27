from django.db import models
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class BilingualMixin:
    """Resolves a `<field>_en` / `<field>_vi` pair against the active language."""

    def localized(self, field):
        suffix = 'vi' if get_language() == 'vi' else 'en'
        return getattr(self, f'{field}_{suffix}')


class Service(BilingualMixin, models.Model):
    class Category(models.TextChoices):
        EAR = 'EAR', _('Ear')
        NOSE = 'NOSE', _('Nose')
        THROAT = 'THROAT', _('Throat')

    title_en = models.CharField(_('title (EN)'), max_length=200)
    title_vi = models.CharField(_('title (VI)'), max_length=200)
    description_en = models.TextField(_('description (EN)'))
    description_vi = models.TextField(_('description (VI)'))
    icon = models.CharField(
        _('icon'), max_length=100,
        help_text=_('Bootstrap Icons class name, e.g. bi-ear'),
    )
    category = models.CharField(_('category'), max_length=10, choices=Category.choices)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        ordering = ['category', 'title_en']

    def __str__(self):
        return self.title_en

    @property
    def title(self):
        return self.localized('title')

    @property
    def description(self):
        return self.localized('description')


class Doctor(BilingualMixin, models.Model):
    name = models.CharField(_('name'), max_length=200)
    specialty = models.CharField(_('specialty'), max_length=200)
    bio_en = models.TextField(_('biography (EN)'))
    bio_vi = models.TextField(_('biography (VI)'))
    photo = models.ImageField(_('photo'), upload_to='doctors/', blank=True, null=True)

    class Meta:
        verbose_name = _('doctor')
        verbose_name_plural = _('doctors')
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def bio(self):
        return self.localized('bio')


class Article(BilingualMixin, models.Model):
    title_en = models.CharField(_('title (EN)'), max_length=300)
    title_vi = models.CharField(_('title (VI)'), max_length=300)
    content_en = models.TextField(_('content (EN)'))
    content_vi = models.TextField(_('content (VI)'))
    thumbnail = models.ImageField(_('thumbnail'), upload_to='articles/', blank=True, null=True)
    published_date = models.DateField(_('published date'), default=timezone.localdate)
    slug = models.SlugField(_('slug'), max_length=350, unique=True)

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ['-published_date', '-id']

    def __str__(self):
        return self.title_en

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('clinic:article_detail', kwargs={'slug': self.slug})

    @property
    def title(self):
        return self.localized('title')

    @property
    def content(self):
        return self.localized('content')

    @property
    def excerpt(self):
        text = ' '.join(self.content.split())
        return text[:180] + '…' if len(text) > 180 else text


class Appointment(models.Model):
    class Branch(models.TextChoices):
        MAIN = 'MAIN', _('Main Clinic – Dương Nội')

    full_name = models.CharField(_('full name'), max_length=200)
    phone = models.CharField(_('phone'), max_length=20)
    email = models.EmailField(_('email'))
    preferred_date = models.DateField(_('preferred date'))
    preferred_time = models.TimeField(_('preferred time'))
    branch = models.CharField(
        _('branch'), max_length=50, choices=Branch.choices, default=Branch.MAIN,
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('appointment')
        verbose_name_plural = _('appointments')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} – {self.preferred_date} {self.preferred_time}'


class ContactMessage(models.Model):
    name = models.CharField(_('name'), max_length=200)
    phone = models.CharField(_('phone'), max_length=20)
    email = models.EmailField(_('email'))
    message = models.TextField(_('message'))
    sent_at = models.DateTimeField(_('sent at'), auto_now_add=True)

    class Meta:
        verbose_name = _('contact message')
        verbose_name_plural = _('contact messages')
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.name} – {self.sent_at:%Y-%m-%d}'
