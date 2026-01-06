# 🚦 Traffic Operating Machine (JAMITOM)

**JAMITOM** — *Just A Mindful and Intelligent Traffic Operating Machine* — is a traffic simulation and optimisation project developed as part of a high school scientific initiation programme. The project starts from a basic traffic intersection simulation and evolves to model more realistic traffic behaviour, such as congestion patterns and adaptive traffic light control, with experiments involving optimisation algorithms.


## Overview

This repository contains multiple versions of a traffic intersection simulator, each representing an incremental development step. It also includes auxiliary scripts for running simulations, collecting results, and experimenting with optimisation techniques such as genetic algorithms.

The main goals of the project are:

- Simulate traffic flow at an intersection with realistic behaviour.
- Explore methods to optimise traffic light timings.
- Experiment with intelligent algorithms to improve traffic efficiency.

---

## Key Features

- Traffic intersection simulation with basic traffic light logic.
- Multiple simulation variants reflecting different development stages.
- Scripts for faster or parallel simulation execution.
- A simple genetic algorithm for traffic light timing optimisation.
- Output images and data for analysis.

---

## Repository Structure

```plaintext
├── images/              # Images used in the simulation
├── algorithm.py         # Genetic algorithm for traffic light optimisation
├── exec.py              # Execution script 
├── fast.py              # Faster simulation used alongside the algorithm
├── latest.py            # Most recent simulation version
├── main.py              # Main entry point
├── main2.py             # Alternative execution version
├── .gitignore
├── README.md            # Project documentation
