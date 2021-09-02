import pandas as pd
from airports import Airport


class LoadFile:
    """Loads the data from file with file extension .csv .xls"""
    def __init__(self, filename):
        if not filename.endswith('.csv') and not filename.endswith('.xls'):
            raise ValueError(f"{filename} is not supported use file with extension .csv or .xls")
        
        if len(filename.strip()) == 0:
            raise ValueError("Empty or No file passed")
            
        self._filename = filename
        
    @property
    def filename(self):
        return self._filename
    
    def loadfile(self):
        """ 
            Reads the file data.
            
            Raises 
                    FileNotFoundError if filename is incorrect.
            
            Return 
                    File Dataframe object.
        """
        header = Airport.prop_names
        
        try:
            if self.filename.endswith('.csv'):
                file_data = pd.read_csv(self.filename, header=None, names=header)
            else:
                file_data = pd.read_excel(self.filename, header=None, names=header)
        except FileNotFoundError as e:
            raise ValueError(f"{self.filename} not found in the directory.") from e
        
        return file_data
        
    @property
    def headers(self):
        return tuple(Airport.prop_names)
    
    def load_airports(self):
        """ Loads airport into a dictionary where keys are IATA codes"""
        airports = {}
        for entry in self.loadfile().values.tolist():
            a = Airport(csv_entry = entry)
            airports[a.iata] = a 
                
        return airports
    
    def country_airports(self, country):
        """Returns the country specific grouped data in tuple form (groupname, Dataframe Object)"""
        g = self.loadfile().groupby(['country'])
        return g.get_group(country.strip().title())
            
    
    def list_airports(self, country):
        """
            Args:
                    Takes the country name as argument in string format.
            
            Returns:
                    Return the counrty specific dictionary where keys are cities and values are IATA codes.
            
            Raises:
                    TypeError if wrong datatype is passed
                    ValueError if non alphabetic value is passed.
        """
        if not isinstance(country, str):
            raise TypeError(f"{country} must be of string type")
            
        if not "".join(country.strip().split()).isalpha():
            raise ValueError(f"{country} should have only alphabetic characters")
            
        if country not in set(self.country_list()):
            raise KeyError(f"{country} not in the list enter valid country name")
            
        data = self.country_airports(country)
        cntry_airports = {}
        for ap in data[['city', 'iata']].values.tolist():
            if ap[1] != '\\N': 
                if ap[0] in cntry_airports:
                    get_value = cntry_airports.get(ap[0])
                    if isinstance(get_value, list):
                        cntry_airports[ap[0]] = get_value + [ap[1]]
                    else:
                        cntry_airports[ap[0]] = [get_value] + [ap[1]]
                else:
                    cntry_airports[ap[0]] = ap[1]
            
        return cntry_airports
    
    def country_list(self):
        return self.loadfile()['country'].unique().tolist()