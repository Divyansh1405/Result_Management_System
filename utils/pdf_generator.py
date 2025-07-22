from fpdf import FPDF
def generate_pdf(student):
    roll, name, math, sci, eng = student
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Student Marksheet", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Roll No: {roll}", ln=True)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Math: {math}", ln=True)
    pdf.cell(200, 10, txt=f"Science: {sci}", ln=True)
    pdf.cell(200, 10, txt=f"English: {eng}", ln=True)
    total = math + sci + eng
    percent = total / 3
    pdf.cell(200, 10, txt=f"Total: {total}", ln=True)
    pdf.cell(200, 10, txt=f"Percentage: {percent:.2f}%", ln=True)
    path = f"static/{roll}_result.pdf"
    pdf.output(path)
    return path
