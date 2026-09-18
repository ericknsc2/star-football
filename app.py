import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Star Football - Modo Carreira", page_icon="⭐", layout="wide"
)

st.title("⭐ Star Football: Modo Carreira")

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

if "carreira_iniciada" not in st.session_state:
  st.session_state.carreira_iniciada = False

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
        st.session_state.jogador = {
            "nome": nome_jogador,
            "idade": idade,
            "posicao": posicao,
            "liga": liga_escolhida,
            "time": time_escolhido,
            "energia": 100,
            "moral": 85,
            "reputacao": 10,
            "partidas_jogadas": 0,
            "gols": 0,
            "assistencias": 0,
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

else:
  jogador = st.session_state.jogador

  st.success(
      f"⚽ Atleta: **{jogador['nome']}** | Clube: **{jogador['time']}**"
      f" ({jogador['liga']})"
  )

  col1, col2, col3, col4, col5 = st.columns(5)
  col1.metric("⚡ Energia", f"{jogador['energia']}%")
  col2.metric("😊 Moral", f"{jogador['moral']}%")
  col3.metric("⭐ Reputação", f"{jogador['reputacao']} pts")
  col4.metric("⚽ Gols", jogador["gols"])
  col5.metric("🎯 Assist.", jogador["assistencias"])

  st.markdown("---")

  aba_visao, aba_treino, aba_partida = st.tabs(
      ["🏠 Visão Geral", "🏋️‍♂️ Centro de Treinamento", "⚽ Próxima Partida"]
  )

  with aba_visao:
    st.subheader("📊 Perfil e Atributos do Atleta")
    st.write(
        f"**Posição:** {jogador['posicao']} | **Idade:** {jogador['idade']} anos"
    )

    attr_df = pd.DataFrame(
        list(jogador["atributos"].items()), columns=["Atributo", "Nível"]
    )
    st.dataframe(attr_df, use_container_width=True, hide_index=True)

    if st.button("🔄 Aposentar / Criar Novo Jogador"):
      st.session_state.carreira_iniciada = False
      st.rerun()

  with aba_treino:
    st.subheader("🏋️‍♂️ Evolução de Atributos")
    st.markdown(
        "Treine duro para subir seus atributos! Cada treino consome **15% de"
        " energia**."
    )

    if jogador["energia"] < 15:
      st.warning(
          "⚠️ Você está muito cansado! Vá para a aba 'Próxima Partida' e jogue"
          " (ou descanse) para recuperar energia."
      )
    else:
      atrib_para_treinar = st.selectbox(
          "Escolha o atributo para treinar:", list(jogador["atributos"].keys())
      )

      if st.button("💪 Realizar Sessão de Treino"):
        jogador["energia"] -= 15
        ganho = random.randint(1, 3)
        jogador["atributos"][atrib_para_treinar] += ganho
        jogador["moral"] = min(100, jogador["moral"] + 2)
        st.success(
            f"📈 Treino concluído! Seu atributo **{atrib_para_treinar}** subiu"
            f" +{ganho} pontos!"
        )
        st.rerun()

  with aba_partida:
    st.subheader("🏟️ Dia de Jogo - Momento Decisivo")

    if jogador["energia"] < 20:
      st.error(
          "❌ Você está com a energia esgotada (< 20%) e o técnico te poupou"
          " do jogo. Descanse ou recupere energias!"
      )
      if st.button("🛌 Descansar e Recuperar Energia"):
        jogador["energia"] = min(100, jogador["energia"] + 50)
        jogador["moral"] = min(100, jogador["moral"] + 5)
        st.success("🔋 Você descansou e recuperou 50% de energia!")
        st.rerun()
    else:
      st.markdown(
          "O jogo está empatado e a sua equipe chegou ao ataque. O técnico"
          " confia na sua tomada de decisão!"
      )

      col_a, col_b = st.columns(2)

      with col_a:
        st.info(
            "🎯 **Opção 1: Finalizar em Cobertura / Chute Direto**\n\n*Usa sua"
            " Finalização e Agilidade.*"
        )
        if st.button("Chutar ao Gol!"):
          jogador["energia"] -= 20
          jogador["partidas_jogadas"] += 1
          chance = (
              jogador["atributos"]["Finalização"]
              + jogador["atributos"]["Agilidade"]
          ) / 200
          if random.random() < chance:
            jogador["gols"] += 1
            jogador["reputacao"] += 5
            jogador["moral"] = min(100, jogador["moral"] + 10)
            st.balloons()
            st.success(
                "GOOOOOOL! Você acertou um chutaço no ângulo e garantiu a"
                " vitória do time! ⚽🎉"
            )
          else:
            st.error(
                "😢 Você chutou forte, mas o goleiro defendeu espetacularmente!"
            )
          st.rerun()

      with col_b:
        st.info(
            "👟 **Opção 2: Passe para o companheiro livre**\n\n*Usa seu Passe e"
            " Visão.*"
        )
        if st.button("Tentar a Assistência"):
          jogador["energia"] -= 20
          jogador["partidas_jogadas"] += 1
          chance = jogador["atributos"]["Passe"] / 100
          if random.random() < chance:
            jogador["assistencias"] += 1
            jogador["reputacao"] += 4
            jogador["moral"] = min(100, jogador["moral"] + 8)
            st.success(
                "PASSE CIRÚRGICO! Você deixou o seu companheiro cara a cara com"
                " o gol para marcar! 🎯"
            )
          else:
            st.warning(
                "⚠️ O zagueiro adversário leu a jogada e cortou o seu passe na"
                " hora H."
            )
          st.rerun()
