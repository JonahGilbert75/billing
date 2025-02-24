from xhtml2pdf import pisa
from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse

def calculate_denominations(amount):
    denominations = [500, 50, 20, 10, 5, 2, 1]    
    result = {}

    for denom in denominations:
        k = f"{denom}_count"
        count = amount // denom  
        result[k] = count  
        amount -= count * denom  
    
    return result

def generate_pdf(context):
    html_string = render_to_string('page4.html', context)
    pdf_io = BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=pdf_io)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    pdf_io.seek(0)
    return pdf_io.read()


def send_email_with_pdf(email, pdf_data):
    if not pdf_data:
        print("Error: PDF generation failed")
        return

    subject = "Your Billing Report"
    message = "Hello,\n\nPlease find attached your billing report below.\n\nThank you."
    
    email_message = EmailMessage(
        subject=subject,
        body=message,
        to=[email]
    )

    email_message.attach('Billing_Report.pdf', pdf_data, 'application/pdf')
    email_message.send()
    print(f"Email sent to {email}")
    