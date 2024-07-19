from read_data import read_in_data, choose_index
import pandas as pd

def main():
    data = read_in_data()
    key = choose_index(data)
    print(f"The column {key} is set as the index of the dataframe.")

if __name__ == "__main__":
    main()