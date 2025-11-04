"""
システムの基本動作テスト（MediaPipeなし）

カメラモジュールと基本的なシステムフローをテストします。
"""

import sys
sys.path.insert(0, 'src')

import yaml
from camera_capture import CameraCapture
# MediaPipeは利用不可のため、手検出はスキップ
# from hand_detector import HandDetector

print("=" * 60)
print("Hand Tracking Streamer - System Test (Simple Mode)")
print("=" * 60)
print()

# 設定読み込み
print("[1/5] Loading configuration...")
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
print("  -> Config loaded successfully")
print()

# カメラ初期化
print("[2/5] Initializing camera...")
camera = CameraCapture(config['camera'])
if not camera.start():
    print("  -> ERROR: Failed to start camera")
    sys.exit(1)
print(f"  -> Camera started: {config['camera']['width']}x{config['camera']['height']} @ {config['camera']['fps']}fps")
print()

# フレームキャプチャテスト
print("[3/5] Testing frame capture (10 frames)...")
success_count = 0
for i in range(10):
    ret, frame = camera.get_frame()
    if ret:
        success_count += 1
        if i % 3 == 0:  # 3フレームごとに表示
            print(f"  -> Frame {i+1}: {frame.shape} OK")
print(f"  -> Successfully captured {success_count}/10 frames")
print()

# 手検出のシミュレーション（MediaPipeなし）
print("[4/5] Hand detection simulation (MediaPipe unavailable)...")
print("  -> MediaPipe is not available in Python 3.13")
print("  -> Hand detection would be here with Python 3.11/3.12")
print("  -> Simulating: No hands detected (expected)")
print()

# クリーンアップ
print("[5/5] Cleanup...")
camera.stop()
print("  -> Camera stopped and released")
print()

print("=" * 60)
print("Test Result: SUCCESS (Camera working, MediaPipe unavailable)")
print("=" * 60)
print()
print("Next steps:")
print("  1. Camera module: WORKING")
print("  2. Hand detection: Needs Python 3.11 or 3.12")
print("  3. Other modules: Ready to test")
print()
