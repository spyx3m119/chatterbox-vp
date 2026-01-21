"""
Sample Audio Configuration for ChatterBox TTS

This module provides configuration and utilities for managing sample reference audio files.
"""

import os
from pathlib import Path
from typing import Dict, Any

# Base path for samples directory
SAMPLES_DIR = Path(__file__).parent.absolute()

# Event tags for Turbo TTS
EVENT_TAGS = [
    "[clear throat]", "[sigh]", "[shush]", "[cough]", "[groan]",
    "[sniff]", "[gasp]", "[chuckle]", "[laugh]"
]

# Language configuration for multilingual TTS
LANGUAGE_CONFIG = {
    "ar": {
        "audio": "mtl_prompts/ar_prompts2.flac",
        "text": "في الشهر الماضي، وصلنا إلى معلم جديد بمليارين من المشاهدات على قناتنا على يوتيوب."
    },
    "da": {
        "audio": "mtl_prompts/da_m1.flac",
        "text": "Sidste måned nåede vi en ny milepæl med to milliarder visninger på vores YouTube-kanal."
    },
    "de": {
        "audio": "mtl_prompts/de_f1.flac",
        "text": "Letzten Monat haben wir einen neuen Meilenstein erreicht: zwei Milliarden Aufrufe auf unserem YouTube-Kanal."
    },
    "el": {
        "audio": "mtl_prompts/el_m.flac",
        "text": "Τον περασμένο μήνα, φτάσαμε σε ένα νέο ορόσημο με δύο δισεκατομμύρια προβολές στο κανάλι μας στο YouTube."
    },
    "en": {
        "audio": "mtl_prompts/en_f1.flac",
        "text": "Last month, we reached a new milestone with two billion views on our YouTube channel."
    },
    "es": {
        "audio": "mtl_prompts/es_f1.flac",
        "text": "El mes pasado alcanzamos un nuevo hito: dos mil millones de visualizaciones en nuestro canal de YouTube."
    },
    "fi": {
        "audio": "mtl_prompts/fi_m.flac",
        "text": "Viime kuussa saavutimme uuden virstanpylvään kahden miljardin katselukerran kanssa YouTube-kanavallamme."
    },
    "fr": {
        "audio": "mtl_prompts/fr_f1.flac",
        "text": "Le mois dernier, nous avons atteint un nouveau jalon avec deux milliards de vues sur notre chaîne YouTube."
    },
    "he": {
        "audio": "mtl_prompts/he_m1.flac",
        "text": "בחודש שעבר הגענו לאבן דרך חדשה עם שני מיליארד צפיות בערוץ היוטיוב שלנו."
    },
    "hi": {
        "audio": "mtl_prompts/hi_f1.flac",
        "text": "पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो अरब व्यूज़।"
    },
    "it": {
        "audio": "mtl_prompts/it_m1.flac",
        "text": "Il mese scorso abbiamo raggiunto un nuovo traguardo: due miliardi di visualizzazioni sul nostro canale YouTube."
    },
    "ja": {
        "audio": "mtl_prompts/ja_prompts1.flac",
        "text": "先月、私たちのYouTubeチャンネルで二十億回の再生回数という新たなマイルストーンに到達しました。"
    },
    "ko": {
        "audio": "mtl_prompts/ko_f.flac",
        "text": "지난달 우리는 유튜브 채널에서 이십억 조회수라는 새로운 이정표에 도달했습니다."
    },
    "ms": {
        "audio": "mtl_prompts/ms_f.flac",
        "text": "Bulan lepas, kami mencapai pencapaian baru dengan dua bilion tontonan di saluran YouTube kami."
    },
    "nl": {
        "audio": "mtl_prompts/nl_m.flac",
        "text": "Vorige maand bereikten we een nieuwe mijlpaal met twee miljard weergaven op ons YouTube-kanaal."
    },
    "no": {
        "audio": "mtl_prompts/no_f1.flac",
        "text": "Forrige måned nådde vi en ny milepæl med to milliarder visninger på YouTube-kanalen vår."
    },
    "pl": {
        "audio": "mtl_prompts/pl_m.flac",
        "text": "W zeszłym miesiącu osiągnęliśmy nowy kamień milowy z dwoma miliardami wyświetleń na naszym kanale YouTube."
    },
    "pt": {
        "audio": "mtl_prompts/pt_m1.flac",
        "text": "No mês passado, alcançámos um novo marco: dois mil milhões de visualizações no nosso canal do YouTube."
    },
    "ru": {
        "audio": "mtl_prompts/ru_m.flac",
        "text": "В прошлом месяце мы достигли нового рубежа: два миллиарда просмотров на нашем YouTube-канале."
    },
    "sv": {
        "audio": "mtl_prompts/sv_f.flac",
        "text": "Förra månaden nådde vi en ny milstolpe med två miljarder visningar på vår YouTube-kanal."
    },
    "sw": {
        "audio": "mtl_prompts/sw_m.flac",
        "text": "Mwezi uliopita, tulifika hatua mpya ya maoni ya bilioni mbili kweny kituo chetu cha YouTube."
    },
    "tr": {
        "audio": "mtl_prompts/tr_m.flac",
        "text": "Geçen ay YouTube kanalımızda iki milyar görüntüleme ile yeni bir dönüm noktasına ulaştık."
    },
    "zh": {
        "audio": "mtl_prompts/zh_f2.flac",
        "text": "上个月，我们达到了一个新的里程碑. 我们的YouTube频道观看次数达到了二十亿次，这绝对令人难以置信。"
    },
}

# Default TTS prompt configuration
TTS_DEFAULT_CONFIG = {
    "audio": "prompts/female_random_podcast.wav",
    "text": "Now let's make my mum's favourite. So three mars bars into the pan. Then we add the tuna and just stir for a bit, just let the chocolate and fish infuse. A sprinkle of olive oil and some tomato ketchup. Now smell that. Oh boy this is going to be incredible."
}

# Sample TTS voices configuration for dropdown
TTS_SAMPLE_VOICES = {
    "female_podcast": {
        "name": "Female Podcast Voice",
        "audio": "prompts/female_random_podcast.wav",
        "description": "Clear female voice with podcast-style delivery"
    },
    "male_narration": {
        "name": "Male Narration Voice",
        "audio": "prompts/male_narration.wav",
        "description": "Deep male voice with narrative style"
    }
}

def get_sample_audio_path(relative_path: str) -> str:
    """
    Get the full path to a sample audio file.
    
    Args:
        relative_path: Relative path from the samples directory
        
    Returns:
        Full path to the audio file
    """
    full_path = SAMPLES_DIR / relative_path
    return str(full_path)

def get_language_samples() -> Dict[str, Dict[str, str]]:
    """
    Get all language sample configurations with absolute paths.
    
    Returns:
        Dictionary of language codes to their sample configurations
    """
    samples = {}
    for lang_code, config in LANGUAGE_CONFIG.items():
        samples[lang_code] = {
            "audio": get_sample_audio_path(config["audio"]),
            "text": config["text"]
        }
    return samples

def get_default_tts_sample() -> Dict[str, str]:
    """
    Get the default TTS sample configuration with absolute path.
    
    Returns:
        Dictionary with audio path and text
    """
    return {
        "audio": get_sample_audio_path(TTS_DEFAULT_CONFIG["audio"]),
        "text": TTS_DEFAULT_CONFIG["text"]
    }

def get_tts_sample_voices() -> Dict[str, Dict[str, str]]:
    """
    Get all TTS sample voice configurations with absolute paths.
    
    Returns:
        Dictionary of voice IDs to their sample configurations
    """
    voices = {}
    for voice_id, config in TTS_SAMPLE_VOICES.items():
        voices[voice_id] = {
            "name": config["name"],
            "audio": get_sample_audio_path(config["audio"]),
            "description": config["description"]
        }
    return voices

def get_tts_voice_dropdown_options() -> list:
    """
    Get dropdown options for TTS sample voices.
    
    Returns:
        List of tuples (value, label) for dropdown
    """
    voices = get_tts_sample_voices()
    print(f"🔍 DEBUG: get_tts_sample_voices() returned {len(voices)} voices")
    options = []
    for voice_id, config in voices.items():
        label = f"{config['name']} - {config['description']}"
        options.append((voice_id, label))
    print(f"🔍 DEBUG: get_tts_voice_dropdown_options() returning: {options}")
    return options

def get_tts_voice_by_id(voice_id: str) -> Dict[str, str]:
    """
    Get TTS voice configuration by ID.
    
    Args:
        voice_id: Voice identifier
        
    Returns:
        Dictionary with voice configuration
    """
    voices = get_tts_sample_voices()
    return voices.get(voice_id, {})

def validate_sample_files():
    """
    Validate that all sample audio files exist.
    
    Returns:
        List of missing files
    """
    missing_files = []
    
    print(f"🔍 DEBUG: SAMPLES_DIR is {SAMPLES_DIR}")
    if os.path.exists(SAMPLES_DIR):
        print(f"🔍 DEBUG: Contents of {SAMPLES_DIR}: {os.listdir(SAMPLES_DIR)}")
        prompts_dir = SAMPLES_DIR / "prompts"
        if os.path.exists(prompts_dir):
            print(f"🔍 DEBUG: Contents of {prompts_dir}: {os.listdir(prompts_dir)}")
        else:
            print(f"❌ DEBUG: {prompts_dir} does NOT exist!")
    else:
        print(f"❌ DEBUG: {SAMPLES_DIR} does NOT exist!")

    # Check TTS default sample
    tts_path = get_sample_audio_path(TTS_DEFAULT_CONFIG["audio"])
    if not os.path.exists(tts_path):
        missing_files.append(tts_path)
    
    # Check TTS sample voices
    for voice_id, config in TTS_SAMPLE_VOICES.items():
        audio_path = get_sample_audio_path(config["audio"])
        if not os.path.exists(audio_path):
            missing_files.append(audio_path)
    
    # Check language samples
    for lang_code, config in LANGUAGE_CONFIG.items():
        audio_path = get_sample_audio_path(config["audio"])
        if not os.path.exists(audio_path):
            missing_files.append(audio_path)
    
    return missing_files

def get_supported_languages_display() -> str:
    """
    Get a formatted display of supported languages.
    
    Returns:
        Formatted string with supported languages
    """
    from chatterbox.mtl_tts import SUPPORTED_LANGUAGES
    
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

# File format requirements
FILE_REQUIREMENTS = {
    "formats": ["WAV", "FLAC"],
    "sample_rates": [16000, 24000],
    "channels": ["Mono"],
    "duration": {"min": 5, "max": 10},
    "quality": "High quality, clear speech"
}
