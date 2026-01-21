#!/usr/bin/env python3
"""
Test script to verify Chatterbox Turbo functionality without HF_TOKEN
This script tests whether the models can be loaded and used without authentication.
After the fix, models should work without requiring Hugging Face tokens.
"""

import os
import sys
import torch
import tempfile
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_without_token():
    """Test loading models without HF_TOKEN environment variable"""
    logger.info("Testing Chatterbox models without HF_TOKEN...")
    
    # Ensure HF_TOKEN is not set
    original_token = os.environ.get('HF_TOKEN')
    if 'HF_TOKEN' in os.environ:
        del os.environ['HF_TOKEN']
        logger.info("Removed existing HF_TOKEN from environment")
    
    try:
        # Test 1: Import the models
        logger.info("1. Testing imports...")
        from chatterbox.tts_turbo import ChatterboxTurboTTS
        from chatterbox.tts import ChatterboxTTS
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        logger.info("✓ All imports successful")
        
        # Test 2: Check device availability
        logger.info("2. Checking device availability...")
        if torch.cuda.is_available():
            device = "cuda"
            logger.info("✓ CUDA available")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = "mps"
            logger.info("✓ MPS available")
        else:
            device = "cpu"
            logger.info("✓ Using CPU")
        
        # Test 3: Test model loading (this will trigger download if needed)
        logger.info("3. Testing model loading...")
        
        # Test with a temporary directory to avoid downloading to default location
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set HF_HOME to temp directory to avoid polluting user's cache
            original_hf_home = os.environ.get('HF_HOME')
            os.environ['HF_HOME'] = temp_dir
            
            try:
                # Test ChatterboxTurboTTS
                logger.info("   Testing ChatterboxTurboTTS...")
                try:
                    turbo_model = ChatterboxTurboTTS.from_pretrained(device)
                    logger.info("   ✓ ChatterboxTurboTTS loaded successfully")
                    turbo_available = True
                except Exception as e:
                    logger.error(f"   ✗ ChatterboxTurboTTS failed: {e}")
                    turbo_available = False
                
                # Test ChatterboxTTS
                logger.info("   Testing ChatterboxTTS...")
                try:
                    tts_model = ChatterboxTTS.from_pretrained(device)
                    logger.info("   ✓ ChatterboxTTS loaded successfully")
                    tts_available = True
                except Exception as e:
                    logger.error(f"   ✗ ChatterboxTTS failed: {e}")
                    tts_available = False
                
                # Test ChatterboxMultilingualTTS
                logger.info("   Testing ChatterboxMultilingualTTS...")
                try:
                    mtl_model = ChatterboxMultilingualTTS.from_pretrained(device)
                    logger.info("   ✓ ChatterboxMultilingualTTS loaded successfully")
                    mtl_available = True
                except Exception as e:
                    logger.error(f"   ✗ ChatterboxMultilingualTTS failed: {e}")
                    mtl_available = False
                
            finally:
                # Restore original HF_HOME
                if original_hf_home:
                    os.environ['HF_HOME'] = original_hf_home
                elif 'HF_HOME' in os.environ:
                    del os.environ['HF_HOME']
        
        # Test 4: Summary
        logger.info("4. Test Summary:")
        logger.info(f"   ChatterboxTurboTTS: {'✓ Available' if turbo_available else '✗ Not available'}")
        logger.info(f"   ChatterboxTTS: {'✓ Available' if tts_available else '✗ Not available'}")
        logger.info(f"   ChatterboxMultilingualTTS: {'✓ Available' if mtl_available else '✗ Not available'}")
        
        # Determine if token is required
        all_available = turbo_available and tts_available and mtl_available
        if all_available:
            logger.info("\n🎉 CONCLUSION: All models work without HF_TOKEN - token is NOT required!")
            return True
        else:
            logger.info("\n⚠️  CONCLUSION: Some models require HF_TOKEN - token may be required")
            return False
            
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Please ensure all dependencies are installed")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False
    finally:
        # Restore original token if it existed
        if original_token:
            os.environ['HF_TOKEN'] = original_token

def test_with_token():
    """Test loading models with a dummy token to see if it makes a difference"""
    logger.info("\nTesting with dummy HF_TOKEN...")
    
    # Set a dummy token
    os.environ['HF_TOKEN'] = 'dummy_token_for_testing'
    
    try:
        from chatterbox.tts_turbo import ChatterboxTurboTTS
        
        # Test with a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            original_hf_home = os.environ.get('HF_HOME')
            os.environ['HF_HOME'] = temp_dir
            
            try:
                logger.info("Testing ChatterboxTurboTTS with dummy token...")
                model = ChatterboxTurboTTS.from_pretrained("cpu")
                logger.info("✓ Model loaded successfully with dummy token")
                return True
            except Exception as e:
                logger.error(f"✗ Model failed with dummy token: {e}")
                return False
            finally:
                if original_hf_home:
                    os.environ['HF_HOME'] = original_hf_home
                elif 'HF_HOME' in os.environ:
                    del os.environ['HF_HOME']
                    
    except Exception as e:
        logger.error(f"Error testing with token: {e}")
        return False
    finally:
        # Remove the dummy token
        if 'HF_TOKEN' in os.environ:
            del os.environ['HF_TOKEN']

if __name__ == "__main__":
    print("Chatterbox Token Functionality Test")
    print("=" * 50)
    
    # Test without token
    works_without_token = test_without_token()
    
    # Test with token (optional, to see if there's any difference)
    works_with_token = test_with_token()
    
    print("\n" + "=" * 50)
    print("FINAL RESULTS:")
    print(f"Works without HF_TOKEN: {'✓ Yes' if works_without_token else '✗ No'}")
    print(f"Works with dummy HF_TOKEN: {'✓ Yes' if works_with_token else '✗ No'}")
    
    if works_without_token:
        print("\n✅ CONCLUSION: HF_TOKEN is NOT required for Chatterbox functionality!")
        print("The models can be used without any API token authentication.")
        sys.exit(0)
    else:
        print("\n❌ CONCLUSION: HF_TOKEN appears to be required for some functionality.")
        print("Further investigation needed.")
        sys.exit(1)
