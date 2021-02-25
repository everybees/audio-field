from rest_framework import status, viewsets
from rest_framework.response import Response

import audio_book.models as am
import audio_book.serializers as aus


# Create your views here.
class AudioViewSets(viewsets.ModelViewSet):
    serializer_class = aus.AudioSerializer
    queryset = am.Audio.objects.all()

    def create(self, request, *args, **kwargs):
        audio_type = request.data.get('audio_type')
        serializer = aus.AudioSerializer(data=request.data)
        if request.data.get('audio_file'):
            if serializer.is_valid():
                audio = serializer.save()
                if audio_type == 'Podcast':
                    am.Podcast.objects.create(audio=audio, host=request.data.get('host'),
                                              participants=request.data.get('participants'))
                elif audio_type == 'Audiobook':
                    am.Audiobook.objects.create(audio=audio, author_of_title=request.data.get('author_of_title'),
                                                narrator=request.data.get('narrator'))
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Enter the audio metadata"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        audio_type = self.request.query_params.get('audio_type')
        try:
            if audio_type == 'Podcast':
                audio = am.Podcast.objects.get(audio_id=pk, audio__audio_type=audio_type)
                serializer = aus.PodcastSerializer(audio)
            elif audio_type == "Audiobook":
                audio = am.Audiobook.objects.get(audio_id=pk, audio__audio_type=audio_type)
                serializer = aus.AudiobookSerializer(audio)
            else:
                audio = am.Audio.objects.get(id=pk, audio_type=audio_type)
                serializer = aus.AudioSerializer(audio)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except am.Audio.DoesNotExist:
            return Response({"message": "This Song does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except am.Podcast.DoesNotExist:
            return Response({"message": "This Podcast does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except am.Audiobook.DoesNotExist:
            return Response({"message": "This Audiobook does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)})

    def list(self, request, *args, **kwargs):
        audio_type = self.request.query_params.get('audio_type')
        try:
            if audio_type == 'Podcast':
                audio = am.Podcast.objects.filter(audio__audio_type=audio_type)
                serializer = aus.PodcastSerializer(audio, many=True)
            elif audio_type == "Audiobook":
                audio = am.Audiobook.objects.filter(audio__audio_type=audio_type)
                serializer = aus.AudiobookSerializer(audio, many=True)
            else:
                audio = am.Audio.objects.filter(audio_type=audio_type)
                serializer = aus.AudioSerializer(audio, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)})

    def update(self, request, pk=None, *args, **kwargs):
        audio_type = self.request.query_params.get('audio_type')
        try:
            if audio_type == 'Podcast':
                audio = am.Podcast.objects.get(audio_id=pk, audio__audio_type=audio_type)
                serializer = aus.PodcastSerializer(audio, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
            elif audio_type == "Audiobook":
                audio = am.Audiobook.objects.get(audio_id=pk, audio__audio_type=audio_type)
                serializer = aus.AudiobookSerializer(audio, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
            else:
                audio = am.Audio.objects.get(id=pk, audio_type=audio_type)
                serializer = aus.AudioSerializer(audio, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        except am.Audio.DoesNotExist:
            return Response({"message": "This Song does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except am.Podcast.DoesNotExist:
            return Response({"message": "This Podcast does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except am.Audiobook.DoesNotExist:
            return Response({"message": "This Audiobook does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)})

    def destroy(self, request, pk=None, *args, **kwargs):
        audio_type = self.request.query_params.get('audio_type')
        try:
            if audio_type == 'Podcast':
                audio = am.Podcast.objects.get(audio_id=pk, audio__audio_type=audio_type)
                audio.delete()
            elif audio_type == "Audiobook":
                audio = am.Audiobook.objects.get(audio_id=pk, audio__audio_type=audio_type)
                audio.delete()
            else:
                audio = am.Audio.objects.get(id=pk, audio_type=audio_type)
                audio.delete()
            return Response({"message": "Audio deleted"}, status=status.HTTP_204_NO_CONTENT)
        except am.Audio.DoesNotExist:
            return Response({"message": "This Song does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except am.Podcast.DoesNotExist:
            return Response({"message": "This Podcast does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except am.Audiobook.DoesNotExist:
            return Response({"message": "This Audiobook does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)})

