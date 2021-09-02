from datetime import datetime, timedelta, time, date
import pytz
from tzlocal import get_localzone
import textwrap
from static import *


class Host:
    
    def __init__(self, yr, mn, d, hr, mint, duration_hours=0, duration_min=15, t_z=None):
        valid_date_time = self.validate_date_time(yr, mn, d, hr, mint)
        if not isinstance(valid_date_time, datetime):
            if (valid_date_time[64:67] == "str"):
                raise TypeError(f"{valid_date_time}")
            else:
                raise ValueError(f"{valid_date_time}")
        
        self._meeting_datetime = self.localize_time(valid_date_time, t_z)
        if duration_hours == 0 and duration_min < 10:
            raise ValueError("Minimum Meeting Duration is 10 minutes.")
        self.__dur_hr = duration_hours
        self.__dur_min = duration_min
        
        
    @property
    def schedule_meeting(self):
        return self._meeting_datetime
    
        
    @property
    def meeting_date(self):
        return self._meeting_datetime.strftime('%d %b %Y')
    
    
    @property
    def meeting_time(self):
        return self._meeting_datetime.strftime('%I:%M %p') 
    
    
    @property
    def meeting_timezone(self):
        return self._meeting_datetime.tzname()
    
    
    @property
    def meeting_start_date_time(self):
        return self._meeting_datetime
    
    
    @property
    def change_dur_hour(self):
        return self.__dur_hr
    
    
    @change_dur_hour.setter
    def change_dur_hour(self, val):
        if (val < 0) or (val > 23):
            raise ValueError(f"{val} is invalid, hours must be in range 0 to 23 (inclusively).")
        self.__dur_hr = val
        
    
    @property
    def change_dur_min(self):
        return self.__dur_min
    
    @change_dur_min.setter
    def change_dur_min(self, val):
        if (val < 0) or (val > 59):
            raise ValueError(f"{val} is invalid, minutes must be in range 0 to 59 (inclusively).")
        self.__dur_min = val
    
    
    @property
    def meeting_end_date_time(self):
        return self._meeting_datetime.tzinfo.normalize(self._meeting_datetime + self.duration(self.__dur_hr, self.__dur_min))
    
    
    @property
    def meeting_duration(self):
        return self.duration(self.__dur_hr, self.__dur_min)
    
    
    @staticmethod
    def validate_date_time(yr, mn, d, hr, mint):
        try:
            dt = datetime(year=yr, month=mn, day=d, hour = hr, minute=mint)
        except (ValueError, TypeError) as e:
            return f"Invalid Value passed, \033[1m\033[31m{e}\033[0m\033[1m"
        return dt
    
    
    @property
    def meeting_weekday(self):
        return weekDays[self._meeting_datetime.weekday()]
    
    
    def reschedule_meeting(self, yr, mn, d, hr, mint, t_z=None):
        new_meeting_dt = self.validate_date_time(yr, mn, d, hr, mint)
        if not isinstance(new_meeting_dt, datetime):
            raise ValueError(f"{new_meeting_dt}")
        self._meeting_datetime = self.localize_time(new_meeting_dt, t_z)
        return self.meeting_start_date_time
        
            
    # time left for meeting to start
    def time_left_for_meeting(self):
        return self._meeting_datetime - self.get_tz("local").localize(datetime.now())
    
    
    # get the timezone
    @staticmethod
    def get_tz(tz_name):
        if (tz_name is None) or (tz_name == "local"):
            return pytz.timezone(str(get_localzone()))
        else:
            try:
                return pytz.timezone(tz_name)
            except pytz.exceptions.UnknownTimeZoneError as t:
                return "Invalid TimeZone value {}".format(tz_name)
        
    
    # set meeting duration
    @staticmethod
    def duration(hour, minutes):
        if (hour < 0) or (hour > 23):
            raise ValueError(f"{hour} is invalid, value should be in between 0 to 23 (inclusively).")
        
        if (minutes < 0) or (minutes > 59):
            raise ValueError(f"{minutes} is invalid, value should be in between 0 to 59 (inclusively).")
            
        time_delta = timedelta(hours=hour, minutes = minutes)
        return time_delta
    
    
    # localize datetime to specific timezones
    def localize_time(self, date_time, tz_name=None):
        tzname = self.get_tz(tz_name)
        if not isinstance(tzname, pytz.tzinfo.tzinfo):
            raise ValueError(f"{tzname}")
            
        try:
            return tzname.localize(date_time, is_dst=None)
        except pytz.exceptions.AmbiguousTimeError as e:
            return tzname.localize(date_time, is_dst=True)
    
    
    def convert_meeting_dt_to_timezone(self, tzname):
        valid_tz = self.get_tz(tzname)
        if not isinstance(valid_tz, pytz.tzinfo.tzinfo):
            raise ValueError(f"{valid_tz}") 
            
        self._meeting_datetime = self._meeting_datetime.astimezone(valid_tz)
        return self._meeting_datetime
    
    
    def __str__(self):
        et_tm = self.meeting_end_date_time.strftime('%I:%M %p')
        ms_st = self.meeting_start_date_time.strftime(fmt)
        me_st = self.meeting_end_date_time.strftime(fmt)
        return textwrap.dedent("""
        Meeting Details:
        
                    Date:                        {0.meeting_date}
                    Weekday:                     {0.meeting_weekday}
                    Start Time:                  {0.meeting_time}
                    End Time:                    {et}
                    Duration:                    {0.meeting_duration}
                    TimeZone:                    {0.meeting_timezone}
                    
                    Time Left for meeting:       {ttl}
                    Meeting Start Standard Time: {ms}
                    Meeting End Standard Time:   {me}
                    
        """.format(self,et = et_tm, ttl=self.time_left_for_meeting(), ms=ms_st, me=me_st))
  
        
    