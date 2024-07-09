from google.colab import drive
import pandas as pd
from scipy.stats import spearmanr

# Montar o Google Drive
drive.mount('/content/drive')

# Caminho para o novo arquivo CSV
file_path = '/content/drive/My Drive/gpp/P_ET_GPP_EWUE_ANOM_12M_TELEC_C_SEM_CORREL.csv'

# Carregar o arquivo CSV em um DataFrame
data = pd.read_csv(file_path)

# Verificar as primeiras linhas do DataFrame
print(data.head())

def calculate_spearman_correlation_with_lag(data, bio_cols, tele_cols, lags):
    all_correlations = []
    for lag in lags:
        for bio_col in bio_cols:
            for tele_col in tele_cols:
                if lag == 0:
                    bio_series = data[bio_col]
                    tele_series = data[tele_col]
                else:
                    bio_series = data[bio_col][lag:].reset_index(drop=True)
                    tele_series = data[tele_col][:-lag].reset_index(drop=True)

                if len(bio_series) == len(tele_series):
                    corr, p_value = spearmanr(bio_series, tele_series)
                    all_correlations.append((bio_col, tele_col, lag, corr, p_value))
    return all_correlations

# Lista de lags
lags = [0, 1, 2, 3, 4, 5, 6]

# Selecionar as colunas de dados biofísicos e teleconexões com e sem autocorrelação
bio_cols = data.columns[1:17]  # Colunas B a Q
tele_cols_auto = data.columns[17:23]  # Colunas R a W (com autocorrelação)
tele_cols_no_auto = data.columns[23:29]  # Colunas X a AC (sem autocorrelação)

# Calcular as correlações de Spearman com lag-time para teleconexões com autocorrelação
correlations_auto = calculate_spearman_correlation_with_lag(data, bio_cols, tele_cols_auto, lags)

# Calcular as correlações de Spearman com lag-time para teleconexões sem autocorrelação
correlations_no_auto = calculate_spearman_correlation_with_lag(data, bio_cols, tele_cols_no_auto, lags)

# Criar DataFrames com todas as correlações
results_df_auto = pd.DataFrame(correlations_auto, columns=['Biophysical', 'Teleconnection_AUTO', 'Lag', 'Correlation', 'P-Value'])
results_df_no_auto = pd.DataFrame(correlations_no_auto, columns=['Biophysical', 'Teleconnection_noAUTO', 'Lag', 'Correlation', 'P-Value'])

# Verificar os DataFrames
print("Correlações com autocorrelação:")
print(results_df_auto)
print("Correlações sem autocorrelação:")
print(results_df_no_auto)

# Caminhos para salvar os arquivos CSV
results_file_path_auto = '/content/drive/My Drive/gpp/LAG-TIME/P_ET_GPP_EWUE_ANOM_12M_TELEC_C_CORREL_LAG-TIME2.csv'
results_file_path_no_auto = '/content/drive/My Drive/gpp/LAG-TIME/P_ET_GPP_EWUE_ANOM_12M_TELEC_SEM_CORREL_LAG-TIME2.csv'

# Salvar os DataFrames em arquivos CSV
results_df_auto.to_csv(results_file_path_auto, index=False)
results_df_no_auto.to_csv(results_file_path_no_auto, index=False)

print("Correlação calculada e resultados salvos com sucesso!")
