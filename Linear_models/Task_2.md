# Week 4: Linear Model

## Task 2 Classification Experiment Who Will Churn?

**Model Comparison**
```python
    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            random_state=42
        ),
    
        "Ridge Classifier": RidgeClassifier(),
    
        "SGD Classifier": SGDClassifier(
            loss='log_loss',
            max_iter=1000,
            random_state=42
        )
    }
    
    results = []
    
    for name, model in models.items():
    
        print(f"\nTraining {name}...")
    
        start_time = time.time()
    
        model.fit(X_train_scaled, y_train)
    
        end_time = time.time()
    
        training_time = end_time - start_time
    
        y_pred = model.predict(X_val_scaled)
    
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_val_scaled)[:, 1]
    
        else:
            y_prob = model.decision_function(X_val_scaled)
    
        accuracy = accuracy_score(y_val, y_pred)
    
        precision = precision_score(y_val, y_pred)
    
        recall = recall_score(y_val, y_pred)
    
        f1 = f1_score(y_val, y_pred)
    
        roc_auc = roc_auc_score(y_val, y_prob)
    
        pr_auc = average_precision_score(y_val, y_prob)
    
        if hasattr(model, "predict_proba"):
            ll = log_loss(y_val, y_prob)
        else:
            ll = np.nan
    
        results.append({
            "Model": name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1,
            "ROC-AUC": roc_auc,
            "PR-AUC": pr_auc,
            "Log Loss": ll,
            "Training Time (sec)": training_time
        })
    
    results_df = pd.DataFrame(results)
    
    print("\nModel Comparison")
    
    print(results_df.sort_values(
        by="F1 Score",
        ascending=False
    ))
```

![Comparison of different models](images/models_comparison.png)

### Important Evaluation Metrics for Churn Prediction

---

1. **Recall (Most Important for Churn Prediction)**

Recall measures how many actual churn customers the model successfully identifies.

 **Formula**

$$
\text{Recall} = \frac{TP}{TP + FN}
$$

Where:

- **TP (True Positives)** = Correctly predicted churn customers
- **FN (False Negatives)** = Actual churn customers predicted as non-churn


In churn prediction, missing a customer who is about to leave can be very costly for the business.


Suppose:
- A customer is actually going to churn
- The model predicts that the customer will stay

This customer becomes a **False Negative (FN)**.

As a result:
- The company fails to take preventive action
- The customer leaves permanently
- Revenue and customer retention decrease

Therefore, recall is important because it measures how well the model avoids missing actual churners.

---
The **SGD Classifier** achieved the highest recall, meaning it identified the largest number of churn customers.

---

2. **F1-Score (Best Balance Metric)**

F1-score balances both **Precision** and **Recall** into a single metric.

**Formula**

$$
F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}
$$


A model with:
- **High recall but low precision** identifies many churners but also produces many false alarms.
- **High precision but low recall** makes fewer false alarms but misses many actual churners.

F1-score provides a balanced evaluation between these two metrics.



Suppose a company targets customers predicted as churners.

**Scenario 1: High Recall, Low Precision**
- The model flags many customers as churners
- Many of them are actually loyal customers

Result:
- The company wastes marketing resources and retention offers

**Scenario 2: High Precision, Low Recall**
- The model only flags a few customers
- Many real churners are missed

Result:
- Customers leave without intervention

Therefore, F1-score helps evaluate the balance between identifying churners and avoiding unnecessary costs.

---

Both **SGD Classifier** and **Logistic Regression** achieved the best balanced performance.

---

3. **PR-AUC — Important for Imbalanced Data**

PR-AUC (Precision-Recall Area Under Curve) evaluates how well the model performs on the positive class, which is the churn class.


Churn datasets are usually highly imbalanced:
- Most customers do **not** churn
- Only a small percentage actually churn

In such cases:
- Accuracy can be misleading
- PR-AUC gives a more realistic evaluation of churn detection performance


Suppose:
- 90% customers stay
- 10% customers churn

A model predicting everyone as "non-churn" would still achieve 90% accuracy.

However:
- It would completely fail to detect churners

PR-AUC focuses specifically on the model’s ability to identify churn customers correctly.

---

The **Logistic Regression** model achieved the best PR-AUC score, indicating stronger performance on the minority churn class.

---

4. **ROC-AUC — Measures Ranking Ability**

ROC-AUC measures how well the model separates churners from non-churners.

A higher ROC-AUC means:
- Churn customers generally receive higher risk scores than non-churn customers
- The model has strong discriminative ability

If two customers are selected randomly:
- One churner
- One non-churner

ROC-AUC measures the probability that the model assigns a higher churn probability to the actual churn customer.

---

All three models achieved strong ROC-AUC scores above 0.84, indicating good separation capability.

---

5. **Accuracy — Least Important Metric**

Accuracy measures the proportion of total correct predictions.

**Formula**

$$
\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
$$

Where:
- **TN (True Negatives)** = Correctly predicted non-churn customers
- **FP (False Positives)** = Non-churn customers predicted as churn


Suppose:
- 90% customers do not churn
- 10% customers churn

If a model predicts:
- Every customer as "non-churn"

Then:
- Accuracy = 90%
- Recall = 0%

Even though accuracy appears very high, the model completely fails to identify churn customers.

Therefore, accuracy alone is not reliable for churn prediction.

---

### Final Recommendation

If the Business Goal Is: **Detecting as Many Churners as Possible**

Then **Recall** should be prioritized.

**Recommended Model:** SGD Classifier

Because it achieved the highest recall score.

---

If the Business Goal is **Balanced Overall Performance**

Then **F1-Score** and **PR-AUC** should be prioritized.

**Recommended Model:** Logistic Regression

Because it achieved:
- Strong F1-score
- Highest PR-AUC
- Best ROC-AUC
- Lowest Log Loss

---

<div style="
    background-color: #F5D327;
    color: black;
    padding: 2px;
    font-size: 16px;
    line-height: 1.6;
">
Since churn prediction is an imbalanced classification problem, accuracy alone is not sufficient to evaluate model performance. In most churn datasets, the number of customers who do not churn is much larger than the number of customers who actually churn. As a result, a model can achieve high accuracy simply by predicting most customers as non-churners, even if it fails to identify actual churn cases. Therefore, metrics such as recall, precision, F1-score, PR-AUC, and ROC-AUC are more important because they provide a better understanding of how effectively the model identifies customers who are likely to churn. In churn prediction, detecting potential churners is critical for businesses because missing these customers may lead to revenue loss and reduced customer retention.
</div>

---


### Which Model Performed Best?
Best Overall Model: **Logistic Regression**

**Why?**

Although **SGD** achieved slightly higher recall, **Logistic Regression** achieved highest accuracy, highest precision, highest ROC-AUC, highest PR-AUC, lowest log loss.

Most importantly, it produced calibrated probabilities, remained highly interpretable, and maintained balanced performance across all metrics.

Its F1-score was essentially tied with SGDClassifier.

---


### Questions on the notebook

1. **Why Your Manager Should NOT Be Excited About 73% Accuracy**

A 73% accuracy score is misleading because the dataset is imbalanced, with approximately 73% non-churn customers and only 27% churn customers. A model can achieve 73% accuracy simply by predicting “No Churn” for every customer while completely failing to identify actual churners. The first question to ask is: “What is the recall for churn customers?” because the business objective is to identify customers likely to leave, not merely maximize overall accuracy.

2. **Why Stratified Splitting?**

Stratified splitting ensures that the proportion of churn and non-churn customers remains approximately consistent across the training, validation, and test sets. Since churn prediction is an imbalanced classification problem, stratification prevents situations where one split contains very few churn customers, which would produce unreliable evaluation metrics.


If your full dataset has:

- 73% class 0  
- 27% class 1  

Then a **stratified split** ensures:

- Train set ≈ 73% class 0 / 27% class 1  
- Test set ≈ 73% class 0 / 27% class 1  

So both sets look like a **mini version of the original dataset**, preserving the same class distribution.

3. **Why Fit Scaler Only on Training Data?**

The scaler is fitted only on the training data to prevent data leakage. If scaling parameters such as mean and standard deviation were computed using validation or test data, information from unseen data would indirectly influence the model training process, leading to overly optimistic evaluation results.

4. **What Happens If You Scale Before Splitting?**

Scaling before splitting causes data leakage because the scaling transformation uses statistical information from the entire dataset, including validation and test samples. This leaks future information into the training process and artificially inflates model performance.