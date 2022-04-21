import http.client
import ssl

from cryptography.hazmat.primitives import serialization
from pyspiffe.workloadapi.default_x509_source import DefaultX509Source

SOCKET_PATH = "unix:///tmp/spire-agent/public/api.sock"

# CERT_FILE = '/Users/client-workload/client.pem'
# KEY_FILE = '/Users/client-workload/client.key'
CERT_FILE = 'client.pem'
KEY_FILE = 'client.key'

# SERVER = 'localhost:8443'
SERVER = 'localhost:5000'

if __name__ == "__main__":
    source = DefaultX509Source(spiffe_socket_path=SOCKET_PATH)

    x509_svid = source.get_x509_svid()
    x509_svid.save(CERT_FILE, KEY_FILE, serialization.Encoding.PEM)

    context = ssl.SSLContext()
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    client = http.client.HTTPSConnection(SERVER, context=context, timeout=1)
    client.connect()
    try:
        client.request('GET', f'https://{SERVER}/')
    except Exception as e:
        print(e)
    response = client.getresponse()
    print(response.read())
    client.close()

    # response = requests.get('https://127.0.0.1:8443', verify=CERT_FILE)
    # print(response)

    # ssl_context = ssl.create_default_context(cafile=CERT_FILE)
    # ssl_context.verify_mode = ssl.CERT_REQUIRED
    # app.run(debug=True)