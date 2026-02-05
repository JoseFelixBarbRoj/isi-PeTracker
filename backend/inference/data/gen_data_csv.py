from pathlib import Path
import pandas as pd
import cv2
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    
    DATASET_PATH = Path(__file__).parent

    image_data = []

    for file in DATASET_PATH.rglob('*.png'):
        image = cv2.imread(file)
        image_class = str(file.parent.name)
        image_data.append((file.stem, Path(image_class) / file.name, 'train', image.shape[0], image.shape[1], image_class))

    initial_df = pd.DataFrame(image_data, columns=['id', 'path', 'partition', 'height', 'width', 'class'])

    x = initial_df[initial_df['partition'] == 'train']
    train, val = train_test_split(x, test_size=0.1)
    train = pd.DataFrame(train)
    val = pd.DataFrame(val).sort_index()

    initial_df.loc[val.index, 'partition'] = 'val'

    x = initial_df[initial_df['partition'] == 'train']
    train, test = train_test_split(x, test_size=0.1/0.9) # Para tener 80 10 10 en train val test
    train = pd.DataFrame(train)
    test = pd.DataFrame(test).sort_index()

    initial_df.loc[test.index, 'partition'] = 'test'
    print(initial_df['partition'].value_counts())
    initial_df.to_csv(DATASET_PATH / 'data.csv', index=False)