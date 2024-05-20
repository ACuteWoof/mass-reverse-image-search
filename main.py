# requirements: google-image-source-search

from google_img_source_search import ReverseImageSearcher
import requests
import os


def tmpfile(file_path):
    url="https://tmpfiles.org/api/v1/upload"
    files={'file': open(file_path, 'rb')}
    res = requests.post(url, files=files)
    r = res.json()['data']['url'].replace("https://tmpfiles.org", "https://tmpfiles.org/dl")
    return r


def get_files(search_path):
    for (dirpath, _, filenames) in os.walk(search_path):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def filter_images(files):
    images = []
    for filepath in files:
        splitfp = filepath.split(".")
        if splitfp[-1] in ["jpeg", "jpg", "png", "dng", "webp"] and splitfp[1] not in ["env"]:
            images.append(filepath)
    return images


if __name__ == '__main__':
    filepaths = filter_images(get_files("."))
    print(f"Searching for: {filepaths}")
    rev_img_searcher = ReverseImageSearcher()

    for filepath in filepaths:
        image_url = tmpfile(filepath)
        res = rev_img_searcher.search(image_url)
        
        print(20*"=")
        print(filepath)
        print(image_url)
        print(20*"-")
        for search_item in res:
            print(f'Title  :    {search_item.page_title}')
            print(f'Site   :    {search_item.page_url}')
            print(f'Image  :    {search_item.image_url}\n')
