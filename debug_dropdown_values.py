#!/usr/bin/env python3
"""
Debug script to test dropdown value handling
"""

import sys
sys.path.insert(0, '.')

from samples.sample_config import get_tts_voice_dropdown_options, get_tts_voice_by_id

def test_dropdown_value(value):
    """Test what happens when a value is received from dropdown"""
    print(f"🔄 Received dropdown value: '{value}'")
    print(f"   Type: {type(value)}")
    print(f"   Length: {len(str(value))}")
    
    # Try to find the voice config
    voice_config = get_tts_voice_by_id(value)
    if voice_config:
        print(f"   ✅ Found voice config: {voice_config['name']}")
        return voice_config['audio']
    else:
        print(f"   ❌ No voice found for: {value}")
        
        # Try to find by name instead
        options = get_tts_voice_dropdown_options()
        for voice_id, display_text in options:
            if display_text == value:
                print(f"   🔍 Found by display text! Voice ID: {voice_id}")
                voice_config = get_tts_voice_by_id(voice_id)
                return voice_config['audio']
        
        return None

if __name__ == "__main__":
    print("=== Testing Dropdown Value Handling ===")
    
    # Test with actual values
    test_values = [
        "female_podcast",
        "male_narration", 
        "Female Podcast Voice - Clear female voice with podcast-style delivery",
        "Male Narration Voice - Deep male voice with narrative style"
    ]
    
    for value in test_values:
        print(f"\n--- Testing: {value} ---")
        result = test_dropdown_value(value)
        print(f"Result: {result}")