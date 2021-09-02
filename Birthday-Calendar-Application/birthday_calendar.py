import calendar

class BirthdayCalendar(calendar.TextCalendar):
    
    def __init__(self, firstweekday, dob):
        
        super(BirthdayCalendar, self).__init__(firstweekday)
        self.dt = dob
        self.year = dob.year
        self.mon = dob.month
        self.day = dob.day
        
    def split_into_weeks(self, monthdays):
        step = 7
        for i in range(0, len(monthdays), step):
            yield monthdays[i:i+step] 

    def formatmonth(self):
        width = 4
        weekheader = self.formatweekheader(width)
        s = (str(self.dt.strftime("%B")) + " "+str(self.year)).center(len(weekheader))
        s += "\n\n"+weekheader + '\n'
        monthdays = list(self.itermonthdays2(self.year, self.mon))
        for week in self.split_into_weeks(monthdays):
            s += self.formatweek(week, width) + '\n'
        return s
    
        
    def formatday(self, day, weekday, width):
        s = super(BirthdayCalendar, self).formatday(day, weekday, width).strip()
        if self.day == day and day != 0:
            s = '[' + s + ']'
        return s.center(width)
    
    def formatweek(self, theweek, width):
        return ' '.join(self.formatday(day, wkday, width) for (day, wkday) in theweek)
    
