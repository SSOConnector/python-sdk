# ssoconnector-python-sdk

Add SAML SSO login for python applications

## Installation

```bash
pip install ssoconnector
```

## Usage

This is sample flask example

```python
from ssoconnector import SSOConnectorClient, InvalidRequest
from flask import Flask, request

@app.route("/sso/login/callback")
def callback():
  token = request.args.get("token")
  client = SSOConnectorClient(os.environ.get("SSOCONNECTOR_CLIENT_ID"), os.environ.get("SSOCONNECTOR_CLIENT_SECRET"))
  try:
    response = client.sso_response(token)
    print(response)
    # login user to your app
  except InvalidRequest:
    # error handling
    pass

```