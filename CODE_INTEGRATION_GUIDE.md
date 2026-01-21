# Code Integration Guide for Local Sample Audio Files

## Overview

This guide provides step-by-step instructions for updating the ChatterBox TTS system to use local sample audio files instead of remote Google Cloud URLs.

## Prerequisites

Before starting the integration:

1. **Complete the setup**:
   - [x] Created `samples/` directory structure
   - [x] Downloaded all audio files from Google Cloud
   - [x] Verified file integrity and format

2. **Backup your current code**:
   ```bash
   # Create a backup of unified_webui.py
   cp unified_webui.py unified_webui.py.backup
   ```

## Integration Steps

### Step 1: Add Configuration Imports

**Location**: `unified_webui.py` (after existing imports)

**Current Code**:
```python
import random
import numpy as np
import torch
import gradio as gr
from chatterbox.tts import ChatterboxTTS
from chatterbox.tts_turbo import ChatterboxTurboTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS, SUPPORTED_LANGUAGES
from chatterbox.vc import ChatterboxVC
```

**Updated Code**:
```python
import random
import numpy as np
import torch
import gradio as gr
from chatterbox.tts import ChatterboxTTS
from chatterbox.tts_turbo import ChatterboxTurboTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS, SUPPORTED_LANGUAGES
from chatterbox.vc import ChatterboxVC

# Import sample audio configuration
from samples.sample_config import (
    get_sample_audio_path,
    get_language_samples,
    validate_sample_files,
    get_supported_languages_display
)
```

### Step 2: Update Turbo TTS Default Audio

**Location**: `unified_webui.py` (around line 553)

**Current Code**:
```python
turbo_ref_wav = gr.Audio(
    sources=["upload", "microphone"],
    type="filepath",
    label="Reference Audio File",
    value="https://storage.googleapis.com/chatterbox-demo-samples/prompts/female_random_podcast.wav"
)
```

**Updated Code**:
```python
turbo_ref_wav = gr.Audio(
    sources=["upload", "microphone"],
    type="filepath",
    label="Reference Audio File",
    value=get_sample_audio_path("prompts/female_random_podcast.wav")
)
```

### Step 3: Update Multilingual TTS Language Configuration

**Location**: `unified_webui.py` (around line 19-112)

**Current Code**:
```python
LANGUAGE_CONFIG = {
    "ar": {
        "audio": "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/ar_f/ar_prompts2.flac",
        "text": "في الشهر الماضي، وصلنا إلى معلم جديد بمليارين من المشاهدات على قناتنا على يوتيوب."
    },
    "da": {
        "audio": "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/da_m1.flac",
        "text": "Sidste måned nåede vi en ny milepæl med to milliarder visninger på vores YouTube-kanal."
    },
    # ... (all other languages with remote URLs)
}
```

**Updated Code**:
```python
LANGUAGE_CONFIG = {
    "ar": {
        "audio": get_sample_audio_path("mtl_prompts/ar_f/ar_prompts2.flac"),
        "text": "في الشهر الماضي، وصلنا إلى معلم جديد بمليارين من المشاهدات على قناتنا على يوتيوب."
    },
    "da": {
        "audio": get_sample_audio_path("mtl_prompts/da_m1.flac"),
        "text": "Sidste måned nåede vi en ny milepæl med to milliarder visninger på vores YouTube-kanal."
    },
    "de": {
        "audio": get_sample_audio_path("mtl_prompts/de_f1.flac"),
        "text": "Letzten Monat haben wir einen neuen Meilenstein erreicht: zwei Milliarden Aufrufe auf unserem YouTube-Kanal."
    },
    "el": {
        "audio": get_sample_audio_path("mtl_prompts/el_m.flac"),
        "text": "Τον περασμένο μήνα, φτάσαμε σε ένα νέο ορόσημο με δύο δισεκατομμύρια προβολές στο κανάλι μας στο YouTube."
    },
    "en": {
        "audio": get_sample_audio_path("mtl_prompts/en_f1.flac"),
        "text": "Last month, we reached a new milestone with two billion views on our YouTube channel."
    },
    "es": {
        "audio": get_sample_audio_path("mtl_prompts/es_f1.flac"),
        "text": "El mes pasado alcanzamos un nuevo hito: dos mil millones de visualizaciones en nuestro canal de YouTube."
    },
    "fi": {
        "audio": get_sample_audio_path("mtl_prompts/fi_m.flac"),
        "text": "Viime kuussa saavutimme uuden virstanpylvään kahden miljardin katselukerran kanssa YouTube-kanavallamme."
    },
    "fr": {
        "audio": get_sample_audio_path("mtl_prompts/fr_f1.flac"),
        "text": "Le mois dernier, nous avons atteint un nouveau jalon avec deux milliards de vues sur notre chaîne YouTube."
    },
    "he": {
        "audio": get_sample_audio_path("mtl_prompts/he_m1.flac"),
        "text": "בחודש שעבר הגענו לאבן דרך חדשה עם שני מיליארד צפיות בערוץ היוטיוב שלנו."
    },
    "hi": {
        "audio": get_sample_audio_path("mtl_prompts/hi_f1.flac"),
        "text": "पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो अरब व्यूज़।"
    },
    "it": {
        "audio": get_sample_audio_path("mtl_prompts/it_m1.flac"),
        "text": "Il mese scorso abbiamo raggiunto un nuovo traguardo: due miliardi di visualizzazioni sul nostro canale YouTube."
    },
    "ja": {
        "audio": get_sample_audio_path("mtl_prompts/ja/ja_prompts1.flac"),
        "text": "先月、私たちのYouTubeチャンネルで二十億回の再生回数という新たなマイルストーンに到達しました。"
    },
    "ko": {
        "audio": get_sample_audio_path("mtl_prompts/ko_f.flac"),
        "text": "지난달 우리는 유튜브 채널에서 이십억 조회수라는 새로운 이정표에 도달했습니다."
    },
    "ms": {
        "audio": get_sample_audio_path("mtl_prompts/ms_f.flac"),
        "text": "Bulan lepas, kami mencapai pencapaian baru dengan dua bilion tontonan di saluran YouTube kami."
    },
    "nl": {
        "audio": get_sample_audio_path("mtl_prompts/nl_m.flac"),
        "text": "Vorige maand bereikten we een nieuwe mijlpaal met twee miljard weergaven op ons YouTube-kanaal."
    },
    "no": {
        "audio": get_sample_audio_path("mtl_prompts/no_f1.flac"),
        "text": "Forrige måned nådde vi en ny milepæl med to milliarder visninger på YouTube-kanalen vår."
    },
    "pl": {
        "audio": get_sample_audio_path("mtl_prompts/pl_m.flac"),
        "text": "W zeszłym miesiącu osiągnęliśmy nowy kamień milowy z dwoma miliardami wyświetleń na naszym kanale YouTube."
    },
    "pt": {
        "audio": get_sample_audio_path("mtl_prompts/pt_m1.flac"),
        "text": "No mês passado, alcançámos um novo marco: dois mil milhões de visualizações no nosso canal do YouTube."
    },
    "ru": {
        "audio": get_sample_audio_path("mtl_prompts/ru_m.flac"),
        "text": "В прошлом месяце мы достигли нового рубежа: два миллиарда просмотров на нашем YouTube-канале."
    },
    "sv": {
        "audio": get_sample_audio_path("mtl_prompts/sv_f.flac"),
        "text": "Förra månaden nådde vi en ny milstolpe med två miljarder visningar på vår YouTube-kanal."
    },
    "sw": {
        "audio": get_sample_audio_path("mtl_prompts/sw_m.flac"),
        "text": "Mwezi uliopita, tulifika hatua mpya ya maoni ya bilioni mbili kweny kituo chetu cha YouTube."
    },
    "tr": {
        "audio": get_sample_audio_path("mtl_prompts/tr_m.flac"),
        "text": "Geçen ay YouTube kanalımızda iki milyar görüntüleme ile yeni bir dönüm noktasına ulaştık."
    },
    "zh": {
        "audio": get_sample_audio_path("mtl_prompts/zh_f2.flac"),
        "text": "上个月，我们达到了一个新的里程碑. 我们的YouTube频道观看次数达到了二十亿次，这绝对令人难以置信。"
    },
}
```

### Step 4: Update Language Change Handler

**Location**: `unified_webui.py` (around line 778)

**Current Code**:
```python
def on_language_change(lang, current_ref, current_text):
    return default_audio_for_lang(lang), default_text_for_lang(lang)
```

**Updated Code**:
```python
def on_language_change(lang, current_ref, current_text):
    samples = get_language_samples()
    return samples[lang]["audio"], samples[lang]["text"]
```

### Step 5: Update Default Text Function

**Location**: `unified_webui.py` (around line 133)

**Current Code**:
```python
def default_audio_for_lang(lang: str) -> str | None:
    return LANGUAGE_CONFIG.get(lang, {}).get("audio")

def default_text_for_lang(lang: str) -> str:
    return LANGUAGE_CONFIG.get(lang, {}).get("text", "")
```

**Updated Code**:
```python
def default_audio_for_lang(lang: str) -> str | None:
    samples = get_language_samples()
    return samples.get(lang, {}).get("audio")

def default_text_for_lang(lang: str) -> str:
    samples = get_language_samples()
    return samples.get(lang, {}).get("text", "")
```

### Step 6: Update Supported Languages Display

**Location**: `unified_webui.py` (around line 139)

**Current Code**:
```python
def get_supported_languages_display() -> str:
    language_items = []
    for code, name in sorted(SUPPORTED_LANGUAGES.items()):
        language_items.append(f"**{name}** (`{code}`)")
    
    mid = len(language_items) // 2
    line1 = " • ".join(language_items[:mid])
    line2 = " • ".join(language_items[mid:])
    
    return f"""
### 🌍 Supported Languages ({len(SUPPORTED_LANGUAGES)} total)
{line1}

{line2}
"""
```

**Updated Code**:
```python
def get_supported_languages_display() -> str:
    return get_supported_languages_display()
```

### Step 7: Add File Validation

**Location**: `unified_webui.py` (after imports, before main app)

**Add this code**:
```python
# Validate sample files exist
def validate_sample_files_on_startup():
    missing_files = validate_sample_files()
    if missing_files:
        print("⚠️  Warning: Missing sample files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("   Please download the missing files or the system may not work properly.")
    else:
        print("✅ All sample files are present and ready to use.")

# Run validation on startup
validate_sample_files_on_startup()
```

### Step 8: Update Initial Language Setup

**Location**: `unified_webui.py` (around line 578)

**Current Code**:
```python
initial_lang = "fr"
mtl_text = gr.Textbox(
    value=default_text_for_lang(initial_lang),
    label="Text to synthesize (max chars 300)",
    max_lines=5
)
```

**Updated Code**:
```python
initial_lang = "fr"
mtl_text = gr.Textbox(
    value=default_text_for_lang(initial_lang),
    label="Text to synthesize (max chars 300)",
    max_lines=5
)
```

## Testing the Integration

### Test 1: Basic Functionality

1. **Start the application**:
   ```bash
   python unified_webui.py
   ```

2. **Check console output** for validation messages:
   ```
   ✅ All sample files are present and ready to use.
   ```

3. **Test Turbo TTS**:
   - Navigate to "Chatterbox Turbo" tab
   - Verify the reference audio file loads correctly
   - Try generating speech

4. **Test Multilingual TTS**:
   - Navigate to "Multilingual TTS" tab
   - Change language dropdown
   - Verify audio and text update correctly
   - Test with different languages

### Test 2: File Path Resolution

```python
# Test the configuration functions
from samples.sample_config import get_sample_audio_path, get_language_samples

# Test path resolution
path = get_sample_audio_path("prompts/female_random_podcast.wav")
print(f"Path: {path}")
print(f"Exists: {os.path.exists(path)}")

# Test language samples
samples = get_language_samples()
print(f"Languages: {list(samples.keys())}")
print(f"English sample: {samples['en']['audio']}")
```

### Test 3: Error Handling

1. **Test missing files**:
   - Temporarily rename a sample file
   - Restart the application
   - Verify warning messages appear

2. **Test fallback behavior**:
   - Ensure the system handles missing files gracefully
   - Verify users can still upload their own files

## Common Issues and Solutions

### Issue 1: File Not Found Errors

**Symptoms**:
- `FileNotFoundError` when loading samples
- Audio files don't appear in the UI

**Solutions**:
1. Verify files are downloaded to correct locations
2. Check file paths in `LANGUAGE_CONFIG`
3. Ensure `samples/` directory is at project root

### Issue 2: Import Errors

**Symptoms**:
- `ModuleNotFoundError` for `samples.sample_config`

**Solutions**:
1. Ensure `samples/` directory exists
2. Check that `sample_config.md` is properly formatted
3. Verify Python can import from the samples directory

### Issue 3: Path Resolution Issues

**Symptoms**:
- Incorrect file paths generated
- Files exist but can't be found

**Solutions**:
1. Check `SAMPLES_DIR` path in `sample_config.md`
2. Verify `get_sample_audio_path()` function
3. Test with absolute vs relative paths

## Performance Considerations

1. **File Loading**: Local files load faster than remote URLs
2. **Memory Usage**: Files are loaded on demand, not preloaded
3. **Startup Time**: Validation adds minimal startup time
4. **Disk Space**: ~50-80 MB for all sample files

## Backward Compatibility

The implementation maintains backward compatibility by:

1. **Graceful Fallback**: System works even if some files are missing
2. **User Uploads**: Users can still upload their own audio files
3. **Configuration**: Easy to switch back to remote URLs if needed

## Final Verification

After completing all steps:

1. ✅ All imports work correctly
2. ✅ File paths resolve properly
3. ✅ Language switching works
4. ✅ Audio files load in UI
5. ✅ TTS generation works with local samples
6. ✅ Error handling is robust
7. ✅ Performance is improved

## Next Steps

1. **User Testing**: Test with actual users
2. **Documentation**: Update user-facing documentation
3. **Deployment**: Deploy to production environment
4. **Monitoring**: Monitor for any issues in production