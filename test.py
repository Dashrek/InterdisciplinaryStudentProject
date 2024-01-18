import pandas as pd

# Przykładowe dane (zmień to na rzeczywiste dane)
data1 = {'POLE_ID': [1, 2, 3], 'TOP_ID': [4, 5, 6]}
data2 = {'POLE_ID': [4, 5, 7], 'NAZWA': ['A', 'B', 'C']}

df_pole_supermarketu = pd.DataFrame(data1)
df_pole_supermarketu_inne = pd.DataFrame(data2)

# Połączenie z zachowaniem wszystkich wierszy z df_pole_supermarketu
result_df = pd.merge(df_pole_supermarketu, df_pole_supermarketu_inne, left_on='TOP_ID', right_on='POLE_ID', how='left', suffixes=('_p', '_t'))

# Zamień NaN na None
#result_df = result_df.where(pd.notna(result_df), None)

print(result_df)
for k,j in enumerate(range(5,9)):
    print(k,j)
print(type(round(248.2)))