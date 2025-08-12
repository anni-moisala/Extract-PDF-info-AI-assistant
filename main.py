from operations.extract_pdf import get_data

CSV_FILE_PATH = "./data/Test.csv"


def main():
    
    get_data(CSV_FILE_PATH, limit=10)


if __name__ == "__main__":
    main()
