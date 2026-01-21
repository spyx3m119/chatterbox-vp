# Sample Audio Files Implementation for ChatterBox TTS

## Summary

This document provides a comprehensive plan for implementing local sample reference audio files for the ChatterBox TTS system, replacing the current remote Google Cloud storage URLs.

## Current State

### Existing Implementation

The current ChatterBox TTS system uses remote URLs from Google Cloud Storage for sample reference audio files:

1. **Turbo TTS**: Uses `https://storage.googleapis.com/chatterbox-demo-samples/prompts/female_random_podcast.wav`
2. **Multilingual TTS**: Uses 23+ language-specific URLs in the format:
   - `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/{language_code}/{filename}`

### Issues with Current Approach

- **Network Dependency**: Requires internet connection to load samples
- **Latency**: Slower loading times due to network requests
- **Reliability**: Dependent on external service availability
- **User Experience**: Poor offline experience
- **Development**: Difficult to test and debug

## Implementation Plan

### Phase 1: Directory Structure ✅

**Completed Tasks:**
- Created `samples/` directory at project root
- Organized subdirectories:
  - `samples/prompts/` - General TTS reference prompts
  - `samples/mtl_prompts/` - Multilingual TTS reference prompts
- Created comprehensive documentation

### Phase 2: Configuration System ✅

**Completed Tasks:**
- Created `samples/sample_config.md` with configuration utilities
- Defined `LANGUAGE_CONFIG` for all 23+ supported languages
- Implemented helper functions:
  - `get_sample_audio_path()` - Convert relative to absolute paths
  - `get_language_samples()` - Get all language configurations
  - `validate_sample_files()` - Check file existence
  - `get_supported_languages_display()` - Generate language lists

### Phase 3: Documentation ✅

**Completed Tasks:**
- Created `samples/README.md` - Overview and usage
- Created `samples/USER_GUIDE.md` - User-facing documentation
- Created `samples/IMPLEMENTATION_PLAN.md` - Technical implementation details
- Documented file format requirements and best practices

### Phase 4: Code Integration (Pending)

**Required Changes to `unified_webui.py`:**

1. **Import Configuration Module**
   ```python
   from samples.sample_config import (
       get_sample_audio_path,
       get_language_samples,
       validate_sample_files
   )
   ```

2. **Update Default Audio References**
   ```python
   # Replace remote URL with local path
   turbo_ref_wav = gr.Audio(
       sources=["upload", "microphone"],
       type="filepath",
       label="Reference Audio File",
       value=get_sample_audio_path("prompts/female_random_podcast.wav")
   )
   ```

3. **Update Multilingual Configuration**
   ```python
   # Replace LANGUAGE_CONFIG with local paths
   LANGUAGE_CONFIG = {
       "ar": {
           "audio": get_sample_audio_path("mtl_prompts/ar_f/ar_prompts2.flac"),
           "text": "في الشهر الماضي، وصلنا إلى معلم جديد بمليارين من المشاهدات على قناتنا على يوتيوب."
       },
       # ... other languages
   }
   ```

4. **Update Language Change Handler**
   ```python
   def on_language_change(lang, current_ref, current_text):
       samples = get_language_samples()
       return samples[lang]["audio"], samples[lang]["text"]
   ```

5. **Add File Validation**
   ```python
   # Check if sample files exist
   missing_files = validate_sample_files()
   if missing_files:
       print(f"Warning: Missing sample files: {missing_files}")
   ```

### Phase 5: Testing and Deployment (Pending)

**Testing Requirements:**
- Verify all sample files load correctly
- Test TTS generation with local samples
- Test multilingual TTS with all languages
- Validate file format requirements
- Test offline functionality

**Deployment Considerations:**
- Include sample files in distribution
- Provide fallback to remote URLs if local files missing
- Ensure backward compatibility
- Update installation instructions

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

## Directory Structure

```
samples/
├── README.md                    # Documentation
├── config.md                    # Configuration guide
├── sample_config.md             # Technical configuration
├── IMPLEMENTATION_PLAN.md       # Implementation details
├── USER_GUIDE.md                # User guide
├── prompts/                     # General TTS prompts
│   └── female_random_podcast.wav
└── mtl_prompts/                 # Multilingual TTS prompts
    ├── ar_f/
    │   └── ar_prompts2.flac
    ├── da_m1.flac
    ├── de_f1.flac
    ├── el_m.flac
    ├── en_f1.flac
    ├── es_f1.flac
    ├── fi_m.flac
    ├── fr_f1.flac
    ├── he_m1.flac
    ├── hi_f1.flac
    ├── it_m1.flac
    ├── ja/
    │   └── ja_prompts1.flac
    ├── ko_f.flac
    ├── ms_f.flac
    ├── nl_m.flac
    ├── no_f1.flac
    ├── pl_m.flac
    ├── pt_m1.flac
    ├── ru_m.flac
    ├── sv_f.flac
    ├── sw_m.flac
    ├── tr_m.flac
    └── zh_f2.flac
```

## Next Steps

1. **Complete Code Integration**
   - Update `unified_webui.py` with local file paths
   - Add configuration imports
   - Implement file validation
   - Test all functionality

2. **Testing and Validation**
   - Test with actual audio files
   - Validate all language samples
   - Test edge cases and error handling
   - Performance testing

3. **Documentation Updates**
   - Update main README.md
   - Create installation guide
   - Add troubleshooting section
   - Update API documentation

4. **User Experience**
   - Add sample file management UI
   - Create sample file upload functionality
   - Add sample file validation
   - Improve error messages

## Risk Mitigation

- **Backward Compatibility**: Keep remote URLs as fallback
- **File Validation**: Check file existence before use
- **Graceful Degradation**: Handle missing files gracefully
- **User Guidance**: Clear documentation for adding samples
- **Testing**: Comprehensive testing of all scenarios

## Conclusion

The implementation of local sample reference audio files will significantly improve the user experience of the ChatterBox TTS system by providing offline support, faster loading times, and better reliability. The comprehensive directory structure and configuration system make it easy to manage and extend the sample files.

The next phase involves updating the code to use local files instead of remote URLs, followed by thorough testing and documentation updates.