def process_uploaded_pdfs(uploaded_files):
    import io
    import pandas as pd
    from datetime import datetime
    from data_pipeline import extract_data_from_pdf
    import streamlit as st
    from charts import dashboard


    if uploaded_files:
        all_data = []

        # Progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        total_files = len(uploaded_files)

        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.markdown(f"📄 Processando `{uploaded_file.name}` ({idx + 1}/{total_files})...")
            pdf_data = extract_data_from_pdf(uploaded_file)
            if pdf_data:
                file_id = uploaded_file.name.split(".")[0]
                for row in pdf_data:
                    row.append(file_id)
                all_data.extend(pdf_data)

            progress_bar.progress((idx + 1) / total_files)

        if all_data:
            try:
                df = pd.DataFrame(all_data, columns=["total_price", "date", "kilometers_traveled", "file_id"])
                df = df.drop_duplicates().reset_index(drop=True)

                st.success("✅ Dados extraídos com sucesso!")
                st.dataframe(df)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)

                excel_saved = output.getvalue()
                button1, button2 = st.columns(2)
                with button1:
                    st.download_button(
                        label="Download Excel",
                        data=excel_saved,
                        file_name=f"uber_expense_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.ms-excel"
                    )
                with button2:
                    st.button("🔄 Recarregar recibos", on_click=lambda: st.rerun())

                dashboard(df)


            except Exception as e:
                st.error(f"❌ Erro ao processar os dados: {e}")
        else:
            st.warning("⚠️ Não foi possível transformar os dados.")

