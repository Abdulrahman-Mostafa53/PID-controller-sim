# MIA PID Monitor & Simulator

An Object-Oriented Programming (OOP) based PID controller simulation and real-time streaming dashboard built with **Python**, **Dash**, and **Plotly**. 

This system uses a dedicated `Pid` class implementing custom anti-windup clamping, zero-crossing integral reset, and deadzone protection, paired with a `Plot` class that streams real-time updates via Dash interval callbacks.

---

## Features

* **Custom OOP PID Logic (`Pid` class)**: 
  * Integral anti-windup clamping (`anti_wind_clamp`) and output capping (`controller_clamp`).
  * Automatic zero-crossing reset that clears accumulated error when sign changes occur.
  * Deadzone threshold protection (`THRES`).
* **Real-Time Dash Streaming (`Plot` class)**: 
  * Uses `dcc.Interval` and `extendData` for live, high-performance graph updates without full page reloads.
  * Dual-graph monitoring tracking both **State Graph** and **Error Graph** simultaneously.
  * Dark-themed responsive dashboard layout.

---

## Prerequisites & Installation

Make sure you have Python installed, then install the required libraries:

```bash
pip install dash numpy
