# Hand Tracking Streamer

Real-time hand tracking system that captures video from a fixed camera, detects hands, measures joint distances, and streams data to a web application.

## Project Overview

This system continuously captures video from a camera and:
1. Detects when a hand appears in the frame
2. Tracks 21 hand landmarks using MediaPipe
3. Calculates joint distances and measurements
4. Streams the data in real-time to a web application

## Architecture

The project is divided into 5 main modules:

- **Agent1**: Camera Capture Module - Camera initialization and frame acquisition
- **Agent2**: Hand Detection & Tracking - MediaPipe Hands integration
- **Agent3**: Joint Measurement - Distance calculations and data processing
- **Agent4**: Data Sender - Communication with web application
- **Agent5**: Main Controller - Module integration and orchestration

## Technology Stack

- **Language**: Python 3.8+
- **Computer Vision**: OpenCV, MediaPipe Hands
- **Data Transfer**: WebSocket / REST API
- **Configuration**: YAML

## Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the System

```bash
python src/main.py
```

## Development

This project uses git worktree for parallel development by multiple agents.
See `AGENTS.md` for agent assignments and workflow.

## Multi-Agent Development

Each agent works on a separate feature branch:
- `feature/camera-capture` - Agent1
- `feature/hand-detection` - Agent2
- `feature/joint-measurement` - Agent3
- `feature/data-sender` - Agent4
- `feature/main-controller` - Agent5
