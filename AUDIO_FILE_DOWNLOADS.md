# Audio File Downloads for ChatterBox TTS

## Overview

This document provides the list of audio files that need to be downloaded from Google Cloud Storage and placed in the local `samples/` directory.

## Download URLs

### General TTS Sample

**File**: `samples/prompts/female_random_podcast.wav`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/prompts/female_random_podcast.wav`

### Multilingual TTS Samples

**File**: `samples/mtl_prompts/ar_f/ar_prompts2.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ar_f/ar_prompts2.flac`

**File**: `samples/mtl_prompts/da_m1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/da_m1.flac`

**File**: `samples/mtl_prompts/de_f1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/de_f1.flac`

**File**: `samples/mtl_prompts/el_m.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/el_m.flac`

**File**: `samples/mtl_prompts/en_f1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/en_f1.flac`

**File**: `samples/mtl_prompts/es_f1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/es_f1.flac`

**File**: `samples/mtl_prompts/fi_m.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/fi_m.flac`

**File**: `samples/mtl_prompts/fr_f1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/fr_f1.flac`

**File**: `samples/mtl_prompts/he_m1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/he_m1.flac`

**File**: `samples/mtl_prompts/hi_f1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/hi_f1.flac`

**File**: `samples/mtl_prompts/it_m1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/it_m1.flac`

**File**: `samples/mtl_prompts/ja/ja_prompts1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ja/ja_prompts1.flac`

**File**: `samples/mtl_prompts/ko_f.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ko_f.flac`

**File**: `samples/mtl_prompts/ms_f.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ms_f.flac`

**File**: `samples/mtl_prompts/nl_m.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/nl_m.flac`

**File**: `samples/mtl_prompts/no_f1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/no_f1.flac`

**File**: `samples/mtl_prompts/pl_m.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/pl_m.flac`

**File**: `samples/mtl_prompts/pt_m1.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/pt_m1.flac`

**File**: `samples/mtl_prompts/ru_m.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ru_m.flac`

**File**: `samples/mtl_prompts/sv_f.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/sv_f.flac`

**File**: `samples/mtl_prompts/sw_m.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/sw_m.flac`

**File**: `samples/mtl_prompts/tr_m.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/tr_m.flac`

**File**: `samples/mtl_prompts/zh_f2.flac`
**URL**: `https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/zh_f2.flac`

## Download Methods

### Method 1: Using wget (Recommended)

```bash
# Create directories
mkdir -p samples/prompts
mkdir -p samples/mtl_prompts/ar_f
mkdir -p samples/mtl_prompts/ja

# Download general TTS sample
wget -O samples/prompts/female_random_podcast.wav "https://storage.googleapis.com/chatterbox-demo-samples/prompts/female_random_podcast.wav"

# Download multilingual samples
wget -O samples/mtl_prompts/ar_f/ar_prompts2.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ar_f/ar_prompts2.flac"
wget -O samples/mtl_prompts/da_m1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/da_m1.flac"
wget -O samples/mtl_prompts/de_f1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/de_f1.flac"
wget -O samples/mtl_prompts/el_m.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/el_m.flac"
wget -O samples/mtl_prompts/en_f1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/en_f1.flac"
wget -O samples/mtl_prompts/es_f1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/es_f1.flac"
wget -O samples/mtl_prompts/fi_m.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/fi_m.flac"
wget -O samples/mtl_prompts/fr_f1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/fr_f1.flac"
wget -O samples/mtl_prompts/he_m1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/he_m1.flac"
wget -O samples/mtl_prompts/hi_f1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/hi_f1.flac"
wget -O samples/mtl_prompts/it_m1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/it_m1.flac"
wget -O samples/mtl_prompts/ja/ja_prompts1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ja/ja_prompts1.flac"
wget -O samples/mtl_prompts/ko_f.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ko_f.flac"
wget -O samples/mtl_prompts/ms_f.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ms_f.flac"
wget -O samples/mtl_prompts/nl_m.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/nl_m.flac"
wget -O samples/mtl_prompts/no_f1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/no_f1.flac"
wget -O samples/mtl_prompts/pl_m.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/pl_m.flac"
wget -O samples/mtl_prompts/pt_m1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/pt_m1.flac"
wget -O samples/mtl_prompts/ru_m.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ru_m.flac"
wget -O samples/mtl_prompts/sv_f.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/sv_f.flac"
wget -O samples/mtl_prompts/sw_m.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/sw_m.flac"
wget -O samples/mtl_prompts/tr_m.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/tr_m.flac"
wget -O samples/mtl_prompts/zh_f2.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/zh_f2.flac"
```

### Method 2: Using curl

```bash
# Download general TTS sample
curl -L -o samples/prompts/female_random_podcast.wav "https://storage.googleapis.com/chatterbox-demo-samples/prompts/female_random_podcast.wav"

# Download multilingual samples (example for one file)
curl -L -o samples/mtl_prompts/en_f1.flac "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/en_f1.flac"
```

### Method 3: Using Python

```python
import os
import requests

# Create directories
os.makedirs("samples/prompts", exist_ok=True)
os.makedirs("samples/mtl_prompts/ar_f", exist_ok=True)
os.makedirs("samples/mtl_prompts/ja", exist_ok=True)

# URLs and file paths
files_to_download = [
    ("https://storage.googleapis.com/chatterbox-demo-samples/prompts/female_random_podcast.wav", "samples/prompts/female_random_podcast.wav"),
    ("https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ar_f/ar_prompts2.flac", "samples/mtl_prompts/ar_f/ar_prompts2.flac"),
    ("https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/en_f1.flac", "samples/mtl_prompts/en_f1.flac"),
    # Add more URLs as needed
]

# Download files
for url, filepath in files_to_download:
    print(f"Downloading {filepath}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Downloaded {filepath}")

print("All downloads completed!")
```

### Method 4: Using gsutil (Google Cloud SDK)

```bash
# Install Google Cloud SDK if not already installed
# Then use gsutil to download files

gsutil cp gs://chatterbox-demo-samples/prompts/female_random_podcast.wav samples/prompts/

gsutil cp gs://chatterbox-demo-samples/mtl_prompts/ar_f/ar_prompts2.flac samples/mtl_prompts/ar_f/
gsutil cp gs://chatterbox-demo-samples/mtl_prompts/en_f1.flac samples/mtl_prompts/
# Add more commands as needed
```

## File Verification

After downloading, verify the files:

```bash
# Check file sizes
ls -lh samples/prompts/
ls -lh samples/mtl_prompts/

# Verify audio files can be played
# (Use your preferred audio player or tool)

# Check file formats
file samples/prompts/female_random_podcast.wav
file samples/mtl_prompts/en_f1.flac
```

## Expected File Sizes

- **General TTS sample**: ~2-5 MB
- **Multilingual samples**: ~1-3 MB each
- **Total download size**: ~50-80 MB

## Troubleshooting

### Download Issues

1. **Network Timeout**: Try downloading files individually
2. **Permission Denied**: Ensure you have write permissions to the samples directory
3. **File Not Found**: Verify the URL is correct
4. **Incomplete Downloads**: Check file sizes and re-download if necessary

### File Format Issues

1. **Corrupted Files**: Re-download the file
2. **Wrong Format**: Verify the file extension matches the expected format
3. **Playback Issues**: Test with different audio players

## Next Steps

After downloading all audio files:

1. **Verify all files are present** in the correct directories
2. **Test a few files** to ensure they play correctly
3. **Update `unified_webui.py`** to use local file paths
4. **Test the TTS system** with local samples
5. **Validate multilingual functionality** with all language samples

## Notes

- All files should be downloaded to the `samples/` directory at the project root
- Ensure the directory structure matches the expected layout
- Files are provided in WAV and FLAC formats for compatibility
- All files are licensed for use with ChatterBox TTS