from rest_framework import serializers
import audio_book.models as am


class AudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = am.Audio
        fields = '__all__'
        read_only_fields = ('upload_time',)


class PodcastSerializer(serializers.ModelSerializer):
    audio_id = serializers.ReadOnlyField(source='audio.id')
    name = serializers.ReadOnlyField(source='audio.name')
    audi_type = serializers.ReadOnlyField(source='audio.audio_type')
    duration = serializers.ReadOnlyField(source='audio.duration')

    class Meta:
        model = am.Podcast
        exclude = ('audio', 'id')


class AudiobookSerializer(serializers.ModelSerializer):
    audio_id = serializers.ReadOnlyField(source='audio.id')
    name = serializers.ReadOnlyField(source='audio.name')
    audi_type = serializers.ReadOnlyField(source='audio.audio_type')
    duration = serializers.ReadOnlyField(source='audio.duration')

    class Meta:
        model = am.Audiobook
        exclude = ('audio', 'id')
