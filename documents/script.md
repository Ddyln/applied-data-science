# OmniRouter Manim Video Script

## Title
OmniRouter: Smarter Routing for Multiple LLMs

---

## Overview

- Duration: 10–20 minutes  
- Style: 3Blue1Brown (visual + intuition + math)  
- Goal: Explain OmniRouter clearly with animation and formulation  

---

## Scene 1 — Hook: Too Many LLMs

### Voiceover
Today, we don’t just use one large language model.  
We use many. Some are fast, some are smart, and some are expensive.

### Visual
- Show 2 models: small, large  
- Queries flowing into system  

---

## Scene 2 — What is Routing?

### Voiceover
For every incoming query, the system must decide:  
which model should answer it?

### Visual
- Example queries:
  - Easy: x² − 1 = 0  
  - Hard: Build a website  
- Arrows from queries to models  

---

## Scene 3 — Greedy Routing (Problem)

### Voiceover
Most systems make decisions one query at a time.  
This is called greedy routing.

### Visual
1. Easy query arrives first → assigned to strong model  
2. Hard query arrives → only weak model left → fails  

### Key Message
Local decisions can lead to global failure  

---

## Scene 4 — OmniRouter Idea

### Voiceover
Instead, we plan assignments jointly across all queries.
We optimize globally under constraints, not one query at a time.

### Visual
1. Start from the greedy (bad) assignment from Scene 3:
  - Easy → strong
  - Hard → weak
2. Show a transition note: "Plan jointly across all queries under constraints"
3. Transform arrows into OmniRouter assignment:
  - Easy → weak
  - Hard → strong
4. Final text: "Joint assignment improves overall success"

### Key Message
Global constrained optimization beats greedy local decisions

---

## Scene 5 — Problem Formulation

### Voiceover
We formalize routing as a constrained optimization problem.
Now read this in plain language, one piece at a time.

### Definitions

$$
x_{i,j} =
\begin{cases}
1 & \text{if query } i \text{ is assigned to model } j \\
0 & \text{otherwise}
\end{cases}
$$

$$
a_{i,j} \in [0,1] \text{ denote the capability model } j \text{ can successfully answer query } i
$$

$$
c_{i,j} \text{ denote the money cost for answering this query }
$$

---

### Objective

$$
\min_{x} \sum_{i=1}^{N} \sum_{j=1}^{M} c_{i,j} x_{i,j}
$$

Meaning: minimize total routing cost.

---

### Constraints

Reveal order in video:
1. Assignment first: one model per query
2. Capacity next: each model has limited concurrency
3. Quality last: global success target must be met

Quality constraint:

$$
\frac{1}{N} \sum_{i=1}^{N} \sum_{j=1}^{M} a_{i,j} x_{i,j} \ge \alpha
$$

Capacity constraint:

$$
\sum_{i=1}^{N} x_{i,j} \le L_j, \quad \forall j
$$

Assignment constraint:

$$
\sum_{j=1}^{M} x_{i,j} = 1, \quad \forall i
$$

---

### Voiceover
We minimize cost while ensuring:
- high performance  
- limited capacity  
- exactly one model per query  

Final transition line:
"Great, but where do c_ij and a_ij come from?"

---

## Scene 6 — Two-Stage Framework

### Voiceover
But we don’t know cost and capability beforehand.

### Visual
Pipeline:
Query → Predictor → Optimizer → Model Selection  

---

## Scene 7 — Predictor (Embedding)

### Voiceover
We encode queries and models into vectors.

$$
E_q, \quad E_l
$$

---

## Scene 8 — Capability Prediction

### Voiceover
We predict how likely a model can solve a query.

$$
a^{pred}_{i,j} = \sigma \left( W_1 (E_q^i \cdot E_l^j) + b_1 \right)
$$

---

## Scene 9 — Length Prediction

### Voiceover
We estimate output length to approximate cost.

$$
l^{pred}_{i,j} = b_s \cdot \text{softmax}(W_2(E_q^i + E_l^j) + b_2)
$$

---

## Scene 10 — Retrieval Augmentation

### Voiceover
We also use similar past queries.

Length:

$$
l^{ret}_{i,j} =
\frac{
\sum_{m \in Q_k} \text{sim}(E_q^i, E_q^m) \cdot l_{m,j}
}{
\sum_{m \in Q_k} \text{sim}(E_q^i, E_q^m)
}
$$

Capability:

$$
a^{ret}_{i,j} =
\frac{
\sum_{m \in Q_k} \text{sim}(E_q^i, E_q^m) \cdot a_{m,j}
}{
\sum_{m \in Q_k} \text{sim}(E_q^i, E_q^m)
}
$$

---

## Scene 11 — Fusion

### Voiceover
We combine prediction and retrieval.

$$
a_{i,j} = \gamma a^{pred}_{i,j} + (1 - \gamma) a^{ret}_{i,j}
$$

$$
c_{i,j} = \delta \cdot tp_j(l^{pred}_{i,j}) + (1 - \delta) \cdot tp_j(l^{ret}_{i,j})
$$

---

## Scene 12 — Lagrangian Formulation

### Voiceover
We convert constraints into penalties.

$$
\mathcal{L}(x, \lambda_1, \lambda_2, \mu)
= \sum_{i,j} c_{i,j} x_{i,j}
+ \lambda_1 \left(\alpha - \frac{1}{N} \sum_{i,j} a_{i,j} x_{i,j} \right)
+ \sum_j \lambda_{2,j} \left( \sum_i x_{i,j} - L_j \right)
+ \sum_i \mu_i \left( \sum_j x_{i,j} - 1 \right)
$$

---

## Scene 13 — Optimal Condition

### Voiceover
We compute the optimality condition.

$$
\frac{\partial \mathcal{L}}{\partial x_{i,j}} =
c_{i,j} - \frac{\lambda_1 a_{i,j}}{N} + \lambda_{2,j} + \mu_i = 0
$$

---

## Scene 14 — Decision Rule

### Voiceover
For each query, we choose the best model.

$$
j^* = \arg\min_j \left( c_{i,j} - \frac{\lambda_1 a_{i,j}}{N} + \lambda_{2,j} \right)
$$

---

## Scene 15 — Dual Updates

### Voiceover
We update the multipliers iteratively.

$$
\lambda_1^{t+1} =
\max \left(
\lambda_1^t + \eta_1 \left(\alpha - \frac{1}{N} \sum_{i,j} a_{i,j} x_{i,j} \right),
0
\right)
$$

$$
\lambda_{2,j}^{t+1} =
\max \left(
\lambda_{2,j}^t + \eta_2 \left( \sum_i x_{i,j} - L_j \right),
0
\right)
$$

---

## Scene 16 — Intuition

### Voiceover
- If quality is too low → increase λ₁  
- If a model is overloaded → increase λ₂  

---

## Scene 17 — Results

### Voiceover
OmniRouter improves both accuracy and cost.

### Visual
- Accuracy increases  
- Cost decreases  

---

## Scene 18 — Conclusion

### Voiceover
By combining prediction and optimization,  
OmniRouter achieves globally optimal routing.

### Final Message
Global constrained optimization is better than greedy decisions.