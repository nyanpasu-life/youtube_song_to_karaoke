import subprocess
import os

# 다운로드할 URL 리스트
play_list_url = [
    "https://www.youtube.com/playlist?list=PLkn9dHJPr0yEmyXOR0i24AgvywiEzHtzn",
    "https://www.youtube.com/watch?v=2gW7G0Hhs4A&list=PL4lD-ksRXc6cCdcMc0OJ08XnbRak_xtg6",
    "https://www.youtube.com/playlist?list=PLy9xDuyr-8eTAfTgT2YSwX9LVLj4cvmPe"
]

# 현재 디렉토리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# 1. download.py 를 각 URL에 대해 실행
for url in play_list_url:
    script_path = os.path.join(current_dir, "download.py")
    print(f"Downloading from {url}...")
    
    result = subprocess.run(["python", script_path, url], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(f"Error downloading from {url}:\n{result.stderr}")
        break  # 에러 발생 시 중단

# 2. 나머지 스크립트 순차 실행
other_scripts = [
    "separate.py",
    "run_amt_subprocess.py",
    "merge.py"
    "clear.py"
]

for script in other_scripts:
    script_path = os.path.join(current_dir, script)
    print(f"Running {script}...")
    
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(f"Error in {script}:\n{result.stderr}")
        break