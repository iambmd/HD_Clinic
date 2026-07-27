from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from .forms import AppointmentForm, ContactForm
from .models import Article, Doctor, Service


def home(request):
    return render(request, 'clinic/home.html', {
        'services': Service.objects.all()[:6],
        'doctors': Doctor.objects.all(),
        'articles': Article.objects.all()[:3],
    })


def about(request):
    return render(request, 'clinic/about.html', {'doctors': Doctor.objects.all()})


def services(request):
    grouped = [
        (label, Service.objects.filter(category=value))
        for value, label in Service.Category.choices
    ]
    return render(request, 'clinic/services.html', {'grouped_services': grouped})


def news(request):
    return render(request, 'clinic/news.html', {'articles': Article.objects.all()})


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'clinic/article_detail.html', {
        'article': article,
        'related': Article.objects.exclude(pk=article.pk)[:3],
    })


def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                _('Thank you! Your appointment request has been received. We will call you shortly to confirm.'),
            )
            return redirect('clinic:appointment')
    else:
        form = AppointmentForm()
    return render(request, 'clinic/appointment.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Thank you! Your message has been sent.'))
            return redirect('clinic:contact')
    else:
        form = ContactForm()
    return render(request, 'clinic/contact.html', {'form': form})


def location(request):
    return render(request, 'clinic/location.html')
