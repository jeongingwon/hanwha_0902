import streamlit as st
import pandas as pd
import numpy as np


# df = pd.DataFrame({
#     'first columm' : [1, 2, 3, 4],
#     'second columm' : [10, 20, 30, 40]
# })
# # df

# st.write(df)

# datframe = np.random.randn(10,20)

# st.dataframe(datframe)
# st.write("반갑고 스트림릿")

# 랜덤한 값들중 가장 큰 수를 하이라이트 하는 코드
# dataframe = pd.DataFrame(
#     np.random.randn(10, 20),
#     columns=('col %d' % i for i in range(20))
# )

# st.dataframe(dataframe.style.highlight_max(axis=0))

# st.write("Hello, *World!* :sunglasses:")

# st.title("Summer Vacation")
# st.title(" :blue[ice] :blue[ice] :sunglasses:")

st.write("This is some text.")
st.slider("This is a slider", 0, 100, (0,0))
st.divider()
st.write("This text is between the horizontal rules.")
st.divider()