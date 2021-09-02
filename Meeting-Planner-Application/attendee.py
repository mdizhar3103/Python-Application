from hostfile import Host
from tzlocal import get_localzone
import textwrap
from static import *


class Attendee(Host):
    
    def __init__(self, meeting_datetime, meeting_details):
        self._meeting_datetime = meeting_datetime
        self._details = meeting_details
        self.loc_dt = self._meeting_datetime.astimezone(get_localzone())
    
    
    @property
    def details(self):
        return self._details

        
    def __str__(self):
        if self.loc_dt.tzname() == self._meeting_datetime.tzname():
            return self.details
        else:
            self._meeting_datetime = self.loc_dt
            ms_st = self._meeting_datetime.strftime(fmt)
            return self.details + textwrap.dedent("""
=================================================================================\n
Meeting Details (Local Timezone)
        
            Date:                        {0.meeting_date}
            Weekday:                     {0.meeting_weekday}
            Start Time:                  {0.meeting_time}
            TimeZone:                    {0.meeting_timezone}
                 
            Time Left for meeting:       {ttl}
            Meeting Start Standard Time: {ms}
""".format(self, ttl=self.time_left_for_meeting(), ms=ms_st))