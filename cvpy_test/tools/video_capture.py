""" mp4動画の再生
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

    win_name = "img1"
    video_capture = cv2.VideoCapture(str(mp4_path))
    cv2.namedWindow('img1')
    can_read: bool = True
    try:
        while(True):
            ### close button checker
            if cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) <= 0:
                break

            can_read, frame = video_capture.read()
            if not can_read:
                break

            cv2.imshow('img1', frame)

            key = cv2.waitKey(1) & 0xff
            if key == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(type(e), e)
    finally:
        cv2.destroyAllWindows()

    ### デストラクタで開放されるが明示的に開放
    video_capture.release()
