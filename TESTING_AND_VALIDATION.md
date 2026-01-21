# Testing and Validation Guide for Local Sample Audio Files

## Overview

This guide provides comprehensive testing procedures to validate the local sample audio files implementation for ChatterBox TTS.

## Testing Phases

### Phase 1: Pre-Integration Testing

#### 1.1 File System Validation

**Objective**: Verify all audio files are properly downloaded and accessible.

**Test Cases**:

1. **File Existence Check**
   ```python
   import os
   
   # Test all expected files exist
   expected_files = [
       "samples/prompts/female_random_podcast.wav",
       "samples/mtl_prompts/ar_f/ar_prompts2.flac",
       "samples/mtl_prompts/en_f1.flac",
       # Add all other expected files
   ]
   
   for file_path in expected_files:
       assert os.path.exists(file_path), f"Missing file: {file_path}"
       print(f"✅ {file_path}")
   ```

2. **File Format Validation**
   ```python
   import wave
   import soundfile as sf
   
   # Test file formats
   test_files = [
       "samples/prompts/female_random_podcast.wav",
       "samples/mtl_prompts/en_f1.flac"
   ]
   
   for file_path in test_files:
       try:
           data, samplerate = sf.read(file_path)
           print(f"✅ {file_path}: {samplerate}Hz, {data.shape}")
       except Exception as e:
           print(f"❌ {file_path}: {e}")
   ```

3. **File Size Validation**
   ```python
   # Check file sizes are reasonable
   for file_path in expected_files:
       size_mb = os.path.getsize(file_path) / (1024 * 1024)
       assert 0.5 < size_mb < 10, f"Unusual file size: {file_path} ({size_mb:.2f}MB)"
       print(f"✅ {file_path}: {size_mb:.2f}MB")
   ```

#### 1.2 Configuration Validation

**Objective**: Verify the configuration system works correctly.

**Test Cases**:

1. **Import Test**
   ```python
   from samples.sample_config import (
       get_sample_audio_path,
       get_language_samples,
       validate_sample_files
   )
   print("✅ Configuration imports successful")
   ```

2. **Path Resolution Test**
   ```python
   # Test path resolution
   path = get_sample_audio_path("prompts/female_random_podcast.wav")
   assert os.path.exists(path), f"Path resolution failed: {path}"
   print(f"✅ Path resolution: {path}")
   ```

3. **Language Samples Test**
   ```python
   samples = get_language_samples()
   assert len(samples) >= 23, f"Expected 23+ languages, got {len(samples)}"
   
   # Test specific languages
   for lang in ["en", "es", "fr", "zh"]:
       assert lang in samples, f"Missing language: {lang}"
       assert os.path.exists(samples[lang]["audio"]), f"Missing audio for {lang}"
       print(f"✅ {lang}: {samples[lang]['audio']}")
   ```

### Phase 2: Integration Testing

#### 2.1 Application Startup

**Objective**: Verify the application starts correctly with local files.

**Test Cases**:

1. **Startup Validation**
   ```bash
   # Start the application
   python unified_webui.py
   
   # Check console output for:
   # ✅ All sample files are present and ready to use.
   # No import errors
   # No file not found errors
   ```

2. **Gradio Interface Loading**
   - Navigate to the web interface
   - Verify all tabs load correctly
   - Check that default audio files appear in UI

#### 2.2 Turbo TTS Testing

**Objective**: Verify Turbo TTS works with local sample files.

**Test Cases**:

1. **Default Sample Loading**
   - Navigate to "Chatterbox Turbo" tab
   - Verify the reference audio shows the local file
   - Check that the audio player loads correctly

2. **Speech Generation**
   ```python
   # Test with default sample
   text = "Hello, this is a test of the local sample system."
   # Generate speech and verify output
   ```

3. **Event Tags Testing**
   - Test with paralinguistic tags: `[chuckle]`, `[cough]`, etc.
   - Verify tags work with local samples

#### 2.3 Multilingual TTS Testing

**Objective**: Verify all 23+ languages work with local samples.

**Test Cases**:

1. **Language Switching**
   - Test switching between all languages
   - Verify audio and text update correctly
   - Check for any broken language configurations

2. **Speech Generation per Language**
   ```python
   # Test each language
   test_languages = ["en", "es", "fr", "de", "zh", "ja", "ar", "hi"]
   
   for lang in test_languages:
       text = "This is a test in " + lang
       # Generate speech and verify output
       print(f"✅ {lang}: Generated successfully")
   ```

3. **Language-Specific Features**
   - Test text normalization for different languages
   - Verify language-specific punctuation handling
   - Check for proper text-to-speech conversion

#### 2.4 Error Handling Testing

**Objective**: Verify the system handles errors gracefully.

**Test Cases**:

1. **Missing File Handling**
   - Temporarily rename a sample file
   - Restart application
   - Verify warning messages appear
   - Verify system still functions

2. **Corrupted File Handling**
   - Create a corrupted audio file
   - Test that system handles it gracefully
   - Verify error messages are user-friendly

3. **Invalid File Format**
   - Test with unsupported file formats
   - Verify proper error handling

### Phase 3: Performance Testing

#### 3.1 Loading Performance

**Objective**: Measure and compare loading times.

**Test Cases**:

1. **File Loading Speed**
   ```python
   import time
   
   # Test loading times
   start_time = time.time()
   # Load all sample files
   load_time = time.time() - start_time
   print(f"✅ Loading time: {load_time:.2f} seconds")
   assert load_time < 5.0, f"Loading too slow: {load_time:.2f}s"
   ```

2. **Startup Time Comparison**
   - Measure startup time with local files
   - Compare to previous remote URL loading time
   - Verify improvement

#### 3.2 Memory Usage

**Objective**: Monitor memory usage with local files.

**Test Cases**:

1. **Memory Footprint**
   - Monitor application memory usage
   - Verify no excessive memory consumption
   - Check for memory leaks

2. **File Caching**
   - Test file caching behavior
   - Verify efficient memory usage

### Phase 4: User Experience Testing

#### 4.1 Usability Testing

**Objective**: Verify the user experience is improved.

**Test Cases**:

1. **Offline Functionality**
   - Disconnect from internet
   - Verify all features still work
   - Test that no network requests are made

2. **Response Time**
   - Measure time from user action to response
   - Verify faster response times
   - Test with various user interactions

3. **Interface Responsiveness**
   - Test UI responsiveness
   - Verify smooth interactions
   - Check for any lag or delays

#### 4.2 Accessibility Testing

**Objective**: Verify the system is accessible to all users.

**Test Cases**:

1. **File Upload Functionality**
   - Test uploading custom audio files
   - Verify compatibility with user files
   - Test file format validation

2. **Error Messages**
   - Verify error messages are clear and helpful
   - Test that users can easily understand issues
   - Check for actionable error guidance

### Phase 5: Regression Testing

#### 5.1 Existing Functionality

**Objective**: Ensure no existing features are broken.

**Test Cases**:

1. **Voice Conversion (VC)**
   - Test VC functionality
   - Verify it still works with local samples
   - Test with different voice samples

2. **Original TTS**
   - Test original ChatterBox TTS
   - Verify compatibility with local files
   - Test all configuration options

3. **Advanced Features**
   - Test CFG weight settings
   - Test exaggeration settings
   - Test all advanced TTS features

#### 5.2 Compatibility Testing

**Objective**: Verify compatibility across different environments.

**Test Cases**:

1. **Operating Systems**
   - Test on Windows
   - Test on macOS
   - Test on Linux
   - Verify consistent behavior

2. **Python Versions**
   - Test with Python 3.10+
   - Verify compatibility
   - Check for version-specific issues

3. **Browser Compatibility**
   - Test Gradio interface in different browsers
   - Verify consistent UI behavior
   - Check for browser-specific issues

### Phase 6: Production Readiness

#### 6.1 Stress Testing

**Objective**: Verify the system handles high load.

**Test Cases**:

1. **Concurrent Users**
   - Test with multiple concurrent users
   - Verify system stability
   - Check for resource conflicts

2. **Long-running Tests**
   - Run system for extended periods
   - Monitor for memory leaks
   - Check for performance degradation

#### 6.2 Security Testing

**Objective**: Verify security of local file system.

**Test Cases**:

1. **File Permissions**
   - Verify proper file permissions
   - Check for security vulnerabilities
   - Test file access controls

2. **Input Validation**
   - Test with malicious file inputs
   - Verify proper input validation
   - Check for security issues

## Automated Testing Scripts

### Test Runner Script

```python
#!/usr/bin/env python3
"""
Automated test runner for local sample audio files implementation.
"""

import os
import sys
import unittest
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

class TestLocalSampleFiles(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment."""
        self.project_root = Path(__file__).parent
        self.samples_dir = self.project_root / "samples"
    
    def test_file_existence(self):
        """Test that all expected sample files exist."""
        expected_files = [
            "prompts/female_random_podcast.wav",
            "mtl_prompts/ar_f/ar_prompts2.flac",
            "mtl_prompts/en_f1.flac",
            # Add all other expected files
        ]
        
        for rel_path in expected_files:
            full_path = self.samples_dir / rel_path
            self.assertTrue(full_path.exists(), f"Missing file: {rel_path}")
    
    def test_configuration_imports(self):
        """Test that configuration modules import correctly."""
        try:
            from samples.sample_config import (
                get_sample_audio_path,
                get_language_samples,
                validate_sample_files
            )
            print("✅ Configuration imports successful")
        except ImportError as e:
            self.fail(f"Configuration import failed: {e}")
    
    def test_path_resolution(self):
        """Test path resolution functionality."""
        from samples.sample_config import get_sample_audio_path
        
        test_path = get_sample_audio_path("prompts/female_random_podcast.wav")
        self.assertTrue(os.path.exists(test_path), "Path resolution failed")
    
    def test_language_samples(self):
        """Test language sample configuration."""
        from samples.sample_config import get_language_samples
        
        samples = get_language_samples()
        self.assertGreaterEqual(len(samples), 23, "Expected 23+ languages")
        
        # Test specific languages
        for lang in ["en", "es", "fr", "zh"]:
            self.assertIn(lang, samples, f"Missing language: {lang}")
            self.assertTrue(
                os.path.exists(samples[lang]["audio"]), 
                f"Missing audio for {lang}"
            )
    
    def test_file_formats(self):
        """Test that audio files have correct formats."""
        import soundfile as sf
        
        test_files = [
            "prompts/female_random_podcast.wav",
            "mtl_prompts/en_f1.flac"
        ]
        
        for rel_path in test_files:
            full_path = self.samples_dir / rel_path
            try:
                data, samplerate = sf.read(str(full_path))
                self.assertGreater(samplerate, 0, f"Invalid sample rate for {rel_path}")
                self.assertGreater(len(data), 0, f"Empty audio data for {rel_path}")
            except Exception as e:
                self.fail(f"Failed to read {rel_path}: {e}")

def run_performance_tests():
    """Run performance tests."""
    print("\n=== Performance Tests ===")
    
    # Test loading performance
    start_time = time.time()
    from samples.sample_config import get_language_samples
    samples = get_language_samples()
    load_time = time.time() - start_time
    
    print(f"✅ Configuration loading time: {load_time:.3f} seconds")
    assert load_time < 1.0, f"Loading too slow: {load_time:.3f}s"

def main():
    """Run all tests."""
    print("=== Local Sample Audio Files Testing ===\n")
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance tests
    run_performance_tests()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()
```

### Continuous Integration Script

```yaml
# .github/workflows/test-local-samples.yml
name: Test Local Sample Files

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-local-samples:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -e .
        pip install soundfile unittest-xml-reporting
    
    - name: Download sample files
      run: |
        # Add commands to download sample files
        mkdir -p samples/prompts samples/mtl_prompts
        # wget or curl commands here
    
    - name: Run tests
      run: python tests/test_local_samples.py
    
    - name: Run performance tests
      run: python tests/test_performance.py
```

## Test Reporting

### Test Results Template

```
# Test Results Report

## Test Summary
- Total Tests: [X]
- Passed: [X]
- Failed: [X]
- Skipped: [X]

## Test Environment
- OS: [Operating System]
- Python: [Version]
- Dependencies: [List]

## Detailed Results

### Phase 1: Pre-Integration Testing
- [ ] File Existence: PASS/FAIL
- [ ] File Format Validation: PASS/FAIL
- [ ] Configuration Validation: PASS/FAIL

### Phase 2: Integration Testing
- [ ] Application Startup: PASS/FAIL
- [ ] Turbo TTS Testing: PASS/FAIL
- [ ] Multilingual TTS Testing: PASS/FAIL
- [ ] Error Handling: PASS/FAIL

### Phase 3: Performance Testing
- [ ] Loading Performance: PASS/FAIL
- [ ] Memory Usage: PASS/FAIL

### Phase 4: User Experience Testing
- [ ] Offline Functionality: PASS/FAIL
- [ ] Response Time: PASS/FAIL
- [ ] Interface Responsiveness: PASS/FAIL

### Phase 5: Regression Testing
- [ ] Existing Functionality: PASS/FAIL
- [ ] Compatibility Testing: PASS/FAIL

### Phase 6: Production Readiness
- [ ] Stress Testing: PASS/FAIL
- [ ] Security Testing: PASS/FAIL

## Issues Found
[List any issues discovered during testing]

## Recommendations
[Provide recommendations for improvements]

## Sign-off
- Tester: [Name]
- Date: [Date]
- Approval: [Yes/No]
```

## Success Criteria

The implementation is considered successful if:

1. ✅ All 23+ language samples work correctly
2. ✅ Turbo TTS functions with local files
3. ✅ Multilingual TTS works with all languages
4. ✅ Error handling is robust
5. ✅ Performance is improved
6. ✅ User experience is enhanced
7. ✅ No regressions in existing functionality
8. ✅ All tests pass
9. ✅ Documentation is complete
10. ✅ Code is maintainable

## Next Steps After Testing

1. **Address any failures** found during testing
2. **Optimize performance** if needed
3. **Update documentation** based on test results
4. **Prepare for deployment** to production
5. **Monitor in production** for any issues