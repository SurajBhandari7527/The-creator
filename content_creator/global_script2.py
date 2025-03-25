

import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, VideoFileClip, CompositeVideoClip
import json
from pydub.utils import mediainfo

def apply_smooth_zoom_in_out(clip, zoom_duration=2, max_zoom=1.1):
  
    def zoom_effect(t):
        if t < zoom_duration:  # First 2 seconds: zoom in
            return 1 + (max_zoom - 1) * (t / zoom_duration)
        elif t < 2 * zoom_duration:  # Next 2 seconds: zoom out
            return max_zoom - (max_zoom - 1) * ((t - zoom_duration) / zoom_duration)
        else:
            return 1  # No zoom after the effect ends

    return clip.fl_time(lambda t: t).resize(lambda t: zoom_effect(t))

def create_video_with_photos_from_folder(image_folder, audio_path, timestamps, output_path, duration, overlay_path=None, overlay_opacity=0.5, fade_duration=0.3):

    # Load audio
    audio = AudioFileClip(audio_path)

    # Get list of image paths sorted by filename
    image_paths = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

    # Create a list to hold the image clips
    clips = []

    # Start time for the first clip
    current_time = 0

    # Iterate over the images and timestamps
    for i, timestamp in enumerate(timestamps):
        if i >= len(image_paths):
            break

        image_duration = timestamp - current_time
        image_clip = ImageClip(image_paths[i]).set_duration(image_duration).crossfadein(fade_duration)
        image_clip = apply_smooth_zoom_in_out(image_clip, zoom_duration=2)
        clips.append(image_clip)
        current_time = timestamp

    # Handle the last image
    if len(image_paths) > len(timestamps):
        last_image_clip = ImageClip(image_paths[-1]).set_duration(duration - timestamps[-1])
        last_image_clip = last_image_clip.crossfadein(fade_duration)
        last_image_clip = apply_smooth_zoom_in_out(last_image_clip, zoom_duration=2)
        clips.append(last_image_clip)

    # Concatenate all the image clips
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)

    # If overlay video is provided, overlay it with scaling and opacity
    if overlay_path:
        overlay_clip = VideoFileClip(overlay_path).set_duration(video.duration).set_opacity(overlay_opacity)
        overlay_clip = overlay_clip.resize(1.1).resize(height=video.h)  # Scale overlay and match height
        video = CompositeVideoClip([video, overlay_clip.set_position(("center", "center"))])

    # Write the final video to a file
    video.write_videofile(output_path, codec="libx264", fps=24)

# Example usage
image_folder = r"D:\models\english\photos"  # Path to the folder containing images
audio_path = r"D:\models\english\output\final_output.wav"  # Path to your audio file
with open ("D:\models\english\list.json",'r') as f:
    timestamps=json.load(f)

    #read counter
with open ("D:\models\english\content_creator\counter.json",'r') as f:
    counter=int(json.load(f))
output_path = r"D:\models\english\output_video\output{}.mp4".format(counter)  # Path for the final video

# Fetch audio duration
info = mediainfo(audio_path)
duration = float(info['duration'])
print(f"Audio Duration: {duration} seconds")
overlay_path = r"D:\models\english\glitch_effect.mp4"  # Path to overlay video
overlay_opacity = 0.3  # Adjust the opacity of the overlay video

create_video_with_photos_from_folder(image_folder, audio_path, timestamps, output_path, duration, overlay_path, overlay_opacity)
counter=counter+1
with open("D:\models\english\content_creator\counter.json",'w') as f:
    json.dump(counter,f)