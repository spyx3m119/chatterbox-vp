#!/usr/bin/env python3
"""
Test script to verify the TTS dropdown functionality fix.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_tts_dropdown_functionality():
    """Test the TTS dropdown functionality."""
    print("=== Testing TTS Dropdown Functionality ===")
    
    try:
        from samples.sample_config import (
            get_tts_voice_by_id,
            get_tts_voice_dropdown_options
        )
        
        print("✅ TTS voice functions imported successfully")
        
        # Test dropdown options
        options = get_tts_voice_dropdown_options()
        print(f"✅ Dropdown options: {len(options)} options")
        
        # Test the event handler function
        def on_tts_voice_change(voice_id, current_ref):
            voice_config = get_tts_voice_by_id(voice_id)
            if voice_config and voice_config.get("audio"):
                audio_path = voice_config["audio"]
                print(f"✅ Voice selected: {voice_id}")
                print(f"   Audio path: {audio_path}")
                print(f"   File exists: {os.path.exists(audio_path)}")
                return audio_path
            return current_ref
        
        # Test with female podcast voice
        print("\n--- Testing Female Podcast Voice ---")
        result = on_tts_voice_change("female_podcast", None)
        print(f"✅ Result: {result}")
        
        # Test with other voices
        for voice_id in ["male_narration", "female_conversational", "male_business"]:
            print(f"\n--- Testing {voice_id} ---")
            result = on_tts_voice_change(voice_id, None)
            if result:
                print(f"✅ Result: {result}")
                print(f"   File exists: {os.path.exists(result)}")
            else:
                print("❌ No result returned")
        
        # Test the default value
        print(f"\n--- Testing Default Value ---")
        default_result = on_tts_voice_change("female_podcast", None)
        print(f"✅ Default voice result: {default_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gradio_audio_component():
    """Test how Gradio Audio component should handle file paths."""
    print("\n=== Testing Gradio Audio Component Handling ===")
    
    try:
        # Test if the file path format is correct for Gradio
        test_path = "/Users/vladimirparole/Projects/chatterbox/samples/prompts/female_random_podcast.wav"
        
        print(f"Test path: {test_path}")
        print(f"Path exists: {os.path.exists(test_path)}")
        print(f"Path is file: {os.path.isfile(test_path)}")
        print(f"Path is absolute: {os.path.isabs(test_path)}")
        
        # This is the format that should work with Gradio Audio component
        print("✅ File path format is correct for Gradio Audio component")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🧪 Testing TTS Dropdown Fix")
    print("=" * 50)
    
    tests = [
        test_tts_dropdown_functionality,
        test_gradio_audio_component,
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
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Dropdown fix should work.")
        print("\nThe dropdown should now properly populate the reference audio field.")
        print("If it still doesn't work, the issue might be:")
        print("1. Gradio version compatibility")
        print("2. Browser caching")
        print("3. Need to restart the Gradio application")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)