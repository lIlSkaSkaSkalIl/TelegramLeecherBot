import gdown

def download_gdrive(url: str, output: str = "gdrive_file"):
    try:
        # ✅ fuzzy=True untuk auto-handle link view?usp=sharing → download
        return gdown.download(url, output, fuzzy=True, quiet=False)
    except Exception as e:
        print(f"[GDRIVE ERROR] {e}")
        return None
