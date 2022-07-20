import logging

from pytube import YouTube, Stream
from pytube.exceptions import RegexMatchError, VideoUnavailable

from app.exceptions.load_api import LoadError
from app.services.api.base import AbstractLoader, Audio
from app.settings.paths import LOADED_CACHE_DIR


class YouTubeLoader(AbstractLoader):

    def load(self, user_id: int) -> Audio:
        """Loads audio from YouTube video"""

        try:
            yt = YouTube(url=self._url)
            videos = yt.streams.filter(only_audio=True, mime_type="audio/mp4")
            video = self._get_best_file(videos)
            video.download(output_path=str(LOADED_CACHE_DIR), filename=f"{user_id}.mp3")
            return Audio(
                file_name=video.title.title(),
                file_path=self.get_dst_path(user_id)
            )

        except (RegexMatchError, VideoUnavailable):
            raise LoadError

        except Exception as e:
            logging.error(e)
            raise LoadError

    def get_dst_path(self, user_id: int) -> str:
        return str(LOADED_CACHE_DIR / f"{user_id}.mp3")

    def _get_best_file(self, streams: list[Stream]) -> Stream:
        return sorted(streams, key=self._get_abr)[-1]

    @staticmethod
    def _get_abr(stream: Stream) -> int:
        return int(str(stream.abr).replace("kbps", ""))
