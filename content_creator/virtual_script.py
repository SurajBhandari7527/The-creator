import json
import numpy as np
import soundfile as sf
import torchaudio
from cached_path import cached_path
import ast
import re
import os
from pydub import AudioSegment
from f5_tts.model import DiT, UNetT
from f5_tts.infer.utils_infer import (
    load_vocoder,
    load_model,
    preprocess_ref_audio_text,
    infer_process,
    remove_silence_for_generated_wav,
    save_spectrogram,
)

with open(r'content_creator\script.json','r', encoding='utf-8') as f:
    script=json.load(f)

script=script[0]
split_list = [item.split(",.") for item in script]

# Flatten, clean up whitespace, and wrap in double quotes
final_script = [f'"{sub_string.strip()}"' for sublist in split_list for sub_string in sublist if sub_string.strip()]

l1=[0]
output_final_path = r'D:\models\english\output\final_output.wav'
if os.path.exists(output_final_path):
    os.remove(output_final_path)

def get_audio_length(audio_path):
    audio = AudioSegment.from_file(audio_path)
    duration_in_ms = len(audio)  # Duration in milliseconds
    duration_in_sec = duration_in_ms / 1000  # Convert to seconds
    l1.append(l1[-1]+duration_in_sec)
    return 

# Load the vocoder and TTS model (e.g., F5-TTS)
vocoder = load_vocoder()

def load_f5tts(ckpt_path=str(cached_path("hf://SWivid/F5-TTS/F5TTS_Base/model_1200000.safetensors"))):
    F5TTS_model_cfg = dict(dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4)
    return load_model(DiT, F5TTS_model_cfg, ckpt_path)

F5TTS_ema_model = load_f5tts()

def infer_without_gradio(ref_audio_path, ref_text, gen_text, model, remove_silence=False):
    """Generates audio without Gradio."""

    ref_audio, ref_text = preprocess_ref_audio_text(ref_audio_path, ref_text)

    final_wave, final_sample_rate, combined_spectrogram = infer_process(
        ref_audio,
        ref_text,
        gen_text,
        model,
        vocoder,
        cross_fade_duration=0.15,
        nfe_step=50,
        speed=1,
        show_info=print,
    )

    if remove_silence:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            sf.write(f.name, final_wave, final_sample_rate)
            remove_silence_for_generated_wav(f.name)
            final_wave, _ = torchaudio.load(f.name)
        final_wave = final_wave.squeeze().cpu().numpy()

    return final_sample_rate, final_wave, combined_spectrogram

# Example usage:
ref_audio_path = r"D:\models\english\clone_samples\narrative_pitch.mp3"
ref_text = "Hi I am Ethan. I am the guy next door delivering engaging narrative content in an easy to digest conversational flow."
count=1
for i in final_script:
    sample_rate, audio_data, spectrogram = infer_without_gradio(ref_audio_path, ref_text, i, F5TTS_ema_model)
    # Save the generated audio
    output_file_path="D:\models\english\output\output{}.wav".format(count)
    sf.write(output_file_path, audio_data, sample_rate)
    get_audio_length(output_file_path)
    count=count+1
    


def merge_wav_files(input_folder, output_file):
    # Create an empty AudioSegment
    combined = AudioSegment.empty()

    # Function to extract the numeric part of the filename
    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else float('inf')

    # Get all .wav files in the folder
    wav_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]

    # Sort the files based on the numeric part of the filename
    wav_files.sort(key=lambda f: extract_number(f))

    # Iterate through the sorted list of .wav files
    for filename in wav_files:
        file_path = os.path.join(input_folder, filename)
        audio_segment = AudioSegment.from_wav(file_path)  # Load the WAV file
        combined += audio_segment  # Append to the combined audio

    # Export the combined audio to a new file
    combined.export(output_file, format="wav")
    print(f"Merged audio saved to: {output_file}")


def delete_files(count,input_folder):
    for i in range(1,count):
        audio_path=input_folder+"/output{}.wav".format(i)
        os.remove(audio_path)
# Example usage
input_folder = r"D:\models\english\output"  # Replace with your folder path
output_file = r"D:\models\english\output\final_output.wav"  # Replace with desired output path
merge_wav_files(input_folder, output_file)
l1.remove(0)
print(l1)
with open("D:\models\english\list.json",'w') as f:
    json.dump(l1,f)
delete_files(count,input_folder) 

print("Audio generated and saved to generated_audio.wav")