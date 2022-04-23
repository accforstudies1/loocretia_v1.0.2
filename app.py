import os
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
from Common import Credentials, CountriesTwitter

warnings.catch_warnings()
warnings.simplefilter("ignore")

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
nlp = spacy.load("en_core_web_sm")

st.markdown(f'<h1 style="color:#3D3D39;font-size:70px;">{"Loocretia"}</h1>', unsafe_allow_html=True)


def run():
    NER_ATTRS = ["text", "label_", "start", "end", "start_char", "end_char"]
    st.write(date.today().strftime("%B %d, %Y"))

    def get_html(ai_resource_file: str, ai_html: str) -> str:
        """
        Convert HTML so it can be rendered
        :param ai_resource_file:
        :param ai_html:
        :return:
        """
        w_content = ""

        if os.path.isfile(ai_resource_file):
            with open(ai_resource_file, "r") as w_file:
                # Newlines seem to mess with the rendering
                w_content = w_file.read().format(ai_html.replace("\n", ""))

        return w_content

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

        w_html = displacy.render(doc, style="ent", options={"ents": label_select})
        style = "<style>mark.entity { display: inline-block }</style>"
        st.write(f"{style}{get_html('Views/Wrapper.html', w_html)}", unsafe_allow_html=True)

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
        word_def = []
        for word in new_doc.ents:
            word_def.append(word.text)

        mylist = list(dict.fromkeys(word_def))
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

        if sentiement_value['compound'] >= 0.05:
            st.markdown("People are sharing a positive opinion")
     
        elif sentiement_value['compound'] <= -0.05:
            st.markdown("People are sharing a negative opinion")

        else:
            st.markdown("People are neutral about the subject")


if __name__ == '__main__':
    run()

with st.sidebar:
    st.title('What is it ?')
    st.markdown('Summarizing of what happening at the moment choosed based on social network analysis. Reiterating the queries allows you to obtain more precision on the current event - Created by **V.Venedittan**')
    # st.markdown('Choose a country to find the top 10 trending')

    with st.form(key='Trends'):
        # Create a list of possible values and multiselect menu with them in it.
        w_countries = CountriesTwitter("datas/country.csv")
        if w_countries.is_valid:
            w_countries_selected = st.multiselect('Select countries [Top trending]', w_countries.values)

            if st.form_submit_button(label='Submit'):
                st.dataframe(pd.DataFrame(top_trends(w_countries.get_id(w_countries_selected[0]), Credentials()),
                                          columns=['Trendings']))
        else:
            print("Cannot read the csv containing the countries")

