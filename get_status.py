"""do the thing."""

import requests

BRULTECH_DEVICE = "192.168.2.5"

response = requests.get(BRULTECH_DEVICE)
print(response)
