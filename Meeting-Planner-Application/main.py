from hostfile import Host
from meetingcalendar import MeetingCalendar
from attendee import Attendee
from static import *
from datetime import datetime, timedelta, time, date
from tzlocal import get_localzone
from createpdf import PDF
import calendar

# check meeting schedule is in future
def check_schedule_date(dt):
    if dt > datetime.now():
        return True
    else:
        return False



if __name__ == "__main__":
    print("#" * 100 + "\n")
    print("Use this link to get timezone list: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568\n\n")
    meeting_description= input("Enter meeting description: >>> ".rjust(60))
    try:
        year = int(input("Enter year: >>> ".rjust(60)))
        month = int(input("Enter month number: >>> ".rjust(60)))
        day = int(input("Enter day: >>> ".rjust(60)))
        meet_time_hr = int(input("Enter Meeting Start hour (0 to 23): >>> ".rjust(60)))
        meet_start_min = int(input("Enter Meeting Start minutes (0 to 59): >>> ".rjust(60)))
        dur_hr = int(input("Enter Meeting duration hour (0 to 23): >>> ".rjust(60)))
        dur_min = int(input("Enter Meeting duration minutes (0 to 59): >>> ".rjust(60)))
    except ValueError as t:
        raise ValueError("The value must be of integer type.")
        
    timezone = input("Enter Timezone  [Type 'local' for your local timezone] >>> ".rjust(60))
    print("\n"+"#" * 100 + "\n")
    
    dt = datetime(year, month, day, meet_time_hr, meet_start_min,)
    
    if check_schedule_date(dt):
        # host meeting
        mt = Host(year, month, day, 
                  meet_time_hr, meet_start_min,
                  dur_hr, dur_min, t_z=timezone)
    else:
        raise ValueError("Meeting must be in future, enter correct datetime")
    
    # Instantiation of PDF class
    pdf = PDF(ORIENTATION, UNIT, FORMAT)
    pdf.add_page()
    pdf.set_font('Times', 'B', 12)

    # rectangle length 
    c_y = pdf.get_y()
    rl = PDF_HEIGHT - c_y - 15
    pdf.rect(pdf.get_x(), c_y, pdf.epw, rl)
    pdf.cell(0, 10, txt=f"Meeting Details: [{meeting_description}]", border=1,ln= 0,align= 'L')
    pdf.ln(14)

    # draw split line
    pdf.line_width = 0.3
    pdf.line(x1=152, x2=152, y2=PDF_HEIGHT - 15, y1=c_y+10)

    pdf.detail_cell("Date: ",f"{mt.meeting_date}")
    pdf.detail_cell("Weekday: ",f"{mt.meeting_weekday}")
    pdf.detail_cell("Start Time: ",f"{mt.meeting_time}")
    pdf.detail_cell("End Time: ",f"{mt.meeting_end_date_time.strftime('%I:%M %p')}")
    pdf.detail_cell("Duration: ",f"{mt.meeting_duration}")
    pdf.detail_cell("Timezone: ",f"{mt.meeting_timezone}")

    pdf.ln(5)
    pdf.detail_cell("Meeting Start Standard Time: ",f"{mt.meeting_start_date_time.strftime(fmt)}")
    pdf.detail_cell("Meeting Start Standard Time: ",f"{mt.meeting_end_date_time.strftime(fmt)}")


    # calendar print
    c = MeetingCalendar(calendar.MONDAY, mt.schedule_meeting)
    h = c.formatweekheader(4).split()
    c = MeetingCalendar(calendar.MONDAY, mt.schedule_meeting)
    mdc2 = c.monthdays2calendar(year=c.year, month=c.mon)
    mdc2.insert(0, h)
    pdf.calendar_cell(mdc2, day, month, year)

    pdf.output('meeting.pdf')
    input("Enter to continue")
    print("PDF generated")
    print("\n"+"#" * 100 + "\n")
    
    print(mt)
    print("\n"+"#" * 100 + "\n")
    
    at = Attendee(mt.meeting_start_date_time, str(mt))
    input("Enter to continue")
    print("Attendee View".center(100))
    print(("-" * len("Attendee View")).center(100))
    
    print(str(at) +"\n\n")
    print(c.formatmonth())
    print("\n\n Check your current Folder to view 'meeting.pdf'")
    print("\n"+"#" * 100 + "\n")