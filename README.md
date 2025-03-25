# Trigonometry Challenges for TikTok

This project contains Python animations for creating engaging trigonometry challenges suitable for TikTok videos. The challenges present mathematical problems in a visually appealing way with vibrant colors and animations.

## Features

- **Basic Trigonometry Challenge**: Mountain climbing scenario with angles and distances to calculate
- **Advanced Trigonometry Challenge**: Lighthouse and ships with angles and distances that require the Law of Cosines
- Smooth animations with eye-catching effects
- TikTok-friendly vertical (9:16) format
- Vibrant color schemes
- Pulsing effects and gradual reveals to maintain viewer interest

## Requirements

- Python 3.7+
- matplotlib
- numpy
- ffmpeg (optional, for MP4 output)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/trig-challenges.git
cd trig-challenges
```

2. Install the required packages:
```bash
pip install matplotlib numpy
```

3. (Optional) Install ffmpeg for MP4 output:
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## Usage

Run the main script to generate both challenges:

```bash
python src/simulations/run_trig_challenges.py
```

### Options

- Generate only the basic challenge:
```bash
python src/simulations/run_trig_challenges.py --challenges basic
```

- Generate only the advanced challenge:
```bash
python src/simulations/run_trig_challenges.py --challenges advanced
```

- Specify a custom output directory:
```bash
python src/simulations/run_trig_challenges.py --output-dir my_animations
```

## Challenge Solutions

### Basic Mountain Challenge
The challenge provides:
- Distance from base to observer: 10m
- Angle from observer to peak: 32°
- Distance from base to peak: 62m

To solve, you need to find the height of the mountain peak above the base station using trigonometry.

### Advanced Lighthouse Challenge
The challenge provides:
- Angles from lighthouse to two ships: 28° and 42°
- Distances from lighthouse to ships: 53m and 32m

To solve, you need to find the distance between the two ships using the Law of Cosines.

## Customization

You can modify the challenges by editing the source files:
- `src/simulations/trigonometry_challenge.py`
- `src/simulations/advanced_trig_challenge.py`

You can change:
- Colors
- Animation timing
- Problem difficulty
- Text and questions
- Dimensions and angles

## License

[MIT License](LICENSE)

## Credits

Created by @Science_In_Motion for educational content on TikTok 