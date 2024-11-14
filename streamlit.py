
# import streamlit 
# streamlit.title("my parents new healthy diner")
# streamlit.header('Breakfast Menu')
# streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
# streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
# streamlit.text('🐔Hard-Boiled Free-Range Egg')
# streamlit.text('🥑🍞 Avacado Toast')

# streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
                 
# import pandas 

# my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# streamlit.dataframe(my_fruit_list)
# # Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# # Display the table on the page.
# streamlit.dataframe(my_fruit_list)
# my_fruit_list = my_fruit_list.set_index('Fruit')

# # lets put a pick list here so they can pick the fruit they want to include
# Fruits_selected= streamlit.multiselect("Pick some fruits:" , list(my_fruit_list.index),['Avacados', 'Strawberries'])
# fruits_to_show = my_fruit_list.loc[Fruits_selected]

# # Display the table on the page.
# streamlit.dataframe(fruits_to_show)

# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response)

# # new session to display fruityvice app response
# streamlit.header("Fruityvice Fruit Advice!")
# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json())

# # write your own comment -what does the next line do? 
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# # write your own comment - what does this do?
# streamlit.dataframe(fruityvice_normalized)


# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
# streamlit.write('The user entered ', fruit_choice)

# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + " kiwi")


# # # takes the json version of response and normalize it 
# # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# # # output it in the screen as table
# # streamlit.dataframe(fruityvice_normalized)


# import snowflake.connector

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()


import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')


streamlit.header('Breakfast Menu')

# streamlit.text('Omega 3 and Blueberry Oatmeal')
# streamlit.text('Kale, Spinach and Rocket Smoothie')
# streamlit.text('Hard-Boiled Free-Range Egg')


streamlit.text('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Apple', 'Grapefruit'])
fruits_to_show = my_fruit_list.loc[fruits_selected] # only show the filtered entries


# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#repeatable code block, called function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
# New Section to display fruityvice API response (fruityvice does not require an API key)
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    

except URLError as e:
  streamlit.error()
  
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)

#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json()) #just displayed the output to the screen

# normalize the json version of the response
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display on the screen as a table
#streamlit.dataframe(fruityvice_normalized)




streamlit.header("View Our Fruit List - Add Your Favorites!!")
#Snowflake Related Function
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()
    
#Add a button to load a fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close() #closing the connection
  streamlit.dataframe(my_data_rows)



# DO NOT RUN ANYTHING POST HERE WHILE TROUBLESHOOTING IS GOING ON
#streamlit.stop()

# import snowflake.connector


#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)


#my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
#my_data_row = my_cur.fetchone() #fetches only one row
# streamlit.text("FRUIT LOAD LIST CONTAINS:")
# streamlit.text(my_data_row)

#my_data_rows = my_cur.fetchall()
#streamlit.header("THE FRUIT LOAD LIST CONTAINS:")
#streamlit.dataframe(my_data_rows)


def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into FRUIT_LOAD_LIST values('" + new_fruit + "')")
    return 'Thanks for adding ' + new_fruit


add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  my_cnx.close() #closing the connection
  streamlit.text(back_from_function)
  
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)
