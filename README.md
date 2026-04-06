# Applied Data Science: OmniRouter Manim Project

This repository contains a Manim project that explains the [OmniRouter paper](https://kdd.org/exploration_files/p107_Omnirouter_camera_ready.pdf) with visual intuition and math.

## Setup

This project use conda for environment management. First, ensure you have conda installed, then run the following command to create the project environment:

Create the environment:

```bash
conda env create -f environment.yml
```
Since all dependencies except LaTeX are handled by conda, you have to install LaTeX separately. Please refer to the Manim documentation for LaTeX installation instructions [here](
https://docs.manim.community/en/stable/installation/uv.html#step-2-optional-installing-latex).

After installing all dependencies, activate and work in the project environment:

```bash
conda activate omni-router-manim
```

## Commands

Low-quality preview render:

```bash
make video-low
```

High-quality render:

```bash
make video-high
```

Clean generated media:

```bash
make clean-media
```

The Makefile currently renders scene class `OmniRouter` from `src/main.py`.
