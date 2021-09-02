from createpdf import PDF
from flight import Flight
from airports import Airport
from loadfile import LoadFile
from showmap import ShowMap
from passenger import Passenger
from static import *
from datetime import datetime, timedelta, date, time
import random
import os
import pathlib

# load Airports
lf = LoadFile("airports.csv")
airports = lf.load_airports()

# flight id
fid = random.choice(list(flights.keys()))

# seat num
seatnum = random.choice(seats)

# terminal/gate
tg = random.choice(terminal_gates)

# validate  IATA code
def validate_iata(iata_code):
    if iata_code not in airports:
            raise KeyError("Code not match, enter the exact code from the list")
    return iata_code
            
# align printing values
def align_text(txt = '', pos = 0):
    print((txt).center(pos))
    
def print_border(n = 0, pos=0,  c='#'):
    print((c * n).center(pos) + "\n")
    

if __name__ == "__main__":
#     passenger details
    print_border(168)
    txt = "PASSENGER DETAILS"
    align_text(txt, 168)
    print_border(len(txt), 168, '-')
    name = input("Enter Your Name: ")
    try:
        age = int(input("Enter your age: "))
    except ValueError as e:
        print("Invalid value enter Numeric value")
    gender = input("Enter you gender [M/F]: ")
    p = Passenger(name, age, gender)

    # country list to display
    print_border(168)
    txt = "COUNTRY LIST"
    align_text(txt, 168)
    print_border(len(txt), 168, '-')
    print(lf.country_list(), "\n")
    print_border( 168)

    # flight source/origin
    txt = "Enter COUNTRY NAME [Source/From]"
    align_text(txt, 168)
    print_border(len(txt), 168, '-')
    csname = input(">>> ").title()
    
    flights_source_city = lf.list_airports(csname)
    txt = f"FLIGHTS AVIALABLE FROM {csname} [CITIES]"
    align_text(txt, 168)
    print_border(len(txt), 168, '-')
    print(list(flights_source_city.keys()))
  
    print_border()
    txt = "Enter ORIGIN CITY Name"
    align_text(txt, 168)
    print_border(len(txt), 168, '-')
    city_origin_name = input(">>> ").title()
    origin_city = flights_source_city.get(validate_city(city_origin_name, flights_source_city ))    
    
    iata_code_src = None
    iata_string = "City has multiple airports enter IATA code from the below list"
    if isinstance(origin_city, list):
        align_text(iata_string, 168)
        print_border(len(iata_string), 168, '-')
        for iata in origin_city:
            print(airports[iata])
        iata_code_src = validate_iata(input(">>> ").upper())
        

    # flight destination
    print_border( 168)
    txt = "Enter COUNTRY NAME [Destination/To]"
    align_text(txt, 168)
    print_border(len(txt), 168, '-')
    dsname = input(">>> ").title()
    flights_destination_city = lf.list_airports(dsname)
    
    txt = f"FLIGHTS AVIALABLE TO {dsname} [CITIES]"
    align_text(txt, 168)
    print_border(len(txt), 168, '-')
    print(list(flights_destination_city.keys()))
    
    print_border()
    txt = "Enter DESTINATION CITY Name"
    align_text(txt, 168)
    print_border(len(txt), 168, '-')
    dest_city_name = input(">>> ").title()
    dest_city = flights_destination_city.get(validate_city(dest_city_name, flights_destination_city))
    print_border(168)

    iata_code_dest = None
    if isinstance(dest_city, list):
        align_text(iata_string, 168)
        print_border(len(iata_string), 168, '-')
        for iata in dest_city:
            print(airports[iata])
        iata_code_dest = validate_iata(input(">>> ").upper())

    
    if city_origin_name == dest_city_name:
        raise ValueError("Source city and destination can't be same")

    # departure time and arrival time
    departure_time = dept_time()
    arrival_time = arr_time()
    while arrival_time < departure_time:
        arrival_time = arr_time()
        
    if iata_code_dest is not None:
        dest_city = iata_code_dest
        
    if iata_code_src is not None:
        origin_city = iata_code_src    
    
    print(origin_city, " =======> ", dest_city)
    
    # get random flight
    flight = Flight(flight_id=fid, 
                    origin=airports[origin_city], 
                    destination=airports[dest_city], 
                    arrival=arrival_time, 
                    departure=departure_time)

    # generate map
    sm = ShowMap(flight.origin, flight.destination)
    map_obj = sm.generate_map()
    map_obj.save("map.html")

    # create pdf
    pdf = PDF(orientation=ORIENTATION, unit=UNIT, format=(PDF_WIDTH, PDF_HEIGHT))
    pdf.add_page()
    pdf.image("world_map3.jpg", x=10, y=20, w=pdf.epw, h=PDF_HEIGHT - 40)


    # dividing page in equal width of each column
    column_width = pdf.epw / int(3)
    cell_height = 14

    pdf.set_font('Times', 'B', 20)
    flight_name, rgb = flights.get(fid)
    pdf.set_fill_color(r=rgb[0], g=rgb[1], b=rgb[2])
    pdf.set_text_color(255, 255, 255)

    # add header to pdf
    pdf.boradingpass_header("",10, cell_height)
    pdf.boradingpass_header(f"{flight_name}", column_width+10, cell_height, alg="C", fill=True)
    pdf.set_font('Times', 'B', 12)
    pdf.boradingpass_header("Boarding Pass\nECONOMY", column_width-20, cell_height ,alg="R", fill=True)

    # pointer for scond half start
    c_x, c_y = pdf.get_x(), pdf.get_y()

    pdf.boradingpass_header("Boarding Pass\nECONOMY", column_width-10, cell_height ,alg="R", fill=True)
    pdf.boradingpass_header("",10, cell_height)

    # add logo
    pdf.set_logo("logo.png",x=12, y=12, w=15, h=10)

    # add dash line
    pdf.draw_dash_line(c_x, c_y)

    # before dash line data
    pdf.ln(20)

    dep_date = flight.departure.strftime("%d %b %Y")
    dep_time = flight.departure.strftime("%I:%M %p")
    pdf.first_half_dash_line_name(column_width, 5, ("Passenger Name", "Date", "Time"), b=0)
    pdf.first_half_dash_line_values(column_width, 5, (f"{name}".upper(), 
                                                      f"{dep_date}",
                                                      f"{dep_time}"), b=0)

    pdf.first_half_dash_line_name(column_width, 5, ("From", "Flight", "Seat"), b=0)
    pdf.first_half_dash_line_values(column_width, 5, (f"{flight.origin.city.upper()}", 
                                                      f"{flight.flight_id}",
                                                      f"{seatnum}"), b=0)

    chk_in = flight.check_in.strftime("%I:%M %p")
    pdf.first_half_dash_line_name(column_width, 5, ("To", "Gate/Terminal", "Check-IN"), b=0)
    pdf.first_half_dash_line_values(column_width, 5, (f"{flight.destination.city.upper()}", 
                                                      f"{tg}" ,
                                                      f"{chk_in}"), b=0)

    # seond half
    pdf.second_half_dash_line_name(column_width, 5, texts="Passenger Name", b=0)
    pdf.second_half_dash_line_value(column_width, 5, texts=f"{name}".upper(), b= 0)

    pdf.second_half_dash_line_name(column_width, 5, texts=("From", "To"), b=0)
    pdf.second_half_dash_line_value(column_width, 5, texts=(f"{flight.origin.city.upper()}", 
                                                            f"{flight.destination.city.upper()}"), b=0)

    pdf.second_half_dash_line_name(column_width, 5, texts=("Date", "Time"), b=0)
    pdf.second_half_dash_line_value(column_width, 5, texts=(f"{dep_date}",
                                                            f"{dep_time}"), b=0)

    pdf.second_half_dash_line_name(column_width, 5, texts=("Flight", "Seat"), b=0)
    pdf.second_half_dash_line_value(column_width, 5, texts=(f"{flight.flight_id}",
                                                            f"{seatnum}"), b=0)

    pdf.second_half_dash_line_name(column_width, 5, texts=("Gate/Termial", "Check-IN"), b=0)
    pdf.second_half_dash_line_value(column_width, 5, texts=(f"{tg}", 
                                                            f"{chk_in}"), b=0)
    end_cell = (pdf.get_x(), pdf.get_y())

    # adding barcode, map link
    urlpath = pathlib.Path(os.path.abspath("map.html")).as_uri()
    pdf.map_link_and_barcode(urlpath, column_width, 5)

    # last ending cell
    pdf.last_cell(rgb, end_cell[0], end_cell[1])

    print_border(168)
    txt = "GENERATING BOARDING PASS"
    align_text(txt, 168)
    print_border(len(txt), 168, '-')
    pdf.output("flight_ticket.pdf")
    print("Pass Generated Successfully 'flight_ticket.pdf' in current folder".center(168))
    print_border(168)
    txt = "FLIGHT DETAILS"
    align_text(txt, 168)
    print_border(len(txt), 168, '-')
    print(flight)
    print("\n\n Note: The arrival time is generated randomly, duration may show unexpected value".center(168))
    print_border(168)