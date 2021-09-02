import pandas as pd



class Data:
    
    def __init__(self, filename):
        self._filename = filename
        
    @property
    def filename(self):
        return self._filename

    def load_file(self, filename):
        header = ["Account Num", "First Name", "Last Name", "Balance", "Pin"]
        try:
            if self.filename.endswith('.csv'):
                file_data = pd.read_csv(self.filename, header=None, names=header, skiprows=1)
            else:
                file_data = pd.read_excel(self.filename, header=None, names=header, skiprows=1)
        except FileNotFoundError as e:
            raise ValueError(f"{self.filename} not found in the directory.") from e

        return file_data


    def index_by_accnt(self):
        data = self.load_file(self.filename).set_index("Account Num")
        return data


    def unique_account_numbers(self):
        data = self.load_file(self.filename)["Account Num"]
        return set(data)
    
    
    def account_details(self):
        details = {}
        for i in self.index_by_accnt().iterrows():
            details[i[0]] = i[1].tolist()
            
        return details
    