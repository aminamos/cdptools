#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path
from typing import Union

import ffmpeg

from .audio_splitter import AudioSplitter

###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)4s: %(module)s:%(lineno)4s %(asctime)s] %(message)s'
)
log = logging.getLogger(__file__)

###############################################################################


class FFmpegAudioSplitter(AudioSplitter):

    def __init__(self):
        pass

    def split(self, video_read_path: Union[str, Path], audio_save_path: Union[str, Path]) -> Path:
        # Check paths
        video_read_path = Path(video_read_path).resolve(strict=True)
        audio_save_path = Path(audio_save_path).resolve()
        if audio_save_path.is_file():
            return audio_save_path

        # Construct ffmpeg dag
        stream = ffmpeg.input(video_read_path)
        stream = ffmpeg.output(stream, filename=audio_save_path, f=audio_save_path.suffix[1:])

        # Run dag
        out, err = ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)

        # Find base log target
        log_target = audio_save_path.parent / "ffmpeg_log"

        # Store logs
        with open(log_target.with_suffix(".out"), "wb") as write_out:
            write_out.write(out)
        with open(log_target.with_suffix(".err"), "wb") as write_err:
            write_err.write(err)

        return audio_save_path