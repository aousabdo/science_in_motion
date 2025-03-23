# Science in Motion

A collection of physics simulations and visualizations optimized for TikTok. This repository contains Python scripts that generate mesmerizing animations of various physical phenomena.

## Repository Structure

```
science_in_motion/
├── src/                  # Source code
│   └── simulations/      # Simulation modules
│       ├── double_pendulum.py
│       └── lorenz_attractor.py
├── examples/             # Example usage scripts
│   └── generate_animations.py
├── output/               # Generated animations (not tracked in git)
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Current Visualizations

### Double Pendulum
The double pendulum script (`src/simulations/double_pendulum.py`) simulates the chaotic motion of a double pendulum system. It creates a visually striking animation with the following features:
- Portrait mode (9:16 aspect ratio) optimized for TikTok
- Dark background with high-contrast elements
- Trace of the pendulum's path
- Full 30 seconds of mesmerizing chaotic motion

### Lorenz Attractor
The Lorenz attractor script (`src/simulations/lorenz_attractor.py`) visualizes the famous Lorenz system, a set of differential equations known for exhibiting chaotic behavior. Features include:
- 3D visualization with animated camera perspective
- Color gradients that change over time
- Mathematical equations displayed
- TikTok-optimized portrait format

## Requirements

All required packages are listed in the `requirements.txt` file. You can install them using:

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start
The simplest way to generate both animations is to run the example script:

```bash
python examples/generate_animations.py
```

This will create both animations and save them in the `output` directory.

### Individual Simulations
You can also import and use the simulation functions directly in your code:

```python
from src.simulations.double_pendulum import create_double_pendulum_animation
from src.simulations.lorenz_attractor import create_lorenz_animation

# Generate animations
create_double_pendulum_animation()
create_lorenz_animation()
```

## About Science in Motion

Science in Motion is a TikTok channel dedicated to creating engaging and visually stunning physics and mathematics visualizations. Follow us for more amazing science content!

## License

MIT 