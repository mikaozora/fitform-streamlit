import streamlit as st

def main_loop():
    st.set_page_config(
        page_title="FitForm",
        page_icon="💪"
    )

    st.title("Sit Up Counter")
    st.divider()
    st.write("""
         ## Sit Up Guide
         1. Lying on your back on the floor
         2. Bend your knees and hook your legs with a secure support.
         3. Place your hands on the side or back of your neck.
         4. Bend your hips and waist to lift your body off the floor.
         5. Lower the body to the starting position.
""")

if __name__ == '__main__':
    main_loop()