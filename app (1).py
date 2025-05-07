
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Aviator Inteligente")

# App title
st.title("✈️ Aviator Inteligente")
st.markdown("### Previsão, Análise e Tendência dos Resultados")

# Iniciar estado da sessão para armazenar dados
if 'valores' not in st.session_state:
    st.session_state['valores'] = []

# ABAS
aba = st.sidebar.radio("Navegar para:", ["Entrar Dados", "Gráfico", "Histórico", "Previsão"])

if aba == "Entrar Dados":
    st.subheader("Inserir novo valor")
    col1, col2 = st.columns(2)
    with col1:
        novo_valor = st.number_input("Digite o valor atual (ex: 1.8)", min_value=0.0, step=0.1)
    with col2:
        if st.button("Adicionar valor"):
            st.session_state['valores'].append(novo_valor)
            st.success("Valor adicionado!")

    # Exibir média e status
    if st.session_state['valores']:
        media = np.mean(st.session_state['valores'])
        cor = "green" if media > 3.0 else "orange" if media > 2.0 else "red"
        st.markdown(f"### Média atual: <span style='color:{cor}'>{media:.2f}</span>", unsafe_allow_html=True)

        if len(st.session_state['valores']) >= 3:
            ultimos = st.session_state['valores'][-3:]
            if all(v < 2.0 for v in ultimos):
                st.warning("Alerta: 3 valores baixos seguidos! Possível queda detectada.")
            elif all(v > 3.0 for v in ultimos):
                st.info("Tendência de subida detectada!")

elif aba == "Gráfico":
    st.subheader("Gráfico de Tendência")
    if st.session_state['valores']:
        df = pd.DataFrame({
            'Index': list(range(1, len(st.session_state['valores'])+1)),
            'Valor': st.session_state['valores']
        })

        fig, ax = plt.subplots()
        ax.plot(df['Index'], df['Valor'], marker='o', linestyle='-', color='blue', label='Valor')
        ax.axhline(y=np.mean(df['Valor']), color='green', linestyle='--', label='Média')
        ax.set_xlabel("Tentativas")
        ax.set_ylabel("Valor")
        ax.set_title("Tendência de Valores")
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("Ainda não há dados para exibir o gráfico.")

elif aba == "Histórico":
    st.subheader("Histórico de Valores")
    if st.session_state['valores']:
        df_hist = pd.DataFrame({
            'Nº': list(range(1, len(st.session_state['valores'])+1)),
            'Valor': st.session_state['valores']
        })
        st.dataframe(df_hist, use_container_width=True)

        csv = df_hist.to_csv(index=False).encode()
        st.download_button("📥 Baixar CSV", csv, "historico_aviator.csv", "text/csv")
    else:
        st.info("Sem valores registrados ainda.")

elif aba == "Previsão":
    st.subheader("Previsão do Próximo Valor (Regressão Linear Simples)")
    if len(st.session_state['valores']) >= 5:
        x = np.arange(len(st.session_state['valores']))
        y = np.array(st.session_state['valores'])
        coef = np.polyfit(x, y, 1)
        prox_valor = coef[0]*len(y) + coef[1]
        st.markdown(f"### Próxima previsão: <span style='color:blue'>{prox_valor:.2f}</span>", unsafe_allow_html=True)
    else:
        st.info("Insira pelo menos 5 valores para gerar uma previsão.")

# Rodapé
st.markdown("---")
st.caption("Criado com ❤️ por Samuel & ChatGPT")
