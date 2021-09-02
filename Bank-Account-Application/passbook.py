header = ("Date Standard Format", "Debited", "Credited", "Balance")


class Passbook:
    
    def __init__(self, txndata):
        self.__txndata = txndata
        
    def print_passbook(self):
        print("{data[0]:^35} {data[1]:^10} {data[2]:^10}  {data[3]:^10}".format(data=header))
        print('-'*70)
        for data in self.__txndata:
            print("{data[0]:^35} {data[1]:^10} {data[2]:^10} {data[3]:^10}".format(data=data))
            
    def __repr__(self):
        return f"Passbook(txndata={self.__txndata})"