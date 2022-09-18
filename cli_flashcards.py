import argparse
from mailbox import linesep
from nis import match
import pandas as pd

def load_questions(file_name: str) -> pd.DataFrame:
    # TODO Store progress in a file and try to read them back according to file name.

    print(f"Reading questions from file: {file_name}")
    df = pd.read_csv(filepath_or_buffer=file_name, sep='\t', names=['Question', 'Answer'], lineterminator='\n')
    print(f"Succesfully loaded {len(df)} questions")
    return df

def read_and_validate_user_input():
    i = input('Input (y/n/s/q):  ').lower()

    if len(i) > 1:
        raise Exception('Wrong input length provided. Please read the doc.')

    if i not in ['y', 'n', 's', 'q']:
        raise Exception('Wrong input char provided. Please read the doc.')
    
    return i

def main(name: str):
    df = load_questions(name)

    print('Type "y" to mark as known, "n" to mark as to study, "s" to show the answer or "q" to exit.')

    while True:
        random_row = df.sample(n=1)
        print(f"\n\t{random_row['Question'].values[0]}\n")

        try:
            i = read_and_validate_user_input()
        except Exception as e:
            print(e)
            continue

        if i == 'q':
            print('Exiting')
            break
        elif i == 'y':
            pass
        elif i == 'n':
            pass
        elif i == 's':
            print(f"Answer for the current question is: {random_row['Answer']}")
        else:
            print(f"Unknown input provided: {i}. Please read the doc")

    # TODO Print stats


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File path to flashcards file', type=argparse.FileType('r', encoding='UTF-8'))

    args = parser.parse_args()
    main(args.file.name)