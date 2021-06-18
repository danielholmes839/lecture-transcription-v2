# Lecture Transcription V2

1. Create a Google Cloud Platform credentials.json
2. Install [ffmpeg](https://www.ffmpeg.org/) for converting .mp4 files into .mp3
3. Install python requirements `pip install -r requirements.txt`
4. Create a folder named "video" and put your .mp4 files in the folder. The folder name can be changed in [constants.py](./constants.py) by changing the `VIDEO_DIR`.
5. Create a bucket in Google Cloud storage and edit the `BUCKET` variable in [constants.py](./constants.py)
6. Run `python main.py`
