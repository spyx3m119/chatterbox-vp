# Sample Audio Files Implementation Plan

## Overview

This document outlines the plan for implementing local sample reference audio files for the ChatterBox TTS system, replacing the current remote Google Cloud storage URLs.

## Current State Analysis

### Existing Remote URLs

The current implementation uses remote URLs from Google Cloud Storage:

1. **Turbo TTS**: `https://storage.googleapis.com/chatterbox-demo-samples/prompts/female_random_podcast.wav`
2. **Multilingual TTS**: 23+ language-specific URLs in the format:
   - `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/{language_code}/{filename}`

### Issues with Remote URLs

- **Network Dependency**: Requires internet connection to load samples
- **Latency**: Slower loading times due to network requests
- **Reliability**: Dependent on external service availability
- **User Experience**: Poor offline experience

## Implementation Strategy

### Phase 1: Directory Structure and Configuration

✅ **Completed**
- Created `samples/` directory structure
- Organized files into `samples/prompts/` and `samples/mtl_prompts/`
- Created configuration files and documentation

### Phase 2: Download and Local Storage

✅ **Completed**
- Identified all remote URLs from `unified_webui.py`
- Created plan for downloading files to local filesystem
- Established file naming conventions

### Phase 3: Code Updates

**Pending Tasks:**

1. **Update unified_webui.py**
   - Replace remote URLs with local file paths
   - Import sample configuration module
   - Update default audio file references
   - Maintain backward compatibility

2. **Update Language Configuration**
   - Modify `LANGUAGE_CONFIG` to use local paths
   - Update `default_audio_for_lang()` function
   - Update `default_text_for_lang()` function

3. **Add Validation**
   - Check if sample files exist before using
   - Provide fallback mechanisms for missing files
   - Add error handling for file access issues

### Phase 4: Testing and Documentation

**Pending Tasks:**

1. **Testing**
   - Verify all sample files load correctly
   - Test TTS generation with local samples
   - Test multilingual TTS with all languages
   - Validate file format requirements

2. **Documentation**
   - Update README with sample file information
   - Create user guide for adding new samples
   - Document file format requirements
   - Provide troubleshooting guide

## Technical Implementation Details

### File Structure

```
samples/
├── README.md                    # Documentation
├── config.md                    # Configuration guide
├── sample_config.md             # Technical configuration
├── prompts/                     # General TTS prompts
│   └── female_random_podcast.wav
└── mtl_prompts/                 # Multilingual TTS prompts
    ├── ar_f/
    │   └── ar_prompts2.flac
    ├── da_m1.flac
    ├── de_f1.flac
    └── ... (20+ more languages)
```

### Configuration Functions

```python
# Key functions to implement:
- get_sample_audio_path(relative_path)  # Convert relative to absolute path
- get_language_samples()                # Get all language configs
- validate_sample_files()               # Check file existence
- get_supported_languages_display()     # Generate language list
```

### Code Changes Required

1. **Import Configuration**
   ```python
   from samples.sample_config import (
       get_sample_audio_path,
       get_language_samples,
       validate_sample_files
   )
   ```

2. **Update Default Values**
   ```python
   # Replace remote URLs with local paths
   initial_lang = "fr"
   mtl_ref_wav = gr.Audio(
       sources=["upload", "microphone"],
       type="filepath",
       label="Reference Audio File (Optional)",
       value=get_sample_audio_path("mtl_prompts/fr_f1.flac")  # Local path
   )
   ```

3. **Update Language Change Handler**
   ```python
   def on_language_change(lang, current_ref, current_text):
       samples = get_language_samples()
       return samples[lang]["audio"], samples[lang]["text"]
   ```

## Benefits of Local Implementation

1. **Offline Support**: Works without internet connection
2. **Faster Loading**: No network latency
3. **Better UX**: Immediate sample availability
4. **Reliability**: Not dependent on external services
5. **Customization**: Easy to add/remove samples
6. **Development**: Easier testing and debugging

## File Format Requirements

- **Formats**: WAV, FLAC
- **Sample Rates**: 16kHz, 24kHz
- **Channels**: Mono
- **Duration**: 5-10 seconds
- **Quality**: High quality, clear speech

## Next Steps

1. Complete code updates in `unified_webui.py`
2. Test the implementation with local files
3. Create comprehensive documentation
4. Add validation and error handling
5. Update user-facing documentation

## Risk Mitigation

- **Backward Compatibility**: Keep remote URLs as fallback
- **File Validation**: Check file existence before use
- **Graceful Degradation**: Handle missing files gracefully
- **User Guidance**: Clear documentation for adding samples