import pandas as pd

df = pd.DataFrame

df1 = pd.DataFrame({'a':['a0','a1','a2','a3'],
                   'b':['b0','b1','b2','b3'],
                   'c':['c0','c1','c2','c3']},
                  index = [0,1,2,3])

df2 = pd.DataFrame({'a':['a2','a3','a4','a5'],
                   'b':['b2','b3','b4','b5'],
                   'c':['c2','c3','c4','c5'],
                   'd':['d2','d3','d4','d5']},
                   index = [2,3,4,5])

print(df1)
print(df2)

small_dfs = {}

# small_df = df1
# small_dfs.append(small_df)
# small_df = df2
# small_dfs.append(small_df)

small_dfs['samsung'] = df1
small_dfs['telecom'] = df2

print(small_dfs)

# if df.empty : 
#     print("비었습니다")
# else :
#     small_dfs.append(df)

# # print(small_dfs)

# large_df = pd.concat(small_dfs, ignore_index=False)

# print(large_df)
