#!/usr/bin/python

import argparse
import dns.name
import dns.query
import dns.dnssec
import dns.message
import dns.resolver
import dns.rdatatype

VERSION = "v1.0.0"
RELEASE = "2023-05-09"

DESCRIPTION = """
This program validates dnssec signatures in domain zones based on dns requests.
Set the domain parameter and then the program returns a message and a status code.

Release: {release}
""".format(release=RELEASE)

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3


def arg_parse() -> argparse:
    """
    Parse input arguments

    :return: argparse
    """

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=VERSION))
    parser.add_argument(
        '--domain', help="Name of domain for check", required=True)
    args = parser.parse_args()

    return args


def validate_dnssec(domain: str) -> dict:
    """
    DNSSEC validation function

    :param domain:
    :return: dict
    """

    domain = domain + "."
    result = {"message": "empty", "code": STATE_UNKNOWN}

    # get nameservers (NS) for the domain
    resolver = dns.resolver.Resolver(configure=False)
    resolver.timeout = 20
    resolver.nameservers = ['1.1.1.1',
                            '9.9.9.9',
                            '8.8.8.8']
    response = resolver.resolve(domain, rdtype=dns.rdatatype.NS)

    # use the first NS
    ns_server = response.rrset[0]
    response = dns.resolver.resolve(str(ns_server), rdtype=dns.rdatatype.A)
    ns_address = response.rrset[0].to_text()

    # get DNSKEY for zone
    request = dns.message.make_query(
        domain, dns.rdatatype.DNSKEY, want_dnssec=True)

    # set a longer timeout (in seconds)
    timeout = 20

    # try DNSSEC validation with retries
    for i in range(3):
        try:
            # send the query to the master NS
            response = dns.query.udp(request, ns_address, timeout=timeout)
            if response.rcode() != 0:
                result.update(
                    {"message": "ERROR: no DNSKEY record found or SERVEFAIL", "code": STATE_WARNING})
                return result

            # find an RRSET for the DNSKEY record
            answer = response.answer
            if len(answer) != 2:
                result.update(
                    {"message": "ERROR: could not find RRSET record (DNSKEY and RR DNSKEY) in zone", "code": STATE_WARNING})
                return result

            # check if is the DNSKEY record signed, RRSET validation
            name = dns.name.from_text(domain)
            dns.dnssec.validate(answer[0], answer[1], {name: answer[0]})
        except dns.exception.Timeout:
            # retry on timeout
            if i == 2:
                result.update(
                    {"message": "ERROR: DNSSEC validation failed after retries", "code": STATE_WARNING})
                return result
        except dns.dnssec.ValidationFailure:
            result.update(
                {"message": "CRITICAL: this domain is not likely signed by dnssec", "code": STATE_CRITICAL})
            return result
        else:
            result.update(
                {"message": "OK: there is a valid dnssec self-signed key for the domain", "code": STATE_OK})
            return result

    return result


if __name__ == "__main__":
    parse_args = arg_parse()
    validation = validate_dnssec(parse_args.domain)

    print(validation['message'])
