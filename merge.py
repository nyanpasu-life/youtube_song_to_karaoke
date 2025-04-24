import pretty_midi
import fluidsynth
from pydub import AudioSegment
import subprocess
import os
from pathlib import Path
from pydub import AudioSegment

def convert_to_synth_lead_pretty(input_path: str, gm_lead_program: int = 80):
    # MIDI 로드
    pm = pretty_midi.PrettyMIDI(input_path)
    # 모든 악기 프로그램 번호를 변경
    # for inst in pm.instruments:
    #     inst.program = gm_lead_program
    # 파일로 쓰기
    pm.write("tmp/tmpvocalconvert.mid")

def midi_to_wav(midi_path, sf2_path, wav_path):
    fs = fluidsynth.Synth()
    fs.start(driver="file")  # 파일 출력
    fs.sfload(sf2_path)
    
    fs.midi_file_play(midi_path)
    fs.write_wav(wav_path)
    fs.delete()

def wav_to_mp3(wav_path, mp3_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")

# 경로 설정
base_dir = Path("/home/xotpqnd/test/yt_to_midimp3")
midi_dir = base_dir / "midis"
sf2_file = base_dir / "resources/kgs88 v1.97.sf2"

# MIDI → WAV → MP3 변환 함수
def convert_midi_to_mp3(midi_path="tmp/tmpvocalconvert.mid", save_path="tmp",):
    # 출력 파일명 설정
    base_name = Path(midi_path).stem
    wav_output =save_path + "/" + f"{base_name}.wav"
    mp3_output = save_path + "/" + f"{base_name}.mp3"

    print(f"Converting: {midi_path} → {mp3_output}")

    # MIDI → WAV
    subprocess.run([
        "fluidsynth", "-ni", str(sf2_file), str(midi_path),
        "-F", str(wav_output), "-r", "44100"
    ])

    # WAV → MP3
    subprocess.run([
        "ffmpeg", "-y", "-i", str(wav_output), str(mp3_output)
    ])

    # 변환 후 WAV 파일 제거 (선택 사항)

def merge_vocal_and_inst(vocal_path, inst_path, save_path):
    vocal = AudioSegment.from_mp3(vocal_path)
    inst = AudioSegment.from_mp3(inst_path)

    # 보컬 볼륨 증폭
    louder_vocal = vocal.apply_gain(10)

    combined = inst.overlay(louder_vocal)
    combined.export(save_path, format="mp3")


if __name__=="__main__":
    for folder in ["res"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    model_output_dir = 'tmp/model_output'
    inst_dir = "tmp/inst"
    for root, dirs, files in os.walk("music_downloads"):
        for f in files:
            if f.endswith(".mp3"):
                relative_path = os.path.relpath(root, "music_downloads") 
                target_folder = os.path.join("res", relative_path)
                os.makedirs(target_folder, exist_ok=True)

                f_midi = f[:-4] + ".mid"
                midi_path = os.path.join(model_output_dir, f_midi)
                source_name = Path(f).stem

                convert_to_synth_lead_pretty(midi_path)
                convert_midi_to_mp3()

                inst_path = os.path.join(inst_dir, f"{source_name}.mp3")
                out_path = os.path.join(target_folder, f"{source_name}_노래방용.mp3")
                merge_vocal_and_inst("tmp/tmpvocalconvert.mp3", inst_path, out_path)

    os.remove("tmp/tmpvocalconvert.mid")
    os.remove("tmp/tmpvocalconvert.wav")
    os.remove("tmp/tmpvocalconvert.mp3")



            


