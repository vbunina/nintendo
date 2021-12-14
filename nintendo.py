import pandas as pd 
import numpy as np 
import scipy 
import seaborn as sns
import matplotlib as plt
from scipy import stats


# загрузим данные и убедимся, что всё считалось правильно (посмотрим на столбцы, типы данных, размерность, наличие пропущенных значений). так как последние есть - удалим их
df = pd.read_csv('https://stepik.org/media/attachments/lesson/383837/games.csv')
df.dtypes
df.value_counts()
df.shape
df.isna()
df_clean = df.dropna()

# посмотрим описательные характеристики переменной Year (год выпуска видеоигры) и моду по ней
df_clean.Year.describe()
df_clean.Year.mode() # или самое часто встречающееся значение в df_clean.value_counts('Year')

# теперь нам интересно узнать платформы, частота встречаемости которых составляет более 7%. при получении названий запишем их в список
platforms = df_clean.value_counts('Platform', normalize=True).to_frame('quantity') * 100
platforms.query('quantity > 7').index.to_list()

# посмотрим, игры каких издателей встречаются в датасете чаще всего
df_clean.value_counts('Publisher') # или stats.mode(df_clean.Publisher)

# сфокусируемся на играх от Nintendo. посчитаем медиану по продажам игр данного издателя в разных регионах
nintendo = df_clean.query('Publisher == "Nintendo"')
(nintendo[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].agg('median'))

# теперь посмотрим на продажи Nintendo в Японии по жанрам, построив боксплот, где: по оси x будет расположен жанр игры, по оси у – объем продаж в Японии
plt.pyplot.figure(figsize=(16,16))
sns.boxplot(data=nintendo, x='Genre', y='JP_Sales')

# напоследок, визуализируем динамику изменения объема мировых продаж по годам для игр Nintendo следующих жанров: Fighting, Simulation, Platform, Racing, Sports
nintendo.query("Genre in ('Fighting', 'Simulation', 'Platform', 'Racing', 'Sports')").groupby(['Genre', 'Year']).sum()
nintendo_graph = nintendo.query("Genre in ('Fighting', 'Simulation', 'Platform', 'Racing', 'Sports')").groupby(['Genre', 'Year']).sum()
sns.lineplot(x = 'Year', y = 'Global_Sales', hue = 'Genre', data=nintendo_graph)