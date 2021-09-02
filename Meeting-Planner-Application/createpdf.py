from fpdf import FPDF
from static import *


class PDF(FPDF):
    
    cal_x = 0
    cal_y = 0
    
    def header(self):
        # Logo
        epw = int(self.epw // 2) - 5
        self.image('logo.jpg', epw, 8, 33)
        # helvetica bold 15
        self.set_font('helvetica', 'B', 20)
        self.ln(20)
        # Move to the center
        self.set_x(epw - 4)
        # Title
        self.cell(40, 10, 'MI Meeting', 0, 0, 'C')
        # Line break
        self.ln(12)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # helvetica italic 10
        self.set_font('helvetica', 'I', 10)
        # Page number
        self.cell(0, 10, 'www.mimeeting.io', 0, 0, 'C')
        
    def detail_cell(self, info, value, w=60, h = 8,):
        self.set_font('Times', '', 12)
        self.set_x(25)
        self.cell(w, h, txt=info, border=0,ln= 0,align= 'L')
        self.set_font('Times', 'B', 12)
        if PDF.cal_x == 0:
            PDF.cal_x = self.get_x() + w
            PDF.cal_y = self.get_y()
        self.cell(w, h, txt=value, border=0,ln= 1,align= 'L')
    
    def calendar_cell(self, mdc2, date=0, month=1, year=1):

        self.set_xy(PDF.cal_x + 15, PDF.cal_y)
        self.cell(70, 8, txt=f"{yearmonths[month-1]} {year}", border=0, ln=1, align='C')
        PDF.cal_y = self.get_y()
        for m in mdc2:    
            self.set_xy(PDF.cal_x + 15, PDF.cal_y)
            cnt = 1
            for d in m:
                if isinstance(d, tuple):
                    d = d[0]
                    if d == date:
                        d = '[' + str(d) + ']'
                        self.set_text_color(163, 0, 0)
                        self.set_font('Times', 'B', 10)
                    else:
                        self.set_font('Times', '', 10)
                        self.set_text_color(0, 0, 0)
                    
                if d == 0:
                    self.cell(10, 8, txt='', border=0, ln=0)
                elif cnt == 7:
                    self.cell(10, 8,txt=str(d), border=0, ln=1, align='C')
                    PDF.cal_y = self.get_y()
                else:
                    self.cell(10, 8,txt=str(d), border=0, ln=0, align='C')
                    
                cnt += 1