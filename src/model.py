import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import mlflow
import mlflow.sklearn
from src.preprocessing import normalize_text

class TransactionClassifier:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(preprocessor=normalize_text)),
            ('clf', LogisticRegression(class_weight='balanced', max_iter=1000))
        ])
        
    def train(self, data_path="data/transactions.csv", test_size=0.2):
        df = pd.read_csv(data_path)
        X = df['description']
        y = df['category']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        mlflow.set_experiment("Transaction_Categorization")
        
        with mlflow.start_run():
            print("Training model...")
            self.pipeline.fit(X_train, y_train)
            
            print("Evaluating model...")
            y_pred = self.pipeline.predict(X_test)
            report = classification_report(y_test, y_pred, output_dict=True)
            
            # Log metrics
            mlflow.log_metric("accuracy", report["accuracy"])
            mlflow.log_metric("macro_f1", report["macro avg"]["f1-score"])
            
            # Confusion Matrix
            from sklearn.metrics import confusion_matrix
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            cm = confusion_matrix(y_test, y_pred)
            plt.figure(figsize=(10, 8))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=self.pipeline.classes_, yticklabels=self.pipeline.classes_)
            plt.title('Confusion Matrix')
            plt.ylabel('Actual')
            plt.xlabel('Predicted')
            plt.tight_layout()
            plt.savefig('confusion_matrix.png')
            mlflow.log_artifact('confusion_matrix.png')
            
            # Log model
            mlflow.sklearn.log_model(self.pipeline, "model")
            
            print(f"Accuracy: {report['accuracy']:.4f}")
            print(f"Macro F1: {report['macro avg']['f1-score']:.4f}")
            print("\nDetailed Report:")
            print(classification_report(y_test, y_pred))
            
    def save_model(self, path="models/model.pkl"):
        with open(path, 'wb') as f:
            pickle.dump(self.pipeline, f)
            
    def load_model(self, path="models/model.pkl"):
        with open(path, 'rb') as f:
            self.pipeline = pickle.load(f)
            
    def predict(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        
        probs = self.pipeline.predict_proba(texts)
        preds = self.pipeline.predict(texts)
        
        results = []
        for pred, prob in zip(preds, probs):
            confidence = max(prob)
            results.append({"category": pred, "confidence": float(confidence)})
            
        return results

if __name__ == "__main__":
    import os
    os.makedirs("models", exist_ok=True)
    clf = TransactionClassifier()
    clf.train()
    clf.save_model()
