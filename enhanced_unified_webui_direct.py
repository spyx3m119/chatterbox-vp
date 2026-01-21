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
    get_supported_languages_display,
    get_tts_sample_voices,
    get_tts_voice_dropdown_options,
    get_tts_voice_by_id
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Event tags for Turbo
EVENT_TAGS = [
    "[clear throat]", "[sigh]", "[shush]", "[cough]", "[groan]",
    "[sniff]", "[gasp]", "[chuckle]", "[laugh]"
]

# Language config for multilingual (copied from multilingual_app.py)
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
        "text": "先月、私たちはYouTubeチャンネルで二十億回の再生回数という新たなマイルストーンに到達しました。"
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

def set_seed(seed: int):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    np.random.seed(seed)

def load_tts_model():
    return ChatterboxTTS.from_pretrained(DEVICE)

def load_turbo_model():
    return ChatterboxTurboTTS.from_pretrained(DEVICE)

def load_mtl_model():
    return ChatterboxMultilingualTTS.from_pretrained(DEVICE)

def load_vc_model():
    return ChatterboxVC.from_pretrained(DEVICE)

def default_audio_for_lang(lang: str) -> str | None:
    samples = get_language_samples()
    return samples.get(lang, {}).get("audio")

def default_text_for_lang(lang: str) -> str:
    samples = get_language_samples()
    return samples.get(lang, {}).get("text", "")

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

# Direct CSS injection with maximum specificity
CUSTOM_CSS = """
/* Direct CSS injection for maximum impact */
:root {
    --primary-500: #3b82f6;
    --primary-600: #2563eb;
    --secondary-500: #8b5cf6;
    --secondary-600: #7c3aed;
    --accent-500: #ec4899;
    --accent-600: #e11d48;
    --bg-dark: #0f172a;
    --bg-darker: #1e293b;
    --bg-panel: #334155;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --border-color: #475569;
}

/* Force dark theme on body */
body {
    background: linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-darker) 100%) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    margin: 0 !important;
    padding: 0 !important;
    min-height: 100vh !important;
}

/* Force gradio container styling */
.gradio-container {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.gr-main {
    background: transparent !important;
    border-radius: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
    box-shadow: none !important;
    overflow: visible !important;
}

/* Force all component styling with maximum specificity */
.gr-textbox, .gr-textbox *, .gr-textbox textarea, .gr-textbox input {
    background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;
    border: 2px solid #475569 !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

.gr-textbox:focus-within, .gr-textbox:focus, .gr-textbox textarea:focus, .gr-textbox input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
    transform: translateY(-2px) !important;
    z-index: 100 !important;
}

.gr-dropdown, .gr-dropdown *, .gr-dropdown select {
    background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;
    border: 2px solid #475569 !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

.gr-dropdown:focus-within, .gr-dropdown:focus, .gr-dropdown select:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
    transform: translateY(-2px) !important;
    z-index: 100 !important;
}

.gr-audio, .gr-audio * {
    background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;
    border: 2px solid #475569 !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

.gr-audio:focus-within, .gr-audio:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
    transform: translateY(-2px) !important;
    z-index: 100 !important;
}

.gr-slider, .gr-slider * {
    background: transparent !important;
    border: none !important;
}

.gr-slider input[type="range"] {
    width: 100% !important;
    height: 6px !important;
    background: linear-gradient(90deg, #475569, #64748b) !important;
    border-radius: 9999px !important;
    outline: none !important;
    -webkit-appearance: none !important;
}

.gr-slider input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none !important;
    width: 20px !important;
    height: 20px !important;
    background: #3b82f6 !important;
    border-radius: 50% !important;
    cursor: pointer !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.2s ease !important;
}

.gr-slider input[type="range"]::-webkit-slider-thumb:hover {
    background: #2563eb !important;
    transform: scale(1.1) !important;
}

/* Force button styling */
.gr-button-primary, .gr-button-primary * {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 14px 24px !important;
    border-radius: 12px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-size: 14px !important;
    border: 2px solid transparent !important;
}

.gr-button-primary:hover, .gr-button-primary:hover * {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 35px -5px rgba(59, 130, 246, 0.5), 0 0 30px rgba(139, 92, 246, 0.3) !important;
    filter: brightness(1.1) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

.gr-button-secondary, .gr-button-secondary * {
    background: linear-gradient(135deg, #475569 0%, #334155 100%) !important;
    border: 2px solid #64748b !important;
    color: #e2e8f0 !important;
    font-weight: 600 !important;
    padding: 14px 24px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

.gr-button-secondary:hover, .gr-button-secondary:hover * {
    background: linear-gradient(135deg, #64748b 0%, #475569 100%) !important;
    border-color: #94a3b8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 20px -4px rgba(100, 116, 139, 0.3) !important;
}

/* Force event tag button styling */
.tag-btn, .tag-btn * {
    background: linear-gradient(135deg, #475569 0%, #334155 100%) !important;
    border: 2px solid #64748b !important;
    color: #e2e8f0 !important;
    border-radius: 9999px !important;
    padding: 10px 16px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    margin: 4px !important;
    display: inline-block !important;
    cursor: pointer !important;
}

.tag-btn:hover, .tag-btn:hover * {
    background: linear-gradient(135deg, #64748b 0%, #475569 100%) !important;
    border-color: #94a3b8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 16px -3px rgba(100, 116, 139, 0.3) !important;
    cursor: pointer !important;
}

/* Force accordion styling */
.gr-accordion, .gr-accordion * {
    background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;
    border: 2px solid #475569 !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2) !important;
    overflow: hidden !important;
    margin-bottom: 16px !important;
}

.gr-accordion .gr-accordion-header, .gr-accordion .gr-accordion-header * {
    background: linear-gradient(135deg, #475569 0%, #334155 100%) !important;
    border-bottom: 2px solid #64748b !important;
    color: #e2e8f0 !important;
    font-weight: 700 !important;
    padding: 16px !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}

.gr-accordion .gr-accordion-content, .gr-accordion .gr-accordion-content * {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    padding: 20px !important;
    border-top: 1px solid #334155 !important;
}

/* Force info and warning message styling */
.gr-info, .gr-info * {
    background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%) !important;
    border: 2px solid #3b82f6 !important;
    color: #bfdbfe !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.2) !important;
}

.audio-note, .audio-note * {
    background: linear-gradient(135deg, #7c2d12 0%, #451a03 100%) !important;
    border: 2px solid #f59e0b !important;
    color: #fed7aa !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.2) !important;
}

/* Force progress bar styling */
.gr-progress-bar, .gr-progress-bar * {
    background: #334155 !important;
    border-radius: 9999px !important;
    height: 8px !important;
    overflow: hidden !important;
}

.gr-progress-bar .progress, .gr-progress-bar .progress * {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899) !important;
    height: 100% !important;
    width: 0% !important;
    transition: width 0.3s ease !important;
    border-radius: 9999px !important;
}

/* Force markdown styling */
.gr-markdown, .gr-markdown * {
    color: #e2e8f0 !important;
}

.gr-markdown h1, .gr-markdown h1 *, .gr-markdown h2, .gr-markdown h2 *, .gr-markdown h3, .gr-markdown h3 * {
    color: #ffffff !important;
    font-weight: 700 !important;
    margin-bottom: 16px !important;
}

.gr-markdown p, .gr-markdown p * {
    margin-bottom: 16px !important;
    line-height: 1.6 !important;
}

.gr-markdown code, .gr-markdown code * {
    background: #1e293b !important;
    color: #bfdbfe !important;
    padding: 2px 6px !important;
    border-radius: 6px !important;
    font-family: 'Courier New', monospace !important;
}

/* Force responsive adjustments */
@media (max-width: 768px) {
    .gr-textbox, .gr-dropdown, .gr-audio, .gr-slider, .gr-textbox *, .gr-dropdown *, .gr-audio *, .gr-slider * {
        font-size: 14px !important;
        padding: 12px !important;
    }
    
    .gr-button-primary, .gr-button-secondary, .gr-button-primary *, .gr-button-secondary * {
        padding: 12px 20px !important;
        font-size: 14px !important;
    }
    
    .tag-btn, .tag-btn * {
        padding: 8px 12px !important;
        font-size: 12px !important;
        margin: 2px !important;
    }
}

/* Force focus management */
*:focus {
    outline: 2px solid #3b82f6 !important;
    outline-offset: 2px !important;
}

/* Force scrollbar styling */
::-webkit-scrollbar {
    width: 8px !important;
    height: 8px !important;
}

::-webkit-scrollbar-track {
    background: #1e293b !important;
    border-radius: 4px !important;
}

::-webkit-scrollbar-thumb {
    background: #475569 !important;
    border-radius: 4px !important;
    transition: background 0.3s ease !important;
}

::-webkit-scrollbar-thumb:hover {
    background: #64748b !important;
}

/* Force all components to use the new styling */
.gr-textbox, .gr-dropdown, .gr-audio, .gr-slider, .gr-button, .gr-accordion, .gr-markdown, .gr-file, .gr-checkbox, .gr-radio,
.gr-textbox *, .gr-dropdown *, .gr-audio *, .gr-slider *, .gr-button *, .gr-accordion *, .gr-markdown *, .gr-file *, .gr-checkbox *, .gr-radio * {
    pointer-events: auto !important;
    z-index: 1000 !important;
    position: relative !important;
}

/* Add custom classes for dashboard styling */
.dashboard-header {
    font-size: 32px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin-bottom: 16px !important;
}

.section-title {
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    border-left: 4px solid #3b82f6 !important;
    padding-left: 16px !important;
    margin-bottom: 24px !important;
}

/* Add animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.animate-fade-in {
    animation: fadeIn 0.5s ease-in-out !important;
}

.animate-slide-up {
    animation: slideUp 0.6s ease-out !important;
}

.animate-float {
    animation: float 6s ease-in-out infinite !important;
}

/* Force loading states */
.gr-loading {
    animation: pulse 1.5s ease-in-out infinite !important;
}

@keyframes pulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

/* Add neon glow effects */
.neon-blue {
    text-shadow: 0 0 5px #3b82f6, 0 0 10px #3b82f6, 0 0 15px #3b82f6 !important;
    box-shadow: 0 0 5px #3b82f6, 0 0 10px #3b82f6, 0 0 15px #3b82f6 !important;
}

.neon-purple {
    text-shadow: 0 0 5px #8b5cf6, 0 0 10px #8b5cf6, 0 0 15px #8b5cf6 !important;
    box-shadow: 0 0 5px #8b5cf6, 0 0 10px #8b5cf6, 0 0 15px #8b5cf6 !important;
}

.neon-pink {
    text-shadow: 0 0 5px #ec4899, 0 0 10px #ec4899, 0 0 15px #ec4899 !important;
    box-shadow: 0 0 5px #ec4899, 0 0 10px #ec4899, 0 0 15px #ec4899 !important;
}

/* Force tab navigation styling */
.gr-tab-nav, .gr-tab-nav * {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    border-bottom: 2px solid #334155 !important;
}

.gr-tab-nav button, .gr-tab-nav button * {
    background: transparent !important;
    border: none !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    padding: 16px 20px !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
    border-radius: 8px !important;
}

.gr-tab-nav button.active, .gr-tab-nav button.active * {
    color: #ffffff !important;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
    border-bottom: 3px solid #ffffff !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

.gr-tab-nav button:hover, .gr-tab-nav button:hover * {
    color: #ffffff !important;
    background: rgba(59, 130, 246, 0.1) !important;
}

/* Add custom JavaScript to force styles after page load */
"""

INSERT_TAG_JS = """
(tag_val, current_text) => {
    const textarea = document.querySelector('#main_textbox textarea');
    if (!textarea) return current_text + " " + tag_val; 

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;

    let prefix = " ";
    let suffix = " ";

    if (start === 0) prefix = "";
    else if (current_text[start - 1] === ' ') prefix = "";

    if (end < current_text.length && current_text[end] === ' ') suffix = "";

    return current_text.slice(0, start) + prefix + tag_val + suffix + current_text.slice(end);
}
"""

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

with gr.Blocks(title="Chatterbox AI - Beautiful Interface", css=CUSTOM_CSS) as demo:
    gr.Markdown("# <div class='dashboard-header animate-fade-in'>Chatterbox AI Voice Studio</div>")
    gr.Markdown("### <div class='section-title animate-slide-up'>A unified interface for all Chatterbox TTS and Voice Conversion features.</div>")
    
    # Model states for lazy loading
    tts_model_state = gr.State(None)
    turbo_model_state = gr.State(None)
    mtl_model_state = gr.State(None)
    vc_model_state = gr.State(None)

    with gr.Tabs(elem_classes=["gr-tab-nav"]):
        # Tab 1: Chatterbox TTS (Original)
        with gr.TabItem("🎤 Classic TTS", elem_classes=["animate-fade-in"]):
            with gr.Row():
                with gr.Column(elem_classes=["gr-column"]):
                    tts_text = gr.Textbox(
                        value="Now let's make my mum's favourite. So three mars bars into the pan. Then we add the tuna and just stir for a bit, just let the chocolate and fish infuse. A sprinkle of olive oil and some tomato ketchup. Now smell that. Oh boy this is going to be incredible.",
                        label="Text to synthesize (max chars 300)",
                        max_lines=5,
                        elem_classes=["gr-textbox"]
                    )
                    
                    gr.Markdown("### 🎙️ Sample Reference Audio")
                    gr.Markdown("Choose a sample voice or upload your own reference audio below:")
                    
                    tts_sample_voice = gr.Dropdown(
                        choices=get_tts_voice_dropdown_options(),
                        value="female_podcast",
                        label="Sample Voice",
                        info="Select a sample voice to use as reference",
                        elem_classes=["gr-dropdown"]
                    )
                    
                    tts_ref_wav = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Reference Audio File", value=get_sample_audio_path("prompts/female_random_podcast.wav"), elem_classes=["gr-audio"])
                    tts_exaggeration = gr.Slider(0.25, 2, step=.05, label="Exaggeration (Neutral = 0.5, extreme values can be unstable)", value=.5, elem_classes=["gr-slider"])
                    tts_cfg_weight = gr.Slider(0.0, 1, step=.05, label="CFG/Pace", value=0.5, elem_classes=["gr-slider"])

                    with gr.Accordion("More options", open=False, elem_classes=["gr-accordion"]):
                        tts_seed_num = gr.Number(value=0, label="Random seed (0 for random)", elem_classes=["gr-textbox"])
                        tts_temp = gr.Slider(0.05, 5, step=.05, label="temperature", value=.8, elem_classes=["gr-slider"])
                        tts_min_p = gr.Slider(0.00, 1.00, step=0.01, label="min_p || Newer Sampler. Recommend 0.02 > 0.1. Handles Higher Temperatures better. 0.00 Disables", value=0.05, elem_classes=["gr-slider"])
                        tts_top_p = gr.Slider(0.00, 1.00, step=0.01, label="top_p || Original Sampler. 1.0 Disables(recommended). Original 0.8", value=1.00, elem_classes=["gr-slider"])
                        tts_repetition_penalty = gr.Slider(1.00, 2.00, step=0.1, label="repetition_penalty", value=1.2, elem_classes=["gr-slider"])

                    tts_run_btn = gr.Button("Generate", variant="primary", elem_classes=["gr-button-primary"])

                with gr.Column(elem_classes=["gr-column"]):
                    tts_audio_output = gr.Audio(label="Output Audio", elem_classes=["gr-audio"])

        # Tab 2: Chatterbox Turbo TTS
        with gr.TabItem("⚡ Turbo TTS", elem_classes=["animate-fade-in"]):
            gr.Markdown("### <div class='section-title animate-slide-up'>Chatterbox Turbo</div>")

            with gr.Row():
                with gr.Column(elem_classes=["gr-column"]):
                    turbo_text = gr.Textbox(
                        value="Oh, that's hilarious! [chuckle] Um anyway, we do have a new model in store. It's the SkyNet T-800 series and it's got basically everything. Including AI integration with ChatGPT and um all that jazz. Would you like me to get some prices for you?",
                        label="Text to synthesize (max chars 300)",
                        max_lines=5,
                        elem_id="main_textbox",
                        elem_classes=["gr-textbox"]
                    )

                    with gr.Row(elem_classes=["tag-container"]):
                        for tag in EVENT_TAGS:
                            btn = gr.Button(tag, elem_classes=["tag-btn"])
                            btn.click(
                                fn=None,
                                inputs=[btn, turbo_text],
                                outputs=turbo_text,
                                js=INSERT_TAG_JS
                            )

                    turbo_ref_wav = gr.Audio(
                        sources=["upload", "microphone"],
                        type="filepath",
                        label="Reference Audio File",
                        value=get_sample_audio_path("prompts/female_random_podcast.wav"),
                        elem_classes=["gr-audio"]
                    )

                    turbo_run_btn = gr.Button("Generate ⚡", variant="primary", elem_classes=["gr-button-primary"])

                with gr.Column(elem_classes=["gr-column"]):
                    turbo_audio_output = gr.Audio(label="Output Audio", elem_classes=["gr-audio"])

                    with gr.Accordion("Advanced Options", open=False, elem_classes=["gr-accordion"]):
                        turbo_seed_num = gr.Number(value=0, label="Random seed (0 for random)", elem_classes=["gr-textbox"])
                        turbo_temp = gr.Slider(0.05, 2.0, step=.05, label="Temperature", value=0.8, elem_classes=["gr-slider"])
                        turbo_top_p = gr.Slider(0.00, 1.00, step=0.01, label="Top P", value=0.95, elem_classes=["gr-slider"])
                        turbo_top_k = gr.Slider(0, 1000, step=10, label="Top K", value=1000, elem_classes=["gr-slider"])
                        turbo_repetition_penalty = gr.Slider(1.00, 2.00, step=0.05, label="Repetition Penalty", value=1.2, elem_classes=["gr-slider"])
                        turbo_min_p = gr.Slider(0.00, 1.00, step=0.01, label="Min P (Set to 0 to disable)", value=0.00, elem_classes=["gr-slider"])
                        turbo_norm_loudness = gr.Checkbox(value=True, label="Normalize Loudness (-27 LUFS)", elem_classes=["gr-checkbox"])

        # Tab 3: Multilingual TTS
        with gr.TabItem("🌍 Multilingual TTS", elem_classes=["animate-fade-in"]):
            gr.Markdown("# <div class='dashboard-header animate-fade-in'>Chatterbox Multilingual Demo</div>")
            gr.Markdown("Generate high-quality multilingual speech from text with reference audio styling, supporting 23 languages.")
            gr.Markdown(get_supported_languages_display())

            with gr.Row():
                with gr.Column(elem_classes=["gr-column"]):
                    initial_lang = "fr"
                    mtl_text = gr.Textbox(
                        value=default_text_for_lang(initial_lang),
                        label="Text to synthesize (max chars 300)",
                        max_lines=5,
                        elem_classes=["gr-textbox"]
                    )
                    
                    mtl_language_id = gr.Dropdown(
                        choices=list(SUPPORTED_LANGUAGES.keys()),
                        value=initial_lang,
                        label="Language",
                        info="Select the language for text-to-speech synthesis",
                        elem_classes=["gr-dropdown"]
                    )
                    
                    mtl_ref_wav = gr.Audio(
                        sources=["upload", "microphone"],
                        type="filepath",
                        label="Reference Audio File (Optional)",
                        value=default_audio_for_lang(initial_lang),
                        elem_classes=["gr-audio"]
                    )
                    
                    gr.Markdown(
                        "💡 **Note**: Ensure that the reference clip matches the specified language tag. Otherwise, language transfer outputs may inherit the accent of the reference clip's language. To mitigate this, set the CFG weight to 0.",
                        elem_classes=["audio-note"]
                    )
                    
                    mtl_exaggeration = gr.Slider(
                        0.25, 2, step=.05, label="Exaggeration (Neutral = 0.5, extreme values can be unstable)", value=.5, elem_classes=["gr-slider"]
                    )
                    mtl_cfg_weight = gr.Slider(
                        0.2, 1, step=.05, label="CFG/Pace", value=0.5, elem_classes=["gr-slider"]
                    )

                    with gr.Accordion("More options", open=False, elem_classes=["gr-accordion"]):
                        mtl_seed_num = gr.Number(value=0, label="Random seed (0 for random)", elem_classes=["gr-textbox"])
                        mtl_temp = gr.Slider(0.05, 5, step=.05, label="Temperature", value=.8, elem_classes=["gr-slider"])

                    mtl_run_btn = gr.Button("Generate", variant="primary", elem_classes=["gr-button-primary"])

                with gr.Column(elem_classes=["gr-column"]):
                    mtl_audio_output = gr.Audio(label="Output Audio", elem_classes=["gr-audio"])

        # Tab 4: Voice Conversion
        with gr.TabItem("🔀 Voice Conversion", elem_classes=["animate-fade-in"]):
            with gr.Row():
                with gr.Column(elem_classes=["gr-column"]):
                    vc_input_audio = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Input audio file", elem_classes=["gr-audio"])
                    vc_target_voice = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Target voice audio file (if none, the default voice is used)", value=None, elem_classes=["gr-audio"])
                    vc_run_btn = gr.Button("Convert", variant="primary", elem_classes=["gr-button-primary"])

                with gr.Column(elem_classes=["gr-column"]):
                    vc_audio_output = gr.Audio(label="Output Audio", elem_classes=["gr-audio"])

    # Models will be loaded lazily when first used

    # TTS generate function
    def tts_generate(text, audio_prompt_path, exaggeration, temperature, seed_num, cfgw, min_p, top_p, repetition_penalty):
        model = tts_model_state.value
        if model is None:
            model = load_tts_model()
            tts_model_state.value = model

        if seed_num != 0:
            set_seed(int(seed_num))

        wav = model.generate(
            text,
            audio_prompt_path=audio_prompt_path,
            exaggeration=exaggeration,
            temperature=temperature,
            cfg_weight=cfgw,
            min_p=min_p,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
        )
        return (model.sr, wav.squeeze(0).numpy())

    # Turbo generate function
    def turbo_generate(text, audio_prompt_path, temperature, seed_num, min_p, top_p, top_k, repetition_penalty, norm_loudness):
        model = turbo_model_state.value
        if model is None:
            model = load_turbo_model()
            turbo_model_state.value = model

        if seed_num != 0:
            set_seed(int(seed_num))

        wav = model.generate(
            text,
            audio_prompt_path=audio_prompt_path,
            temperature=temperature,
            min_p=min_p,
            top_p=top_p,
            top_k=int(top_k),
            repetition_penalty=repetition_penalty,
            norm_loudness=norm_loudness,
        )
        return (model.sr, wav.squeeze(0).numpy())

    # MTL generate function
    def mtl_generate(text, language_id, audio_prompt_path, exaggeration, temperature, seed_num, cfg_weight):
        model = mtl_model_state.value
        if model is None:
            model = load_mtl_model()
            mtl_model_state.value = model

        if seed_num != 0:
            set_seed(int(seed_num))

        chosen_prompt = audio_prompt_path or default_audio_for_lang(language_id)

        generate_kwargs = {
            "exaggeration": exaggeration,
            "temperature": temperature,
            "cfg_weight": cfg_weight,
        }
        if chosen_prompt:
            generate_kwargs["audio_prompt_path"] = chosen_prompt
        
        wav = model.generate(
            text[:300],
            language_id=language_id,
            **generate_kwargs
        )
        return (model.sr, wav.squeeze(0).numpy())

    # VC generate function
    def vc_generate(audio, target_voice_path):
        model = vc_model_state.value
        if model is None:
            model = load_vc_model()
            vc_model_state.value = model

        wav = model.generate(
            audio, target_voice_path=target_voice_path,
        )
        return model.sr, wav.squeeze(0).numpy()

    # Event handlers with enhanced progress indicators
    tts_run_btn.click(
        fn=tts_generate,
        inputs=[
            tts_text,
            tts_ref_wav,
            tts_exaggeration,
            tts_temp,
            tts_seed_num,
            tts_cfg_weight,
            tts_min_p,
            tts_top_p,
            tts_repetition_penalty,
        ],
        outputs=tts_audio_output,
        api_name="tts_generate",
        show_progress="full"
    )

    turbo_run_btn.click(
        fn=turbo_generate,
        inputs=[
            turbo_text,
            turbo_ref_wav,
            turbo_temp,
            turbo_seed_num,
            turbo_min_p,
            turbo_top_p,
            turbo_top_k,
            turbo_repetition_penalty,
            turbo_norm_loudness,
        ],
        outputs=turbo_audio_output,
        api_name="turbo_generate",
        show_progress="full"
    )

    mtl_run_btn.click(
        fn=mtl_generate,
        inputs=[
            mtl_text,
            mtl_language_id,
            mtl_ref_wav,
            mtl_exaggeration,
            mtl_temp,
            mtl_seed_num,
            mtl_cfg_weight,
        ],
        outputs=mtl_audio_output,
        api_name="mtl_generate",
        show_progress="full"
    )

    vc_run_btn.click(
        fn=vc_generate,
        inputs=[vc_input_audio, vc_target_voice],
        outputs=vc_audio_output,
        api_name="vc_generate",
        show_progress="full"
    )

    # Language change for MTL
    def on_language_change(lang, current_ref, current_text):
        samples = get_language_samples()
        return samples[lang]["audio"], samples[lang]["text"]

    mtl_language_id.change(
        fn=on_language_change,
        inputs=[mtl_language_id, mtl_ref_wav, mtl_text],
        outputs=[mtl_ref_wav, mtl_text],
        show_progress=False
    )

    # TTS sample voice change handler
    def on_tts_voice_change(voice_selection, current_ref):
        print(f"🔄 TTS Dropdown change triggered: '{voice_selection}'")
        print(f"   Type: {type(voice_selection)}")
        
        # Try to find by voice ID first
        voice_config = get_tts_voice_by_id(voice_selection)
        
        # If not found, try to find by display text
        if not voice_config:
            print(f"   Voice ID not found, trying display text lookup...")
            options = get_tts_voice_dropdown_options()
            for voice_id, display_text in options:
                if display_text == voice_selection:
                    print(f"   🔍 Found by display text! Voice ID: {voice_id}")
                    voice_config = get_tts_voice_by_id(voice_id)
                    break
        
        if voice_config and voice_config.get("audio"):
            audio_path = voice_config["audio"]
            print(f"   ✅ Audio path: {audio_path}")
            print(f"   File exists: {audio_path and audio_path.exists() if hasattr(audio_path, 'exists') else 'N/A'}")
            # Return the audio path directly for Gradio Audio component
            return audio_path
        print(f"   ❌ No audio found for: {voice_selection}")
        return current_ref

    tts_sample_voice.change(
        fn=on_tts_voice_change,
        inputs=[tts_sample_voice, tts_ref_wav],
        outputs=[tts_ref_wav],
        show_progress=False
    )

if __name__ == "__main__":
    demo.queue(
        max_size=50,
        default_concurrency_limit=1,
    ).launch(share=True)