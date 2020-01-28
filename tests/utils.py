import os


def get_relative_path(filepath: str):
    return os.path.join(os.path.dirname(__file__), filepath)
