from database import create_db, Session
from model import AvitoItem

#Main function (API) is parse_avito(), the example call is at the bottom, commented out.

def parse_avito(url, print_report: bool=False, file_format: str=''): 
    '''Parses the avito page, creates an instance of AvitoItem with parsed data and saves it to database. \n
    Optional argument `print_report` can be set to `True`, in which case the kwarg `file_format` is expected (pdf, html or xlsx)'''
    create_db()
    item = AvitoItem(url)
    with Session() as session:
        session.add(item)
        session.commit()
        if print_report:
            _print_report(item, session, file_format)
            
def _print_report(item, session, file_format):
    def to_pdf():
        '''Uses fpdf2 package. \n
        Standard fonts do not support cyrillic. 'DejaVuSansCondensed' font is in the root directory to solve the issue.'''
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.core_fonts_encoding = 'utf-8'
        pdf.set_font("times", size = 15)
        pdf.add_font('DejaVu', fname='DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', size=14)
        for head in AvitoItem.__table__.columns.keys():
            pdf.cell(200, 10, txt = f"{head}: {str(item_db.__dict__[head])}", ln = 1, align = 'C')
        pdf.output(f'Report {item.id}.pdf')
    
    def to_html():
        with open(f'Report {item.id}.html', 'w', encoding='utf-8') as file:
            file.write('<p style="white-space: pre-line">')
            for head in AvitoItem.__table__.columns.keys():
                file.write(f'{head}: {item_db.__dict__[head]}\n')
            file.write('</p>')

    def to_xlsx():
        '''Uses XlsxWriter package'''
        import xlsxwriter
        workbook = xlsxwriter.Workbook(f'Report {item.id}.xlsx')
        worksheet = workbook.add_worksheet()
        row, col = 0, 0
        for head in AvitoItem.__table__.columns.keys():
            worksheet.write(row, col, head)
            if type(item_db.__dict__[head]) == dict:
                worksheet.write(row+1, col, str(item_db.__dict__[head]))
            else:
                worksheet.write(row+1, col, item_db.__dict__[head])
            col += 1
        workbook.close()

    for item_db in session.query(AvitoItem).filter(AvitoItem.id == item.id):
        if file_format == 'pdf':
            to_pdf()
        elif file_format == 'html':
            to_html()
        elif file_format == 'xlsx':
            to_xlsx()
        else:
            raise ValueError ("Incorrect file_format argument. 'file_format' must be 'pdf', 'html' or 'xlsx'")

# Example:
# url = 'https://www.avito.ru/moskva/mebel_i_interer/divan_krovat_bu_2333010835'
# parse_avito(url, print_report=True, file_format='xlsx')