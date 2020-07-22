import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

array = [[46,4,0,0],
         [0,50,0,0],
         [2,5,42,1],
         [0,3,0,47]]

df_cm = pd.DataFrame(array, index=["Đốm Đen", "Loét", "Vàng Lá", "Khoẻ Mạnh"], columns=["Đốm đen", "Loét", "Vàng Lá", "Khoẻ Mạnh"])
sn.set(font_scale=1.0) # for label size
sn.heatmap(df_cm, annot=True, annot_kws={"size": 16})
plt.show()
