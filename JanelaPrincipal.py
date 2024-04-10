import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

def projeto():
    import ProjetoCanhadas
    ProjetoCanhadas.main()

def authenticate():
    st.session_state["authentication_status"] = None
    
    # Caminho absoluto do diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Caminho para o arquivo config.yaml, normalizando o caminho
    config_file_path = os.path.normpath(os.path.join(script_dir, 'ProjetoCanhadas', 'config.yaml'))
    
    # Verificação para garantir que o arquivo existe
    if not os.path.exists(config_file_path):
        st.error(f"Arquivo de configuração não encontrado: {config_file_path}")
        return

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
        success_message.empty()
    elif st.session_state["authentication_status"] is False:
        st.error("Usuário e/ou Senha Incorretos")
    elif st.session_state["authentication_status"] is None:
        st.warning("Digite um usuário e uma senha")

if __name__ == "__main__":
    main()
