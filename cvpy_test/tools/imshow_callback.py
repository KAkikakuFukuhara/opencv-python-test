import cv2
import numpy as np


def get_image(hsize: int=480, wsize: int=640) -> np.ndarray:
    return np.random.randint(0, 255, (hsize, wsize, 3), dtype=np.uint8)


def callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


if __name__ == "__main__":

    win_name = "canvas"
    cv2.namedWindow(win_name)
    cv2.setMouseCallback(win_name, callback)
    try:
        while(True):
            ### close button checker
            if cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) <= 0:
                break

            img = get_image()
            cv2.imshow(win_name, img)

            ### key checker
            key = cv2.waitKey(1) & 0xff
            if key == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()


