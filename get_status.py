"""Do the thing."""

# TODO: - add tests
#       - make sure info is actually getting posted

import codecs

import urllib3

BRULTECH_DEVICE = "192.168.2.5"
EMONCMS = "192.168.2.4"
first = "?"
last = " HTTP/1.1"

http = urllib3.PoolManager()


def find_between(s, first, last):
    """Find string."""
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def get_btinfo(btdev_ip):
    """Return device information."""
    url = "http://" + btdev_ip + "/4?SPK=Show+Packet"
    return http.request('GET', url, preload_content=False)


def decode_reponse(response):
    """Return utf-8 string."""
    reader = codecs.getreader('utf-8')
    return reader(response.data)


def get_new_request(response, first, last):
    """Create new request payload."""
    return find_between(response, first, last)


def post_to_emoncms(emoncms_ip, updated_request):
    """Post data to emoncms."""
    url = ("http://" + emoncms_ip + "/emoncms/input/post.json?"
           + updated_request)
    return http.request('POST', url)


def all_the_things(btdev_ip, emoncms_ip):
    """Put it all together."""
    response = get_btinfo(btdev_ip)
    decoded_reponse = decode_reponse(response)
    updated_response = get_new_request(decoded_reponse, first, last)
    post_to_emoncms(emoncms_ip, updated_response)


all_the_things(BRULTECH_DEVICE, EMONCMS)
