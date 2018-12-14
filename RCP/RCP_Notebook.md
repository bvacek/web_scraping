
# RealClearPolitics Analysis
---

This is an analysis of the news and politics aggregator [RealClearPolitics](https://www.realclearpolitics.com). The data was scraped from the site using Scrapy.

### Scrapy
---------

[Scrapy](https://scrapy.org/) is an open source text scraping app. It is written in Python.

My scrapy spider starts with the most current page of realclearpolitics, downloads the date, title, source, author, and link of each article and exports and yields them as rows for a .csv file. It then follows the link to the previous days page and repeats the process. 

I currently have the spider designed to run until the date reads <b>12/31/2017</b> which returns 9335 articles but this can be easily changed if you desire more or less data.


### The Analysis
------
The analysis side is done using the following packages:

* [Pandas:](https://pandas.pydata.org) a package for data manipulation. I used it for its DataFrame data structure.

* [NumPy:](https://www.numpy.org) a package for large, multidimensional arrays. Pandas is dependent on it.

* [MatPlotLib:](https://matplotlib.org) a package for basic data visualization.

* [Plotly:](https://plot.ly) a package for more advanced data visualization.


```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='benvacek', api_key='hdJj4MRyb6oNYJYnG7pI')
```


Reads data into a DataFrame and prints the first 4 and last 4 rows.

As you can see the data contains **date**, **title**, **source** (the publication the article was taken from), **author**, **link**.


```python
rcp_df = pd.read_csv('rcp.csv')
rcp_df.iloc[np.r_[0:4, -4:0]]
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>title</th>
      <th>source</th>
      <th>author</th>
      <th>link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018/12/11</td>
      <td>Republicans, Don't Break Our Democracy</td>
      <td>CNN</td>
      <td>Tom Perez</td>
      <td>https://www.realclearpolitics.com/2018/12/11/r...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2018/12/11</td>
      <td>Build the Wall--Do What We Said We'd Do</td>
      <td>FOX News</td>
      <td>Reps. Jordan</td>
      <td>https://www.realclearpolitics.com/2018/12/11/b...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018/12/11</td>
      <td>Why Democrats Need Nancy Pelosi as Speaker</td>
      <td>USA Today</td>
      <td>Jill Lawrence</td>
      <td>https://www.realclearpolitics.com/2018/12/11/w...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2018/12/11</td>
      <td>Will the Leakers in the Flynn Case Escape Just...</td>
      <td>American Greatness</td>
      <td>Julie Kelly</td>
      <td>https://www.realclearpolitics.com/2018/12/11/w...</td>
    </tr>
    <tr>
      <th>9331</th>
      <td>2018/01/02</td>
      <td>This Moment Is About Iran, Not About Trump</td>
      <td>CNN</td>
      <td>Aaron David Miller</td>
      <td>https://www.realclearpolitics.com/2018/01/02/t...</td>
    </tr>
    <tr>
      <th>9332</th>
      <td>2018/01/02</td>
      <td>Congress's Gift to Blue-State Taxpayers</td>
      <td>Wall Street Journal</td>
      <td>Alfredo Ortiz</td>
      <td>https://www.realclearpolitics.com/2018/01/02/c...</td>
    </tr>
    <tr>
      <th>9333</th>
      <td>2018/01/02</td>
      <td>Hope It'll Be a Better Year for Immigrants Aft...</td>
      <td>NYDN</td>
      <td>Allan Wernick</td>
      <td>https://www.realclearpolitics.com/2018/01/02/h...</td>
    </tr>
    <tr>
      <th>9334</th>
      <td>2018/01/02</td>
      <td>From Detroit to Selma: Viola Liuzzo's Sacrifice</td>
      <td>RealClearPolitics</td>
      <td>Carl Cannon</td>
      <td>https://www.realclearpolitics.com/2018/01/02/f...</td>
    </tr>
  </tbody>
</table>
</div>



---

### First Graph
The first graph simply shows the 10 most common sources that RCP takes from along with the percentage of all posts that each source represents.


```python
rcp_df['source'].value_counts(normalize=True).head(10).plot.bar()
plt.title('Sources')
plt.show()
```


![png](output_5_0.png)


---

exported the top 10 sources to an array


```python
top10sources = list(rcp_df['source'].value_counts().head(10).keys())
top10sources
```




    ['New York Times',
     'RealClearPolitics',
     'Washington Post',
     'The Hill',
     'The Atlantic',
     'CNN',
     'FOX News',
     'USA Today',
     'Politico',
     'Bloomberg']



---

The **date** column in the original .csv file is a string which is not very useful for analysis so I had to convert it into a series of integers.

First I made 3 new columns in the DataFrame: **month**, **day**, and **year**.


```python
rcp_df.insert(1,'month',None)
rcp_df.insert(2,'day',None)
rcp_df.insert(3,'year',None)
rcp_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>month</th>
      <th>day</th>
      <th>year</th>
      <th>title</th>
      <th>source</th>
      <th>author</th>
      <th>link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018/12/11</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Republicans, Don't Break Our Democracy</td>
      <td>CNN</td>
      <td>Tom Perez</td>
      <td>https://www.realclearpolitics.com/2018/12/11/r...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2018/12/11</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Build the Wall--Do What We Said We'd Do</td>
      <td>FOX News</td>
      <td>Reps. Jordan</td>
      <td>https://www.realclearpolitics.com/2018/12/11/b...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018/12/11</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Why Democrats Need Nancy Pelosi as Speaker</td>
      <td>USA Today</td>
      <td>Jill Lawrence</td>
      <td>https://www.realclearpolitics.com/2018/12/11/w...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2018/12/11</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Will the Leakers in the Flynn Case Escape Just...</td>
      <td>American Greatness</td>
      <td>Julie Kelly</td>
      <td>https://www.realclearpolitics.com/2018/12/11/w...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2018/12/11</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>What Has the President Been 'Smocking'?</td>
      <td>Washington Post</td>
      <td>Eugene Robinson</td>
      <td>https://www.realclearpolitics.com/2018/12/11/w...</td>
    </tr>
  </tbody>
</table>
</div>



- - - 
I then iterated over the DataFrame and for each row, converted the **date** value into three integers representing the month, day, and year of the post and saved each in its respective column.


```python
for count,i in enumerate(rcp_df['date']):
    rcp_df['month'][count] = int(i.split('/')[1])
    rcp_df['day'][count] = int(i.split('/')[2])
    rcp_df['year'][count] = int(i.split('/')[0])

rcp_df.sample(10)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>month</th>
      <th>day</th>
      <th>year</th>
      <th>title</th>
      <th>source</th>
      <th>author</th>
      <th>link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>6551</th>
      <td>2018/04/15</td>
      <td>4</td>
      <td>15</td>
      <td>2018</td>
      <td>The Obscene Cost of Politics</td>
      <td>Newsday</td>
      <td>Michael Dobie</td>
      <td>https://www.realclearpolitics.com/2018/04/15/t...</td>
    </tr>
    <tr>
      <th>2543</th>
      <td>2018/09/09</td>
      <td>9</td>
      <td>9</td>
      <td>2018</td>
      <td>Could There Be Another Chinese Revolution?</td>
      <td>New York Times</td>
      <td>Yi-Zheng Lian</td>
      <td>https://www.realclearpolitics.com/2018/09/09/c...</td>
    </tr>
    <tr>
      <th>7115</th>
      <td>2018/03/25</td>
      <td>3</td>
      <td>25</td>
      <td>2018</td>
      <td>Senate Map</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.realclearpolitics.com/epolls/2018/...</td>
    </tr>
    <tr>
      <th>7789</th>
      <td>2018/02/28</td>
      <td>2</td>
      <td>28</td>
      <td>2018</td>
      <td>Globalization Has Created a Chinese Monster</td>
      <td>Foreign Policy</td>
      <td>Emile Simpson</td>
      <td>https://www.realclearpolitics.com/2018/02/28/g...</td>
    </tr>
    <tr>
      <th>8704</th>
      <td>2018/01/25</td>
      <td>1</td>
      <td>25</td>
      <td>2018</td>
      <td>'This Is Serious': Facebook Begins Its Downwar...</td>
      <td>Vanity Fair</td>
      <td>Nick Bilton</td>
      <td>https://www.realclearpolitics.com/2018/01/25/0...</td>
    </tr>
    <tr>
      <th>4953</th>
      <td>2018/06/12</td>
      <td>6</td>
      <td>12</td>
      <td>2018</td>
      <td>Trump, Kim Meet</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.realclearpolitics.com/video/2018/0...</td>
    </tr>
    <tr>
      <th>2554</th>
      <td>2018/09/08</td>
      <td>9</td>
      <td>8</td>
      <td>2018</td>
      <td>When I Challenge the President, I Do It Directly</td>
      <td>Washington Post</td>
      <td>Nikki Haley</td>
      <td>https://www.realclearpolitics.com/2018/09/08/w...</td>
    </tr>
    <tr>
      <th>7722</th>
      <td>2018/03/02</td>
      <td>3</td>
      <td>2</td>
      <td>2018</td>
      <td>Trump Says Trade Wars Are 'Good, and Easy to Win'</td>
      <td>Bloomberg</td>
      <td>Deaux</td>
      <td>https://www.realclearpolitics.com/2018/03/02/t...</td>
    </tr>
    <tr>
      <th>8238</th>
      <td>2018/02/12</td>
      <td>2</td>
      <td>12</td>
      <td>2018</td>
      <td>Here's What War With North Korea Would Look Like</td>
      <td>Vox</td>
      <td>Yochi Dreazen</td>
      <td>https://www.realclearpolitics.com/2018/02/12/h...</td>
    </tr>
    <tr>
      <th>6889</th>
      <td>2018/04/02</td>
      <td>4</td>
      <td>2</td>
      <td>2018</td>
      <td>Social Media Firms Want Us Hooked, Not Informed</td>
      <td>USA Today</td>
      <td>Glenn Reynolds</td>
      <td>https://www.realclearpolitics.com/2018/04/02/s...</td>
    </tr>
  </tbody>
</table>
</div>



---

### Second Graph

I decided to graph the prevalence of each of the top 10 sources over the course of the year.

First I created a *dictionary* containing as its keys, each of the 10 sources and as its values, their for each month.


```python
temp_df = pd.concat([rcp_df[rcp_df['source'].isin(top10sources)]['source'],
                     rcp_df[rcp_df['source'].isin(top10sources)]['month']],
                    axis = 1)
data = {}

for i in list(temp_df['source'].unique()):
    arr = []
    for j in list(temp_df['month'].unique()):
        arr.append(temp_df[(temp_df['source'] == i) & (temp_df['month'] == j)].size)
    data[i] = arr
data
```




    {'Bloomberg': [18, 30, 26, 28, 44, 24, 32, 28, 36, 48, 30, 34],
     'CNN': [16, 42, 48, 40, 54, 50, 48, 58, 42, 68, 46, 68],
     'FOX News': [32, 60, 48, 40, 58, 58, 52, 42, 42, 28, 24, 30],
     'New York Times': [44, 80, 118, 116, 108, 88, 102, 86, 100, 88, 94, 114],
     'Politico': [10, 48, 28, 32, 24, 30, 44, 40, 42, 42, 46, 46],
     'RealClearPolitics': [28, 120, 96, 60, 94, 98, 80, 72, 66, 88, 62, 66],
     'The Atlantic': [18, 60, 58, 58, 54, 50, 54, 60, 58, 54, 48, 44],
     'The Hill': [12, 52, 60, 56, 76, 74, 52, 78, 44, 62, 44, 32],
     'USA Today': [20, 36, 44, 56, 28, 58, 36, 40, 32, 32, 22, 30],
     'Washington Post': [22, 70, 70, 74, 72, 68, 70, 78, 62, 62, 76, 88]}



---
I then created a **Plotly** *line* object for each source.


```python
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
         'August', 'September', 'October', 'November', 'December']

trace0 = go.Scatter(
    x = month,
    y = data['Bloomberg'],
    name = 'Bloomberg'
)

trace1 = go.Scatter(
    x = month,
    y = data['CNN'],
    name = 'CNN'
)

trace2 = go.Scatter(
    x = month,
    y = data['FOX News'],
    name = 'FOX News'
)

trace3 = go.Scatter(
    x = month,
    y = data['New York Times'],
    name = 'New York Times'
)

trace4 = go.Scatter(
    x = month,
    y = data['Politico'],
    name = 'Politico'
)

trace5 = go.Scatter(
    x = month,
    y = data['RealClearPolitics'],
    name = 'RealClearPolitics'
)

trace6 = go.Scatter(
    x = month,
    y = data['The Atlantic'],
    name = 'The Atlantic'
)

trace7 = go.Scatter(
    x = month,
    y = data['The Hill'],
    name = 'The Hill'
)

trace8 = go.Scatter(
    x = month,
    y = data['USA Today'],
    name = 'USA Today'
)

trace9 = go.Scatter(
    x = month,
    y = data['Washington Post'],
    name = 'Washington Post'
)
```

And finally I graphed each of these lines. 

Pass over them with your cursor to see how Plotly allows for interactive graphs.


```python
py.iplot([trace0,trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9])
```




<iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~benvacek/8.embed" height="525px" width="100%"></iframe>


