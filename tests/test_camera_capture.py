"""
Unit tests for Camera Capture Module
Agent1が実装してください
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.camera_capture import CameraCapture


def test_camera_initialization():
    """カメラの初期化テスト"""
    config = {
        "device_id": 0,
        "width": 1280,
        "height": 720,
        "fps": 30
    }
    camera = CameraCapture(config)

    assert camera is not None
    assert camera.device_id == 0
    assert camera.width == 1280
    assert camera.height == 720
    assert camera.fps == 30
    assert camera.cap is None


def test_camera_initialization_with_defaults():
    """デフォルト設定での初期化テスト"""
    config = {}
    camera = CameraCapture(config)

    assert camera.device_id == 0
    assert camera.width == 1280
    assert camera.height == 720
    assert camera.fps == 30


@patch('cv2.VideoCapture')
def test_camera_start_success(mock_video_capture):
    """カメラ起動成功のテスト"""
    config = {"device_id": 0, "width": 1280, "height": 720, "fps": 30}
    camera = CameraCapture(config)

    # モックの設定
    mock_cap = Mock()
    mock_cap.isOpened.return_value = True
    mock_cap.get.side_effect = [1280, 720, 30]  # width, height, fps
    mock_video_capture.return_value = mock_cap

    result = camera.start()

    assert result is True
    assert camera.cap is not None
    mock_video_capture.assert_called_once_with(0)
    mock_cap.set.assert_any_call(3, 1280)  # CAP_PROP_FRAME_WIDTH
    mock_cap.set.assert_any_call(4, 720)   # CAP_PROP_FRAME_HEIGHT
    mock_cap.set.assert_any_call(5, 30)    # CAP_PROP_FPS


@patch('cv2.VideoCapture')
def test_camera_start_failure(mock_video_capture):
    """カメラ起動失敗のテスト"""
    config = {"device_id": 0, "width": 1280, "height": 720, "fps": 30}
    camera = CameraCapture(config)

    # モックの設定: カメラが開けない
    mock_cap = Mock()
    mock_cap.isOpened.return_value = False
    mock_video_capture.return_value = mock_cap

    result = camera.start()

    assert result is False


def test_frame_capture_without_start():
    """カメラ起動前のフレーム取得テスト"""
    config = {"device_id": 0, "width": 1280, "height": 720, "fps": 30}
    camera = CameraCapture(config)

    ret, frame = camera.get_frame()

    assert ret is False
    assert frame is None


@patch('cv2.VideoCapture')
def test_frame_capture_success(mock_video_capture):
    """フレーム取得成功のテスト"""
    config = {"device_id": 0, "width": 1280, "height": 720, "fps": 30}
    camera = CameraCapture(config)

    # モックの設定
    mock_cap = Mock()
    mock_cap.isOpened.return_value = True
    mock_cap.get.side_effect = [1280, 720, 30]
    test_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    mock_cap.read.return_value = (True, test_frame)
    mock_video_capture.return_value = mock_cap

    camera.start()
    ret, frame = camera.get_frame()

    assert ret is True
    assert frame is not None
    assert isinstance(frame, np.ndarray)
    assert frame.shape == (720, 1280, 3)


@patch('cv2.VideoCapture')
def test_frame_capture_failure(mock_video_capture):
    """フレーム取得失敗のテスト"""
    config = {"device_id": 0, "width": 1280, "height": 720, "fps": 30}
    camera = CameraCapture(config)

    # モックの設定
    mock_cap = Mock()
    mock_cap.isOpened.return_value = True
    mock_cap.get.side_effect = [1280, 720, 30]
    mock_cap.read.return_value = (False, None)
    mock_video_capture.return_value = mock_cap

    camera.start()
    ret, frame = camera.get_frame()

    assert ret is False
    assert frame is None


@patch('cv2.VideoCapture')
def test_camera_stop(mock_video_capture):
    """カメラ停止のテスト"""
    config = {"device_id": 0, "width": 1280, "height": 720, "fps": 30}
    camera = CameraCapture(config)

    # モックの設定
    mock_cap = Mock()
    mock_cap.isOpened.return_value = True
    mock_cap.get.side_effect = [1280, 720, 30]
    mock_video_capture.return_value = mock_cap

    camera.start()
    camera.stop()

    mock_cap.release.assert_called_once()
    assert camera.cap is None


def test_camera_stop_without_start():
    """カメラ起動前の停止テスト"""
    config = {"device_id": 0, "width": 1280, "height": 720, "fps": 30}
    camera = CameraCapture(config)

    # エラーなく停止できることを確認
    camera.stop()
    assert camera.cap is None


@patch('cv2.VideoCapture')
def test_is_opened_true(mock_video_capture):
    """is_opened()がTrueを返すテスト"""
    config = {"device_id": 0, "width": 1280, "height": 720, "fps": 30}
    camera = CameraCapture(config)

    # モックの設定
    mock_cap = Mock()
    mock_cap.isOpened.return_value = True
    mock_cap.get.side_effect = [1280, 720, 30]
    mock_video_capture.return_value = mock_cap

    camera.start()

    assert camera.is_opened() is True


def test_is_opened_false():
    """is_opened()がFalseを返すテスト"""
    config = {"device_id": 0, "width": 1280, "height": 720, "fps": 30}
    camera = CameraCapture(config)

    assert camera.is_opened() is False


@patch('cv2.VideoCapture')
def test_camera_error_handling(mock_video_capture):
    """エラーハンドリングテスト"""
    config = {"device_id": 0, "width": 1280, "height": 720, "fps": 30}
    camera = CameraCapture(config)

    # モックの設定: 例外を発生させる
    mock_video_capture.side_effect = Exception("Camera error")

    result = camera.start()

    assert result is False
