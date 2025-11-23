import shap
import pickle
import pandas as pd
from src.preprocessing import normalize_text

class Explainer:
    def __init__(self, model_path="models/model.pkl"):
        with open(model_path, 'rb') as f:
            self.pipeline = pickle.load(f)
            
        self.vectorizer = self.pipeline.named_steps['tfidf']
        self.classifier = self.pipeline.named_steps['clf']
        
    def explain(self, text):
        # Create a masker for text
        masker = shap.maskers.Text(r"\W+")
        
        # Create the explainer
        # We need to pass the prediction function that takes raw text
        # But SHAP for linear models usually works better with the coefficients directly
        # For simplicity in this demo, we'll use the linear explainer on the transformed features
        # Or we can use the generic Explainer which might be slower but easier to setup
        
        # Let's use the Linear explainer on the coefficients and feature names
        # We need to transform the text first
        
        clean_text = normalize_text(text)
        features = self.vectorizer.transform([clean_text])
        
        explainer = shap.LinearExplainer(
            self.classifier, 
            self.vectorizer.transform([" "]), # Background sample
            feature_perturbation="interventional"
        )
        
        shap_values = explainer.shap_values(features)
        
        # Map indices back to words
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Since it's multiclass, shap_values is a list of arrays OR a 3D array
        # We need to find the predicted class
        prediction = self.classifier.predict(features)[0]
        classes = self.classifier.classes_
        class_idx = list(classes).index(prediction)
        
        if isinstance(shap_values, list):
            class_shap_values = shap_values[class_idx]
            # class_shap_values is (n_samples, n_features)
            get_score = lambda idx: class_shap_values[0, idx]
        elif len(shap_values.shape) == 3:
            # (n_samples, n_features, n_classes)
            class_shap_values = shap_values[0, :, class_idx]
            # class_shap_values is (n_features,)
            get_score = lambda idx: class_shap_values[idx]
        else:
            # Fallback or binary case (n_samples, n_features)
            class_shap_values = shap_values
            get_score = lambda idx: class_shap_values[0, idx]
        
        # Get non-zero indices
        import numpy as np
        indices = features.nonzero()[1]
        
        explanation = []
        for idx in indices:
            word = feature_names[idx]
            score = get_score(idx)
            explanation.append({"word": word, "score": float(score)})
            
        return sorted(explanation, key=lambda x: x["score"], reverse=True)

if __name__ == "__main__":
    # Test
    exp = Explainer()
    print(exp.explain("STARBUCKS COFFEE NY"))
