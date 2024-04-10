import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os  # Importando o módulo os

def projeto():
    import ProjetoCanhadas
    ProjetoCanhadas.main()

def authenticate():
    st.session_state["authentication_status"] = None  # Definir sempre como None para solicitar login
    
    # Construindo o caminho absoluto para o arquivo config.yaml
    script_dir = os.path.dirname(__file__)  # Diretório do script atual
    config_file_path = os.path.join(script_dir, 'ProjetoCanhadas', 'config.yaml')  # Caminho para o arquivo config.yaml
    
    with open(config_file_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    authenticator.login()

def main():
    st.set_page_config(page_title="Projeto Canhadas", page_icon="ProjetoCanhadas/servmarico.ico")
        
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
        success_message.empty()  # Remove a mensagem após 3 segundos
    elif st.session_state["authentication_status"] is False:
        st.error("Usuário e/ou Senha Incorretos")
    elif st.session_state["authentication_status"] is None:
        st.warning("Digite um usuário e uma senha")

if __name__ == "__main__":
    main()
