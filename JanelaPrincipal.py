import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


def projeto():
    import ProjetoCanhadas
    ProjetoCanhadas.main()

def authenticate():
    st.session_state["authentication_status"] = None  # Definir sempre como None para solicitar login
    with open('ProjetoCanhadas/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    autenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    autenticator.login()

def main():
    st.set_page_config(page_title="Projeto Canhadas", page_icon="servmarico.ico")
        
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    titulo=st.title("SERVMAR")

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