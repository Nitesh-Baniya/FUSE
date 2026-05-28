# Week 4: Linear Model

## Task 1: Understand the Problem First

# 1. Formulation of the ML Problem Formally
   - The main goal of this week's task is to predict whether a customer will churn or not based on various features.

   - **Feature Space (X):**  
     The feature matrix \(X\) consists of all predictor variables except the target column `Churn`. Examples include:
     - gender
     - SeniorCitizen
     - tenure
     - MonthlyCharges
     - TotalCharges
     - Contract
     - InternetService
     - PaymentMethod
     - OnlineSecurity
     - TechSupport
     - other customer-related attributes

     These features collectively indicate customer behavior, subscription details, and service usage patterns.

   - **Target Variable (Y):**  
     The target variable is `Churn` with values:
     - `No (0)` → customer retained
     - `Yes (1)` → customer churned

   - **Probability Distribution:**  
     The target variable has two possible values, so this is a **binary classification problem**. Hence, the natural probability distribution is the **Bernoulli distribution**.

     For each customer:

     $$
     y_i \sim \text{Bernoulli}(p_i)
     $$

     where:

     $$
     p_i = \text{probability that customer } i \text{ churns}
     $$

   - **Appropriate Loss Function:**  
     Because the target variable follows a Bernoulli distribution, the most appropriate loss function is:

     **Binary Cross Entropy (Log Loss)**

     This loss function penalizes incorrect probability predictions and is commonly used in:
     - Logistic Regression
     - SGD Classifier with log loss
     - probabilistic binary classifiers

     The mathematical form of  **Binary Cross Entropy** is:

     $$
     L = -\frac{1}{N}\sum_{i=1}^{N}
     \left[
     y_i \log(\hat{p}_i)
     + (1-y_i)\log(1-\hat{p}_i)
     \right]
     $$


---
# 2. Assumptions About the Data-Generating Process

   - **Assumption 1: Observations are Independent**  
     The model assumes each customer is independent of others.

     **If Violated:**  
     If customers influence one another (family plans, shared contracts, regional effects), the model may underestimate correlations and produce overconfident predictions.

   - **Assumption 2: Training and Future Data Follow Similar Distributions**  
     The model assumes future customer behavior will resemble historical behavior.

     **If Violated:**  
     Changes in pricing, promotions, competitors, or economic conditions could cause concept drift, reducing model performance over time.

   - **Assumption 3: Features are Measured Correctly**  
     The model assumes variables such as `MonthlyCharges` and `TotalCharges` are recorded accurately.

     **If Violated:**  
     Incorrect billing values or data-entry errors may distort customer behavior patterns and create unreliable predictions.

   - **Assumption 4: Training and Deployment Data Come from the Same Distribution**  
     The model assumes future customers resemble the customers in the training dataset.

     **If Violated:**  
     If the company expands into new markets or customer segments, predictions may generalize poorly.

   - **Assumption 5: Labels are correct**
     The model assumes that the `Churn` column is accurately labeled.

     **If Violated:**
     If labels are incorrect then the model learns incorrect relationships, classification boundaries become noisy, performance metrics become misleading.
  

---
# 3. Sources of Uncertainty, Noise, and Bias

   - **Missing / Incomplete Billing Data (TotalCharges)**  
     The `TotalCharges` column contains whitespace-only entries instead of proper null values.

     These rows mostly correspond to customers with:
     - `tenure = 0`
     - newly joined customers

     This creates uncertainty because their billing history is incomplete.

     **Handling:**  
     Whitespace values were converted to `NaN` and removed because they represent only a tiny fraction of the dataset.

   - **Self-Selection Bias**  
     Customers who churn may behave differently for reasons not captured in the dataset, such as:
     - competitor promotions
     - customer satisfaction
     - network quality
     - economic factors

     These hidden variables introduce unobserved bias.

   - **Class Imbalance (Churn)**  
     Only about 27% of customers churn.

     This imbalance can cause models to favor predicting the majority class (No) and ignore minority churn cases.

   - **Potential Correlated Features**  
     `tenure`, `MonthlyCharges`, and `TotalCharges` are naturally related:

     $$
     \text{TotalCharges} \approx \text{MonthlyCharges} \times \text{tenure}
     $$

     This may introduce multicollinearity for linear models.

---

# 4. Distribution Profiling



   - ## MonthlyCharges  
     `MonthlyCharges` is roughly continuous and near-symmetric, with a slight left skew. In practice, it often looks bimodal or mildly multi-peaked, because customers tend to fall into pricing groups (basic plans vs premium/bundled services). So it is not perfectly normal, but it is fairly well-behaved and does not show extreme skewness.

     ```python
        df['MonthlyCharges'].skew()
        # np.float64(-0.22210292770166232) 
     ```
     ![MonthlyCharges distribution](images/distro_MonthlyCharges.png)

     **Suspicious Values:**  
     - No impossible negative values should exist  

     **Handling:**  
     - Keep all values because they are valid business outcomes  

   - ### tenure
     `tenure` follows a discrete, mildly right-skewed distribution. Many customers are concentrated at lower tenure values (new customers), while fewer customers have very high tenure (long-term customers). It is not continuous in the strict sense because tenure is recorded in integer months, but its overall shape is closer to a decaying distribution than a normal one.

     ```python
        df['tenure'].skew()
        # np.float64(0.23773083190513133)
     ```
     ![tenure distribution](images/distro_tenure.png)

     **Suspicious Values:**  
     - Customers with `tenure = 0` deserve inspection because some have missing `TotalCharges`  

     **Handling:**  
     - Keep valid tenure values but investigate zero-tenure records  

   - ## TotalCharges
     `TotalCharges` is strongly right-skewed and continuous, with a long tail of high values. This happens because it accumulates over time:
    $$
        TotalCharges≈MonthlyCharges×tenure
    $$
So customers with long tenure naturally create very large values, producing a heavy right tail.

     ```python
        df['TotalCharges'].skew()
        # np.float64(0.9616424997242504)
     ``` 
     ![TotalCharges distribution](images/distro_TotalCharges.png)

     **Suspicious Values:**  
     - Whitespace entries and missing values exist  

     **Handling:**  
     - Convert to numeric, coerce invalid entries to NaN, and remove affected rows  

     **Example cleaning step:**
     ```python
     df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
     ```
     ![TotalCharges datatype change](images/totalcharges_dtype_change.png)



---

# 5. Naive Baseline Model

A naive baseline predicts the majority class for every customer.

Since approximately 73% of customers do not churn:

$$
\text{baseline accuracy} = 0.73
$$

So the naive model achieves roughly **73% accuracy**.

![naive model accuracy](images/model_naive.png)

---

### Why This Accuracy is Misleading

Even though 73% sounds good, the model is actually not learning anything. It is just exploiting class imbalance.

The problem is that it predicts everyone will NOT churn. sS it is correct for the 73% who don’t churn but it completely ignores the 27% who do churn

So, the naive model has high accuracy but poor real usefulness failing to identify actual churners.

---

### Why This Model is Dangerous

 1. **It fails the main business goal**

In churn prediction, the primary objective is to identify customers who are likely to leave. However, this naive model completely fails at that goal because it always predicts the majority class (non-churn). As a result, it detects **0% of churners**, meaning the recall for the churn class is **0**. This is critical because every at-risk customer is missed, making the model useless for any retention strategy.

---

2. **False sense of performance**

Although the model achieves around **73% accuracy**, this is misleading. The high score does not reflect real predictive ability; instead, it simply comes from always predicting that customers will stay. In reality, this is equivalent to a naive rule such as “everyone stays.” The model has no learning or discrimination power between churners and non-churners, despite appearing effective based on accuracy alone.

---

3. **Business impact risk**

If this model were used in a real business setting, it could lead to serious negative consequences. Since it never identifies churners, no retention actions would ever be triggered for at-risk customers. This means companies would continue losing customers without warning or intervention. Over time, this silent failure can result in significant revenue loss and reduced customer lifetime value.

---

4. **Metric deception in imbalanced data**

Accuracy becomes unreliable when classes are imbalanced because it is dominated by the majority class. In this case, the model’s accuracy is essentially:

$$
\text{Accuracy} = \frac{5163}{5163 + 1869} \approx 0.734
$$

This shows that the score mainly reflects the distribution of the dataset rather than the model’s actual predictive quality. Therefore, high accuracy does not imply good performance, especially when the minority class (churners) is the most important to detect.

Therefore, metrics such as:
- `Precision`  
- `Recall`
- `F1-score`  
- `ROC-AUC`  

are more informative than accuracy alone.