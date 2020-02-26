#!/usr/bin/env python3

import os
import sys
import time
import requests
import subprocess
import bs4


class Web:
    @staticmethod
    def get(url: str, params=None) -> requests.models.Response:
        page = requests.get(url, params=params)
        page.raise_for_status()
        return page

    @staticmethod
    def get_v(url: str, params=None) -> requests.models.Response:
        print(f'[R] open {url} with {params}')
        return Web.get(url, params)

    @staticmethod
    def parse(page: requests.models.Response) -> bs4.BeautifulSoup:
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        return soup

    @staticmethod
    def parse_v(page: requests.models.Response) -> bs4.BeautifulSoup:
        print('[S] parse')
        return Web.parse(page)

    @staticmethod
    def find(soup: bs4.BeautifulSoup, *args, **kwargs) -> bs4.element.Tag:
        return soup.find(*args, **kwargs)

    @staticmethod
    def find_href(soup: bs4.BeautifulSoup, **kwargs) -> str:
        a = Web.find(soup, 'a', **kwargs)
        return a['href']

    @staticmethod
    def download(href: str, directory: str, filename: str) -> str:
        file = Web.get(href)
        if not os.path.exists(directory):
            os.mkdir(directory)
        path = os.path.join(directory, filename)
        with open(path, 'wb') as f:
            f.write(file.content)
        return path

    @staticmethod
    def download_v(href: str, directory: str, filename: str) -> str:
        print(f'[R] download {href} into {directory} as {filename}')
        return Web.download(href, directory, filename)


class SmuleDownloader:
    @staticmethod
    def download(link: str) -> str:
        page = Web.get_v('https://sing.salon/smule-downloader/', {'url': link})
        soup = Web.parse_v(page)
        href = Web.find_href(soup, class_='ipsButton ipsButton_medium ipsButton_important')
        m4a_filename = str(time.time()) + '.m4a'
        m4a_directory = os.path.join(os.getcwd(), 'downloads')
        m4a_path = Web.download_v(href, m4a_directory, m4a_filename)
        return m4a_path


class Converter:
    @staticmethod
    def convert_m4a_to_mp3(m4a_path, mp3_path):
        print('[S] convert')
        subprocess.call(["ffmpeg", "-i", m4a_path, mp3_path])


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <smule-recording-link>')
        return

    m4a_path = SmuleDownloader.download(sys.argv[1])
    mp3_path = m4a_path.replace('.m4a', '.mp3')
    Converter.convert_m4a_to_mp3(m4a_path, mp3_path)


if __name__ == '__main__':
    main()
