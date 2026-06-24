# Product Requirement Document (PRD)

## Project Name: Minimalist Spam Detection System

**Version:** 1.0

**Status:** Draft

---

## 1. Executive Summary & Objective

The objective is to build a lightweight, high-performance, and minimal **Spam Detection System**. Instead of relying on complex, resource-heavy architectures, this system focuses on a clean, core set of lexical and text-based features to classify messages as either **Spam** or **Ham (Legitimate)**.

The primary goal is to achieve high precision and recall using traditional Machine Learning (ML) techniques, making it easy to deploy, maintain, and integrate into existing messaging or email pipelines.

---

## 2. Core Features (Minimum Viable Product)

To keep the system minimal yet highly effective, the feature engineering pipeline will restrict itself to the following five critical signals:

### Feature Matrix

| Feature ID | Feature Name | Data Type | Description |
| --- | --- | --- | --- |
| **FEAT-01** | `message_length` | Integer | Total character count of the message. (Spam tends to skew very short or maximum length). |
| **FEAT-02** | `caps_ratio` | Float | The ratio of uppercase characters to total characters (`0.0` to `1.0`). |
| **FEAT-03** | `contains_currency_symbol` | Binary | `1` if symbols like `$`, `€`, `£`, or `₹` are present; `0` otherwise. |
| **FEAT-04** | `contains_suspicious_url` | Binary | `1` if the text contains a hyperlink or common URL shortener domain; `0` otherwise. |
| **FEAT-05** | `tfidf_top_words` | Matrix (Float) | A small, localized TF-IDF vector mapping the frequency of the top 100 most common spam keywords (e.g., *free, click, claim, urgent*). |

---

## 3. System Architecture & Workflow

The system will operate as a synchronous pipeline:

```
[ Raw Message Input ] 
         │
         ▼
[ Feature Extraction Pipeline ] ──► (Length, Caps, Currency, URL, TF-IDF)
         │
         ▼
[ ML Classifier Model ] ──────────► (e.g., Naive Bayes / Logistic Regression)
         │
         ▼
[ Classification Output ] ────────► JSON: { "is_spam": true/false, "confidence": float }
```

### Functional Requirements

* **Input Format:** The system must accept a raw string text (SMS or Email body).
* **Processing Time:** Feature extraction and model inference must take less than **100ms** per message.
* **Classification Output:** The system must return a binary classification (`1` for Spam, `0` for Ham) alongside a confidence score between `0.0` and `1.0`.

---

## 4. Technology Stack (Proposed)

* **Language:** Python 3.x
* **Data Manipulation:** `pandas`, `numpy`
* **Machine Learning & NLP:** `scikit-learn` (for TF-IDF vectorization and classification algorithms like Multinomial Naive Bayes or Logistic Regression).
* **Deployment (Optional):** Flask or FastAPI for a minimal REST API endpoint.

---

## 5. Success Metrics & Performance Indicators

To ensure the minimal feature set is sufficient, the model must meet the following baseline evaluation metrics during testing:

* **Accuracy:** $\ge 95\%$
* **Precision:** $\ge 97\%$ (Crucial, as marking a legitimate message as spam—a false positive—is highly disruptive to users).
* **Recall:** $\ge 90\%$

---
