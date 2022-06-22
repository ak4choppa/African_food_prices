#import libaries
from turtle import color
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt

@st.cache
def get_data():
    #fetching the dataset
    url = "./dataset/africa_food_prices.csv"
    data = pd.read_csv(url)

    #droping unwanted column
    cols_to_drop = ['Unnamed: 0','mp_commoditysource']
    data = data.drop(columns=cols_to_drop)

    #renaming column name
    new_names = {    
    'pt_id':'market_type_id',
    'um_unit_id':'measurement_id',
    'market':'town',
    'market_id':'town_id',
    'price':'price_paid',
    'produce':'commodity_purchased',
    'produce_id':'commodity_purchased_id',
    'month':'month_recorded',
    'year':'year_recorded',
    }
    data = data.rename(columns=new_names)
 
    # remove null records
    data.dropna(axis=0, how='any', inplace = True)
    data.isnull().sum()

    return data


# title
st.write("# African Food Price Map")


# Display result using Python  
print(get_data())

#display result using Streamlit
data = get_data()
  


#create a structure for the app

try:
   st.sidebar.header('User input Controls')
   st.sidebar.header('Filter Records')
   data = get_data()
   states = st.sidebar.multiselect("Choose state",data.state.unique(),"Abia")
   product = st.sidebar.selectbox("Choose product",data.produce.unique())


   if not states:
      st.sidebar.error("Please select at least one state")

   else:
      for i,index in enumerate(states):
         data = data[data.state == states[i]]
         st.write(f"### Prices of goods in {states[i]} Markets",

data.head())

   pvt = pd.pivot_table(data, index=['state','market_type','produce','year'], values=['price'], aggfunc='mean')
   pvt_data = pvt.reset_index()
   selected_state = states[i]
   st.write(selected_state)
   pvt_data = pvt_data[pvt_data['state'] == selected_state ]

  # selected product
   selected_product = product
   st.write(selected_product)
   pvt_data = pvt_data[pvt_data['produce'] == selected_product ]

# using the data to build a line chat
   chart = alt.Chart(pvt_data).mark_line().encode(x = 'year',y = 'price',tooltip=['market_type','price'])
   #st.write(f"### Price chart {selected_product} in {selected_state}")
   #st.altair_chart(chart,use_container_width=True)

# using the data to build an area chart
   chart = alt.Chart(pvt_data).mark_area().encode(x = 'year',y = 'price',tooltip=['market_type','price'])
   #st.write(f"### Price chart {selected_product} in {selected_state}")
   #st.altair_chart(chart,use_container_width=True)

# using the data to build a different market
   chart = alt.Chart(pvt_data).mark_area().encode(x = 'year', color = 'market_type',y = 'price',tooltip=['market_type','price']).interactive()
   st.write(f"### Price chart {selected_product} in {selected_state}")
   st.altair_chart(chart,use_container_width=True)

except RuntimeError as e:
   st.error(e.reason)       