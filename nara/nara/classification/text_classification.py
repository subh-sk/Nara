from nara.llm.check_and_install import check_and_install
check_and_install('sentence_transformers')
check_and_install('sklearn')

from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import pickle
import os


        
def cosine_similarity(A: np.ndarray, B: np.ndarray) -> float:
    """
    Calculate the cosine similarity between two vectors.

    :param A: First vector (numpy array).
    :param B: Second vector (numpy array).
    :return: Cosine similarity score between A and B.
    """
    # Compute dot product of vectors A and B
    dot_product = np.dot(A.flatten(), B.flatten())
    
    # Compute L2 norms (magnitudes) of A and B
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    
    # Compute cosine similarity
    return dot_product / (norm_A * norm_B)


class TextClassifier:
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L12-v2'):
        """
        Initialize the TextClassifier with a specified sentence transformer model.

        :param model_name: Name of the pre-trained sentence transformer model.
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.label_prototypes: dict[str, np.ndarray] = {}

        

    def loadData(self, file_path: str, text_column: str = 'Examples', label_column: str = 'Labels') -> tuple[list[str], list[str]]:
        """
        Load data from a CSV file.

        :param file_path: Path to the CSV file containing text examples and labels.
        :param text_column: Name of the column containing text examples.
        :param label_column: Name of the column containing labels.
        :return: A tuple of lists containing sentences and labels.
        """
        data = pd.read_csv(file_path)
        sentences = data[text_column].tolist()
        labels = data[label_column].tolist()
        return sentences, labels

    def eqloadData(self, file_path: str, text_column: str = 'Examples', label_column: str = 'Labels') -> tuple[list[str], list[str]]:
        """
        Load data from a CSV file and downsample to balance classes.

        :param file_path: Path to the CSV file containing text examples and labels.
        :param text_column: Name of the column containing text examples.
        :param label_column: Name of the column containing labels.
        :return: A tuple of lists containing downsampled sentences and labels.
        """
        # Load the dataset
        data = pd.read_csv(file_path)
        
        # Find the minimum count of examples for any label
        min_count = data[label_column].value_counts().min()
        
        # Downsample each group to match the size of the minority label
        downsampled_data = pd.concat([
            group.sample(n=min_count, random_state=42)  # Downsample to min_count
            for label, group in data.groupby(label_column)
        ])
        
        # Shuffle the downsampled data to mix examples from different labels
        downsampled_data = downsampled_data.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Extract the sentences and labels
        sentences = downsampled_data[text_column].tolist()
        labels = downsampled_data[label_column].tolist()
        
        return sentences, labels
    
    def createPrototypes(self, sentences: list[str], labels: list[str]) -> None:
        """
        Create prototypes for each label by averaging the embeddings of their examples.

        :param sentences: List of text examples.
        :param labels: List of corresponding labels.
        """
        embeddings = self.model.encode(sentences)
        for label in set(labels):
            label_embeddings = embeddings[np.array(labels) == label]
            self.label_prototypes[label] = np.mean(label_embeddings, axis=0)

    def classify(self, new_example: str) -> str:
        """
        Classify a new example based on the cosine similarity to label prototypes.

        :param new_example: The new text input to classify.
        :return: The predicted label for the new example.
        """
        new_embedding = self.model.encode([new_example])
        similarities = {
            label: cosine_similarity(new_embedding, prototype)
            for label, prototype in self.label_prototypes.items()
        }
        predicted_label = max(similarities, key=similarities.get)
        return predicted_label
    
    def advanceClassify(self, new_example: str) -> tuple[str, dict[str, float]]:
        """
        Classify the new example and return the predicted label along with distances
        (cosine similarities) for all labels.

        :param new_example: The new text input to classify.
        :return: A tuple containing the predicted label and a dictionary with the
                 cosine similarity scores for all labels.
        """
        # Encode the new example into an embedding
        new_embedding = self.model.encode([new_example])
        
        # Calculate the cosine similarity for all label prototypes
        similarities = {
            label: cosine_similarity(new_embedding, prototype)
            for label, prototype in self.label_prototypes.items()
        }
        
        # Find the label with the highest cosine similarity
        predicted_label = max(similarities, key=similarities.get)
        
        # Return the predicted label and all similarity scores (distances)
        return predicted_label, similarities

    def saveModel(self, file_path: str = 'text_classifier_model.pkl') -> None:
        """
        Save the trained model and label prototypes to a file.

        :param file_path: Path to the file where the model will be saved.
        """
        with open(file_path, 'wb') as f:
            pickle.dump({
                'model_name': self.model_name,
                'label_prototypes': self.label_prototypes
            }, f)
        print(f'Model saved to {file_path}')

    def loadModel(self, file_path: str = 'text_classifier_model.pkl') -> None:
        """
        Load a trained model and label prototypes from a file.

        :param file_path: Path to the file from which the model will be loaded.
        :raises FileNotFoundError: If the specified file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            self.model_name = data['model_name']
            self.model = SentenceTransformer(self.model_name)
            self.label_prototypes = data['label_prototypes']

        print(f'Model loaded from {file_path}')


# Example usage:
if __name__ == "__main__":
    from rich import print
    classifier = TextClassifier()
    sentences, labels = classifier.loadData(r'data/test/data.csv', text_column='Examples', label_column='Labels')
    classifier.createPrototypes(sentences, labels)
    classifier.saveModel('trained_text_classifier.pkl')
    # classifier.loadModel('trained_text_classifier.pkl')
    
    while True:
        new_example = input("Enter a new example: ")
        predicted_label = classifier.advanceClassify(new_example)
        print(f"The predicted label for the new example is: {predicted_label}")
