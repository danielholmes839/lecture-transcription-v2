import os
import shutil

from constants import TEXT_DIR, AUDIO_DIR, VIDEO_DIR


def setup():
    # Reset the TEXT_DIR
    if os.path.exists(TEXT_DIR):
        shutil.rmtree(TEXT_DIR)
    os.mkdir(TEXT_DIR)

    # Reset the AUDIO_DIR
    if os.path.exists(AUDIO_DIR):
        shutil.rmtree(AUDIO_DIR)
    os.mkdir(AUDIO_DIR)

    # Create the VIDEO_DIR
    if not os.path.exists(VIDEO_DIR):
        os.mkdir(VIDEO_DIR)
