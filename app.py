from typing import List, Sequence, Optional
from spacy import displacy
import streamlit as st
import wikipedia
from data_collect import twitter_queries
from fonctions import wiki_data
from fonctions import sentiment_scores
from fonctions import top_trends
import pandas as pd
from datetime import date
import spacy
import warnings
warnings.catch_warnings()
warnings.simplefilter("ignore")
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
nlp = spacy.load("en_core_web_sm")

st.markdown(f'<h1 style="color:#1E90FF;font-size:70px;">{"Loocretia"}</h1>', unsafe_allow_html=True)

def run():
    word_def = []
    NER_ATTRS = ["text", "label_", "start", "end", "start_char", "end_char"]
    today = date.today()
    st.write(today.strftime("%B %d, %Y"))

    def get_html(html: str):
        """Convert HTML so it can be rendered."""
        WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
        # Newlines seem to mess with the rendering
        html = html.replace("\n", " ")
        return WRAPPER.format(html)

    def visualize_ner(
        doc: spacy.tokens.Doc,
        *,
        labels: Sequence[str] = tuple(),
        attrs: List[str] = NER_ATTRS,
        show_table: bool = True,
        title: Optional[str] = "What's going on ?",
        sidebar_title: Optional[str] = "Identify the elements of the summary",
        key=None,  
    ) -> None:
        """Visualizer for named entities."""
        if title:
            st.header(title)
        if sidebar_title:
            st.sidebar.header(sidebar_title)
        label_select = st.sidebar.multiselect(
            "Feels free to add what you want", options=labels, default=list(labels), key=key # add key now
        )
        html = displacy.render(doc, style="ent", options={"ents": label_select})
        style = "<style>mark.entity { display: inline-block }</style>"
        st.write(f"{style}{get_html(html)}", unsafe_allow_html=True)
        if show_table:
            data = [
                [str(getattr(ent, attr)) for attr in attrs]
                for ent in doc.ents
                if ent.label_ in labels
            ]
            df = pd.DataFrame(data, columns=attrs)
            st.dataframe(df)

    with st.form(key='Enter name'):
        search_words = st.text_input('Enter the subject :')
        number_of_tweets = st.number_input('Enter the number (max -> 100) :', 0,100,100)
        submit_button = st.form_submit_button(label='Submit')  
    if submit_button:
        doc = nlp(twitter_queries(search_words, number_of_tweets))
        visualize_ner(doc, labels=nlp.get_pipe("ner").labels, key=1)
        
        st.subheader("Some definitions :")
        new_doc = doc
        # print(new_doc.ents)
        for word in new_doc.ents:
                word_def.append(word.text)
 
        mylist = list(dict.fromkeys(word_def))
        print(mylist)
        for element in enumerate(mylist):
            # print(element)
            try:
                st.write(wiki_data(element[1]))
            except (wikipedia.DisambiguationError, wikipedia.PageError, TypeError, KeyError):
                continue
 
        chart_data = pd.DataFrame(word_def, columns=["Most used words"])
        st.area_chart(chart_data)    

        st.title('Poeple sentiment')
        sentiement_value = sentiment_scores(twitter_queries(search_words, number_of_tweets))
        st.write("Overall sentiment dictionary is : ", sentiement_value)
        st.write("sentence was rated as ", sentiement_value['neg']*100, "% Negative")
        st.write("sentence was rated as ", sentiement_value['neu']*100, "% Neutral")
        st.write("sentence was rated as ", sentiement_value['pos']*100, "% Positive")
        if sentiement_value['compound'] >= 0.05 :
           st.markdown("People are sharing a positive opinion")
     
        elif sentiement_value['compound'] <= - 0.05 :
           st.markdown("People are sharing a negative opinion")
     
        else :
           st.markdown("People are neutral about the subject")

if __name__=='__main__':
    run()
    
with st.sidebar:
    st.title('What is it ?')
    st.markdown('Summarizing of what happening at the moment choosed based on social network analysis. Reiterating the queries allows you to obtain more precision on the current event - Created by **V.Venedittan**')
    # st.markdown('Choose a country to find the top 10 trending')
    with st.form(key='Trends'):      
        data = pd.read_csv("datas/country.csv")        
        # Create a list of possible values and multiselect menu with them in it.
        COUNTRIES = data['value'].unique()
        COUNTRIES_SELECTED = st.multiselect('Select countries [Top trending]', COUNTRIES)
        submit_button = st.form_submit_button(label='Submit')  
    if submit_button:
        top_10 = top_trends(COUNTRIES_SELECTED[0])
        df = pd.DataFrame(top_10, columns=['Trendings'])
        st.dataframe(df) 
