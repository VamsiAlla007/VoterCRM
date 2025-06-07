import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Welcome",
        page_icon="👋",
    )

    st.write("# Welcome to VOTERCRM-Vijayawada-Central-Assembly-Constituency App! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        
        """

        Vijayawada Central Assembly constituency


    """
    )


if __name__ == "__main__":
    run()
