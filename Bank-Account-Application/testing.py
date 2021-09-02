import unittest
from accounts import Account
import pytz
from tzlocal import get_localzone
from transaction import TransactionId
from datetime import datetime
from hashpin import HashPin



class TestAccount(unittest.TestCase):
    
    def setUp(self):
        self.accountNumber = '7299MI'
        self.firstName = "Mohd"
        self.LastName = "Izhar"
        self.initialBalance = 0.0
        self.timezone = None
        self.interest = 6
        
    def get_account(self):
        return Account(self.accountNumber, self.firstName, self.LastName,
                       self.initialBalance, self.timezone)
    
    def test_positive_true_firstname(self):
        accn = self.get_account()
        self.assertEqual(accn.firstname, self.firstName)
        
    def test_positive_false_firstname(self):
        accn = self.get_account()
        self.assertNotEqual(accn.firstname, "Mohd ")
        
    def test_negative_true_firstname(self):
        self.firstName = "Mohd "
        accn = self.get_account()
        self.assertNotEqual(accn.firstname, self.firstName)
            
    def test_negative_false_firstname(self):
        self.firstName = "Mohd72 "
        with self.assertRaises(ValueError):
            self.get_account()    
            
    # test lastname
    def test_positive_true_lastname(self):
        accn = self.get_account()
        self.assertEqual(accn.lastname, self.LastName)
        
    def test_positive_false_lastname(self):
        accn = self.get_account()
        self.assertNotEqual(accn.lastname, "Izhar ")
        
    def test_negative_true_lastname(self):
        self.LastName = "Izhar "
        accn = self.get_account()
        self.assertNotEqual(accn.lastname, self.LastName)
            
    def test_negative_false_lastname(self):
        self.LastName = "Izhar99 "
        with self.assertRaises(ValueError):
            self.get_account()  
            
    # test accountnumber
    def test_positive_true_account_number(self):
        accn = self.get_account() 
        self.assertEqual(accn.accountnumber, self.accountNumber)
        
    def test_negative_true_account_number(self):
        self.accountNumber = "MI99 72"
        with self.assertRaises(ValueError):
            self.get_account()  
            
    # test balance
    def test_positive_true_balance(self):
        self.initialBalance = 10
        accn = self.get_account()
        self.assertEqual(accn.balance, self.initialBalance)
        
    def test_positive_false_balance(self):
        accn = self.get_account()
        self.initialBalance = 10
        self.assertNotEqual(accn.balance, self.initialBalance)
        
    def test_negative_true_balance(self):
        self.initialBalance = -10.5
        with self.assertRaises(ValueError):
            self.get_account()
            
    def test_negative_false_balance(self):
        self.initialBalance = "-10.5"
        with self.assertRaises(ValueError):
            self.get_account()
    
    # test interest
    def test_positive_false_interest(self):
        accn = self.get_account()
        accn.set_interestRate(8)
        self.assertNotEqual(accn.get_interestRate(), self.interest)
            
    def test_positive_true_interest(self):
        accn = self.get_account()
        accn.set_interestRate(8)
        accn2 = self.get_account()
        self.assertEqual(accn.get_interestRate(), accn.get_interestRate())
        
    def test_negative_true_interest(self):
        accn = self.get_account()
        with self.assertRaises(ValueError):
            accn.set_interestRate(-8)
            
    # test timezone
    def test_positive_true_timezone(self):
        accn = self.get_account()
        local = pytz.timezone(str(get_localzone()))
        self.assertEqual(accn.timezone, local)
        
        
    def test_negative_true_timezone(self):
        self.timezone = "esdvSDV"
        with self.assertRaises(ValueError):
            self.get_account()
    
    # test deopsit
    def test_positive_true_deposit(self):
        accn = self.get_account()
        accn.deposit(100)
        self.assertEqual(accn.balance, 100)
      
    def test_positive_false_deposit(self):
        accn = self.get_account()
        with self.assertRaises(ValueError):
            accn.deposit("100")
            
    def test_negative_true_deposit(self):
        accn = self.get_account()
        with self.assertRaises(ValueError):
            accn.deposit(-100)
        
    def test_negative_false_deposit(self):
        accn = self.get_account()
        with self.assertRaises(ValueError):
            accn.deposit("-100")
            
    #test withdrawl        
    def test_positive_true_withdrawl(self):
        self.initialBalance = 500
        accn = self.get_account()
        accn.withdraw(100)
        self.assertEqual(accn.balance, 400)
      
    def test_positive_false_withdrawl(self):
        accn = self.get_account()
        accn.withdraw(100)
        self.assertEqual(accn.balance, 0.0)
            
    def test_negative_true_withdrawl(self):
        accn = self.get_account()
        with self.assertRaises(ValueError):
            accn.withdraw("100")
        
    def test_negative_false_withdrawl(self):
        accn = self.get_account()
        accn.withdraw(100)
        self.assertNotEqual(accn.balance, -100)
            
    # test interest
    def test_positive_true_interest(self):
        self.initialBalance = 500
        accn = self.get_account()
        accn.set_interestRate(6)
        accn.payInterest()
        self.assertEqual(accn.balance, 530)
        
    def test_positive_false_interest(self):
        self.initialBalance = 0.01
        accn = self.get_account()
        accn.set_interestRate(6)
        accn.payInterest()
        self.assertAlmostEqual(accn.balance, 0.0, 1)
        
        
class TestTransaction(unittest.TestCase):
    
    def setUp(self):
        self.txnCode = "Dummy"
        self.accountnum = "MI7299"
        self.counter = 25
        
    def start_txn(self):
        return TransactionId(self.txnCode, self.accountnum, self.counter)
    
    def test_deposit_txn_code(self):
        self.txnCode = 'D'
        txn = self.start_txn()
        code = txn.generate_txn_confirmation_code()
        utcnow = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        self.assertEqual(code, f"{self.txnCode}-MI7299-{utcnow}-25")
        
    def test_withdraw_txn_code(self):
        self.txnCode = 'W'
        txn = self.start_txn()
        code = txn.generate_txn_confirmation_code()
        utcnow = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        self.assertEqual(code, f"{self.txnCode}-MI7299-{utcnow}-25")    
    
    def test_interest_txn_code(self):
        self.txnCode = 'I'
        txn = self.start_txn()
        code = txn.generate_txn_confirmation_code()
        utcnow = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        self.assertEqual(code, f"{self.txnCode}-MI7299-{utcnow}-25")
        
    def test_rejected_txn_code(self):
        self.txnCode = 'X'
        txn = self.start_txn()
        code = txn.generate_txn_confirmation_code()
        utcnow = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        self.assertEqual(code, f"{self.txnCode}-MI7299-{utcnow}-25")
        
    def test_parse_valid_txn_code(self):
        self.txnCode = 'D'
        txn = self.start_txn()
        code = txn.generate_txn_confirmation_code()
        timezone = pytz.timezone("Asia/Calcutta")
        parsed_code = txn.parse_txn_confirmation_code(code, timezone)
        #print(parsed_code)
        self.assertEqual(len(parsed_code), 5)
        
    def test_invalid_parse_txn_code(self):
        self.txnCode = 'D'
        txn = self.start_txn()
        timezone = pytz.timezone("Asia/Calcutta")
        code = "MOHD IZHAR"
        with self.assertRaises(ValueError):
            txn.parse_txn_confirmation_code(code, timezone)
     
        
class TestHashPin(unittest.TestCase):
    
    def setUp(self):
        self.h = HashPin("7299")
        
    def test_positive_true_pin(self):
        sha = HashPin("7299").calculate_hash()
        self.assertEqual(self.h.calculate_hash(), sha) 
        
    def test_negative_true_pin(self):
        sha = HashPin("7929").calculate_hash()
        self.assertNotEqual(self.h.calculate_hash(), sha) 
        
        
if __name__ == "__main__":
    unittest.main()