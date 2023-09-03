import os
from pathlib import Path

def download_post(url: str) -> list[Path, list[Path]] | None:
    short_code = list(filter(lambda x: bool(x), url.split('?')[0].split('/')))[-1]

    os.system(f'instaloader --no-captions --no-metadata-json --no-video-thumbnails -- -{short_code}')
    
    folder_path = Path(f'-{short_code}').absolute()
    if os.path.exists(folder_path):
        path_files = []
        for i in os.listdir(folder_path):
            path_files.append(Path(os.path.join(folder_path, i)))
        return [Path(f'-{short_code}'), path_files]
    else:
        return None
def main() -> None:
    # post_path = download_post(url='https://youtu.be/nF1XwHnwtps?si=KZBA8WqZ-rP0Msed')
    post_path = download_post(url='https://www.instagram.com/p/CvTlTdZKueT/')
    print(post_path)
if __name__ == "__main__":
    main()