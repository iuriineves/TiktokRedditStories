from video_resources import create_video_resources as cvr
from moviepy.editor import *
from moviepy.video.fx.all import crop
import random
import os
import pyperclip

videos, titles = cvr('TrueOffMyChest', 1)

for video_name in videos:

    #Setting video and music starting time
    video_duration = 0
    i = k = r = 0
    random_video_time = random.randint(30, 4200)
    random_music_time = random.randint(0, 3600)

    #Setting video duration, images and audios
    for audio in sorted(os.listdir(f'video-resources/{video_name}/audios')):
        audio = AudioFileClip(f'video-resources/{video_name}/audios/{audio}')
        image = ImageClip(f'video-resources/{video_name}/images/{sorted(os.listdir(f"video-resources/{video_name}/images"))[k]}')
        image = image.set_duration(audio.duration)
        image = image.resize(width = 985)
        video_duration += audio.duration
        if i == 0:
            voice = audio
            text = image
            i += 1
        else:
            voice = concatenate_audioclips([voice, audio])
            text = concatenate([text, image])
        k += 1
    #Setting background music and video
    music = AudioFileClip(f'music/{random.choice(os.listdir("music"))}').subclip(random_music_time, random_music_time + video_duration + 2).volumex(0.05)
    background = VideoFileClip('backgroundvideo.mp4').subclip(random_video_time, random_video_time + video_duration + 2).resize(height=1920).volumex(0.0)
    text = text.set_position('center')


    (w, h) = background.size
    background = crop(background, height=1920, width=1080, x_center=w/2, y_center=h/2)

    final_audio = CompositeAudioClip([voice, music])
    final_video = background.set_audio(final_audio).volumex(0.7)
    final_video = CompositeVideoClip([final_video, text])
    final_video.write_videofile(f'{video_name}.mp4')

    print(titles[r])
    k = i = 0
    r += 1

