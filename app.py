
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Aviator Predictor", layout="wide")
st.title("✈️ Aviator Queda - Previsor Inteligente")

# Inicialização de sessão
if 'valores' not in st.session_state:
    st.session_state.valores = []

# Entrada
st.markdown("### Inserir valor do Aviator")
novo_valor = st.number_input("Valor (ex: 1.76)", step=0.01)

if st.button("Adicionar"):
    if novo_valor > 0:
        st.session_state.valores.append(novo_valor)

# Cores por intervalo
def cor_intervalo(v):
    if v < 2.0:
        return "red"
    elif v < 4.0:
        return "orange"
    else:
        return "green"

# Mostrar histórico com cores
if st.session_state.valores:
    st.markdown("### Histórico de Valores")
    for i, val in enumerate(reversed(st.session_state.valores[-10:])):
        cor = cor_intervalo(val)
        st.markdown(f"<span style='color:{cor}; font-size:20px'>#{len(st.session_state.valores)-i} → {val}</span>", unsafe_allow_html=True)

    # Estatísticas
    media = np.mean(st.session_state.valores)
    max_val = np.max(st.session_state.valores)
    min_val = np.min(st.session_state.valores)
    ultimos = st.session_state.valores[-5:]
    tendencia = "Subida" if all(ultimos[i] <= ultimos[i+1] for i in range(len(ultimos)-1)) else "Queda" if all(ultimos[i] >= ultimos[i+1] for i in range(len(ultimos)-1)) else "Instável"

    st.markdown("### Estatísticas:")
    st.write(f"Média: {media:.2f}")
    st.write(f"Máximo: {max_val}")
    st.write(f"Mínimo: {min_val}")
    st.write(f"Tendência Atual: **{tendencia}**")

    # Previsão simples (baseado na média e tendência)
    if tendencia == "Subida":
        previsao = media + 0.5
    elif tendencia == "Queda":
        previsao = media - 0.3
    else:
        previsao = media

    st.markdown("### Previsão Inteligente:")
    st.write(f"Próximo valor provável: **{previsao:.2f}**")

    # Gráfico com cores
    df = pd.DataFrame({'Valor': st.session_state.valores})
    df['Cor'] = df['Valor'].apply(cor_intervalo)

    fig, ax = plt.subplots()
    ax.plot(df['Valor'], marker='o')
    for i, row in df.iterrows():
        ax.plot(i, row['Valor'], marker='o', color=row['Cor'])
    ax.set_title("Gráfico de Tendência")
    ax.set_ylabel("Valor")
    ax.grid(True)
    st.pyplot(fig)

# Reset
if st.button("Limpar Histórico"):
    st.session_state.valores = []
