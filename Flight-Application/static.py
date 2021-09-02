from datetime import datetime, timedelta, time, date
import random

flights = {"EK 318": ("Fly Emirates", (189, 13, 13)), 
           "SV 1024": ("Saudia Airlines", (51, 102, 0)), 
           "QR 3352": ("Qatar Airways", (153, 0, 76)),
           "LH 400": ("Lufthansa Airline", (64, 1, 128)),
           "SQ 634": ("Singapore Airlines", (255, 128, 0)),
           "EY 77": ("Etihad Airways", (218,165,32))}

terminal_gates = ("T1", "T2", "T3", "G1", "G7", "G5", "G9")
seats = ("A1","B1","C1", "D1", "E1", "F1", "A2","B2","C2", "D2", "E2", "F2", "A3","B3","C3", "D3", "E3", "F3")

# PDF Specifications
PDF_WIDTH = 220
PDF_HEIGHT = 115
ORIENTATION = 'P' #PORTRAIT
UNIT = "mm"

def validate_city(city, cntry_dict):
    if city in cntry_dict:
        return city
    else:
        raise KeyError("Invalid City name entered. Enter the correct city name from the list.")
        
        
def dept_time():
    now = datetime.now()
    flight_schedule_month = random.randint(now.month+1, 12)
    flight_schedule_day = random.randint(1, 28)
    flight_hour = random.randint(0, 23)
    flight_min = random.randint(0, 59)
    ftime = datetime(year=now.year, month=flight_schedule_month, day=flight_schedule_day, hour=flight_hour, minute=flight_min)
    return ftime

def arr_time():
    ar_time = timedelta(hours=(random.randint(1, 18)), minutes=(random.randint(0, 59)))
    dptm = dept_time()
    act = dptm + ar_time
    return act

