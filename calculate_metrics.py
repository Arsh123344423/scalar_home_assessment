import json
from collections import defaultdict

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_key(entity):
    """Normalize for comparison: lowercase text + type"""
    text = entity['text'].strip().lower()
    entity_type = entity.get('type', '').upper()
    return (text, entity_type)

def calculate_metrics(ground_truth_path, predicted_path):
    gt = load_json(ground_truth_path)
    pred = load_json(predicted_path)
    
    gt_set = {normalize_key(e) for e in gt}
    pred_set = {normalize_key(e) for e in pred}
    
    true_positives = len(gt_set & pred_set)
    false_positives = len(pred_set - gt_set)
    false_negatives = len(gt_set - pred_set)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    # Print Results
    print("=== PII Detection Metrics ===\n")
    print(f"Ground Truth Entities : {len(gt_set)}")
    print(f"Predicted Entities    : {len(pred_set)}")
    print(f"True Positives (TP)   : {true_positives}")
    print(f"False Positives (FP)  : {false_positives}")
    print(f"False Negatives (FN)  : {false_negatives}")
    print("-" * 40)
    print(f"Precision             : {precision:.4f} ({precision*100:.2f}%)")
    print(f"Recall                : {recall:.4f} ({recall*100:.2f}%)")
    print(f"F1-Score              : {f1:.4f} ({f1*100:.2f}%)")
    
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tp": true_positives,
        "fp": false_positives,
        "fn": false_negatives
    }
if __name__ == "__main__":
    # Change these filenames as needed
    gt_path = "ground_truth.json"
    pred_path = "predicted.json"
    
    metrics = calculate_metrics(gt_path, pred_path)