# Montar o Google Drive
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import os

# Caminho da pasta gpp no Google Drive
folder_path = '/content/drive/My Drive/gpp/'

# Lista dos arquivos a serem processados
files = ["teleconexoes_2001_2020.csv"]

def remove_autocorrelation(df):
    # Aplica a diferenciação nas colunas C até BO (indice 2 até o final)
    for column in df.columns[2:]:
        df[column] = df[column].diff().dropna().reset_index(drop=True)
    # Também remover as linhas correspondentes nas colunas A e B para manter a consistência
    df = df.dropna().reset_index(drop=True)
    return df

# Processar cada arquivo
for file in files:
    # Carregar o arquivo CSV
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)

    # Remover autocorrelação
    df_sem_autocorrelacao = remove_autocorrelation(df)

    # Salvar o novo arquivo com o sufixo "_SEM_AUTOCORRELAÇÃO"
    new_file_name = file.replace(".csv", "_SEM_AUTOCORRELAÇÃO_TESTE2.csv")
    new_file_path = os.path.join(folder_path, new_file_name)
    df_sem_autocorrelacao.to_csv(new_file_path, index=False)

print("Processamento concluído!")
