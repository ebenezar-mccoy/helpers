#!env python3
import requests

websites = [
    ['country', 'code', 'website_url'],
]


class Cache:
    """Scripts that verifies cahe headers."""

    def verify():
        for e in websites:
            tenant, id, address = e[0], e[1], e[2]
            cookie = {'{!s}webXX'.format(tenant): '{!s}web01'.format(tenant)}
            url = "https://{!s}/xmedia/img/{!s}/film.placeholder.poster.jpg".format(
                address, id
            )
            response = requests.get(url, cookies=cookie)
            try:
                header_x_f5_cache = response.headers['X-F5-Cache']
            except:
                header_x_f5_cache = 'NO_HEADER'
            print('{!s:20} X-Cache: {!s:<5} X-F5-Cache: {!s}'.format(
                address,
                response.headers['X-Cache'],
                header_x_f5_cache)
            )

if __name__ == '__main__':
    Cache.verify()
