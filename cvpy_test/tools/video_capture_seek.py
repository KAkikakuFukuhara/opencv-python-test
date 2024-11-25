""" 動画ファイルの再生位置をシークバーを用いて変更
"""
from __future__ import annotations
from typing import Any
import datetime
import time

from pathlib import Path
from argparse import ArgumentParser

import cv2
import numpy as np


def callback(value: int):
    curr_pos_ms = video_capture.get(cv2.CAP_PROP_POS_MSEC) # ms
    curr_frame_pos = int(round(curr_pos_ms/1000*fps, 0))
    ### call from without pointer
    if value == curr_frame_pos:
        return

    ### update frame postion
    time_pos = value/fps
    time_pos = time_pos*1000 # sec to ms
    video_capture.set(cv2.CAP_PROP_POS_MSEC, time_pos)

    ### update window when state is stop
    if not is_update:
        can_read, frame = video_capture.read()
        if can_read:
            cv2.imshow('img1', frame)
    print("{}: {}".format(datetime.datetime.now(), value))


class ContextDelay:
    """ デフォルトだと読み込みが早すぎるのでFPSに合わせるように擬似的に遅延させるクラス
        with構文で用いる
    """
    def __init__(self, fps):
        self.last_capture_time = 0.0
        self.fps = fps


    def __enter__(self):
        self.start_time = time.time()
        self.spf = 1 / self.fps


    def __exit__(self, *args, **kwargs):
        curr_time = time.time()
        if curr_time - self.last_capture_time < self.spf:
            elapd_time = time.time() - self.start_time
            time.sleep(self.spf-elapd_time)
        self.last_capture_time = curr_time


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("mp4", type=str, help="mp4 file path")
    cli_args: dict[str, Any] = vars(parser.parse_args())

    mp4_path = Path(cli_args['mp4'])
    assert mp4_path.exists()
    assert mp4_path.suffix == ".mp4"

    video_capture = cv2.VideoCapture(str(mp4_path))
    num_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    context_delay = ContextDelay(fps)
    is_update: bool = True

    win_name = "img1"
    cv2.namedWindow('img1')
    cv2.createTrackbar("track1", "img1", 0, num_frames, callback)
    can_read: bool = True
    try:
        while(True):
            ### close button checker
            if cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) <= 0:
                break

            if is_update:
                with context_delay:
                    can_read, frame = video_capture.read()
                if not can_read:
                    video_capture.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
                    continue

                ### update trackbar sync frame loading
                curr_pos_ms = video_capture.get(cv2.CAP_PROP_POS_MSEC) # ms
                curr_frame_pos = int(round(curr_pos_ms/1000*fps, 0))
                cv2.setTrackbarPos("track1", "img1", curr_frame_pos)

                cv2.imshow('img1', frame)

            key = cv2.waitKey(1) & 0xff
            if key == ord('q'): # quit
                break
            if key == ord('s'): # stop
                is_update = False
            if key == ord('b'): # begin
                is_update = True
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(type(e), e)
    finally:
        cv2.destroyAllWindows()

    ### デストラクタで開放されるが明示的に開放
    video_capture.release()

