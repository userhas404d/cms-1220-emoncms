"""Do the thing."""

import requests
from invoke import task


@task
def repost(ctx, apikey, json, node, host):
    """Repost CMS REST call."""
    url = ("http://" + host + "/emoncms/input/post?node=" + node + "&json="
           + json + "&apikey=" + apikey)
    requests.get(url)
