import requests
import zipfile
import os
from tqdm import tqdm
import shutil

url = 'http://data.csail.mit.edu/tofu/dataset/vimeo_septuplet.zip'
filename = 'vimeo90k.zip'

resume_headers = {}
if os.path.exists(filename):
    resume_headers = {'Range': f'bytes={os.path.getsize(filename)}-'}

response = requests.get(url, headers=resume_headers, stream=True)
total_size = int(response.headers.get('content-length', 0))

with open(filename, 'ab') as out_file:
    with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                out_file.write(chunk)
                pbar.update(len(chunk))

with zipfile.ZipFile(filename, 'r') as zip_ref:
    script_dir = os.path.dirname(os.path.abspath(__file__))

    dest_zip = os.path.join(script_dir, os.path.basename(filename))
    if os.path.abspath(filename) != os.path.abspath(dest_zip):
        try:
            shutil.move(filename, dest_zip)
            filename = dest_zip
        except Exception:
            pass

    src_dir = os.path.abspath('vimeo90k')
    dest_dir = os.path.join(script_dir, 'vimeo90k')
    if os.path.abspath(src_dir) != os.path.abspath(dest_dir) and os.path.exists(src_dir):
        try:
            if os.path.exists(dest_dir):
                shutil.rmtree(src_dir)
            else:
                shutil.move(src_dir, dest_dir)
        except Exception:
            pass
