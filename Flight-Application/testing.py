import os
import folium
import unittest
from loadfile import LoadFile
from airports import Airport
from flight import Flight
from datetime import datetime, date, time, timedelta
from showmap import ShowMap
from passenger import Passenger


class TestFileName(unittest.TestCase):
    
    def setUp(self):
        self.filename = "airports.dat"
        
    def load_file(self):
        return LoadFile(self.filename)
        
    def test_invalid_file_extension(self):
        with self.assertRaises(ValueError):
            lf = self.load_file()
            
    def test_valid_file_extension(self):
        self.filename = "airports.csv"
        lf = LoadFile(self.filename)
        self.assertEqual(lf.filename, self.filename)
        
    def test_filename_with_spaces(self):
        self.filename = "    "
        with self.assertRaises(ValueError):
            lf = self.load_file()
            
    def test_incorrect_filename_with_valid_extension(self):
        self.filename = "air ports.csv"
        with self.assertRaises(ValueError):
            lf = self.load_file().loadfile()
        
        
class TestFileData(unittest.TestCase):
    
    def setUp(self):
        self.filename = "airports.csv"
        self.lf = LoadFile(self.filename)
        
    def test_headers(self):
        self.assertEqual(len(Airport.prop_names), len(self.lf.headers))
        
    def test_rows_count(self):
        self.assertEqual(7184, len(self.lf.loadfile().index))
        
    def test_airport_iata_codes(self):
        self.assertEqual(5654, len(self.lf.load_airports().keys()))
        
    def test_invalid_country_name(self):
        with self.assertRaises(ValueError):
            self.lf.list_airports('Afghan1stan')
            
        with self.assertRaises(KeyError):
            self.lf.list_airports('Afghan stan')
        
        with self.assertRaises(TypeError):
            self.lf.list_airports(123221)
            
    def test_valid_country_name(self):
        d = self.lf.list_airports('Afghanistan')
        self.assertNotEqual(self.lf.country_airports('Afghanistan')['city'].count(), len(d.keys()))
        self.assertEqual(16, len(d.keys()))
        self.assertTrue(self.lf.list_airports('United Arab Emirates'))
        
class TestFlights(unittest.TestCase):
    
    def setUp(self):
        lf = LoadFile("airports.csv")
        airports = lf.load_airports()
        departure_time = datetime(year=2021, month=9, day=22, hour=0, minute=0)
        arrival_time = datetime(year=2021, month=9, day=22, hour=5, minute=30)
        self.flight = Flight(flight_id="EK 318", origin=airports['DXB'], 
                             destination=airports['LKO'], arrival=arrival_time, departure=departure_time)
        
    def test_flight_id(self):
        self.assertEqual(self.flight.flight_id, "EK 318")
        self.assertNotEqual(self.flight.flight_id, "EK 418")
        
    def test_flight_origin(self):
        self.assertEqual(str(self.flight.origin),"DXB (Dubai International Airport)")
        
    def test_flight_destination(self):
        self.assertEqual(str(self.flight.destination), "LKO (Chaudhary Charan Singh International Airport)")
        
    def test_flight_duration(self):
        self.assertEqual(self.flight.duration, timedelta(hours=4))
    
    def test_time_left_for_departure(self):
        self.assertNotEqual(self.flight.time_left_to_departure().days, 30)
        
    def test_departure_date_time(self):
        self.assertEqual(self.flight.departure.date(), date(2021, 9, 22))
        self.assertEqual(self.flight.departure.time(), time(0,0))
        
    def test_arrival_date_time(self):
        self.assertEqual(self.flight.arrival.date(), date(2021, 9, 22))
        self.assertEqual(self.flight.arrival.time(), time(5,30))
        

class TestMap(unittest.TestCase):
    
    def setUp(self):
        lf = LoadFile("airports.csv")
        airports = lf.load_airports()
        departure_time = datetime(year=2021, month=9, day=22, hour=0, minute=0)
        arrival_time = datetime(year=2021, month=9, day=22, hour=5, minute=30)
        self.flight = Flight(flight_id="EK 318", origin=airports['DXB'], 
                             destination=airports['LKO'], arrival=arrival_time, departure=departure_time)
        self.sm = ShowMap(self.flight.origin, self.flight.destination)
        
    def test_origin_lat_long(self):
        origin_ll = self.sm.get_lat_long(self.flight.origin)
        dest_ll = self.sm.get_lat_long(self.flight.destination)
        self.assertEqual(origin_ll[0], self.flight.origin.lat)
        self.assertEqual(origin_ll[1], self.flight.origin.long)
        self.assertEqual(dest_ll[0], self.flight.destination.lat)
        self.assertEqual(dest_ll[1], self.flight.destination.long)
        
    def test_map_object(self):
        map_obj = self.sm.generate_map()
        self.assertTrue(isinstance(map_obj, folium.Map))
        
class TestPassenger(unittest.TestCase):
    
    def setUp(self):
        self.name = "Mohd Izhar"
        self.age = 22
        self.gender = "M"
        
    def passenger(self):
        return Passenger(self.name, self.age, self.gender)
    
    def test_valid_name(self):
        p=self.passenger()
        self.assertEqual(p.name, "Mohd Izhar")
        
    def test_invalid_names(self):
        self.name = "Mohd3103"
        with self.assertRaises(ValueError):
            self.passenger()
        
        self.name = "Mdizhar 99$@"
        with self.assertRaises(ValueError):
            self.passenger()
            
    def test_valid_genders(self):
        self.gender = "Male"
        p = self.passenger()
        self.assertTrue(p)
        
        self.gender = "FeMale"
        p = self.passenger()
        self.assertTrue(p)
        
        self.gender = "M"
        p = self.passenger()
        self.assertTrue(p)
        
        self.gender = "F"
        p = self.passenger()
        self.assertTrue(p)
        
        self.gender = "other"
        p = self.passenger()
        self.assertTrue(p)
        
        self.gender = "O"
        p = self.passenger()
        self.assertTrue(p)
        
    def test_invalid_genders(self):
        self.gender = "Boy"
        with self.assertRaises(ValueError):
            p = self.passenger()
            
    def test_valid_age(self):
        p = self.passenger()
        self.assertEqual(p.age, 22)
        
    def test_invalid_age(self):
        self.age = -23
        with self.assertRaises(ValueError):
            self.passenger()
    
        self.age = 111
        with self.assertRaises(ValueError):
            self.passenger()
        
        self.age = "sdfvsdV"
        with self.assertRaises(TypeError):
            self.passenger()
            
class Test_Map_Pdf_generated(unittest.TestCase):
    
    def test_map_html_file_in_current_directory(self):
        self.assertTrue(os.path.exists("map.html"))
    def test_flight_pdf_in_current_directory(self):
        self.assertTrue(os.path.exists("flight_ticket.pdf"))
        
        
if __name__ == "__main__":
    unittest.main()