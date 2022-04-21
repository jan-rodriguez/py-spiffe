import logging
import log

from pyspiffe.workloadapi.default_x509_source import DefaultX509Source

SOCKET_PATH = "unix:///tmp/spire-agent/public/api.sock"

loggger = logging.getLogger()


def main():
    source = DefaultX509Source(spiffe_socket_path=SOCKET_PATH)

    x509_svid = source.get_x509_svid()

    # bundle = source.get_bundle_for_trust_domain(TrustDomain.parse('spiffe://example.org/random'))

    loggger.info(x509_svid)


if __name__ == '__main__':
    log.set_up_logging()
    main()

