from datetime import datetime
from tzlocal import get_localzone
import pytz


fmt = '%d %b %Y %H:%M:%S %Z %z'

class TransactionId:
    def __init__(self, txn_code, acc_num, txn_counter):
        self.txncode = txn_code
        self.acc_num = acc_num
        self.txn_counter = txn_counter

    def generate_txn_confirmation_code(self):
        dt_str = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f"{self.txncode}-{self.acc_num}-{dt_str}-{self.txn_counter}"

    @staticmethod
    def parse_txn_confirmation_code(confirmationCode, preferredTimeZone):
        parts = confirmationCode.split("-")
        if len(parts) != 4:
            raise ValueError("Invalid Conirmation Code")

        txnCode, accountNumber, raw_dt_utc, txnCounter = parts

        try:
            dt_utc = datetime.strptime(raw_dt_utc, '%Y%m%d%H%M%S')
        except ValueError as ex:
            raise ValueError("Invalid transaction datetime.") from ex

        dt_preferred = preferredTimeZone.fromutc(dt_utc)
        dt_preferred_str = f"{dt_preferred.strftime(fmt)}"

        return (accountNumber, txnCode, txnCounter, dt_utc.isoformat(), dt_preferred_str)
    
    
    def __repr__(self):
        return f"TransactionId(txn_code={self.txn_code}, acc_num={self.acc_num}, txn_counter={self.txn_counter})"