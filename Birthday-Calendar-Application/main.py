from birthday_calendar import BirthdayCalendar
import calendar
from datetime import date


today = date.today()


def get_birthday_date(b_month, b_day):    
    try:
        my_birthday = date(today.year, b_month, b_day)
    except ValueError as e:
        return e
    
    if my_birthday < today:
        my_birthday = my_birthday.replace(year=today.year + 1)
    return my_birthday

def time_left_for_birthday(my_birthday):
    time_to_birthday = abs(my_birthday - today)
    return time_to_birthday



if __name__ == "__main__":
    
    print(('#'*168).center(168) + "\n")
    try:
        b_month = int(input("Enter your Birth month >>> ".rjust(100)))
        b_day = int(input("Enter your Birth day >>> ".rjust(100)))
        
        birthday_date = get_birthday_date(b_month, b_day)
        if isinstance(birthday_date, date):
            bday_cal = BirthdayCalendar(calendar.MONDAY, birthday_date)
            ttl = time_left_for_birthday(birthday_date)
            print(('#'*168).center(168) + "\n")
            print(bday_cal.formatmonth().center(100))
            print("Coming Birthday Date: ", birthday_date)
            print("Time Left for Birthday: ", ttl.days," days")
            print(('#'*168).center(168) + "\n")
        else:
            print(str(birthday_date).center(100))
            print(('#'*168).center(168) + "\n")
            
    except ValueError as e:
        print("Only Numeric Value are Allowed".center(100))
        print(('#'*168).center(168) + "\n")
        

    