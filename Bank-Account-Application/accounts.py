import textwrap
import numbers
from tzlocal import get_localzone
import pytz
import itertools
from transaction import TransactionId
from datafile import Data


file_data = Data("register.csv")


class Account:
    
    _interestRate = 6
    _txnCode = {"deposit": 'D', "withdrawl": 'W',
                 "interest": 'I', "aborted": 'X'}
    _txnNumber = itertools.count(10)
    
    
    def __init__(self, accountNumber, firstName, lastName, initialBalance=0.0, timezone=None):
        if not accountNumber.isalnum():
            raise ValueError(f"{accountNumber} is invalid" )

        self._accountNumber = accountNumber
        self._firstName = self.validate_string(firstName)
        self._lastName = self.validate_string(lastName)
        self._balance = self.validate_number(initialBalance, minVal = 0)
        tzname = self.get_tz(timezone)
        if not isinstance(tzname, pytz.tzinfo.tzinfo):
            raise ValueError(f"{tzname}")
        self._timezone = tzname
            
        
    @staticmethod
    def get_tz(tz_name):
        if (tz_name is None):
            return pytz.timezone(str(get_localzone()))
        else:
            try:
                return pytz.timezone(tz_name)
            except pytz.exceptions.UnknownTimeZoneError as t:
                return "Invalid TimeZone {}".format(tz_name)
        
    @staticmethod
    def validate_number(value, minVal=0):
        if not isinstance(value, numbers.Real):
            raise ValueError("Value must be a real number.")
        if minVal is not None and value < minVal:
            raise ValueError(f"Value must be at least {minVal}.")

        return value
    
    @staticmethod
    def validate_string(value):
        val = value.strip()
        if len(val) == 0 or not val.isalpha():
            raise ValueError(f"{val} is invalid, the value can have characters only.")
        return val  
    
    @property
    def firstname(self):
        return self._firstName
    
    @firstname.setter
    def firstname(self, value):
        self._firstName = self.validate_string(val)
        
    @property
    def lastname(self):
        return self._lastName
    
    @lastname.setter
    def lastname(self, value):
        self._lastName = self.validate_string(val)
        
    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        self._timezone = self.get_tz(value)
        
    @property
    def accountnumber(self):
        return self._accountNumber
    
    @property
    def balance(self):
        return self._balance
    
    @classmethod
    def get_interestRate(cls):
        return cls._interestRate

    @classmethod
    def set_interestRate(cls, value):
        if not isinstance(value, numbers.Real):
            raise ValueError("Interest rate must be a real number.")

        if value < 0:
            raise ValueError("Interest can not be negative.")

        cls._interestRate = value
        
        
    def deposit(self, value):
        value = self.validate_number(value, 0.01)

        txncode = Account._txnCode.get('deposit')
        txn = TransactionId(txncode, self.accountnumber, next(Account._txnNumber))
        conf_code = txn.generate_txn_confirmation_code()
        self._balance += value
        
        parse_code = txn.parse_txn_confirmation_code(conf_code, self.timezone)
        passbook = (parse_code[4], "", value, self.balance)
        
        data = file_data.index_by_accnt()
        data.loc[self.accountnumber, "Balance"] = self.balance
        data.to_csv("register.csv")
        
        self.add_entry_passbook(passbook)
        return conf_code
    
    
    def withdraw(self, value):
        value = self.validate_number(value, 0.01)
        accepted = False
        if self.balance - value < 0:
            txncode = Account._txnCode.get('aborted')
            print("Transaction Aborted insufficient withdrawl amount")
        else:
            accepted = True
            txncode = Account._txnCode.get('withdrawl')

        txn = TransactionId(txncode, self.accountnumber, next(Account._txnNumber))
        conf_code = txn.generate_txn_confirmation_code()
        if accepted:
            self._balance -= value

        parse_code = txn.parse_txn_confirmation_code(conf_code, self.timezone)
        passbook = (parse_code[4], value,"", self.balance)
        
        data = file_data.index_by_accnt()
        data.loc[self.accountnumber, "Balance"] = self.balance
        data.to_csv("register.csv")
        
        self.add_entry_passbook(passbook)
        
        return conf_code       
    
        
    def payInterest(self):
        interest = round(self.balance * Account.get_interestRate() / 100, 2)
        txncode = Account._txnCode.get('interest')
        txn = TransactionId(txncode, self.accountnumber, next(Account._txnNumber))
        conf_code = txn.generate_txn_confirmation_code()
        self._balance += interest
        
        parse_code = txn.parse_txn_confirmation_code(conf_code, self.timezone)
        passbook = (parse_code[4], "", interest, self.balance)
        
        data = file_data.index_by_accnt()
        data.loc[self.accountnumber, "Balance"] = self.balance
        data.to_csv("register.csv")
        
        self.add_entry_passbook(passbook)
        
        return conf_code
    
    
    def add_entry_passbook(self, pbook):
        with open("passbook_data.txt", "a+", encoding="utf-8") as file:
            data = f"{self.accountnumber}\t{pbook[0]},{pbook[1]},{pbook[2]},{pbook[3]}\n"
            file.write(data)
            
            
    def __str__(self):
        return textwrap.dedent("""
        Account Details:
        
            Account Holder Name:   {0.firstname} {0.lastname}
            Account Number:        {0.accountnumber}
            Timezone (location):   {0.timezone}
            
            Initial Balance:       $ {0.balance}

        """.format(self))
    
    
    def __repr__(self):
        return """Account(accountNumber={0.accountnumber}, 
        firstName={0.firstname}, lastName={0.lastname}, 
        balance={0.balance}, timezone={0.timezone})""".format(self)
    
    
