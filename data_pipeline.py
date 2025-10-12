import streamlit as st
import pdfplumber
import pandas as pd
import re

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


# Função para extrair dados do PDF
def extract_data_from_pdf(pdf_file):
    df = pd.DataFrame(columns=["total_price", "date", "kilometers_traveled"])
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
                    # add price, date and km to dataframe
                    if price is not None and date is not None and km is not None:
                        df.loc[len(df)] = {
                            "total_price": price,
                            "date": date,
                            "kilometers_traveled": km
                        }
                        price = date= km = None  # Reset values after adding to DataFrame
    return df


def uber_csv(csv):
    df = pd.read_csv(csv)
    # extrair somente corridas concluídas
    try:
        df = df[df['status'] == 'completed']
        df['request_time'] = pd.to_datetime(df['request_time'])
        df['fare_amount'] = pd.to_numeric(df['fare_amount'], errors='coerce')
        df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
        df['product_type'] = df['product_type'].str.title()
        st.success("✅ Dados carregados com sucesso!")
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {e}")



extract_data_from_pdf("Receipt_02Mar2024_153137.pdf")