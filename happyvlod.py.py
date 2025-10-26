import streamlit as st
from pathlib import Path
import base64
import mimetypes

# --- Константы и настройки ---
SECRET_CODEWORD = "Лейкопластер"
PERSON_NAME = "Лейкопластер"
PROMO_CODE = "17963"

# Картинка рядом с app.py (или замените на "assets/my_photo.jpg", если лежит в папке assets)
IMAGE_FILE_NAME = "my_photo.jpg"
IMAGE_PATH = Path(__file__).parent / IMAGE_FILE_NAME


def image_to_data_uri(path: Path) -> str:
    """
    Читает файл, кодирует содержимое в base64 и формирует data URI,
    чтобы картинку можно было вставить в <img src="..."> без внешних ссылок.
    """
    mime, _ = mimetypes.guess_type(str(path))
    if mime is None:
        mime = "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


# --- Настройка страницы ---
# Должен быть первым вызовом st.*
st.set_page_config(page_title="Промокод на День Рождения", page_icon="🎉")

# --- CSS для кастомизации ---
st.markdown("""
<style>
    /* Основной блок приложения */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Стиль для кнопок */
    .stButton > button {
        width: 100%; /* Растягиваем кнопку на всю ширину колонки */
        border: 1px solid grey;
        border-radius: 8px; /* Скругленные углы */
        color: black;
        background-color: white;
        font-family: 'Calibri', sans-serif;
    }
    .stButton > button:hover {
        border-color: black;
        color: black;
        background-color: #f0f0f0; /* Легкое выделение при наведении */
    }
</style>
""", unsafe_allow_html=True)


# --- Логика приложения ---
# Инициализация состояния аутентификации
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False


# --- Функция для проверки кодового слова ---
def check_codeword():
    """
    Безопасно проверяет введенное слово.
    Использует .get() для предотвращения KeyError.
    """
    entered_code = st.session_state.get("codeword_input", "")
    if entered_code == SECRET_CODEWORD:
        st.session_state['authenticated'] = True
        # Удаляем ключ только если он существует, для чистоты
        if "codeword_input" in st.session_state:
            del st.session_state["codeword_input"]
    elif entered_code != "":  # Показываем ошибку только если что-то было введено
        st.error("Кодовое слово неверно")


# --- Отрисовка страниц ---
# Если пользователь еще не аутентифицирован, показываем страницу входа.
if not st.session_state['authenticated']:
    # Центрируем контент с помощью колонок
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h3 style='text-align: center; font-family: Calibri;'>Введи пароль, Мистер сосистер, колбастер и самый настоящий ... кто?.</h3>",
            unsafe_allow_html=True
        )

        # Поле для ввода. type="password" скроет вводимые символы.
        # Ключ 'codeword_input' используется для доступа к значению в st.session_state
        st.text_input(
            "Кодовое слово",
            label_visibility="collapsed",
            key="codeword_input",
            type="password",
            on_change=check_codeword  # Проверяем при нажатии Enter
        )

        # Кнопка подтверждения
        st.button("Подтвердить", on_click=check_codeword)

# Если пользователь успешно вошел, показываем страницу с промокодом.
else:
    # CSS для градиентного фона ВТОРОЙ страницы
    st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to top, #F13A13, #FFFFFF);
        background-attachment: fixed;
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

    st.balloons()

    st.markdown(
        f"<h1 style='text-align: center; font-family: Calibri;'>{PERSON_NAME}, с днем рождения!</h1>,</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-family: Calibri; font-size: 1.2em;'>Прими от нас соСветкойй этот скромный дар :)</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Блок с картинкой ПЕРЕД промокодом
    IMAGE_DATA_URI = image_to_data_uri(IMAGE_PATH)

    st.markdown(
        "<h3 style='text-align: center; font-family: Calibri;'>Твоя картинка:</h3>",
        unsafe_allow_html=True
    )
    st.markdown(f"""
    <div style="
        background-color: #FFFFFF;
        border-radius: 0.5rem;
        padding: 1em;
        text-align: center;
    ">
        <img src="{IMAGE_DATA_URI}" style="max-width: 100%; border-radius: 0.5rem;" />
    </div>
    """, unsafe_allow_html=True)

    # Блок с промокодом
    st.markdown(
        "<h3 style='text-align: center; font-family: Calibri;'>Твой промокод на дрифт 28.10.2025:</h3>",
        unsafe_allow_html=True
    )
    st.markdown(f"""
    <div style="
        background-color: #FFFFFF;  /* ИЗМЕНЕНИЕ: Фон изменен на белый */
        border-radius: 0.5rem;
        padding: 1em;
        font-family: monospace;
        font-size: 1.25em;
        text-align: center;
        overflow-wrap: break-word;
    ">
        {PROMO_CODE}
    </div>
    """, unsafe_allow_html=True)
