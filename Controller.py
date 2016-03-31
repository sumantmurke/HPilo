
import sys
import ssl
if (sys.version_info >= (3, 0)):
   from urllib.parse import urlparse
else:
   from urlparse import urlparse
   from httplib import HTTPSConnection, HTTPConnection

import base64
import json

# REST operation generic handler
def rest_op(operation, host, suburi, request_headers, request_body, iLO_loginname, iLO_password, x_auth_token=None, enforce_SSL=False):

    print "inside rest_op"
    url = urlparse('https://' + host + suburi)
    if request_headers is None:
        request_headers = dict()

    # if X-Auth-Token specified, supply it instead of basic auth
    if x_auth_token is not None:
        request_headers['X-Auth-Token'] = x_auth_token
    # else use iLO_loginname/iLO_password and Basic Auth
    elif iLO_loginname is not None and iLO_password is not None:
        request_headers['Authorization'] = "BASIC " + base64.b64encode(iLO_loginname + ":" + iLO_password)
        print request_headers['Authorization']


    conn = None
    if url.scheme == 'https':
        if( sys.version_info.major == 2 and
            sys.version_info.minor == 7 and
            sys.version_info.micro >= 9 and
            enforce_SSL            == False):
            cont=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            cont.verify_mode = ssl.CERT_NONE
            conn = HTTPSConnection(host=url.netloc, strict=True, context=cont, port=443)
        else:
            conn = HTTPSConnection(host=url.netloc, strict=True, port=443)
    else:
        assert(False)
    conn.request(operation, url.path, headers=request_headers, body=json.dumps(request_body))
    resp = conn.getresponse()
    body = resp.read()
    print body


def main():
    # my code here
    # print "inside main"
    rest_op('GET', "<ip-address>", "/rest/v1", None, None, "<username>", "<password>")

if __name__ == "__main__":
    main()