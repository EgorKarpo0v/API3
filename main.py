from urllib.parse import urlparse
import requests
import json
import os
import argparse


def shorten_link(token, link):
    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {"Authorization": f"Bearer {token}"}

    params = {"long_url": link}

    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(token, bitlink):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks"
    headers = {"Authorization": f"Bearer {token}"}

    params = {"unit": "month", "units": "-1"}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["units"]


def is_bitlink(token, bitlink):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(description='Программа позволяет получать сокращенную ссылку, а также посчитать клики по ссылкам')
    parser.add_argument('--url', type=str, help='Введите ссылку')
    args = parser.parse_args()
    parser_url = urlparse(args.url)
    parser_url = f"{parser_url.netloc}{parser_url.path}"
    try:
        if is_bitlink(token, parser_url):
            print(count_clicks(token, parser_url))
        else:
            print(shorten_link(token, args.url))
    except requests.exceptions.HTTPError:
        print("Ошибка, проверьте ссылку или токен")


if __name__ == '__main__':
    main()
