import abc


class StorageBackend(abc.ABC):
    @abc.abstractmethod
    def create_account(self, account):
        pass

    @abc.abstractmethod
    def delete_account(self, account_name: str):
        pass

    @abc.abstractmethod
    def add_entry(self, entry):
        pass

    @abc.abstractmethod
    def delete_entry(self, entry_name: str):
        pass
