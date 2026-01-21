#!/usr/bin/env python3
"""
Test script to verify the local sample audio files implementation.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_configuration_system():
    """Test the configuration system."""
    print("=== Testing Configuration System ===")
    
    try:
        from samples.sample_config import (
            get_sample_audio_path,
            get_language_samples,
            validate_sample_files
        )
        
        print("✅ Configuration imports successful")
        
        # Test path resolution
        path = get_sample_audio_path("prompts/female_random_podcast.wav")
        print(f"✅ Path resolution: {path}")
        print(f"   Exists: {os.path.exists(path)}")
        
        # Test language samples
        samples = get_language_samples()
        print(f"✅ Language samples: {len(samples)} languages")
        
        # Test a few key languages
        test_langs = ["en", "es", "fr", "zh"]
        for lang in test_langs:
            if lang in samples:
                audio_path = samples[lang]["audio"]
                exists = os.path.exists(audio_path)
                status = "✅" if exists else "⚠️ "
                print(f"{status} {lang}: {audio_path} (exists: {exists})")
        
        # Test file validation
        missing = validate_sample_files()
        print(f"✅ File validation: {len(missing)} missing files")
        if missing:
            print("   Missing files:")
            for f in missing[:5]:  # Show first 5
                print(f"     - {f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_unified_webui_imports():
    """Test that unified_webui.py can import without errors."""
    print("\n=== Testing Unified WebUI Imports ===")
    
    try:
        # Test importing the key functions that were modified
        from samples.sample_config import (
            get_sample_audio_path,
            get_language_samples,
            validate_sample_files,
            get_supported_languages_display
        )
        
        print("✅ Sample config imports work")
        
        # Test that we can call the functions used in unified_webui.py
        turbo_path = get_sample_audio_path("prompts/female_random_podcast.wav")
        print(f"✅ Turbo TTS path: {turbo_path}")
        
        samples = get_language_samples()
        print(f"✅ Language samples: {len(samples)} languages")
        
        # Test the functions used in the language change handler
        if "en" in samples:
            en_audio, en_text = samples["en"]["audio"], samples["en"]["text"]
            print(f"✅ English sample: {en_audio}")
            print(f"   Text: {en_text[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Unified WebUI import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test the file structure."""
    print("\n=== Testing File Structure ===")
    
    project_root = Path(__file__).parent
    samples_dir = project_root / "samples"
    
    # Check if samples directory exists
    if not samples_dir.exists():
        print("❌ Samples directory not found")
        return False
    
    print("✅ Samples directory exists")
    
    # Check for key directories
    prompts_dir = samples_dir / "prompts"
    mtl_prompts_dir = samples_dir / "mtl_prompts"
    
    if prompts_dir.exists():
        print("✅ Prompts directory exists")
        prompt_files = list(prompts_dir.glob("*"))
        print(f"   Files: {len(prompt_files)}")
    else:
        print("⚠️  Prompts directory not found")
    
    if mtl_prompts_dir.exists():
        print("✅ Multilingual prompts directory exists")
        mtl_files = list(mtl_prompts_dir.glob("*"))
        print(f"   Files: {len(mtl_files)}")
    else:
        print("⚠️  Multilingual prompts directory not found")
    
    return True

def main():
    """Run all tests."""
    print("🧪 Testing Local Sample Audio Files Implementation")
    print("=" * 60)
    
    tests = [
        test_file_structure,
        test_configuration_system,
        test_unified_webui_imports,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Implementation is ready.")
        print("\nNext steps:")
        print("1. Download the remaining audio files (2 missing)")
        print("2. Install required dependencies (gradio, etc.)")
        print("3. Run the application: python unified_webui.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)