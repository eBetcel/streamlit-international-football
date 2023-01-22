import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/results.csv")

# Recebe os gols e cria uma coluna de se foi vitória, derrota ou empate
df = df.assign(result=lambda x: np.where(x['home_score'] > x['away_score'], x['home_team'],
                                         np.where(x['home_score'] < x['away_score'], x['away_team'], 'draw')))
print(df.head())

st.title('Comparador de Seleções')

col1, col2 = st.columns(2)

selecoes_casa = set(df['home_team'].unique())
selecoes_fora = set(df['away_team'].unique())
selecoes = selecoes_fora.union(selecoes_casa)

with col1:
    home_team = st.selectbox(
        'Seleção 1',
        (sorted(selecoes)))

with col2:
    away_team = st.selectbox(
        'Seleção 2',
        (sorted(selecoes)))


def plot_historico(df, team_a, team_b):

    empates = df.query("((home_team == @team_a and away_team == @team_b) or (home_team == @team_b and away_team == @team_a)) and result == 'draw'").shape[0]
    vitorias_a = df.query("((home_team == @team_a and away_team == @team_b) or (home_team == @team_b and away_team == @team_a)) and result == @team_a").shape[0]
    vitorias_b = df.query("((home_team == @team_a and away_team == @team_b) or (home_team == @team_b and away_team == @team_a)) and result == @team_b").shape[0]
    
    results = empates, vitorias_b, vitorias_a

    df_results = pd.DataFrame({'results': ['Empate', 'Vitórias B', 'Vitórias A'], 'valor': results})

    fig = plt.figure(figsize=(15, 5))
    sns.countplot(x=df_results['valor'], data=df_results)
    st.write(df_results)
    st.pyplot(fig)



st.write(plot_historico(df, home_team, away_team))