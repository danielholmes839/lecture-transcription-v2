import os

from constants import VIDEO_DIR, AUDIO_DIR


def video_to_audio():
    print('------------ CONVERTING VIDEO TO AUDIO ------------')
    for video in os.listdir(VIDEO_DIR):
        video_name, video_extension = tuple(video.split('.'))

        video_path = os.path.abspath(os.path.join(
            VIDEO_DIR, video_name)) + '.' + video_extension

        audio_path = os.path.abspath(os.path.join(AUDIO_DIR, video_name))
        os.system(
            f'ffmpeg -i {video_path} -ar 16000 -ac 1 {audio_path}.wav -y')
