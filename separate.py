import torchaudio
from openunmix.predict import separate
import numpy as np
from pydub import AudioSegment
import os

def save_tensor_as_mp3(tensor, save_path):
    wave_tensor = tensor.to('cpu').squeeze(0) 
    wave_tensor = wave_tensor.float()

    # 텐서를 [-1.0, 1.0] 범위로 정규화 후 int16로 변환
    wave_np = wave_tensor.numpy()
    wave_np = wave_np / np.max(np.abs(wave_np))  # 정규화
    wave_np = (wave_np * 32767).astype(np.int16)

    # 스테레오 처리
    samples = np.stack([wave_np[0], wave_np[1]], axis=1).flatten()

    # AudioSegment로 변환
    audio = AudioSegment(
        samples.tobytes(),
        frame_rate=44100,
        sample_width=2,  # 16bit = 2 bytes
        channels=2
    )

    # mp3로 저장
    audio.export(save_path, format="mp3")


def separate_audio(load_dir, audio_path, save_dir):

    load_path = os.path.join(load_dir, audio_path)
    audio_name = audio_path.split(".")[0]

    # 1) 오디오 파일 로드
    audio, rate = torchaudio.load(load_path)
    # ▷ audio: Tensor(shape=(channels, samples)), rate: 샘플레이트 :contentReference[oaicite:1]{index=1}

    # 2) 분리 실행
    estimates = separate(
        audio=audio,                              # 입력 오디오 Tensor
        rate=rate,                                # 오디오 샘플레이트
        model_str_or_path='umxl',                 # 사용할 사전학습 모델 (기본: 'umx') :contentReference[oaicite:2]{index=2}
        targets=['vocals'],                       # 분리할 타겟 (여기서는 보컬) 
        niter=1,                                  # Wiener 필터링 반복 횟수
        residual=True,                           # 잔여(residual) 스템 생성 여부
        device='cuda',                            # GPU 사용 (없으면 'cpu')
    )
    # ▷ estimates: {'vocals': Tensor, 'drums': Tensor, …} 형태 딕셔너리 반환 :contentReference[oaicite:3]{index=3}

    vocal_tensor = estimates["vocals"]
    inst_tensor = estimates["residual"]

    save_vocal_dir = os.path.join(save_dir, "vocal")
    save_vocal_path = os.path.join(save_vocal_dir, audio_path)
    save_tensor_as_mp3(vocal_tensor, save_vocal_path)

    save_inst_dir = os.path.join(save_dir, "inst")
    save_inst_path = os.path.join(save_inst_dir, audio_path)
    save_tensor_as_mp3(inst_tensor, save_inst_path)



if __name__=="__main__":
    for folder in ["tmp/vocal", "tmp/inst", "tmp/vocal_midi"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    load_dir = 'music_downloads'
    save_dir = "tmp"
    for f in os.listdir(load_dir):
        if f.endswith('.mp3'):
            separate_audio(load_dir, f, save_dir)