# part-time-tax-efficiency

This script evaluates the variations in tax efficiency achieved through part-time employment models within the Danish labor market under the 2026 Danish rules.

## Model

Let:
- $g$ be the yearly gross salary.
- $\mathtt{skat}(g)$ be a function getting the yearly gross salary and returning the yearly net salary.
- $n$ be the yearly net salary.
- $x \in [0,5]$ be the number of working days per week.
- $g_r(x) = \frac{x}{5} \cdot g$ be the gross yearly salary retained taking into account part-time. It is assumed gross yearly salary increases uniformly with respect to the number of working days per week.
- $g_r^\\%(x) = \frac{g_r(x)}{g}$ be the percentual gross yearly salary retained taking into account part-time.
- $n_r(x) = \mathtt{skat}(g_r(x))$ be the net yearly salary retained taking into account part-time.
- $n_r^\\%(x) = \frac{n_r(x)}{n}$ be the percentual net yearly salary retained taking into account part-time.

In the adopted model, tax efficiency is quantified by the premium retention function:

$$p_r^\\%(x) = n_r^\\%(x) - g_r^\\%(x)$$

Thus, the optimal number of working days per week $x_{\text{opt}}$ is defined as:

$$x_{\text{opt}} = \arg\max_{x \in [0,5]} \left( p_r^\\%(x) \right)$$

## Analysis

Given the taxation function below:

![Figure 1:  Danish salary tax: gross vs. net salary (Copenhagen 2026)](danish_salary_tax.png)
*Figure 1: Comparison between gross salary and net salary under the 2026 Copenhagen tax rules.*

It is possible to observe variation in tax efficiency:

![Figure 2:  Part-time tax efficiency: premium retention (%) (Copenhagen 2026)](part_time_tax_efficiency.png)
*Figure 2: Analysis of the premium retention for different full-time yearly gross salaries. Specifically, the bracket entry points are taken into account.*

## Example

For a gross yearly salary $g = 900,000$ DKK, topskat entry threshold is crossed at full-time capacity.
* By working $x=5$ days per week, the net salary $n$ represents a baseline for a full-time job. No premium retention is generated ($p_r^\\%(5) = 0\\%$).
* By working $x=3$ days per week, gross salary (and labor time) decreases to $60\\%$ of full-time, yet the retained net salary is $60\\%+4.52\\%=64.52\\%$ of the full-time net salary baseline $n$. 

Thus a positive retention premium is generated:
$$p_r^\\%(3) = 64.52\\% - 60.00\\% = +4.52\\%$$

Note that while absolute net salary is lower for $x=3$, lowering the gross salary base below the mellemskat entry threshold optimizes tax efficiency, allowing the worker to retain a higher proportion of net salary relative to time invested.

Numerically:

```
# Full-time tax rate
(1 - n / g) * 100 = 37.39 %

# Optimal number of working days per week and premium retention
x_opt = 3.0
p_r_perc_max = n_r_perc(x_opt) - g_r_perc(x_opt) = 4.52 %

g_r(5) = 900000.0 DKK
g_r_perc(5) = 100.0 %
n_r(5) = 563535.0 DKK
n_r_perc(5) = 100.0 %

g_r(x_opt) = 539639.64 DKK
g_r_perc(x_opt) = 59.96 %
n_r(x_opt) = 363375.53 DKK
n_r_perc(x_opt) = 64.48 %

# Optimal part-time tax rate
(1 - n_r(x_opt) / g_r(x_opt)) * 100 (optimal part-time tax rate) = 32.66 %

# Difference between full-time tax rate and optimal part-time tax rate 
(1 - n / g) * 100 - (1 - n_r(x_opt) / g_r(x_opt)) * 100 = 4.72 %
```
