from fpdf import FPDF
from static import PDF_WIDTH, PDF_HEIGHT, ORIENTATION, UNIT


class PDF(FPDF):
    secondHalf = 0
    
    def header(self):
        self.image("https://htmlcolorcodes.com/assets/images/colors/light-gray-color-solid-background-1920x1080.png",
                   x=0, y=0, w=PDF_WIDTH, h=PDF_HEIGHT)
        
    def boradingpass_header(self, text, width, height, alg="C", fill=True):
        self.multi_cell(width, 
                        height, 
                        border=0, txt=text,
                        ln=3, 
                        fill=fill, 
                        align=alg, 
                        max_line_height=9)
    
    def set_logo(self, logoname, x=0, y=0, w=50, h=50):
        self.image(logoname, x=x, y=y, w=w, h=h)
        
    def draw_dash_line(self, c_x, c_y):
        self.set_line_width(0.5)
        self.set_draw_color(r=203, g=203, b=203)
        self.dashed_line(x1=c_x+5, y1=c_y, x2=c_x+5, y2=PDF_HEIGHT, dash_length=2, space_length=3)
        
    def first_half_dash_line_name(self, width, height, texts, b=0):
        self.set_x(20)
        self.set_text_color(137,137,137)
        self.cell(width-10, height, txt=texts[0], border=b, align="L")
        self.cell(width-30, height, txt=texts[1], border=b, align="L")
        # get first half line xy pointer for second half working
        if PDF.secondHalf == 0:
            fhl_xy = [self.get_x() + width - 40, self.get_y()]
            PDF.secondHalf = fhl_xy
            self.cell(width-40, height, txt=texts[2], border=b, align="L", ln=1)
        else:
            self.cell(width-40, height, txt=texts[2], border=b, align="L", ln=1)
        
    def first_half_dash_line_values(self, width, height, values, b=1):
        self.set_x(20)
        self.set_text_color(0,0,0)
        self.cell(width-10, height, txt=values[0], border=b, align="L")
        self.cell(width-30, height, txt=values[1], border=b, align="L")
        self.cell(width-40, height, txt=values[2], border=b, align="L", ln=1)
        self.ln(3)
        
    def second_half_dash_line_name(self, width, height, texts, b=0):
        self.set_font('Times', 'B', 10)
        self.set_xy(PDF.secondHalf[0] + 15, PDF.secondHalf[1])
        self.set_text_color(137,137,137)
        if not isinstance(texts, tuple):
            self.cell(width - 15, height, txt=texts, border=b, align="L",ln=1)
            PDF.secondHalf[1] = self.get_y()
        else:
            self.cell(width - 40, height, txt=texts[0], border=b, align="L",ln=0)
            self.cell(width - 40, height, txt=texts[1], border=b, align="L",ln=1)
            PDF.secondHalf[1] = self.get_y()
        
    def second_half_dash_line_value(self, width, height, texts, b=0):
        self.set_font('Times', 'B', 10)
        self.set_xy(PDF.secondHalf[0] + 15, PDF.secondHalf[1])
        self.set_text_color(0,0,0)
        if not isinstance(texts, tuple):
            self.cell(width - 15, height, txt=texts, border=b, align="L",ln=1)
            self.ln(2)
            PDF.secondHalf[1] = self.get_y()
        else:
            self.cell(width - 40, height, txt=texts[0], border=b, align="L",ln=0)
            self.cell(width - 40, height, txt=texts[1], border=b, align="L",ln=1)
            self.ln(2)
            PDF.secondHalf[1] = self.get_y()
            
    def map_link_and_barcode(self, urlpath, width, height, b=0):
        self.set_xy(20, self.get_y() - 15)
        self.cell(txt="Click here to see Route Map.", w=width - 10, h=height, link=urlpath, border=0)
        # adding barcode
        self.code39("*MDI7*", x=self.get_x()+10, y=self.get_y(), w=1, h=height)
        
    def last_cell(self, rgb, e1, e2):
        self.set_fill_color(r=rgb[0], g=rgb[1], b=rgb[2])
        self.set_xy(e1, e2)
        self.cell(w=self.epw, h=5, txt="", border=1, fill=True)
        