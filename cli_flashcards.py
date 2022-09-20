import argparse
import re
import pandas as pd
import warnings
import pathlib

warnings.simplefilter(action='ignore', category=FutureWarning)

def load_questions(file_name: str, known_dir: pathlib.Path) -> pd.DataFrame:
    # TODO Store progress in a file and try to read them back according to file name.
    if not known_dir.is_dir():
        known_dir.mkdir(parents=True, exist_ok=True)

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

def main(file_name: str, known_dir: pathlib.Path):
    question_df = load_questions(file_name=file_name, known_dir=known_dir)
    known_df = pd.DataFrame(columns=question_df.columns)

    print('Type "y" to mark as known, "n" to mark as to study, "s" to show the answer or "q" to exit.')

    while True:
        random_row = question_df.sample(n=1)
        print(f"\n*** New question: \n\t{random_row['Question'].values[0]}\n")

        try:
            i = read_and_validate_user_input()
        except Exception as e:
            print(e)
            continue

        if i == 'q':
            print('Exiting')
            break
        elif i == 'y':
            known_df = known_df.append(random_row, ignore_index=True)
            question_df.drop(random_row.index, inplace=True)
        elif i == 'n':
            pass
        elif i == 's':
            print(f"Answer for the current question is: {random_row['Answer'].values[0]}")
        else:
            print(f"Unknown input provided: {i}. Please read the doc")

    print(f"\nQuestions recap: \n\t Known: {known_df.shape[0]} \n\t Still to learn: {question_df.shape[0]}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File path to flashcards file', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('--store', help='File path to store known answers dir', type=pathlib.Path, default='./store_known/')

    args = parser.parse_args()
    main(args.file.name, args.store)
