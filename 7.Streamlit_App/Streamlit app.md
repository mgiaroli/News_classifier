# Streamlit app

The last step of our project is develop a web application to try our model. For the ease of use, and no front-end experience required, we chose [**Streamlit**](https://streamlit.io/).

The application is very simple. Requieres that the user enter the title and a short description of an article, and then the app will predict the category, and show the probabilities for each of the categories.

The files in this folder are:

- createfeatures.py - Scrip that allow us to create the features given text input.
- news_streamlit.py - Script of the streamlit application.