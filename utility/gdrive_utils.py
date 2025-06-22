import gdown

def download_gdrive(url: str, output: str = None):
    try:
        return gdown.download(url, output=output, fuzzy=True, quiet=False)
    except Exception as e:
        print(f"[GDRIVE ERROR] {e}")
        return None
