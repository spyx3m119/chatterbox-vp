# CUDA Device Error Fix for Mac Users

## Problem Description

When using the multilingual TTS model on Mac systems without CUDA support, users encountered the following error:

```
RuntimeError: Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False. If you are running on a CPU-only machine, please use torch.load with map_location=torch.device('cpu') to map your storages to the CPU.
```

This error occurred because the model files were saved on CUDA-enabled systems and contain CUDA device information, but Mac users without CUDA support cannot load them directly.

## Solution Implemented

The fix involves adding proper device detection and mapping logic to handle CUDA-saved models on CPU-only systems. The solution was implemented in two key methods in [`src/chatterbox/mtl_tts.py`](src/chatterbox/mtl_tts.py):

### 1. Enhanced `from_local` Method (Lines 161-197)

Added device detection logic that:
- Checks if the target device is "cpu" or "mps" (Apple Silicon)
- Sets `map_location=torch.device('cpu')` for non-CUDA devices
- Uses `map_location=None` for CUDA devices (normal behavior)

```python
# Determine map_location for non-CUDA devices to handle CUDA-saved models
if device in ["cpu", "mps"]:
    map_location = torch.device('cpu')
else:
    map_location = None

# Apply map_location to torch.load() calls (not safetensors.load_file)
ve.load_state_dict(
    torch.load(ckpt_dir / "ve.pt", map_location=map_location, weights_only=True)
)
```

### 2. Enhanced `from_pretrained` Method (Lines 199-210)

Added MPS availability checking for Mac users:
- Detects if MPS (Apple Silicon GPU) is available
- Provides informative error messages if MPS is not available
- Falls back to CPU if MPS is unavailable

```python
# Check if MPS is available on macOS
if device == "mps" and not torch.backends.mps.is_available():
    if not torch.backends.mps.is_built():
        print("MPS not available because the current PyTorch install was not built with MPS enabled.")
    else:
        print("MPS not available because the current MacOS version is not 12.3+ and/or you do not have an MPS-enabled device on this machine.")
    device = "cpu"
```

## How It Works

1. **Device Detection**: The code checks if the target device is CPU or MPS (Apple Silicon)
2. **Map Location Setting**: For non-CUDA devices, it sets `map_location='cpu'` to force loading models onto CPU
3. **Model Loading**: All `torch.load()` calls use the appropriate `map_location` parameter (note: `safetensors.load_file()` doesn't support device mapping)
4. **MPS Fallback**: If MPS is requested but unavailable, the system gracefully falls back to CPU

## Benefits

- **Cross-Platform Compatibility**: Works on Windows, Linux, and Mac systems
- **Graceful Degradation**: Automatically falls back to CPU when GPU is unavailable
- **Informative Error Messages**: Users get clear feedback about device availability
- **No Performance Impact**: CUDA devices continue to work normally
- **Backward Compatibility**: Existing code continues to work without changes

## Testing

The fix has been tested with a comprehensive test script that verifies:
- Device detection logic for CPU, MPS, and CUDA
- Map location setting for different device types
- MPS availability checking on Mac systems
- Graceful fallback behavior

## Files Modified

- [`src/chatterbox/mtl_tts.py`](src/chatterbox/mtl_tts.py) - Added device detection and mapping logic

## Usage

Users can now use the multilingual TTS on Mac systems without CUDA by simply specifying the appropriate device:

```python
# For Mac users without CUDA
tts = ChatterboxMultilingualTTS.from_pretrained(device="cpu")

# For Mac users with Apple Silicon (if MPS is available)
tts = ChatterboxMultilingualTTS.from_pretrained(device="mps")
```

The system will automatically handle device detection and model loading, preventing the CUDA device error.