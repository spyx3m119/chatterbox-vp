# User Guide: Sample Reference Audio Files

## Overview

ChatterBox TTS now includes local sample reference audio files to help you get started with text-to-speech synthesis. These files provide example voices that you can use as references for voice cloning and style transfer.

## What Are Sample Audio Files?

Sample audio files are pre-recorded voice samples that serve as references for the TTS system. When you use a sample file as a reference:

- **Voice Cloning**: The system analyzes the voice characteristics
- **Style Transfer**: The generated speech adopts similar speaking style
- **Language Matching**: For multilingual TTS, samples help with language-specific pronunciation

## Using Sample Audio Files

### In the WebUI

1. **Open ChatterBox WebUI**: Launch the unified web interface
2. **Select a TTS Mode**: Choose from Chatterbox TTS, Turbo, or Multilingual
3. **Use Default Samples**: Each mode comes with pre-loaded sample files
4. **Upload Your Own**: Replace samples with your own audio files

### Available Sample Categories

#### 1. General TTS Samples (`samples/prompts/`)
- **female_random_podcast.wav**: Female voice sample for general use
- Use with: Chatterbox TTS and Chatterbox Turbo

#### 2. Multilingual Samples (`samples/mtl_prompts/`)
Supports 23+ languages including:
- **Arabic (ar)**: Arabic female voice
- **English (en)**: English female voice
- **Spanish (es)**: Spanish female voice
- **French (fr)**: French female voice
- **Chinese (zh)**: Chinese female voice
- **And many more...**

## Adding Your Own Sample Files

### Step 1: Prepare Your Audio

Ensure your audio files meet these requirements:
- **Format**: WAV or FLAC
- **Sample Rate**: 16kHz or 24kHz
- **Channels**: Mono (single channel)
- **Duration**: 5-10 seconds
- **Quality**: Clear speech, minimal background noise

### Step 2: Place Files in Correct Directory

```
samples/
├── prompts/           # General TTS samples
│   ├── your_sample.wav
│   └── another_sample.flac
└── mtl_prompts/       # Multilingual samples
    ├── en_your_voice.wav
    ├── es_tu_voz.wav
    └── fr_ta_voix.wav
```

### Step 3: Update Configuration

Edit `samples/sample_config.md` to add your samples:

```python
# For general TTS
TTS_DEFAULT_CONFIG = {
    "audio": "prompts/your_sample.wav",
    "text": "Your sample text here"
}

# For multilingual TTS
LANGUAGE_CONFIG["en"] = {
    "audio": "mtl_prompts/en_your_voice.wav",
    "text": "Your English sample text"
}
```

## Best Practices

### Choosing Good Reference Audio

1. **Clear Speech**: Use recordings with clear, understandable speech
2. **Consistent Volume**: Avoid recordings with volume fluctuations
3. **Minimal Noise**: Use quiet environments or noise-cancellation
4. **Natural Pace**: Speak at a natural, conversational pace
5. **Good Quality**: Use good microphones and recording equipment

### Voice Cloning Tips

1. **Match Language**: Use samples in the same language as your text
2. **Similar Style**: Choose samples with similar speaking style to your desired output
3. **Duration Matters**: Longer samples (8-10 seconds) provide better voice cloning
4. **Multiple Samples**: Try different samples to find the best match

## Troubleshooting

### Common Issues

**Sample File Not Found**
- Check file exists in correct location
- Verify file path in configuration
- Ensure proper file permissions

**Poor Voice Quality**
- Try different sample files
- Check audio quality and format
- Ensure sample matches target language

**Long Loading Times**
- Use smaller file sizes (under 10MB)
- Convert to appropriate format (WAV/FLAC)
- Check file corruption

### Getting Help

If you encounter issues:

1. Check file format requirements
2. Verify file paths are correct
3. Test with provided sample files
4. Consult the technical documentation
5. Report issues on GitHub

## Advanced Usage

### Custom Language Support

To add support for new languages:

1. Add language code and name to `SUPPORTED_LANGUAGES`
2. Create sample audio file in `samples/mtl_prompts/`
3. Add configuration entry
4. Test with sample text in target language

### Batch Processing

For multiple samples:

```python
# Process multiple files
import os
from samples.sample_config import get_sample_audio_path

sample_files = os.listdir("samples/prompts/")
for file in sample_files:
    if file.endswith(('.wav', '.flac')):
        audio_path = get_sample_audio_path(f"prompts/{file}")
        # Process with your TTS model
```

## File Management

### Organizing Samples

- **By Language**: Group files by language in subdirectories
- **By Speaker**: Organize by speaker characteristics
- **By Use Case**: Separate samples for different applications

### Backup and Sharing

- **Backup**: Keep copies of important sample files
- **Sharing**: Share sample files with team members
- **Version Control**: Track changes to sample configurations

## Examples

### Basic Usage

```python
from chatterbox.tts import ChatterboxTTS

# Load model
model = ChatterboxTTS.from_pretrained("cuda")

# Use sample file
sample_path = "samples/prompts/female_random_podcast.wav"
text = "Hello, this is a test of the TTS system."

# Generate speech
wav = model.generate(text, audio_prompt_path=sample_path)
```

### Multilingual Example

```python
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

# Load model
model = ChatterboxMultilingualTTS.from_pretrained("cuda")

# Generate French speech
french_text = "Bonjour, comment allez-vous?"
wav = model.generate(french_text, language_id="fr", audio_prompt_path="samples/mtl_prompts/fr_f1.flac")
```

## Contributing

We welcome contributions of new sample files:

1. Follow file format requirements
2. Include appropriate metadata
3. Test with the TTS system
4. Submit via GitHub pull request
5. Include language and speaker information

## Legal Considerations

- **Copyright**: Ensure you have rights to use sample audio
- **Privacy**: Don't use recordings without consent
- **Licensing**: Follow appropriate licensing for distribution
- **Attribution**: Credit original speakers when appropriate

## Additional Resources

- [Technical Documentation](sample_config.md)
- [Implementation Plan](IMPLEMENTATION_PLAN.md)
- [File Format Specifications](README.md)
- [GitHub Repository](https://github.com/resemble-ai/chatterbox)