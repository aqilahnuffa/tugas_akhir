import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


st.header('Analisis Data Sharing Sepeda Berdasarkan Faktor Faktor Eksternal untuk Mengetahui Pola Penggunaan')

def create_user_count_df(df):
  user_count_df = df.groupby(by='date').agg({
    "date": "first",
    "all_user": "sum"
  })

  return user_count_df

def create_user_byseason_df(df):
  user_byseason_df = df.groupby(by='season').agg({
    "all_user": "sum"
  })

  return user_byseason_df

def create_user_byworkingday_df(df):
  user_byworkingday_df = df.groupby(by='workingday').agg({
    "workingday": "first",
    "all_user": "sum"
  })
  
  return user_byworkingday_df

def create_user_byweather_df(df):
  user_byweather_df = df.groupby(by='weathersit').agg({
    "weathersit": "first",
    "all_user": "sum"
  })
  
  return user_byweather_df

def create_user_byhour_df(df):
  user_byhour_df = df.groupby(by='hour').agg({
    "all_user": "sum"
  })

  return user_byhour_df

bike_df = pd.read_csv('dataset/bike_sharing.csv')


datetime_columns = ['date']
bike_df.sort_values(by='date', inplace=True)
bike_df.reset_index(inplace=True)

for column in datetime_columns:
  bike_df[column] = pd.to_datetime(bike_df[column])

# MEMBUAT KOMPONEN FILTER
min_date = bike_df['date'].min()
max_date = bike_df['date'].max()

with st.sidebar:
  # Load gambar dari pexels.com
  st.image('https://images.pexels.com/photos/127016/pexels-photo-127016.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')

  start_date, end_date = st.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
  )

  main_df = bike_df[(bike_df['date'] >= str(start_date)) & 
                    (bike_df['date'] <= str(end_date))]

user_count_df = create_user_count_df(main_df)
user_byseason_df = create_user_byseason_df(main_df)
user_byworkingday_df = create_user_byworkingday_df(main_df)
user_byweather_df = create_user_byweather_df(main_df)
user_byhour_df = create_user_byhour_df(main_df)

# Membuat Visualisasi Data

# Daily User
st.subheader('Daily User')

col1, col2, col3 = st.columns(3)

with col1:
  total_user = user_count_df.all_user.sum()
  st.metric("Total Users", value=total_user)

with col2:
  total_user_workday = user_byworkingday_df[user_byworkingday_df['workingday'] == 'work_day']['all_user'].sum()
  st.metric("Total Users Workday", value=total_user_workday)

with col3:
  total_user_holiday_weekday = user_byworkingday_df[user_byworkingday_df['workingday'] == 'holiday_weekend']['all_user'].sum()
  st.metric("Total Users Holiday or Weekday", value=total_user_holiday_weekday)

# Users Distribution by Daily

date = user_count_df['date']
users = user_count_df['all_user']
palette = "#4E4FEB"

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
  date,
  users,
  marker="o",
  linewidth=2,
  color=palette
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

ax.scatter([], [], c='red', marker='o', s=100, label='Akhir Data (2012-12-31)')
ax.legend(loc='upper left', fontsize=12)

st.pyplot(fig)

# Users Distribution by Weather
st.subheader('Users Distribution by Weather')
palette = ["#4E4FEB" if user == user_byweather_df['all_user'].max() else "#BDCDD6" for user in user_byweather_df['all_user']]

plt.figure(figsize=(16, 12))
weathersit_mapping = {
    "Clear, Few clouds, Partly cloudy, Partly cloudy": "Clear + Cloudy",
		"Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist": "Mist + Cloudy",
		"Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds": "Light Snow + Rain + Thunderstorm",
		"Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog": "Heavy Rain + Snow + Fog"
}
user_byweather_df['weathersit'] = user_byweather_df['weathersit'].map(weathersit_mapping)

user_byweather_df = user_byweather_df.sort_values(by='all_user', ascending=False)
users = user_byweather_df['all_user']
weather = user_byweather_df['weathersit']

ax = plt.bar(
  x=weather,
  height=users,
  color=palette
)

st.pyplot(plt.gcf())

# Users Distribution by Seasons
st.subheader('Users Distribution by Season')
palette = ["#4E4FEB" if user == user_byweather_df['all_user'].max() else "#BDCDD6" for user in user_byweather_df['all_user']]
user_byseason_df = user_byseason_df.sort_values(by='all_user', ascending=False)

plt.figure(figsize=(16, 8))
ax = sns.barplot(
  data=user_byseason_df, 
  x="all_user", 
  y="season", 
  orient="h", 
  palette=palette)

ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=20)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'))

st.pyplot(plt.gcf())

# Users Distribution by Hours
st.subheader('Users Distribution by Time of Day')
palette = "#4E4FEB"

plt.figure(figsize=(16, 8))

ax = sns.lineplot(
  data=user_byhour_df,
  x="hour",
  y="all_user",
  marker="o",
  color=palette
)
plt.xlabel('Hour')
plt.ylabel('Total User')

st.pyplot(plt.gcf())