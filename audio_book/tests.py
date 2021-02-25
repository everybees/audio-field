from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

import audio_book.models as am


# Create your tests here.
class AudioVieTestCase(TestCase):
    """Test Suite for the api views."""

    baseURL = "http://127.0.0.1:8000/api/audio"

    def setUp(self):
        self.client = APIClient()
        self.song_data = {
            "name": "Break Dancing",
            "audio_type": "Song",
            "duration": 300,
            "audio_file": {
                "metadata": {
                    "reconciliation_id": "123-abc-xyz"
                }
            },
        }

        self.song_data_without_duration = {
            "name": "Break Dancing",
            "audio_type": "Song",
            "audio_file": {
                "metadata": {
                    "reconciliation_id": "123-abc-xyz"
                }
            },
        }

        self.podcast_data = {
            "name": "Break Dancing",
            "audio_type": "Song",
            "duration": 300,
            "audio_file": {
                "metadata": {
                    "reconciliation_id": "123-abc-xyz"
                }
            },
            "host": "Jimmy Kimmel",
            "participants": ["Jack Daniels", "Jimmy Fallon", "Jack Dorsey"]
        }

        self.podcast_data_without_audio_file = {
            "name": "Break Dancing",
            "audio_type": "Song",
            "duration": 300,
            "host": "Jimmy Kimmel",
            "participants": ["Jack Daniels", "Jimmy Fallon", "Jack Dorsey"]
        }

        self.audiobook_data = {
            "name": "Break Dancing",
            "audio_type": "Song",
            "duration": 300,
            "audio_file": {
                "metadata": {
                    "reconciliation_id": "123-abc-xyz"
                }
            },
            "author_of_title": "Jimmy Kimmel",
            "narrator": "Jack Daniels"
        }

        self.song = am.Audio.objects.create(name="Break Dancing", duration=100, audio_type="Song", audio_file={})
        self.song_2 =am.Audio.objects.create(name="Bogey Dancing", duration=100, audio_type="Song", audio_file={})

    def test_api_can_create_audio(self):
        self.response = self.client.post(reverse('audio-list'), self.song_data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        self.response = self.client.post(reverse('audio-list'), self.song_data_without_duration, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        self.response = self.client.post(reverse('audio-list'), self.podcast_data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        self.response = self.client.post(reverse('audio-list'), self.podcast_data_without_audio_file, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        self.response = self.client.post(reverse('audio-list'), self.audiobook_data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_update_audio(self):
        data = {
            "name": "Bogey Down"
        }
        self.response = self.client.patch("{}/{}/?audio_type=Song".format(self.baseURL, self.song.id), data=data)
        self.assertEqual(self.response.status_code, status.HTTP_206_PARTIAL_CONTENT)

    def test_api_can_get_audio(self):
        self.response = self.client.get(reverse('audio-detail', kwargs={"pk": self.song_2.id}), {"audio_type": "Song"})
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_get_all_audio_for_type(self):
        self.response = self.client.get(reverse('audio-list'), {"audio_type": "Song"})
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data), 2)

        self.response = self.client.get(reverse('audio-list'), {"audio_type": "Audiobook"})
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data), 0)

    def test_api_can_delete_audio(self):

        self.response = self.client.delete("{}/{}/?audio_type=Song".format(self.baseURL, self.song.id))
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)
