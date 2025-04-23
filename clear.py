import shutil

if __name__=="__main__":
    try:
        shutil.rmtree("tmp")
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree("res")
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree("music_downloads")
    except FileNotFoundError:
        pass