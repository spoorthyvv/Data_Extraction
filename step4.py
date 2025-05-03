import fitz
import os
import re
import pandas as pd

def extract_pdf_data(pdf_path):
    doc = fitz.open(pdf_path)
    pdf_data = {}
    page = doc[0]
    text = page.get_text("text")
    invoice_number = re.search(r"Invoice Number\s*:\s*(\S+)", text)
    if invoice_number:
        pdf_data['Invoice Number'] = invoice_number.group(1)
    gstin = re.search(r"GSTIN\s*:\s*(\S+)", text)
    if gstin:
        pdf_data['GSTIN'] = gstin.group(1)
    grand_total = re.search(r"Grand Total\s*([\d,]+\.\d+)", text)
    if grand_total:
        pdf_data['Grand Total'] = grand_total.group(1)
    service_period = re.search(r"Service Period\s*:\s*(\d{2}/\d{2}/\d{4}) to (\d{2}/\d{2}/\d{4})", text)
    if service_period:
        pdf_data['Service Period Start'] = service_period.group(1)
        pdf_data['Service Period End'] = service_period.group(2)

    return pdf_data

folder_path = "/home/spoorthy/Downloads/Cleaning_of_Data_and_Merging_into_single_excel/Commission_Invoices"
pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]
all_pdf_data = []

for pdf_file in pdf_files:
    print(f"Extracting data from: {pdf_file}")
    pdf_data = extract_pdf_data(pdf_file)
    pdf_data['Source File'] = os.path.basename(pdf_file)
    all_pdf_data.append(pdf_data)

df = pd.DataFrame(all_pdf_data)
df.to_csv("/home/spoorthy/Downloads/Cleaning_of_Data_and_Merging_into_single_excel/Commission_Invoices/extracted_pdf_data_spoo.csv", index=False)
print(df.head())
