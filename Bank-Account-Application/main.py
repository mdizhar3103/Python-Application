from accounts import Account
from transaction import TransactionId
from passbook import Passbook
from datafile import Data
from hashpin import HashPin
from getpass import getpass
import pandas as pd



def register_user():
    acnum = input("Enter your account Number [Must be Alpha Numeric] 'MI3103' >>> ".rjust(100))
    fname = input("Enter your First Name >>> ".rjust(100)).title()
    lname = input("Enter your Last Name >>> ".rjust(100)).title()
    bal = int(input("Enter the initial balance amount >>> ".rjust(100)))
    
    return (acnum, fname, lname, bal)


file_data = Data("register.csv")

def get_passbook(acnum):
    columns = ["Account Num", "Passbook data"]
    pdata = pd.read_table("passbook_data.txt", header=None, sep="\t",names=columns )
    grps = pdata.groupby("Account Num")
    temp = None
    for g in grps:
        if g[0] == acnum:
            temp = g[1]["Passbook data"].apply(lambda x: x.split(","))
            break
    if temp is not None:
        return temp.to_list()
    else:
        return "No trasaction Found!".center(100)
    

if __name__ == "__main__":
    flag = True
    
    while flag:
        accnt_already_exist = file_data.unique_account_numbers()
        accnt_details = file_data.account_details()
        
        print(('#' * 168).center(168))
        print("""
        PRESS 1: For Account Creation
        PRESS 2: For Passbook Print
        PRESS 3: For Withdrawl
        PRESS 4: For Deposit
        PRESS 5: For Interest
        PRESS 6: For Account Info
        
        PRESS 7: To Exit

        """.center(100))

        userinput = int(input("Enter the Choice from above: >>> ".rjust(100)))
        
        if userinput == 7:
            flag = False
            
        elif userinput == 1:
            user = register_user()
            if user[0] in accnt_already_exist:
                print(('#' * 168).center(168) + "\n")
                print("Account Number Already Exist enter different account number\n".rjust(100))
            else:            
                a = Account( accountNumber=user[0], firstName=user[1], lastName=user[2], initialBalance=user[3])
                raw_pin = getpass("Enter 4 digit PIN: >>> ".rjust(100))
                hp = HashPin(raw_pin)
                pin = hp.calculate_hash()
                with open("register.csv", 'a+') as file1:
                    file1.write(f"{user[0]},{user[1]},{user[2]},{user[3]},{pin}\n")
                print(('#' * 168).center(168) + "\n")
                print("Account Created Successfully!".rjust(100))
                print(a)
                
        elif userinput == 2:
            acnum = input("Enter your account Number: >>> ".rjust(100))
            if acnum not in accnt_already_exist:
                print(('#' * 168).center(168) + "\n")
                print("Account Doesn't Exist or Incorrect Account Number".rjust(100))
            else: 
                book = get_passbook(acnum)
                if isinstance(book, str):
                    print(book)
                else:
                    pbook = Passbook(book)
                    pbook.print_passbook()
                
        elif userinput == 3:
            acnum = input("Enter your account Number: >>> ".rjust(100)).strip()
            if acnum not in accnt_already_exist:
                print(('#' * 168).center(168) + "\n")
                print("Account Doesn't Exist or Incorrect Account Number".rjust(100))
            else:
                detail = accnt_details.get(acnum)
                a = Account(acnum, detail[0], detail[1], detail[2])
                raw_pin = getpass("Enter 4 digit PIN: >>> ".rjust(100))
                hp = HashPin(raw_pin)
                pin = hp.calculate_hash()
                if pin != detail[3]:
                    print("Invalid Login Pin".rjust(100))
                else:
                    amt = int(input("Enter amount to withdraw: >>> ".rjust(100)))
                    code = a.withdraw(amt)
                    print(('#' * 168).center(168) + "\n")
                    print("Transaction processed: ".rjust(100), code)
                    print(a)
        
        elif userinput == 4:
            acnum = input("Enter your account Number: >>> ".rjust(100)).strip()
            if acnum not in accnt_already_exist:
                print(('#' * 168).center(168) + "\n")
                print("Account Doesn't Exist or Incorrect Account Number".rjust(100))
            else:
                detail = accnt_details.get(acnum)
                a = Account(acnum, detail[0], detail[1], detail[2])
                raw_pin = getpass("Enter 4 digit PIN: >>> ".rjust(100))
                hp = HashPin(raw_pin)
                pin = hp.calculate_hash()
                if pin != detail[3]:
                    print("Invalid Login Pin".rjust(100))
                else:
                    amt = int(input("Enter amount to deposit: >>> ".rjust(100)))
                    code = a.deposit(amt)
                    print(('#' * 168).center(168) + "\n")
                    print("Transaction processed: ".rjust(100), code)
                    print(a)
        
        elif userinput == 5:
            acnum = input("Enter your account Number: >>> ".rjust(100)).strip()
            if acnum not in accnt_already_exist:
                print(('#' * 168).center(168) + "\n")
                print("Account Doesn't Exist or Incorrect Account Number".rjust(100))
            else:
                detail = accnt_details.get(acnum)
                print("Paying Interest")
                a = Account(acnum, detail[0], detail[1], detail[2])
                code = a.payInterest()
                print(('#' * 168).center(168) + "\n")
                print("Transaction processed: ".rjust(100), code)
                print(a)
                
        elif userinput == 6:
            acnum = input("Enter your account Number: >>> ".rjust(100)).strip()
            if acnum not in accnt_already_exist:
                print(('#' * 168).center(168) + "\n")
                print("Account Doesn't Exist or Incorrect Account Number".rjust(100))
            else:
                detail = accnt_details.get(acnum)
                a = Account(acnum, detail[0], detail[1], detail[2])
                print(a)
        
        else:
            print(('#' * 168).center(168) + "\n")
            print("Invalid Input".rjust(100))
            
            
            
