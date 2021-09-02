class Passenger:
    def __init__(self, full_name, age, gender='M'):
        if self.check_value("".join(full_name.strip().split())):
            self._name = full_name
        
        if age <=0 or age > 110:
            raise ValueError("Age Can't be less than zero and greater 110 in years, only enter Integer value")
            
        if not isinstance(age, int):
            raise TypeError("Invalid age, only numeric values are allowed")

        self.age = age
        
        if isinstance(gender, str) and gender.upper() in {"MALE", "FEMALE", "OTHER", "M", "F", "O"}:
            self.gender = gender
        else:
            raise ValueError("Invalid value passed for gender accepted value [M/F]")
    
    def check_value(self, value):
        if value.isalpha():
            return True
        else:
            raise ValueError("Name should contain alphabets only and spaces between firstname and last name no special characters are allowed")
        return False
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if self.check_value(value):
            self._name= value
        
    def select_flight_from(self, country):
        pass
    
    def cancel_flight(self):
        pass
        
    