import argparse


def parse_odoo_arguments():
    parser = argparse.ArgumentParser(
        description="Application for the reception of the foodhub in munich"
    )
    parser.add_argument("url", help="url of odoo instance")
    parser.add_argument("db", help="database in odoo instance")
    parser.add_argument("username", help="username to use the xmlrcp of odoo")
    parser.add_argument("password", help="password to use the xmlrcp of odoo")
    return parser.parse_args()
