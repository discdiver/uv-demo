# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas>2",
#     "prefect",
# ]
# ///

from prefect import flow
import pandas as pd



@flow
def my_function():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    print(df)


if __name__ == "__main__":
    my_function()
