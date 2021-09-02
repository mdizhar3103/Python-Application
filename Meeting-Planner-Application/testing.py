import unittest
from datetime import datetime, timedelta, date, time
import pytz
from hostfile import Host
from attendee import Attendee
from tzlocal import get_localzone


class TestHost(unittest.TestCase):
    def setUp(self):
        self.yr = 2021
        self.m = 8
        self.d = 26
        self.hr = 13
        self.mn = 15
        self.tz_nm = None
        self.dur_hr = 1
        self.dur_min = 30
        
    def get_meeting_dt(self):
        return Host(self.yr, self.m, self.d, 
                    self.hr, self.mn, 
                    self.dur_hr, self.dur_min,self.tz_nm)
    
    def test_valid_date_time(self):
        h = self.get_meeting_dt()
        dt = datetime(2021, 8, 26, 13, 15, tzinfo=get_localzone())
        self.assertEqual(h.meeting_start_date_time, dt)
        
        
    def test_invalid_date_time(self):
        # feb with 30 days
        self.m = 2
        self.d = 30
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
        
        
    def test_invalid_date_time_hour(self):
        self.hr = -2
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.hr = 25
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.hr = "2"
        with self.assertRaises(TypeError):
            self.get_meeting_dt()
            
        self.hr = "-2.4"
        with self.assertRaises(TypeError):
            self.get_meeting_dt()
            
            
    def test_invalid_date_time_minute(self):
        self.mn = -2
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.mn = 60
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.mn = "2"
        with self.assertRaises(TypeError):
            self.get_meeting_dt()
            
        self.mn = "-2.4"
        with self.assertRaises(TypeError):
            self.get_meeting_dt()
            
            
    def test_invalid_date_time_day(self):
        self.d = 0
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.d = 32
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.d = "2"
        with self.assertRaises(TypeError):
            self.get_meeting_dt()
            
        self.d = "-2.4"
        with self.assertRaises(TypeError):
            self.get_meeting_dt()
            
            
    def test_invalid_date_time_month(self):
        self.m = 0
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.m = 32
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.m = "2"
        with self.assertRaises(TypeError):
            self.get_meeting_dt()
            
        self.m = "-2.4"
        with self.assertRaises(TypeError):
            self.get_meeting_dt()
            
            
    def test_invalid_date_time_year(self):
        self.yr = 0
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.yr = 10000
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.yr = 2021.1
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
            
        self.yr = "2"
        with self.assertRaises(TypeError):
            self.get_meeting_dt()
            
        self.yr = "-2.4"
        with self.assertRaises(TypeError):
            self.get_meeting_dt()
            
            
    def test_valid_meeting_date(self):
        h = self.get_meeting_dt()
        self.assertEqual(h.meeting_date, "26 Aug 2021")
        
        
    def test_invalid_meeting_date(self):
        h = self.get_meeting_dt()
        self.assertNotEqual(h.meeting_date, "26-08-2021")
        self.assertNotEqual(h.meeting_date, "2021 Aug 26")
        self.assertNotEqual(h.meeting_date, "2021-08-26")
        
        
    def test_valid_meeting_time(self):
        h = self.get_meeting_dt()
        self.assertEqual(h.meeting_time, "01:15 PM")
        
        
    def test_invalid_meeting_time(self):
        h = self.get_meeting_dt()
        self.assertNotEqual(h.meeting_time, "13:15")
            
            
    def test_meeting_time_valid_timezone(self):
        self.tz_nm = "Europe/London"
        h = self.get_meeting_dt()
        dt = datetime(2021, 8, 26, 13, 15,)
        self.assertEqual(h.meeting_start_date_time, pytz.timezone(self.tz_nm).localize(dt, is_dst=True))
            
    def test_meeting_time_with_invalid_timezone(self):
        self.tz_nm = "izhar"
        with self.assertRaises(ValueError):
            self.get_meeting_dt()
        
            
    def test_duration(self):
        h = self.get_meeting_dt()
        td = timedelta(hours=1, minutes=30)
        self.assertEqual(h.duration(self.dur_hr, self.dur_min), td)
        
    
    def test_meeting_end_time(self):
        h = self.get_meeting_dt()
        td = timedelta(hours=1, minutes=30)
        self.assertEqual(h.meeting_end_date_time, h.meeting_start_date_time + td)
        
    
    def test_time_left_for_meeting(self):
        self.yr = 2021
        self.m = 8
        self.d = 29
        self.hr = 13
        self.mn = 30
        h = self.get_meeting_dt()
        #self.assertEqual(h.time_left_for_meeting().days, 3)
        self.assertNotEqual(h.time_left_for_meeting().days, 4)
        
        
    def test_meeting_weekday(self):
        h = self.get_meeting_dt()
        self.assertEqual(h.meeting_weekday, "Thursday")
        
        
    def test_reschdeule_meeting(self):
        h = self.get_meeting_dt()
        initial_meeting_dt = h.meeting_start_date_time
        dt = datetime(2021, 8, 29, 16, 30, )
        new_meeting_dt = h.reschedule_meeting(2021, 8, 29, 16, 30,)
        self.assertEqual(h.meeting_start_date_time, 
                         new_meeting_dt)
        
    def test_change_duration_hr(self):
        h = self.get_meeting_dt()
        h.change_dur_hour = 2
        self.assertEqual(h.meeting_duration, timedelta(hours=2, minutes=30))
        
        
    def test_change_duration_min(self):
        h = self.get_meeting_dt()
        h.change_dur_hour = 2
        h.change_dur_min = 45
        self.assertEqual(h.duration(2, 45), h.meeting_duration)
        
        
    def test_convert_time_zone(self):
        h = self.get_meeting_dt()
        self.assertEqual(h.meeting_start_date_time, h.convert_meeting_dt_to_timezone("Europe/London"))
        
    
    def test_time_zone(self):
        h = self.get_meeting_dt()
        self.assertEqual(h.meeting_timezone, "IST")
        h.convert_meeting_dt_to_timezone("Europe/London")
        self.assertNotEqual(h.meeting_timezone, "IST")
        

class TestAttendee(unittest.TestCase):
    
    def setUp(self):
        self.yr = 2021
        self.m = 8
        self.d = 26
        self.hr = 13
        self.mn = 15
        self.tz_nm = None
        self.dur_hr = 1
        self.dur_min = 30
        
        
    def get_meeting_dt(self):
        return Host(self.yr, self.m, self.d, 
                    self.hr, self.mn, 
                    self.dur_hr, self.dur_min,self.tz_nm)
    
    
    def test_attendee_details_with_same_timezone(self):
        h = self.get_meeting_dt()
        display = str(h)
        at = Attendee(h.meeting_start_date_time, display)
        self.assertEqual(str(at), display)
        
        
    
    def test_attendee_details_with_diff_timezone(self):
        h = self.get_meeting_dt()
        display = str(h)
        change_tz = h.convert_meeting_dt_to_timezone("Europe/London")
        at = Attendee(h.meeting_start_date_time, display)
        self.assertNotEqual(str(at), display)
        
        
    def test_details(self):
        h = self.get_meeting_dt()
        display = str(h)
        at = Attendee(h.meeting_start_date_time, display)
        self.assertEqual(at.details, display)

        
if __name__ == "__main__":
    unittest.main()