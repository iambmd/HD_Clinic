from rest_framework import serializers

from . import opening_hours
from .models import Appointment, Article, ContactMessage, Doctor, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title_en', 'title_vi', 'description_en', 'description_vi', 'icon', 'category']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialty', 'bio_en', 'bio_vi', 'photo']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id', 'title_en', 'title_vi', 'content_en', 'content_vi',
            'thumbnail', 'published_date', 'slug',
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id', 'full_name', 'phone', 'email',
            'preferred_date', 'preferred_time', 'branch', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        errors = opening_hours.slot_errors(
            attrs.get('preferred_date'), attrs.get('preferred_time')
        )
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'phone', 'email', 'message', 'sent_at']
        read_only_fields = ['id', 'sent_at']
