# Import python packages
import streamlit as st

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose Your Favorite Fruit you want in your smoothie!
       """)

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name in the smoothie will be:', name_on_order)


cnx = st.connection('snowflake')
session = cnx.session

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients: '
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:
    

    Ingredients_string = ''

    for fruit_chosen in ingredients_list:
        Ingredients_string +=fruit_chosen + ' '
        
    #st.write(Ingredients_string)

    
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES ('{Ingredients_string}', '{name_on_order}')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success(f"Your Smoothie order for '{name_on_order}' has been placed!", icon="✅")
