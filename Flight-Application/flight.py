import textwrap
import pytz
from tzlocal import get_localzone
from datetime import timedelta, datetime

class Flight:
    def __init__(self, flight_id, origin, destination, arrival, departure):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        
        self.departure = self.localize_flight_time(departure, origin.tz)
        self.arrival = self.localize_flight_time(arrival, destination.tz)
        
    @staticmethod
    def localize_flight_time(date_time, tz_name):
        tzname = pytz.timezone(tz_name)
        try:
            return tzname.localize(date_time, is_dst=None)
        except pytz.exceptions.AmbiguousTimeError:
            return tzname.localize(date_time, is_dst=True)
        
    @property
    def duration(self):
        return self.arrival - self.departure
    
    def time_left_to_departure(self):
        return self.departure - pytz.timezone(str(get_localzone())).localize(datetime.now())
    
    @property
    def check_in(self):
        return self.departure.tzinfo.normalize(self.departure - timedelta(hours=2))
    
    def __str__(self):
        return textwrap.dedent("""\
        Flight {0.flight_id}:
                From                         : {0.origin}
                To                           : {0.destination}
                
                Departure Date-Time          : {0.departure} {0.departure.tzinfo}
                Arrival   Date-Time          : {0.arrival}  {0.arrival.tzinfo}
                Flight Duration              : {0.duration}
                
                Time left to Depature        : {timeleft}
                Check-in Time                : {0.check_in}
        """.format(self, timeleft = self.time_left_to_departure()))
    
    def __repr__(self):
        return f"Flight=(filght_id={self.filght_id}, origin={self.origin}, destination={self.destination}, arrival={self.arrival}, departure={self.departure})"