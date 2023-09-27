import torch
from transformers import BertForSequenceClassification, AutoTokenizer
import torch.nn.functional as F

class SimplifiedBertClassifier:
    def __init__(self, model_path, tokenizer_path, classes, max_length=128):
        """
        Initialisiert den Classifier mit Model, Tokenizer und Klasseninformation.

        Args:
        - model_path (str): Pfad zum vortrainierten Modell.
        - tokenizer_path (str): Pfad zum zugehörigen Tokenizer.
        - classes (List[str]): Liste der Klassennamen für die Klassifikation.
        - max_length (int, optional): Maximale Sequenzlänge für den Tokenizer. Default ist 128.
        """
        self.classes = classes
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path, num_labels=len(classes))
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.max_length = max_length
        
    def predict(self, text):
        """
        Führt eine Vorhersage mit dem geladenen Modell durch und gibt die besten 4 Klassen mit ihren Wahrscheinlichkeiten zurück.

        Args:
        - text (str): Eingabetext für die Vorhersage.

        Returns:
        - tuple: (Beste Klasse, Wahrscheinlichkeit der besten Klasse, Liste der besten 4 Klassen, Liste der Wahrscheinlichkeiten der besten 4 Klassen)
        """
        self.model.eval()
        inputs = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )
        
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        with torch.no_grad():
            logits = self.model(input_ids=input_ids, attention_mask=attention_mask).logits
            probs = F.softmax(logits, dim=1)
            top4_probs, top4_indices = torch.topk(probs, 4, dim=1)
            top4_indices = top4_indices.squeeze(0).tolist()
            top4_probs = top4_probs.squeeze(0).tolist()
            top_label = self.classes[top4_indices[0]]
            top_label_prob = top4_probs[0]
            top4_labels = [self.classes[idx] for idx in top4_indices]
        
        return top_label, top_label_prob, top4_labels, top4_probs
