import gdown

def download_gdrive(url: str, output: str = "gdrive_file"):
    try:
        return gdown.download(url, output, quiet=False)
    except Exception as e:
        print(f"[GDRIVE ERROR] {e}")
        return None
