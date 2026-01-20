import requests
import zipfile
import os
from tqdm import tqdm

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
    zip_ref.extractall('vimeo90k')
