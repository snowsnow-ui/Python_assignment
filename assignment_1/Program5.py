class BankError(Exception):
    pass


class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = int(balance)

    def deposit(self, amount):
        if amount <= 0:
            raise BankError("Invalid amount")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise BankError("Invalid amount")
        if amount > self.balance:
            raise BankError("Insufficient funds")
        self.balance -= amount


class Transaction:
    def __init__(self, operation, account1, account2, amount):
        self.operation = operation
        self.account1 = account1
        self.account2 = account2
        self.amount = amount


class Bank:
    def __init__(self, accounts):
        self.accounts = accounts
        self.history = []

    def execute(self, transaction):
        if transaction.operation == "DEPOSIT":
            self.accounts[transaction.account1].deposit(transaction.amount)
        elif transaction.operation == "WITHDRAW":
            self.accounts[transaction.account1].withdraw(transaction.amount)
        elif transaction.operation == "TRANSFER":
            self.accounts[transaction.account1].withdraw(transaction.amount)
            self.accounts[transaction.account2].deposit(transaction.amount)
        else:
            raise BankError("Invalid operation")
        self.history.append(transaction)


def main():
    try:
        n = int(input())
        accounts = {}

        for _ in range(n):
            account_id, balance = input().split()
            accounts[account_id] = Account(account_id, int(balance))

        q = int(input())
        bank = Bank(accounts)
        batch_number = 0
        in_batch = False
        batch_failed = False
        old_balances = {}
        failed_batches = []

        for _ in range(q):
            parts = input().split()

            if parts[0] == "BATCH_BEGIN":
                batch_number += 1
                in_batch = True
                batch_failed = False
                old_balances = {}
                for key in accounts:
                    old_balances[key] = accounts[key].balance
                continue

            if parts[0] == "BATCH_END":
                if in_batch and batch_failed:
                    for key in accounts:
                        accounts[key].balance = old_balances[key]
                    failed_batches.append(batch_number)
                in_batch = False
                batch_failed = False
                continue

            if in_batch and batch_failed:
                continue

            try:
                if parts[0] == "DEPOSIT" and len(parts) == 3:
                    if parts[1] not in accounts:
                        raise BankError
                    transaction = Transaction("DEPOSIT", parts[1], "", int(parts[2]))
                    bank.execute(transaction)

                elif parts[0] == "WITHDRAW" and len(parts) == 3:
                    if parts[1] not in accounts:
                        raise BankError
                    transaction = Transaction("WITHDRAW", parts[1], "", int(parts[2]))
                    bank.execute(transaction)

                elif parts[0] == "TRANSFER" and len(parts) == 4:
                    if parts[1] not in accounts or parts[2] not in accounts:
                        raise BankError
                    transaction = Transaction("TRANSFER", parts[1], parts[2], int(parts[3]))
                    bank.execute(transaction)

                else:
                    raise BankError

            except (ValueError, BankError):
                if in_batch:
                    batch_failed = True

        if in_batch and batch_failed:
            for key in accounts:
                accounts[key].balance = old_balances[key]
            failed_batches.append(batch_number)

        for number in failed_batches:
            print("FAILED", number)

        for account_id in sorted(accounts):
            print(account_id, accounts[account_id].balance)

    except (ValueError, EOFError):
        print("INVALID INPUT")


if __name__ == "__main__":
    main()
