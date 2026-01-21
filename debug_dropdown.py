#!/usr/bin/env python3
"""
Debug script to investigate why the TTS dropdown change event isn't triggering.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def debug_dropdown_event():
    """Debug the dropdown event handler."""
    print("=== Debugging TTS Dropdown Event Handler ===")
    
    try:
        from samples.sample_config import (
            get_tts_voice_by_id,
            get_tts_voice_dropdown_options
        )
        
        print("✅ TTS voice functions imported successfully")
        
        # Test the exact event handler function
        def on_tts_voice_change(voice_id, current_ref):
            print(f"🔄 Dropdown change triggered!")
            print(f"   Voice ID: {voice_id}")
            print(f"   Current ref: {current_ref}")
            
            voice_config = get_tts_voice_by_id(voice_id)
            print(f"   Voice config: {voice_config}")
            
            if voice_config and voice_config.get("audio"):
                audio_path = voice_config["audio"]
                print(f"   Audio path: {audio_path}")
                print(f"   File exists: {os.path.exists(audio_path)}")
                return audio_path
            else:
                print(f"   No audio found for voice: {voice_id}")
                return current_ref
        
        # Test with different voices
        test_voices = ["female_podcast", "male_narration"]
        
        for voice_id in test_voices:
            print(f"\n--- Testing {voice_id} ---")
            result = on_tts_voice_change(voice_id, "/Users/vladimirparole/Projects/chatterbox/samples/prompts/female_random_podcast.wav")
            print(f"   Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def compare_with_multilingual():
    """Compare with working multilingual TTS dropdown."""
    print("\n=== Comparing with Multilingual TTS Dropdown ===")
    
    try:
        from samples.sample_config import get_language_samples
        
        # Test multilingual dropdown handler
        def on_language_change(lang, current_ref, current_text):
            print(f"🔄 Multilingual dropdown change triggered!")
            print(f"   Language: {lang}")
            print(f"   Current ref: {current_ref}")
            
            samples = get_language_samples()
            result = samples[lang]["audio"], samples[lang]["text"]
            print(f"   Result: {result}")
            return result
        
        # Test with English
        print("--- Testing English language change ---")
        result = on_language_change("en", None, None)
        print(f"   Multilingual result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_gradio_audio_format():
    """Check if the audio format is correct for Gradio."""
    print("\n=== Checking Gradio Audio Format ===")
    
    try:
        test_path = "/Users/vladimirparole/Projects/chatterbox/samples/prompts/female_random_podcast.wav"
        
        print(f"Test path: {test_path}")
        print(f"Path exists: {os.path.exists(test_path)}")
        print(f"Path is file: {os.path.isfile(test_path)}")
        print(f"Path is absolute: {os.path.isabs(test_path)}")
        
        # Check if this is the format Gradio expects
        print("✅ File path format should work with Gradio Audio component")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all debug tests."""
    print("🐛 Debugging TTS Dropdown Issue")
    print("=" * 50)
    
    tests = [
        debug_dropdown_event,
        compare_with_multilingual,
        check_gradio_audio_format,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Debug Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All debug tests passed!")
        print("\nThe issue might be:")
        print("1. Gradio version compatibility")
        print("2. Browser caching issues")
        print("3. Event handler not properly connected")
        print("4. Need to restart Gradio application")
    else:
        print("⚠️  Some debug tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)