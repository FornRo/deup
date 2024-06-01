import pandas as pd

# df1 = pd.DataFrame(
#     data=[["AAA" * 10, "BBB" * 10]],
#     index=['row 1', 'row 2'],
#     columns=["test_test_test_test_test", "test_test_test_test_test"],
# )
# df2 = pd.DataFrame([["ABC"*22, "XYZ"*22]], columns=["Foo", "Bar"])


df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],
                   index=['row 1', 'row 2'],
                   columns=['col 1', 'col 2'])
df1.to_excel("output.xlsx")

df1.to_excel("output.xlsx",
             sheet_name='Sheet_name_1')

df2 = df1.copy()
with pd.ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sheet_name_1')
    df2.to_excel(writer, sheet_name='Sheet_name_2')
