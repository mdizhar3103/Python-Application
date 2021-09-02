import calendar

class MeetingCalendar(calendar.TextCalendar):
    
    def __init__(self, firstweekday, meeting_dt):
        
        super(MeetingCalendar, self).__init__(firstweekday)
        self.meet_dt = meeting_dt
        self.year = self.meet_dt.year
        self.mon = self.meet_dt.month
        self.day = self.meet_dt.day
        
    def split_into_weeks(self, monthdays):
        step = 7
        for i in range(0, len(monthdays), step):
            yield monthdays[i:i+step] 

    def formatmonth(self):
        width = 4
        weekheader = self.formatweekheader(width)
        s = (str(self.meet_dt.strftime("%B")) + " "+str(self.year)).center(len(weekheader))
        s += "\n\n"+weekheader + '\n'
        monthdays = list(self.itermonthdays2(self.year, self.mon))
        for week in self.split_into_weeks(monthdays):
            s += self.formatweek(week, width) + '\n'
        return s
    
        
    def formatday(self, day, weekday, width):
        s = super(MeetingCalendar, self).formatday(day, weekday, width).strip()
        if self.day == day and day != 0:
            s = '[' + s + ']'
        return s.center(width)
    
    def formatweek(self, theweek, width):
        return ' '.join(self.formatday(day, wkday, width) for (day, wkday) in theweek)
    