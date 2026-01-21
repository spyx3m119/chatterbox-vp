# Sample Audio Configuration for ChatterBox TTS

This module provides configuration and utilities for managing sample reference audio files.

## Configuration Structure

The sample audio files are organized in the `samples/` directory with the following structure:

- `samples/prompts/` - General TTS reference prompts
- `samples/mtl_prompts/` - Multilingual TTS reference prompts organized by language

## Usage

```python
from samples.sample_config import get_sample_audio_path, get_language_samples

# Get path to general TTS sample
tts_sample = get_sample_audio_path("prompts/female_random_podcast.wav")

# Get all multilingual samples
mtl_samples = get_language_samples();

# Get specific language sample
fr_sample = get_sample_audio_path("mtl_prompts/fr_f1.flac")
```

## Adding New Samples

1. Add audio files to the appropriate directory in `samples/`
2. Ensure files meet the requirements:
   - WAV or FLAC format
   - 16kHz or 24kHz sample rate
   - Mono channel
   - 5-10 seconds duration
   - Clear speech quality

3. Update any relevant configuration if needed

## File Format Requirements

- **Formats**: WAV, FLAC
- **Sample Rates**: 16kHz, 24kHz
- **Channels**: Mono
- **Duration**: 5-10 seconds
- **Quality**: High quality, clear speech

## Language Configuration

The multilingual TTS system supports 23+ languages with pre-configured sample audio files and text:

- Arabic (ar), Danish (da), German (de), Greek (el), English (en)
- Spanish (es), Finnish (fi), French (fr), Hebrew (he), Hindi (hi)
- Italian (it), Japanese (ja), Korean (ko), Malay (ms), Dutch (nl)
- Norwegian (no), Polish (pl), Portuguese (pt), Russian (ru), Swedish (sv)
- Swahili (sw), Turkish (tr), Chinese (zh)

Each language includes:
- Sample audio file for voice reference
- Sample text in the target language