from accounts import Account
from passbook import Passbook


a = Account("MI7299", "Mohd","Izhar", 500)
print(a)
print(("#" * 100).center(100))

# Deposit Money
code = a.deposit(100)
print("Depositing Money ($100)\n".center(100))
print("\nTransaction Code: ",  code)
print("New Balance: ", a.balance)
print(("#" * 100).center(100))


# withdraw money
code = a.withdraw(70)
print("Withdrawing Money ($70)\n".center(100))
print("\nTransaction Code: ",  code)
print("\nNew Balance: ", a.balance)
print(("#" * 100).center(100))


# interest money
code = a.payInterest()
print("Paying Interest ($)\n".center(100))
print("\nTransaction Code: ",  code)
print("\nNew Balance: ", a.balance)
print(("#" * 100).center(100))


# Print passbook
print("Printing PassBook\n\n".center(100))
pbook = Passbook([['01 Sep 2021 13:36:05 IST +0530', '100', '', '300'],
 ['01 Sep 2021 13:36:16 IST +0530', '', '700', '1000'],
 ['01 Sep 2021 13:36:25 IST +0530', '', '60.0', '1060.0']])
pbook.print_passbook()
print("\n\n\n")
print(("#" * 100).center(100))

print(repr(a))