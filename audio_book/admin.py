from django.contrib import admin
import audio_book.models as am


# Register your models here.
class AudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'audio_type', 'audio_file' ,'upload_time')


class PodcastAdmin(admin.ModelAdmin):
    list_display = ('audio', 'host', 'participants')


class AudiobookAdmin(admin.ModelAdmin):
    list_display = ('audio', 'author_of_title', 'narrator')


admin.site.register(am.Audio, AudioAdmin)
admin.site.register(am.Podcast, PodcastAdmin)
admin.site.register(am.Audiobook, AudiobookAdmin)
