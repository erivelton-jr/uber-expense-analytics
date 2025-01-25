import streamlit as st
import pdfplumber
import pandas as pd
import re


# Função para extrair dados do PDF
def extract_data_from_pdf(pdf_file):
    extracted_data = []
    with pdfplumber.open(pdf_file) as pdf:
        for pages in pdf.pages:
            text = pages.extract_text()
            print(text)

            price = None
            date = None
            km = None

            if text:  # Verificar se o texto foi extraído
                lines = text.split("\n")  # Dividir o texto em linhas
                for line in lines:

                    #procura valor total
                    if "R$" in line and "Total" in line:
                        price = float(line.split("R$")[-1].strip().replace(",", "."))
                    if "/" in line and len(line.strip()) >= 10:
                        date = extract_date(line)
                    if "Quilômetros" in line:
                        km = extract_km(line)

                    if price and date and km:
                        extracted_data.append([price, date, km])
        print(extracted_data)

    return extracted_data


def extract_date(line):
    date_pattern = r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b'
    match = re.search(date_pattern, line)
    if match:
        return pd.to_datetime(match.group(1), format='%d/%m/%Y', errors="coerce").date()
    else:
        return None

def extract_km(line):
    match = re.search(r'(\d+(?:\.\d+)?) Quilômetros', line)
    if match:
        return float(match.group(1))
    else:
        return None

extract_data_from_pdf("C:/Users/velto/PycharmProjects/UberExpenseAnalytics/Dataset/receipt_uber (20).pdf")