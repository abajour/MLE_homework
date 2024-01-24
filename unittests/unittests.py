import unittest
import pandas as pd
import os
import sys
import json
import torch
from sklearn.metrics import f1_score

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(ROOT_DIR))
CONF_FILE = os.getenv('CONF_PATH')

from training.train import DataProcessor, Training, SimpleClassifier

class TestDataProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(CONF_FILE, "r") as file:
            conf = json.load(file)
        cls.data_dir = conf['general']['data_dir']
        cls.train_path = os.path.join(cls.data_dir, conf['train']['table_name'])

    def test_data_extraction(self):
        dp = DataProcessor()
        df = dp.data_extraction(self.train_path)
        self.assertIsInstance(df, pd.DataFrame)

    def test_prepare_data(self):
        dp = DataProcessor()
        df = dp.prepare_data(100)
        self.assertEqual(df.shape[0], 100)


class TestTraining(unittest.TestCase):
    def test_train(self):
        tr = Training()
        # assume you have some prepared data
        X_train = pd.DataFrame({
            'x1': [1, 0, 1, 0],
            'x2': [1, 1, 0, 0]
        })
        y_train = pd.Series([0, 1, 1, 0])
        tr.train(X_train, y_train)
        self.assertIsNotNone(tr.model.tree_)

    def test_simple_classifier(self):
        # Assuming your SimpleClassifier takes input_size and output_size as parameters
        classifier = SimpleClassifier(input_size=2, output_size=2)
        # assuming you have some prepared data
        X_train = torch.tensor([[1, 1], [0, 1], [1, 0], [0, 0]], dtype=torch.float32)
        y_train = torch.tensor([0, 1, 1, 0])
        classifier.train(X_train, y_train)
        # assuming you have some test data
        X_test = torch.tensor([[1, 0], [0, 1]], dtype=torch.float32)
        y_pred = classifier.predict(X_test)
        self.assertIsInstance(y_pred, torch.Tensor)

if __name__ == '__main__':
    unittest.main()