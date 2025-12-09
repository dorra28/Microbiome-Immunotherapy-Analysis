import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score
from scipy.stats import wilcoxon
import joblib

def analyze_data(input_path, output_path, report_path):
    df = pd.read_csv(input_path, index_col=0)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1].map({"Responder": 1, "Non-Responder": 0})  # Binary encoding
    
    # Differential abundance (example: Wilcoxon for two groups)
    responders = X[y == 1]
    non_responders = X[y == 0]
    p_values = {col: wilcoxon(responders[col], non_responders[col]).pvalue for col in X.columns}
    
    # Train Random Forest
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred)
    cv_scores = cross_val_score(model, X, y, cv=5)
    
    # Save model
    joblib.dump(model, output_path)
    
    # Report
    with open(report_path, "w") as f:
        f.write(f"Accuracy: {acc:.2f}\nAUC: {auc:.2f}\nCV Mean: {cv_scores.mean():.2f}\n")
        f.write("Top differential features:\n")
        for feature, p in sorted(p_values.items(), key=lambda x: x[1])[:10]:
            f.write(f"{feature}: p={p:.4f}\n")
    print(f"Analysis complete. Model saved to {output_path}, report to {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze microbiome data")
    parser.add_argument("--input", required=True, help="Input processed CSV")
    parser.add_argument("--output", required=True, help="Output model path")
    parser.add_argument("--report", required=True, help="Output report path")
    args = parser.parse_args()
    analyze_data(args.input, args.output, args.report)
