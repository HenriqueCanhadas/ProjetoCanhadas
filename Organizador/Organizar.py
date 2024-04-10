import pandas as pd

def main(novo_caminho):
    # Define o caminho do arquivo Excel de entrada.
    caminho_excel = novo_caminho
    # Abre o arquivo Excel para leitura.
    excel = pd.ExcelFile(caminho_excel)

    # Dicionário para armazenar os DataFrames finais, um para cada aba.
    data_frame_final = {}

    # Itera sobre cada aba do arquivo Excel.
    for sheet_name in excel.sheet_names:
        # Lê os dados da aba atual para um DataFrame.
        data_frame = pd.read_excel(caminho_excel, sheet_name)

        # Obtém listas únicas dos nomes das amostras e dos analitos.
        lista_pm = data_frame['SAMPLENAME'].unique()
        lista_analyte = data_frame['ANALYTE'].unique()

        # Cria um novo DataFrame vazio com uma estrutura inicial.
        # Adiciona uma linha a mais no início para a data.
        data_frame_tabelado = pd.DataFrame(index=range(len(lista_analyte) + 1), columns=['Parametro', 'CAS', 'Unidade'] + list(lista_pm))

        # Dicionários para armazenar as unidades e números CAS correspondentes a cada analito.
        correspondencia_unidades = {}
        correspondencia_cas = {}

        # Preenche os dicionários com unidades e números CAS para cada analito.
        for analyte in lista_analyte:
            filtro_analyte = data_frame[data_frame['ANALYTE'] == analyte]
            if not filtro_analyte.empty:
                correspondencia_unidades[analyte] = filtro_analyte['UNITS'].iloc[0]
                correspondencia_cas[analyte] = filtro_analyte['CASNUMBER_x'].iloc[0]

        # Preenche as colunas 'Parametro', 'CAS', e 'Unidade' do DataFrame.
        for i, analyte in enumerate(lista_analyte, start=1):
            data_frame_tabelado.at[i, 'Parametro'] = analyte
            data_frame_tabelado.at[i, 'Unidade'] = correspondencia_unidades.get(analyte, '')
            data_frame_tabelado.at[i, 'CAS'] = correspondencia_cas.get(analyte, '')

        # Adiciona datas e resultados para cada amostra, colocando a data na linha correta.
        for pm in lista_pm:
            data_frame_pm = data_frame[data_frame['SAMPLENAME'] == pm]
            # Coloca a data diretamente na primeira linha sob o nome da amostra, ajustando a posição para a segunda linha do DataFrame.
            data_frame_tabelado.at[0, pm] = str(data_frame_pm['SAMPDATE'].iloc[0])
            for i, analyte in enumerate(lista_analyte, start=1):
                resultado = data_frame_pm[data_frame_pm['ANALYTE'] == analyte]['Result'].values
                if resultado.size > 0:
                    data_frame_tabelado.at[i, pm] = resultado[0]
                else:
                    data_frame_tabelado.at[i, pm] = "n.a"

        # Armazena o DataFrame reorganizado no dicionário.
        data_frame_final[sheet_name] = data_frame_tabelado

    # Salva os DataFrames reorganizados em um novo arquivo Excel.
    with pd.ExcelWriter(novo_caminho) as writer:
        for sheet_name, df in data_frame_final.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

if __name__ == "__main__":
    main()
