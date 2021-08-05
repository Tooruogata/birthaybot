# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 22:39:10 2021
@author: tooru
**Install Requirements**
"""

!pip install -U discord.py
!pip install nest_asyncio
!pip install pygsheets

'''
Paths and parameters
'''

service_file_json = 'path to service file (json)'
gsheet_url = 'gsheet with birthday data'
TOKEN = 'discord token'
channel_id = 'discord channel id'


"""**Get today date**"""

from datetime import datetime
import pytz
peru_time_zone = pytz.timezone('Etc/GMT+5') 
peru_time = datetime.now(peru_time_zone)

peru_date = peru_time.strftime("%d/%m")
peru_month = peru_time.strftime("%m")

print(peru_date)
print(peru_month)

"""**Read gsheet with directory into a dataframe**"""

import pygsheets

'''Service account to drive'''
gc = pygsheets.authorize(service_file=service_file_json) 

'''Open gsheet'''
sh = gc.open_by_url(gsheet_url)

'''Select sheet'''
wks = sh[0]

'''Transform to dataframe'''
df = wks.get_as_df(has_header=True)

df.columns = ['name','date','status']

'''Minimun clean'''
new_df = df["date"].str.split("/", n = 3, expand = True)
  
# making separate first name column from new data frame
df["month"] = new_df[0]
df["month"] = df["month"].str.zfill(2)

# making separate last name column from new data frame
df["day"] = new_df[1]
df["day"] = df["day"].str.zfill(2)

# Dropping old Name columns
df.drop(columns =["date"], inplace = True)
del new_df

print(df)

"""**Monthly birthdays**"""

import pandas as pd
df_month = df
df_month['date'] = df_month['day'] + '/' + df_month['month']

df_month = df_month.query('(month == "' + peru_month + '")')
df_month = df_month.sort_values(by=['date'])
df_month = df_month[['name','date']]
count = len(df_month)

table_date = ''
table_date = ''
for index, row in df_month.iterrows():    
    str_name = str(row['name'])
    str_date = str(row['date']) 
    table_date = table_date + '(' + str_date + ') ' + str_name  + '\n'

print(table_date)

"""**Filter only today's birthdays**"""

import pandas as pd
df_contactos = df
df_contactos['date'] = df_contactos['date'].str[:5]
df_contactos = df_contactos.query('(date == "' + peru_date + '")')

list_name = ''
for name in df_contactos['name']:
  list_name = list_name + ' & ' + name

list_name = list_name[3:]

"""**Dummys de texto**"""

if list_name != '':
  msg = 'Hoy es cumpleaños de: ' + list_name + ', toca su respectivo saludo Impacta.'
  print(msg)
else:
  msg = 'Hoy nadie de impacta cumple años.'
  print(msg)

if count != 0 :
  msg = 'Los cumpleaños de este mes son:' + '\n' + table_date
  print(msg)
else:
  msg = 'No hay cumpleaños este mes.'

"""**Discord functions for bot**"""

import discord
import asyncio
import nest_asyncio
nest_asyncio.apply()
 
client = discord.Client()

@client.event
async def on_message(message):

    channel = client.get_channel(channel_id)
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
 
    if message.content.startswith('!birthday'):
      if count != 0 :
        msg = 'Los cumpleaños de este mes son:' + '\n' + table_date.format(message)
      else:
        msg = 'No hay cumpleaños este mes.'.format(message)
 
      await message.channel.send(msg)
 
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
 
    channel = client.get_channel(channel_id)
 
    if list_name != '':
      msg = 'Versión alpha: Hoy es cumpleaños de: ' + list_name + ', toca su respectivo saludo Impacta.'
    else:
      msg = 'Versión alpha: Hoy nadie de Impacta cumple años.'
 
    await channel.send(msg)
 
client.run(TOKEN)
