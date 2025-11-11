import streamlit as st
from streamlit_option_menu import option_menu
import fiona
import Sobre, SoundPLAN, soundscape

st.set_page_config(page_title="Multipage app", layout='wide')

# URL da logo
LOGO_URL_LARGE = "https://raw.githubusercontent.com/VictorMagno-Acoustics/mynoisebox/refs/heads/main/logo_mynoisebox.png"
LOGO_URL_SMALL = "https://raw.githubusercontent.com/VictorMagno-Acoustics/mynoisebox/refs/heads/main/logo_mynoisebox.png"

# Logo
st.logo(LOGO_URL_LARGE,link="https://mynoisebox.streamlit.app/", icon_image=LOGO_URL_LARGE, size="large")

st.html("""
  <style>
    [alt=Logo] {
      height: 5rem;
    }
  </style>
        """)

############ APP #############

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title=False,
                options=['About', 'Noise Mapping','Soundscape'],
                icons=['info-circle', 'soundwave','ear'],
                menu_icon='chat_text_fill',
                default_index=1,
            )

            # Adiciona o rodapé na barra lateral
            footer = """
            <style>
            .footer {
                position: absolute;
                bottom: 0;
                width: 100%;
                color: grey;
                text-align: center;
            }
            a {
                color: grey;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            </style>
            <div class='footer'>
                <p>Developed by <a href='https://www.linkedin.com/in/victor-magno/' target='_blank'>Victor Magno</a></p>
            </div>
            """
            st.sidebar.markdown("<div style='height: 570px;'></div>", unsafe_allow_html=True)  # Adiciona espaço antes do rodapé
            st.sidebar.markdown(footer, unsafe_allow_html=True)

        if app == 'About':
            Sobre.app()
        elif app =='Noise Mapping':
            SoundPLAN.app()
        elif app == 'Soundscape':
            soundscape.app()
                
# Cria e executa a aplicação MultiApp
app = MultiApp()
app.run()
