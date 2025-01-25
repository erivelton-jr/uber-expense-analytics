import io
import streamlit as st
import pandas as pd
from data_extraction import extract_data_from_pdf
from datetime import datetime


st.title("Uber Expense Analytics")
st.write("Carregue arquivos PDF para extrair os dados de valor, quilômetros percorridos e data.")

uploaded_files = st.file_uploader("Selecione seus recibos em PDF", accept_multiple_files=True, type="pdf")

if uploaded_files:
    all_data = []
    for uploaded_file in uploaded_files:
        st.write("Carregando arquivo:", uploaded_file.name)
        pdf_data = extract_data_from_pdf(uploaded_file)
        if pdf_data:
            # Extrair o identificador do nome do arquivo
            file_id = uploaded_file.name.split(".")[0]
            for row in pdf_data:
                row.append(file_id)

            all_data.extend(pdf_data)


    if all_data:
        df = pd.DataFrame(all_data, columns=["total_price", "date","kilometers_traveled", "file_id"])
        df = df.drop_duplicates().reset_index(drop=True)
        st.write("Dados extraídos com sucesso!")

        df_ready = st.dataframe(df)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        excel_saved = output.getvalue()

        st.download_button(
            label="Download Excel",
            data=excel_saved,
            file_name=f"uber_expense_dataset_{datetime.now()}.xlsx",
            mime="application/vnd.ms-excel"
        )
    else:
        st.write("Não foi possivel transformar os dados")