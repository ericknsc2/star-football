import pandas as pd
import streamlit as st

# Configuração da página para visual mobile-friendly e wide
st.set_page_config(
    page_title="Star Football - Modo Carreira", page_icon="⭐", layout="wide"
)

st.title("⭐ Star Football: Modo Carreira")

# Dicionário de Ligas e Times
LIGAS_TIMES = {
    "Brasileirão Série A (Brasil)": [
        "Flamengo",
        "Palmeiras",
        "Fluminense",
        "Botafogo",
        "São Paulo",
        "Corinthians",
        "Grêmio",
        "Internacional",
        "Atlético-MG",
        "Cruzeiro",
    ],
    "Premier League (Inglaterra)": [
        "London FC",
        "Red City",
        "Blue United",
        "Northampton",
        "Capital City",
    ],
}

# Inicializar o estado da sessão para controlar se a carreira começou
if "carreira_iniciada" not in st.session_state:
  st.session_state.carreira_iniciada = False

# --- TELA 1: CRIAÇÃO DO PERSONAGEM ---
if not st.session_state.carreira_iniciada:
  st.subheader("📝 Criação do Atleta")
  st.markdown(
      "Defina a identidade do seu craque e escolha onde a sua jornada vai"
      " começar!"
  )

  with st.form("form_criacao"):
    nome_jogador = st.text_input("Nome do Jogador", "Craque 10")
    idade = st.number_input("Idade", min_value=16, max_value=40, value=18)
    posicao = st.selectbox(
        "Posição Principal",
        [
            "Atacante (ATA)",
            "Meia-Atacante (MEI)",
            "Ponta (PON)",
            "Volante/Meio (VOL)",
            "Zagueiro/Defesa (ZAG)",
        ],
    )

    liga_escolhida = st.selectbox("Escolha a Liga", list(LIGAS_TIMES.keys()))
    time_escolhido = st.selectbox("Escolha o Time", LIGAS_TIMES[liga_escolhida])

    submitted = st.form_submit_button("🚀 Assinar Contrato e Iniciar Carreira")

    if submitted:
      if nome_jogador.strip() == "":
        st.error("Por favor, insira um nome válido para o jogador.")
      else:
        # Criando o perfil do jogador com os 7 atributos escolhidos
        st.session_state.jogador = {
            "nome": nome_jogador,
            "idade": idade,
            "posicao": posicao,
            "liga": liga_escolhida,
            "time": time_escolhido,
            "energia": 100,
            "moral": 85,
            "reputacao": 10,
            "atributos": {
                "Velocidade": 60,
                "Finalização": 60,
                "Força": 55,
                "Vitalidade": 70,
                "Agilidade": 60,
                "Passe": 58,
                "Defesa": 40,
            },
        }
        st.session_state.carreira_iniciada = True
        st.rerun()

# --- TELA 2: PAINEL PRINCIPAL DA CARREIRA ---
else:
  jogador = st.session_state.jogador

  st.success(
      f"⚽ Bem-vindo ao clube, **{jogador['nome']}**! Atleta do"
      f" **{jogador['time']}** ({jogador['liga']})."
  )

  # Barra de Status do Jogador
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("⚡ Energia", f"{jogador['energia']}%")
  col2.metric("😊 Moral", f"{jogador['moral']}%")
  col3.metric("⭐ Reputação", f"{jogador['reputacao']} pts")
  col4.metric("🎂 Idade", f"{jogador['idade']} anos")

  st.markdown("---")
  st.subheader("📊 Painel de Atributos do Atleta")

  # Tabela limpa mostrando os 7 atributos escolhidos
  attr_df = pd.DataFrame(
      list(jogador["atributos"].items()), columns=["Atributo", "Nível"]
  )
  st.dataframe(attr_df, use_container_width=True, hide_index=True)

  st.markdown("---")
  st.info(
      "💡 **Próximo passo:** Nas próximas atualizações, vamos adicionar o"
      " simulador de partidas e o sistema de treinos para evoluir estes"
      " atributos!"
  )

  if st.button("🔄 Aposentar / Criar Novo Jogador"):
    st.session_state.carreira_iniciada = False
    st.rerun()
