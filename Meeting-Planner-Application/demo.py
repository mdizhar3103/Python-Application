from hostfile import Host
from attendee import Attendee
from meetingcalendar import MeetingCalendar
import calendar


# schedule meeting
print("===============Scheduling Meeting========================")
input("Enter to Continue.....")
mt = Host(2021, 8, 28, 23,45,1, 30, t_z=None)
print(mt)

# convert meeting datetime to different timezone 
print("===============Converting Meeting To Different Timezone========================")
input("Enter to Continue.....")
cn = mt.convert_meeting_dt_to_timezone("Europe/London")
print(mt)

# reschedule meeting
print("===============Rescheduling Meeting========================")
input("Enter to Continue.....")
rs = mt.reschedule_meeting(2021, 8, 30, 23, 45,)
print(mt)

# check reschedule meeting to different timezone
print("===============Checking Meeting reschedule with Different Timezone========================")
input("Enter to Continue.....")
cn = mt.convert_meeting_dt_to_timezone("Europe/London")
print(mt)

# change meeting duration without changing datetime
print("===============Changing Meeting Duration Hour========================")
input("Enter to Continue.....")
mt.change_dur_hour = 2
print(mt)

print("===============Changing Meeting Duration Hour and Minutes========================")
input("Enter to Continue.....")
mt.change_dur_hour = 1
mt.change_dur_min = 45
print(mt)


print("============== Attendee View =============")
at = Attendee(mt.meeting_start_date_time, str(mt))
print(at)

print("============== Calendar=============")
c = MeetingCalendar(calendar.MONDAY, mt.schedule_meeting)
s = c.formatmonth()
print(s)