import sys
import pandas as pd

def main():
    df = pd.DataFrame({
        "outlet" : [1011111111111111111111111111],
        "refresh" : ["hi222222222222"]
    })
    print(df.to_string(index=False, justify="left"))


if __name__ == "__main__":
    main()
