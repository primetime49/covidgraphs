from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def normalize_data(l):
    result = []
    for n in l:
        if n == 'null':
            result.append(0)
        else:
            result.append(int(n))
    return result

def moving_average(d,l):
    result = []
    i = d-1
    while i < len(l):
        sums = 0
        back = i
        num = 1
        while num <= d:
            sums += l[back]
            back -= 1
            num += 1
        avg = sums/d
        result.append(avg)
        i += 1
    return result

country = input('insert country name: ').replace(' ','-')
page = requests.get('https://www.worldometers.info/coronavirus/country/'+country.lower())
soup = BeautifulSoup(page.content, 'html.parser')
res = str(soup)
if 'We might have removed the page from our website' in res:
  print('country not found')
  exit()

case = re.search('\'Daily Cases.+\n.+\n.+\n.+\[.+\]',res).group().split('[')[1][:-1].split(',')
death = re.search('\'Daily Deaths.+\n.+\n.+\n.+\[.+\]',res).group().split('[')[1][:-1].split(',')
days = re.search('categories: \[.+\]',res).group().replace('\"','').split('[')[1][:-1].split(',')

daily_new_case = normalize_data(case)
daily_new_death = normalize_data(death)

d = int(input('n-day moving average: n? (suggested 3/5/7/10) '))

fig, axs = plt.subplots(2, 1, constrained_layout=True)
plt.grid()

axs[0].plot(days[(d-1):], moving_average(d,daily_new_case))
axs[0].xaxis.set_major_locator(mticker.MultipleLocator(3))
axs[0].xaxis.set_minor_locator(mticker.MultipleLocator(1))
axs[0].xaxis.set_minor_formatter(mticker.NullFormatter())
axs[0].set_ylabel('Daily new cases')
axs[0].xaxis.set_tick_params(rotation=90)
axs[0].grid()

axs[1].plot(days[(d-1):], moving_average(d,daily_new_death))
axs[1].xaxis.set_major_locator(mticker.MultipleLocator(3))
axs[1].xaxis.set_minor_locator(mticker.MultipleLocator(1))
axs[1].xaxis.set_minor_formatter(mticker.NullFormatter())
axs[1].set_ylabel('Daily new deaths')
axs[1].xaxis.set_tick_params(rotation=90)

fig.suptitle(country)

plt.show()