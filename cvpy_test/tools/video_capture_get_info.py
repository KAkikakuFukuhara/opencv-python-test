""" 動画ファイルからのデータの取得（FPSなど)
"""
from __future__ import annotations
from typing import Any

from pathlib import Path
from argparse import ArgumentParser

import cv2
import numpy as np


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("mp4", type=str, help="mp4 file path")
    cli_args: dict[str, Any] = vars(parser.parse_args())

    mp4_path = Path(cli_args['mp4'])
    assert mp4_path.exists()
    assert mp4_path.suffix == ".mp4"

    video_capture = cv2.VideoCapture(str(mp4_path))

    ### https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
    print("{1}: {0}".format(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH), "FrameWidth\t\t"))
    print("{1}: {0}".format(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT), "FrameHeight\t\t"))
    print("{1}: {0}".format(video_capture.get(cv2.CAP_PROP_FPS), "FPS\t\t\t"))
    print("{1}: {0}".format(video_capture.get(cv2.CAP_PROP_FRAME_COUNT), "総フレーム数\t\t"))
    print("{1}: {0}".format(video_capture.get(cv2.CAP_PROP_POS_MSEC), "ビデオファイルの現在位置(ms)"))
    ### 開始位置=0, 終端位置=1
    # print("{1}: {0}".format(video_capture.get(cv2.CAP_PROP_POS_AVI_RATIO), "ビデオファイルの開始位置か終端位置か"))

