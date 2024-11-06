import sys
from pathlib import Path


def __add_path():
    # /cvpy_test/tools
    file_dir = Path(__file__).absolute().parent
    # /
    root_dir = file_dir.parent.parent

    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))


__add_path()

if __name__ == "__main__":
    import pprint
    pprint.pprint(sys.path)
