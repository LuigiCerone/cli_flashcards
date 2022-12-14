import argparse
import pandas as pd
import warnings
from pathlib import Path

warnings.simplefilter(action='ignore', category=FutureWarning)


def load_questions(file_name: Path, known_dir: Path) -> pd.DataFrame:
    """
    Method responsible for reading the csv file with the specified questions. 
    It also tries to restore any old statuses stored within the specified folder. 
    It returns two dataframes: the first contains the questions and their answers
    from which to randomly extract questions; the second contains the questions 
    that the user has already been able to answer.

    Args:
        file_name (Path): Path for questions file
        known_dir (Path): Path for old state searching dir

    Returns:
        df (DataFrame): Questions information
        known_df (DataFrame): Known questions information 
    """

    if not known_dir.is_dir():
        known_dir.mkdir(parents=True, exist_ok=True)

    print(f"Reading questions from file: {file_name}")
    df = pd.read_csv(filepath_or_buffer=file_name, sep='\t', names=[
                     'Question', 'Answer'], lineterminator='\n')

    old_state_df = get_old_state(file_name=file_name, known_dir=known_dir)

    if not old_state_df.empty:
        known_df = df[df.index.isin(old_state_df['Known_id'])]
        df.drop(old_state_df['Known_id'], axis=0, inplace=True)
        print(
            f"Succesfully loaded {len(df)} questions, restored {len(old_state_df)} known questions from previous runs.\n")
    else:
        known_df = pd.DataFrame(columns=df.columns)
        print(
            f"Succesfully loaded {len(df)} questions, restored 0 known questions from previous runs.\n")
    return df, known_df


def get_old_state(file_name: Path, known_dir: Path):
    """
    Method used to retrieve old state information obtained from previous executions.

    Args:
        file_name (Path): Path for questions file
        known_dir (Path): Path for old state searching dir

    Returns:
        old_state_df (pd.DataFrame): Known question information
    """

    old_state = Path.joinpath(known_dir, file_name.with_suffix('.csv').name)
    print(f"Searching for: {old_state}")

    if old_state.is_file() and old_state.stat().st_size != 0:
        return pd.read_csv(filepath_or_buffer=old_state, header=None, names=['Known_id'])
    else:
        return pd.DataFrame()


def read_and_validate_user_input():
    """
    Method responsible for managing and validating user input

    Raises:
        Exception: Custom execption to report incorrect input

    Returns:
        i (str): character with the user input action
    """

    i = input('Input (y/n/s/q):\t').lower()

    if len(i) > 1:
        raise Exception('Wrong input length provided. Please read the doc.')

    if i not in ['y', 'n', 's', 'q']:
        raise Exception('Wrong input char provided. Please read the doc.')

    return i


def store_known_questions(known_df: pd.DataFrame, file_name: Path, known_dir: Path):
    """
    Method responsible for updating the csv file of questions known to the user 
    for the purpose of being able to restore them in the next run

    Args:
        known_df (pd.DataFrame): Known questions information 
        file_name (Path): Path for questions file
        known_dir (Path): Path for old state searching dir
    """

    dest = Path.joinpath(known_dir, file_name.name)
    known_df.to_csv(dest, columns=[], header=False)


def main(file_name: Path, known_dir: Path):
    questions_df, known_df = load_questions(
        file_name=file_name, known_dir=known_dir)

    print('Type "y" to mark as known, "n" to mark as to study, "s" to show the answer or "q" to exit.')

    while True:
        if len(questions_df) <= 0:
            print("Congratulations! Deck mastered!")
            break

        random_row = questions_df.sample(n=1)
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
            known_df = known_df.append(random_row, ignore_index=False)
            questions_df.drop(random_row.index, inplace=True)
        elif i == 'n':
            pass
        elif i == 's':
            print(
                f"Answer for the current question is: {random_row['Answer'].values[0]}")
        else:
            print(f"Unknown input provided: {i}. Please read the doc")

    print(
        f"\nQuestions recap: \n\t Known: {known_df.shape[0]} \n\t Still to learn: {questions_df.shape[0]}")
    store_known_questions(known_df, file_name, known_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File path to flashcards file', type=Path)
    parser.add_argument('--store', help='File path to store known answers dir',
                        type=Path, default='./store_known/')

    args = parser.parse_args()
    main(args.file, args.store)
