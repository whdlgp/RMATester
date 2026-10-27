# RMATester

A RMA (Rate Monotonic Analysis) implementation and testing tool.

[**Open RMATester**](https://whdlgp.github.io/RMATester/)

## Utilization

Total CPU utilization:\
$$U = \sum_{i=1}^{n} \frac{C_i}{T_i}$$

where:
- $C_i$: Execution time of task $i$
- $T_i$: Period of task $i$
- $n$: Number of tasks

## Sufficient Schedulability Test

RMS utilization bound:\
$$U \leq n\left(2^{1/n}-1\right)$$

Passing guarantees schedulability, but failing does not imply unschedulability.
