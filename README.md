## Don't Blink Application

A computer vision-based game that challenges you to keep your eyes open as long as possible! The game uses MediaPipe for accurate blink detection and ends immediately when you blink once.

### Features

- **Real-time Blink Detection**: Uses MediaPipe Face Mesh for precise eye tracking
- **Timer**: Counts the time until your first blink
- **Tkinter GUI**: Clean, user-friendly interface
- **Video Feed Control**: Start/stop camera feed
- **Replay Functionality**: Restart the game instantly
- **Visual Feedback**: Shows eye landmarks and EAR (Eye Aspect Ratio) values

### Project Structure

```
dont_stare/
├── blink.py          # Blink detection module using MediaPipe
├── game.py           # Main game file with tkinter UI
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

### Requirements

- Python 3.10 (recommended)
- Webcam/Camera
- Required packages (see requirements.txt)

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

**Challenge yourself: How long can you keep your eyes open?** 👁️
