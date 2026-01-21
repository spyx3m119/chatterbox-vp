# ChatterBox Sample Audio Files

This directory contains sample reference audio files for the ChatterBox TTS system.

## Directory Structure

```
samples/
├── README.md                    # This file
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

## Usage

These sample files are used by the ChatterBox TTS system to provide reference voices for:

- **ChatterBox TTS**: General text-to-speech with voice cloning
- **ChatterBox Turbo**: Fast TTS with paralinguistic tags
- **ChatterBox Multilingual**: Multilingual TTS supporting 23+ languages

## Adding New Sample Files

1. Place new audio files in the appropriate subdirectory
2. Update the configuration in `unified_webui.py` to include the new files
3. Ensure audio files are:
   - High quality (16kHz or 24kHz sample rate recommended)
   - At least 5 seconds long
   - Clear speech without background noise
   - Properly licensed for distribution

## File Format Requirements

- **Format**: WAV or FLAC
- **Sample Rate**: 16kHz or 24kHz
- **Channels**: Mono (single channel)
- **Duration**: Minimum 5 seconds, maximum 10 seconds
- **Quality**: High quality, clear speech

## License

These sample files are provided under the same license as the ChatterBox project.