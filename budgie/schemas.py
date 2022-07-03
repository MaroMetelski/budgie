from marshmallow import Schema, fields, validate, post_load

ACCOUNT_TYPES = ("expense", "income", "equity", "asset", "liability")


class Account:
    def __init__(self, name, type, description=""):
        self.name = name
        self.description = description
        self.type = type


class Entry:
    def __init__(
        self, when, credit_account, debit_account, amount, who="", description=""
    ):
        self.when = when
        self.credit_account = credit_account
        self.debit_account = debit_account
        self.amount = amount
        self.who = who
        self.description = description


class AccountSchema(Schema):
    class Meta:
        ordered = True

    name = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(ACCOUNT_TYPES))
    description = fields.Str()

    @post_load
    def make_account(self, data, **kwargs):
        return Account(**data)


class EntrySchema(Schema):
    class Meta:
        ordered = True

    when = fields.Date(required=True)
    credit_account = fields.Str(required=True)
    debit_account = fields.Str(required=True)
    amount = fields.Number(required=True)
    who = fields.Str()
    description = fields.Str()

    @post_load
    def make_entry(self, data, **kwargs):
        return Entry(**data)
