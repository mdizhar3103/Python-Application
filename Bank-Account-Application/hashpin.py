from Crypto.Hash import SHA3_512

class HashPin:
    
    def __init__(self, pin):
        self._pin = pin
        
    def calculate_hash(self):
            h = SHA3_512.new()
            h.update(bytes(self._pin, encoding='utf-8'))
            return h.hexdigest()
        
        
