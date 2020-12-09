import pandas as pd
import plotly.express as px
import collections
import numpy as np

# Creating a dataframe using the csv
data = pd.read_csv('kompass-textiles-cleaned.csv')
df = pd.DataFrame(data)

# falta eliminar por si una palabra se repite en el texto restante en el data cleaning

# I am only interested in columns from 10
columns2use = df.iloc[:, 10:]
columnNumberElements = []
columnNames = []

for x in columns2use.columns:
    # First I have to save the name of each column in an array
    columnNames.append(x)
    columnName = df[x]
    # Here we are counting the rows that has 1 for that field so at the end we are gonna have the number of stores that do that activity in a variable called columnNumberElements
    columnNumberElements.append(columnName[columnName == 1].count())

# Creating a dictionary for ordering from 2 arrays:
dictionary = dict(zip(columnNames, columnNumberElements))

# Ordering the dictionary from higher to lower
orderedDictionary = sorted(dictionary.items(), key=lambda kv: (
    kv[1], kv[0]), reverse=True)

# Creating a dataframe with the data to graph.
dataToGraph = pd.DataFrame(orderedDictionary, columns=['Name', 'Quantity'])

# Storing the graph in fig and showing it
fig = px.bar(dataToGraph, x="Name", y="Quantity")
fig.show()
