#!/usr/bin/env python3

import argparse
from pprint import pprint

from budgie.schemas import AccountSchema, EntrySchema
from budgie.postgres import PostgresStorageBackend

parser = argparse.ArgumentParser(prog="Budgie")
subparsers = parser.add_subparsers(dest="subcommand", required=True)

add_account = subparsers.add_parser("add_account")
add_account.add_argument("name")
add_account.add_argument("type")
add_account.add_argument("--description")

list_accounts = subparsers.add_parser("list_accounts")

add_entry = subparsers.add_parser("add_entry")
add_entry.add_argument("when")
add_entry.add_argument("cr")
add_entry.add_argument("dr")
add_entry.add_argument("amount")
add_entry.add_argument("--who")
add_entry.add_argument("--description")
add_entry.add_argument("--tag", action="append", help="can be specified multiple times")

list_entries = subparsers.add_parser("list_entries")


add_tag = subparsers.add_parser("add_tag")
add_tag.add_argument("tag")

if __name__ == "__main__":
    args = parser.parse_args()
    backend = PostgresStorageBackend()

    if args.subcommand == "add_account":
        input = {
            "name": args.name,
            "type": args.type,
        }
        if args.description:
            input["description"] = args.description
        account = AccountSchema().load(input)
        backend.create_account(account)

    if args.subcommand == "list_accounts":
        pprint(AccountSchema(many=True).dump(backend.list_accounts()))

    if args.subcommand == "add_entry":
        input = {
            "when": args.when,
            "credit_account": args.cr,
            "debit_account": args.dr,
            "amount": args.amount,
        }
        if args.who:
            input["who"] = args.who
        if args.description:
            input["description"] = args.description
        if args.tag:
            input["tags"] = args.tag
        entry = EntrySchema().load(input)
        backend.add_entry(entry)

    if args.subcommand == "list_entries":
        pprint(EntrySchema(many=True).dump(backend.list_entries()))

    if args.subcommand == "add_tag":
        backend.create_tag(args.tag)
