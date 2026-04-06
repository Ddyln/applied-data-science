# OmniRouter — Problem Breakdown

## Goal

Understand the routing problem before introducing the solution.

---

## 1. Problem Setup

We are given:

- \( N \) queries
- \( M \) language models

Each query must be assigned to exactly one model.

---

## 2. Decision Variable

$$
x_{i,j} =
\begin{cases}
1 & \text{if query } i \text{ is assigned to model } j \\
0 & \text{otherwise}
\end{cases}
$$

$$
x_{i,j} \in \{0,1\}
$$

---

## 3. Key Quantities

### Capability (Quality)

$$
a_{i,j} \in [0,1]
$$

- Measures how likely model \( j \) can correctly answer query \( i \)

---

### Cost

$$
c_{i,j}
$$

- Cost of assigning query \( i \) to model \( j \)
- Usually proportional to output length and model pricing

---

## 4. Objective

Minimize total cost:

$$
\min_{x} \sum_{i=1}^{N} \sum_{j=1}^{M} c_{i,j} x_{i,j}
$$

---

## 5. Constraints

### 5.1 Assignment Constraint

Each query must be assigned to exactly one model:

$$
\sum_{j=1}^{M} x_{i,j} = 1, \quad \forall i
$$

---

### 5.2 Quality Constraint

Average performance must exceed a threshold:

$$
\frac{1}{N} \sum_{i=1}^{N} \sum_{j=1}^{M} a_{i,j} x_{i,j} \ge \alpha
$$

- \( \alpha \): required performance level

---

### 5.3 Capacity Constraint

Each model has limited capacity:

$$
\sum_{i=1}^{N} x_{i,j} \le L_j, \quad \forall j
$$

- \( L_j \): maximum number of queries model \( j \) can handle

---

## 6. Full Optimization Problem

$$
\begin{aligned}
\min_{x} \quad & \sum_{i=1}^{N} \sum_{j=1}^{M} c_{i,j} x_{i,j} \\
\text{s.t.} \quad 
& \sum_{j=1}^{M} x_{i,j} = 1, && \forall i \\
& \frac{1}{N} \sum_{i=1}^{N} \sum_{j=1}^{M} a_{i,j} x_{i,j} \ge \alpha \\
& \sum_{i=1}^{N} x_{i,j} \le L_j, && \forall j \\
& x_{i,j} \in \{0,1\}
\end{aligned}
$$

---

## 7. Why This Problem Is Hard

### Combinatorial Explosion

Number of possible assignments:

$$
M^N
$$

- Example: 10 queries, 3 models → \( 3^{10} = 59049 \)

---

### Discrete Optimization

- Binary variables \( x_{i,j} \)
- Cannot solve directly with simple gradient methods

---

### Conflicting Objectives

- Cheap models → low cost but poor quality  
- Strong models → high quality but expensive  

---

## 8. Greedy Approach (Baseline)

### Strategy

For each query \( i \):

$$
j^* = \arg\min_j c_{i,j}
$$

or

$$
j^* = \arg\max_j a_{i,j}
$$

---

### Problem

- Ignores global constraints
- Can violate:
  - capacity
  - overall quality

---

## 9. Failure Example

### Scenario

- Query 1: easy  
- Query 2: hard  

### Greedy decision

- Assign easy query → strong model  
- Assign hard query → weak model  

### Result

- Hard query fails  
- Global performance drops  

---

## 10. Key Insight

Greedy optimization:

$$
\text{optimize each } i \text{ independently}
$$

OmniRouter:

$$
\text{optimize all } x_{i,j} \text{ jointly}
$$

---

## 11. Reformulation Idea

Instead of:

- independent decisions

We solve:

$$
\text{global constrained optimization}
$$

---

## 12. Bridge to Next Step

### Problem

We don’t know:

$$
a_{i,j}, \quad c_{i,j}
$$

### Solution

- Estimate them using a predictor
- Then solve optimization

---

## Key Takeaway

Routing is not just selection.  
It is a **global assignment problem under constraints**.

$$
\text{Minimize cost} \quad \text{subject to quality and capacity}
$$