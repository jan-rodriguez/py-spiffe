import logging
import ssl

import cryptography.x509
from cryptography.hazmat.primitives import serialization
from flask import Flask
from pyspiffe.spiffe_id.spiffe_id import TrustDomain
from pyspiffe.workloadapi.default_x509_source import DefaultX509Source

import log

SOCKET_PATH = "unix:///tmp/spire-agent/public/api.sock"

app = Flask(__name__)

CERT_FILE = 'server.pem'
KEY_FILE = 'server.key'
BUNDLE_FILE = 'bundle.pem'

logger = logging.getLogger()


@app.route("/")
def hello():
    logger.info("Hello")
    return "Hello World!"


def main():
    source = DefaultX509Source(spiffe_socket_path=SOCKET_PATH)

    trust_domain = TrustDomain.parse("spiffe://example.org/server")

    trust_bundle = source.get_bundle_for_trust_domain(trust_domain)
    trust_bundle.save(bundle_path=BUNDLE_FILE, encoding=serialization.Encoding.PEM)

    x509_svid = source.get_x509_svid()
    x509_svid.save(CERT_FILE, KEY_FILE, serialization.Encoding.PEM)
    context = ssl.SSLContext()
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    context.load_verify_locations(capath=BUNDLE_FILE)
    # context.verify_mode = ssl.VerifyMode.CERT_REQUIRED
    # context.verify_flags = ssl.VerifyFlags.VERIFY_X509_STRICT

    # logger.info(context.cert_store_stats())
    app.run(ssl_context=context, debug=True)


def load_cert_file():
    with open(CERT_FILE, 'rb') as cert_file:
        data = cert_file.read()
        cert = cryptography.x509.load_pem_x509_certificate(data=data)
        print(cert)


if __name__ == "__main__":
    log.set_up_logging()
    main()
    # load_cert_file()
