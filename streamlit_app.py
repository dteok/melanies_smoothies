# Import python packages
import requests
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name of Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", my_dataframe, max_selections=5  # keyword argument
)

if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

        # New section to display fruityvice nutrition information
        fruityvice_response = requests.get(
            "https://fruityvice.com/api/fruit/watermelon", timeout=30
        )
        fv_dataframe = st.dataframe(
            data=fruityvice_response.json(), use_container_width=True
        )

    # st.write(ingredients_string)

    my_insert_stmt = (
        """ insert into smoothies.public.orders (name_on_order, ingredients)
        values ('"""
        + name_on_order
        + """', '"""
        + ingredients_string
        + """')"""
    )
    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button("Submit Order")

    if ingredients_string:
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success(
                "Thank you, " + name_on_order + ", your Smoothie is ordered!", icon="✅"
            )
