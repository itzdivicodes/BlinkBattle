# Don't Blink Application

A computer vision-based game that challenges you to keep your eyes open as long as possible! The game uses MediaPipe for accurate blink detection and ends immediately when you blink once.

## Features

- **Real-time Blink Detection**: Uses MediaPipe Face Mesh for precise eye tracking
- **Timer**: Counts the time until your first blink
- **Tkinter GUI**: Clean, user-friendly interface
- **Video Feed Control**: Start/stop camera feed
- **Replay Functionality**: Restart the game instantly
- **Visual Feedback**: Shows eye landmarks and EAR (Eye Aspect Ratio) values

## Project Structure

```
dont_stare/
├── blink.py          # Blink detection module using MediaPipe
├── game.py           # Main game file with tkinter UI
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Requirements

- Python 3.10 (recommended)
- Webcam/Camera
- Required packages (see requirements.txt)

## Installation

### Option 1: Using Conda Environment (Recommended)

1. Create and activate conda environment:
```bash
conda create -n btm_1907_clap_counter_new python=3.10
conda activate btm_1907_clap_counter_new
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Using Default Environment

If the conda environment gives trouble, use your default Python environment:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Game

```bash
python game.py
```

### Game Controls

1. **Start Video Feed**: Click to activate your camera
2. **Start Game**: Begin the challenge (timer starts)
3. **Replay**: Restart the game after it ends

### How to Play

1. Click "Start Video Feed" to activate your camera
2. Position yourself so your face is clearly visible
3. Click "Start Game" to begin the challenge
4. Keep your eyes open as long as possible
5. The game ends immediately when you blink once
6. Your time will be displayed and recorded
7. Click "Replay" to try again and beat your record!

## Technical Details

### Blink Detection Algorithm

The application uses the **Eye Aspect Ratio (EAR)** method:

1. **Face Detection**: MediaPipe Face Mesh detects facial landmarks
2. **Eye Landmarks**: Extracts specific eye landmark points
3. **EAR Calculation**: Computes the ratio of vertical to horizontal eye distances
4. **Blink Detection**: When EAR drops below threshold (0.25), a blink is detected

### Key Parameters

- **EAR Threshold**: 0.25 (adjustable in `blink.py`)
- **Consecutive Frames**: 2 frames to confirm blink
- **Video Resolution**: 640x480 pixels
- **Frame Rate**: ~30 FPS

## File Descriptions

### `blink.py`
- Contains the `BlinkDetector` class
- Handles MediaPipe initialization and face mesh processing
- Implements EAR calculation and blink detection logic
- Provides visual feedback with eye landmarks

### `game.py`
- Main application file with tkinter GUI
- Manages game state and timer
- Integrates camera feed with blink detection
- Handles user interactions and game flow

## Troubleshooting

### Camera Issues
- Ensure your camera is not being used by another application
- Try changing the camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`

### Environment Issues
- If conda environment fails, use your default Python environment
- Ensure all dependencies are properly installed

### Performance Issues
- Close other applications using the camera
- Ensure good lighting for better face detection
- Keep your face centered in the camera view

## Tips for Better Performance

1. **Lighting**: Ensure good, even lighting on your face
2. **Distance**: Sit about 2-3 feet from the camera
3. **Position**: Keep your face centered in the frame
4. **Stability**: Avoid excessive head movement during the game

## Game Statistics

The application displays:
- **Current EAR Value**: Real-time eye aspect ratio
- **Blink Count**: Total blinks detected (resets each game)
- **Timer**: Time elapsed since game start
- **Final Score**: Your lasting time when the game ends

## Customization

You can modify the following parameters in `blink.py`:

```python
self.EAR_THRESHOLD = 0.25      # Lower = more sensitive
self.CONSECUTIVE_FRAMES = 2     # Frames to confirm blink
```

## Dependencies

- `opencv-python`: Camera handling and image processing
- `mediapipe`: Face mesh detection and landmark extraction
- `Pillow`: Image format conversion for tkinter
- `numpy`: Numerical computations
- `scipy`: Distance calculations for EAR

## License

This project is for educational and entertainment purposes.

## Contributing

Feel free to fork this project and submit improvements!

---

**Challenge yourself: How long can you keep your eyes open?** 👁️
