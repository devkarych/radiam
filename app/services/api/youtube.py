import logging

from pytube import YouTube

from app.exceptions.load_api import LoadError
from app.services.api.base import AbstractLoader, Audio
from app.settings.paths import LOADED_CACHE_DIR
from pytube.exceptions import RegexMatchError, VideoUnavailable


class YouTubeLoader(AbstractLoader):

    path = str

    def load(self, user_id: int) -> Audio:
        """Loads audio from YouTube video"""

        try:
            yt = YouTube(url=self._url)
            video = yt.streams.filter(only_audio=True).first()
            video.download(output_path=LOADED_CACHE_DIR, filename=f"{user_id}.mp3")
            return Audio(
                file_name=video.title.title(),
                file_path=self.get_dst_path(user_id)
            )

        except (RegexMatchError, VideoUnavailable):
            raise LoadError

        except Exception as e:
            logging.error(e)
            raise LoadError

    def get_dst_path(self, user_id: int) -> path:
        return str(LOADED_CACHE_DIR / f"{user_id}.mp3")
