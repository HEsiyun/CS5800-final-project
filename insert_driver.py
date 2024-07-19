from read_data import read_in_data, choose_index, sort_data
import pandas as pd

def main():
    data = read_in_data()
    key = choose_index(data)
    data = sort_data(data, key)
    print(data)

if __name__ == "__main__":
    main()