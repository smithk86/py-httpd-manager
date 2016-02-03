#!/usr/bin/env python

import os
import argparse
import requests
import logging

import py_balancer_manager
from py_balancer_manager import printer
from py_balancer_manager.prettystring import PrettyString


# disable warnings
requests.packages.urllib3.disable_warnings()


def main():

    def print_routes(routes):

        for route in routes:
            for key, status in route.get('_validate', {}).items():
                color = 'green' if status else 'red'
                route[key] = PrettyString(route[key], color)

        printer.routes(
            routes,
            args.verbose
        )

    parser = argparse.ArgumentParser()
    parser.add_argument('profile-json')
    parser.add_argument('-e', '--enforce', help='enforce profile', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='print all route information', action='store_true', default=False)
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.WARN
    logging.basicConfig(level=log_level)

    try:
        with open(getattr(args, 'profile-json')) as fh:
            full_profile_json = fh.read()
    except FileNotFoundError:
        print('file does not exist: {profile}'.format(profile=getattr(args, 'profile-json')))

    routes, compliance_status = py_balancer_manager.validate(full_profile_json, enforce=args.enforce)
    print_routes(routes)

    if args.enforce and compliance_status is False:
        print()
        print(PrettyString('***** compliance has been enforced *****', 'red'))

        routes, compliance_status = py_balancer_manager.validate(full_profile_json)
        print_routes(routes)

        if compliance_status is False:
            raise Exception('profile has been enforced but still not compliant')


if __name__ == '__main__':

    main()
