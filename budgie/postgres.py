from sqlalchemy import create_engine, String, Column, Integer, Date, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .backend import StorageBackend
from .schemas import AccountSchema, EntrySchema

DB_STRING = "postgresql+psycopg2://postgres:postgres@localhost:5433/budgie-v0"

base = declarative_base()


class AccountModel(base):
    __tablename__ = "account"
    name = Column(String, primary_key=True)
    description = Column(String)
    type = Column(String)


class EntryModel(base):
    __tablename__ = "entry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    who = Column(String)
    when = Column(Date)
    credit_account = Column(String, ForeignKey(AccountModel.name))
    debit_account = Column(String, ForeignKey(AccountModel.name))
    amount = Column(Numeric)
    description = Column(String)


class PostgresStorageBackend(StorageBackend):
    def __init__(self):
        self.db = create_engine(DB_STRING)
        Session = sessionmaker(self.db)
        self.session = Session()
        base.metadata.create_all(self.db)

    def create_account(self, account):
        acc = AccountModel(
            name=account.name,
            description=account.description,
            type=account.type,
        )
        self.session.add(acc)
        self.session.commit()

    def delete_account(self, account_name: str):
        pass

    def add_entry(self, entry):
        entry = EntryModel(
            who=entry.who,
            when=entry.when,
            credit_account=entry.credit_account,
            debit_account=entry.debit_account,
            amount=entry.amount,
            description=entry.description,
        )
        self.session.add(entry)
        self.session.commit()

    def delete_entry(self, entry_name: str):
        pass

    def list_entries(self):
        entries = self.session.query(EntryModel)
        entry_list = []
        for entry in entries:
            entry_list.append(
                EntrySchema().load(
                    {
                        "when": str(entry.when),
                        "description": entry.description,
                        "credit_account": entry.credit_account,
                        "debit_account": entry.debit_account,
                        "amount": entry.amount,
                        "who": entry.who,
                    }
                )
            )
        return entry_list

    def list_accounts(self):
        accounts = self.session.query(AccountModel)
        acc_list = []
        for account in accounts:
            acc_list.append(
                AccountSchema().load(
                    {
                        "name": account.name,
                        "description": account.description,
                        "type": account.type,
                    }
                )
            )
        return acc_list
