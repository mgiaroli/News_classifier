"""
creation of the streamlit app
"""
import pickle
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from createfeatures import create_features
import re

#streamlit run news_streamlit.py --> to view this Streamlit app on a browser

#we load the chosen model
with open('7.Streamlit_App/best_lsvc.pickle', 'rb') as input_file:
        model= pickle.load(input_file)

#We create a dictionary
reversed_label_codes={}
categorias=['Cultura y Espectáculos', 'Deportes', 'Economía','Internacional','Política','Sociedad/Policiales']
for num in [0,1,2,3,4,5]:
    reversed_label_codes[num]=categorias[num]

#title
st.title('Clasificador de noticias argentinas')

st.markdown('#### Ingresá el título y una corta descripción de una noticia ')

#input
news=st.text_area('')

if st.button('Predicción'):
    aux= re.sub('\n', '', news)
    aux= re.sub('\s+', '',aux).strip()
    if aux=='':
        st.info('Ingresá texto para hacer la predicción.')
    else:
        #we create the features
        features=create_features(news)
        
        #we calculate the prediction probabilities for this sample
        probabilities=model.predict_proba(features)
        
        #we sort the indices by probability, 
        sorted_indices=np.argsort(probabilities)[0].tolist()[::-1]
        sorted_categories=[reversed_label_codes[num] for num in sorted_indices]
        
        #we sort the probabilities, and we round each number up to 2 decimals.
        sorted_probabilities=np.sort(probabilities)[0].tolist()[::-1]
        rounded_probabilities=[round(num,2) for num in sorted_probabilities]
        
        #Plot prediction probabilities
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(y=sorted_categories,x=rounded_probabilities)
        #adds labels to bars
        ax.bar_label(ax.containers[-1], fontsize=15, padding=5)
        #we hide some parts of the box
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        #we set the ticklabels and params
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels(sorted_categories,fontsize=15)
        plt.tick_params(bottom=False)
        
        #Text for different cases
        if (np.max(probabilities)>=0.40 and ( sorted_probabilities[0]- sorted_probabilities[1])>0.05) or (np.max(probabilities)>=0.30 and ( sorted_probabilities[0]- sorted_probabilities[1])>0.15):
            st.write('La categoría de la noticia es: ' + sorted_categories[0] +'.')
            with st.expander('Probabilidades de predicción', expanded=False):
                st.pyplot(fig)
               
        elif np.max(probabilities)>=0.40 and ( sorted_probabilities[0]- sorted_probabilities[1])<=0.05:
            st.write('Está parejo. La categoría de la noticia es ' + sorted_categories[0]  +' con probabilidad ' +
                      str(rounded_probabilities[0]) + ' y ' + sorted_categories[1] 
                      + ' con probabilidad ' +  str(rounded_probabilities[1]) + '.')
            with st.expander('Probabilidades de predicción', expanded=False):
                st.pyplot(fig)
        else:
            st.write("""No está muy definido. La noticia también podría ser de otra categoría no 
                     incluida en las que tenemos. Las probabilidades de predicción de la categoría de la noticia son:""")
            st.pyplot(fig)
