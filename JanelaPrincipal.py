import streamlit as st
import streamlit_authenticator as stauth
import yaml
import requests
import time

# Função do Projeto Canhadas
def projeto():
    import ProjetoCanhadas
    ProjetoCanhadas.main()

# Função para validar a entrada
def authenticate():
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None

    config_url = 'https://raw.githubusercontent.com/TecnologiaServmar/ProjetoCanhadas/main/config.yaml'
    try:
        response = requests.get(config_url)
        if response.status_code == 200:
            config = yaml.load(response.content, Loader=yaml.SafeLoader)
        else:
            st.error("Falha ao carregar o arquivo de configuração.")
            return
    except Exception as e:
        st.error(f"Erro ao buscar o arquivo de configuração: {e}")
        return

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    authenticator.login()

# Função para exibir a mensagem temporária
def display_temporary_success_message():
    titulo = st.title("SERVMAR")
    # Exibe a mensagem de sucesso
    success_message = st.success("Login Feito, Seja Bem Vindo!")
    # Aguarda 5 segundos
    time.sleep(5)
    titulo.empty()
    # Remove a mensagem de sucesso
    success_message.empty()

# Função principal que define a configuração da página e o fluxo de autenticação
def main():
    global titulo
    st.set_page_config(page_title="Projeto Canhadas", page_icon="servmarico.ico")
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None

    if st.session_state.get("authentication_status") is None or st.session_state.get("authentication_status") is False:
        titulo = st.title("SERVMAR")
        authenticate()

    if st.session_state.get("authentication_status"):
        # Verifica se a mensagem de sucesso já foi exibida
        if not st.session_state.get("success_message_displayed", False):
            # Exibe a mensagem de sucesso temporária
            display_temporary_success_message()
            # Marca que a mensagem foi exibida para não repetir na próxima execução
            st.session_state["success_message_displayed"] = True
        # Continua para carregar o projeto sem esperar explicitamente aqui
        projeto()
    elif st.session_state.get("authentication_status") is False:
        st.error("Usuário e/ou Senha Incorretos")

if __name__ == "__main__":
    main()
