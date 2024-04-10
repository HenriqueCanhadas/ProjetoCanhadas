import streamlit as st
import streamlit_authenticator as stauth
import yaml
import requests
import os

def projeto():
    import ProjetoCanhadas
    ProjetoCanhadas.main()

def authenticate():
    st.session_state["authentication_status"] = None
    
    # URL do arquivo config.yaml em modo raw
    config_url = 'https://raw.githubusercontent.com/TecnologiaServmar/ProjetoCanhadas/main/config.yaml'
    
    try:
        response = requests.get(config_url)
        # Verifica se o request foi bem sucedido
        if response.status_code == 200:
            # Carregando o conteúdo do YAML
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

def main():
    st.set_page_config(page_title="Projeto Canhadas", page_icon=":shark:")
        
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    titulo = st.title("SERVMAR")

    st.session_state["authentication_status"] = None
    authenticate()

    if st.session_state.get("authentication_status"):
        titulo.empty()
        success_message = st.success("Login Feito, Seja Bem Vindo!")
        projeto()
        success_message.empty()
    elif st.session_state["authentication_status"] is False:
        st.error("Usuário e/ou Senha Incorretos")
    elif st.session_state["authentication_status"] is None:
        st.warning("Digite um usuário e uma senha")

if __name__ == "__main__":
    main()
