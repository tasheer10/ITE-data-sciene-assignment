# Data Science Assignment: Visitor-Exhibitor Matching & Insights

## Objective
You are given data from a large-scale corporate event where visitors register by answering questions, and exhibitors register by selecting categories relevant to their business. Your task is to process and analyze the data to derive meaningful insights and develop a visitor-exhibitor matchmaking system.

## Dataset Overview

### 1. Visitors (`visitors.csv`)
- `email`: Unique email identifier for visitors.
- `gender` : Visitor Gender
- `id` : Unique registration Id
- `data`: JSON data of answers selected during registration.

### 2. Answers (`answers.csv`)
- `id`: Unique identifier for an answer.
- `questionid`: The ID of the question this answer belongs to.
- `answer`: The text of the selected answer.

### 3. Questions (`questions.csv`)
- `questionid`: Unique identifier for a question.
- `questionTypeId` : Unique identifier for a question Type
- `Step Id` : Unique identifier for a question Step
- `question`: The text of the question.

### 4. Exhibitor Categories (`exhibitor_categories.csv`)
- `categoryId`: Unique identifier for an exhibitor category.
- `categoryName`: Description of the category.

### 5. Exhibitors (`exhibitors.csv`)
- `exhibitorID`: Unique identifier for an exhibitor.
- `Name` : Exhibitor Name
- `MainCategories`: Pipe-separated (`|`) list of categories selected by the exhibitor.

---

## Tasks

### 1. Data Cleaning & Processing

### 2. Visitor Profile Analysis
- Kindly mention a heading with details for all the analysis 


### 3. Exhibitor Profile Analysis
- Kindly mention a heading with details for all the analysis


### 4. Visitor-Exhibitor Matching Model
- Develop a **visitor-exhibitor recommendation model** based on common interests:
  - Map visitor answers to exhibitor categories (e.g., a visitor answering "I am looking for travel services" should match an exhibitor under "Travel").
  - Create a **scoring system** to rank exhibitor matches provided visitor Email, Suggest top **7 exhibitors** for provided visitor
  - Create a **scoring system** to rank visitors matches for each exhibitor, Suggest top **7 visitors** for provided exhibitor

- Mostly, the Exhibitor selects all the available categories, this might create issues for the recommendations, kindly create a logic to penalize such exhibitors while recommending them to the visitors

### 5. Data Visualization

### 6. Test Cases
- Kindly create the Unit tests for the methods created

### 7. Advanced Insights (Bonus)
- **Predictive Analysis**: Based on visitor preferences, predict what new categories should be introduced for exhibitors.
- **Cluster Analysis**: Segment visitors into different groups based on their answers and analyze their distinct characteristics.

---

## Expected Deliverables
- A **Jupyter Notebook/Python script** with all analysis and code.
- A **short presentation (PPT or PDF)** summarizing key insights and recommendations.

---

This assignment will test your ability to handle **data wrangling, EDA, recommendation models, and visualization**. Good luck! 🚀

