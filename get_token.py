import requests
from requests.auth import HTTPBasicAuth

consumer_key = "SGNxFR4Qt25tyF9DM2Yaq3ckfxWQPbANdYtGO9GmPYACqxrS"
consumer_secret = "VGYhA3e7mFrG9yxZlES5fOJ4E8XgGlm4UbZUhKqxs1f1DsDwGGSIwRzH4n5nRgkh"

url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

print(response.text)
