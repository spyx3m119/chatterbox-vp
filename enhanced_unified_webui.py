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

# Enhanced CSS with Dashboard-style design inspired by ReactWind template
CUSTOM_CSS = """
/* Import Tailwind CSS */
@import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');

/* Dashboard Layout Styles */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    min-height: 100vh;
    margin: 0;
}

/* Dashboard Container */
.gradio-container {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    min-height: 100vh;
    padding: 0;
}

.gr-main {
    background: transparent;
    border-radius: 0;
    margin: 0;
    max-width: 100%;
    box-shadow: none;
    overflow: visible;
}

/* Enhanced Layout Structure */
.gr-column {
    @apply p-6;
}

.gr-row {
    @apply gap-6;
}

/* Component Styling - Dashboard Theme */
.gr-textbox, .gr-dropdown, .gr-audio {
    @apply rounded-xl border-2 border-slate-600 bg-gradient-to-br from-slate-800 to-slate-700 text-white transition-all duration-300 shadow-lg hover:border-slate-500 focus:border-blue-400 focus:ring-4 focus:ring-blue-400/20;
}

.gr-textbox:focus, .gr-dropdown:focus, .gr-audio:focus {
    @apply border-blue-400 ring-4 ring-blue-400/20 transform -translate-y-1 shadow-xl;
}

.gr-textbox {
    @apply text-base bg-gradient-to-br from-slate-800 to-slate-700 border-slate-600;
}

.gr-textbox textarea {
    @apply text-base leading-relaxed bg-transparent;
}

/* Enhanced Audio Components */
.gr-audio {
    @apply bg-gradient-to-r from-slate-700 to-slate-600 border-slate-600;
}

.gr-audio .gr-audio-player {
    @apply bg-slate-800 rounded-xl border border-slate-600 shadow-lg;
}

/* Slider Enhancements */
.gr-slider {
    @apply rounded-lg;
}

.gr-slider input[type="range"] {
    @apply h-3 rounded-lg bg-gradient-to-r from-slate-600 to-slate-500;
}

/* Button Enhancements - Neon Style */
.gr-button-primary {
    @apply bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 hover:from-blue-500 hover:via-purple-500 hover:to-pink-500 text-white font-bold py-4 px-8 rounded-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl shadow-lg text-sm uppercase tracking-wide border border-white/20;
}

.gr-button-primary:hover {
    @apply -translate-y-2 shadow-purple-500/50 animate-pulse;
}

.gr-button-secondary {
    @apply bg-gradient-to-r from-slate-700 to-slate-600 border-2 border-slate-500 text-slate-100 font-semibold py-4 px-8 rounded-xl transition-all duration-300 hover:from-slate-600 hover:to-slate-500 hover:-translate-y-1 hover:border-slate-400;
}

/* Event Tags Styling - Neon Accents */
.tag-container {
    @apply flex flex-wrap gap-4 mt-6 mb-8 border-0 bg-transparent p-0;
}

.tag-btn {
    @apply min-w-fit w-auto h-12 text-sm bg-gradient-to-r from-slate-700 to-slate-600 border-2 border-slate-500 text-slate-100 rounded-full px-6 m-0 shadow-lg transition-all duration-300 font-semibold hover:from-slate-600 hover:to-slate-500 hover:-translate-y-2 hover:scale-110 hover:border-slate-400 hover:shadow-xl;
}

/* Accordion Enhancements */
.gr-accordion {
    @apply rounded-xl border-2 border-slate-600 bg-gradient-to-br from-slate-800 to-slate-700 shadow-xl;
}

.gr-accordion .gr-accordion-header {
    @apply font-bold text-slate-100 bg-gradient-to-r from-slate-700 to-slate-600 border-b-2 border-slate-600;
}

.gr-accordion .gr-accordion-content {
    @apply p-6 bg-slate-800/50;
}

/* Info and Warning Messages - Dashboard Style */
.gr-info {
    @apply bg-gradient-to-r from-blue-900/50 to-blue-800/50 border-2 border-blue-500/50 text-blue-200 rounded-xl p-6 font-semibold shadow-lg;
}

.audio-note {
    @apply bg-gradient-to-r from-amber-900/50 to-amber-800/50 border-2 border-amber-500/50 rounded-xl p-6 text-amber-200 font-semibold shadow-lg;
}

/* Success and Error States */
.gr-success {
    @apply bg-gradient-to-r from-green-900/50 to-green-800/50 border-2 border-green-500/50 text-green-200 rounded-xl p-6 font-semibold shadow-lg;
}

.gr-error {
    @apply bg-gradient-to-r from-red-900/50 to-red-800/50 border-2 border-red-500/50 text-red-200 rounded-xl p-6 font-semibold shadow-lg;
}

/* Progress Bar - Neon Style */
.gr-progress-bar {
    @apply h-4 rounded-lg bg-slate-700;
}

.gr-progress-bar .progress {
    @apply h-full rounded-lg bg-gradient-to-r from-blue-500 to-purple-500 transition-width duration-300 shadow-lg;
}

/* Statistics Cards */
.stat-card {
    @apply bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border border-slate-600 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1;
}

.stat-number {
    @apply text-3xl font-bold text-white mb-2;
}

.stat-label {
    @apply text-slate-400 text-sm uppercase tracking-wider;
}

.stat-change {
    @apply text-green-400 text-sm font-semibold mt-2;
}

/* Responsive Design */
@media (max-width: 768px) {
    .gr-column {
        @apply p-4;
    }
    
    .gr-row {
        @apply gap-4;
    }
    
    .tag-btn {
        @apply h-10 text-xs px-4;
    }
    
    .gr-button-primary, .gr-button-secondary {
        @apply py-3 px-6 text-sm;
    }
}

/* Loading States */
.gr-loading {
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% {
        opacity: 0.6;
    }
    50% {
        opacity: 1;
    }
}

/* Focus Management */
*:focus {
    @apply outline-2 outline-blue-400 outline-offset-2;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    @apply w-3 h-3;
}

::-webkit-scrollbar-track {
    @apply bg-slate-800 rounded-md;
}

::-webkit-scrollbar-thumb {
    @apply bg-slate-600 rounded-md;
}

::-webkit-scrollbar-thumb:hover {
    @apply bg-slate-500;
}

/* Additional Tailwind utility classes for enhanced styling */
.gr-block {
    @apply block;
}

.gr-box {
    @apply block;
}

.gr-form {
    @apply block visible;
}

/* Ensure text content is visible */
.gr-textbox, .gr-markdown, .gr-audio, .gr-slider, .gr-button {
    @apply block visible;
}

/* Dashboard-specific styles */
.dashboard-header {
    @apply text-white font-bold text-4xl mb-8 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent;
}

.section-title {
    @apply text-white font-semibold text-2xl mb-6 border-l-4 border-blue-500 pl-4;
}

/* Neon glow effects */
.neon-blue {
    text-shadow: 0 0 5px #3b82f6, 0 0 10px #3b82f6, 0 0 15px #3b82f6;
    box-shadow: 0 0 5px #3b82f6, 0 0 10px #3b82f6, 0 0 15px #3b82f6;
}

.neon-purple {
    text-shadow: 0 0 5px #8b5cf6, 0 0 10px #8b5cf6, 0 0 15px #8b5cf6;
    box-shadow: 0 0 5px #8b5cf6, 0 0 10px #8b5cf6, 0 0 15px #8b5cf6;
}

.neon-pink {
    text-shadow: 0 0 5px #ec4899, 0 0 10px #ec4899, 0 0 15px #ec4899;
    box-shadow: 0 0 5px #ec4899, 0 0 10px #ec4899, 0 0 15px #ec4899;
}

/* Enhanced tab styling */
.gr-tab-nav {
    @apply bg-gradient-to-r from-slate-800 to-slate-700 border-b border-slate-600;
}

.gr-tab-nav button {
    @apply bg-transparent border-0 text-slate-400 hover:text-white font-semibold py-4 px-6 transition-all duration-300 relative;
}

.gr-tab-nav button.active {
    @apply text-white border-b-2 border-blue-500;
}

.gr-tab-nav button:hover {
    @apply text-white;
}

/* Enhanced markdown styling */
.gr-markdown {
    @apply text-slate-300;
}

.gr-markdown h1, .gr-markdown h2, .gr-markdown h3 {
    @apply text-white font-bold mb-4;
}

.gr-markdown p {
    @apply mb-4 leading-relaxed;
}

.gr-markdown code {
    @apply bg-slate-700 text-slate-200 px-2 py-1 rounded;
}

/* Enhanced file upload styling */
.gr-file {
    @apply bg-gradient-to-br from-slate-800 to-slate-700 border-2 border-slate-600 rounded-xl p-6 hover:border-slate-500 transition-all duration-300;
}

.gr-file input[type="file"] {
    @apply text-slate-300;
}

/* Enhanced dropdown styling */
.gr-dropdown {
    @apply bg-gradient-to-br from-slate-800 to-slate-700 border-slate-600;
}

.gr-dropdown select {
    @apply bg-transparent text-white;
}

/* Enhanced checkbox styling */
.gr-checkbox {
    @apply text-blue-400 hover:text-blue-300;
}

/* Enhanced radio button styling */
.gr-radio {
    @apply text-blue-400 hover:text-blue-300;
}

/* Enhanced label styling */
.gr-label {
    @apply text-slate-300 font-semibold mb-2;
}

/* Enhanced error message styling */
.gr-error {
    @apply bg-red-900/20 border-red-500/50 text-red-200;
}

/* Enhanced warning message styling */
.gr-warning {
    @apply bg-yellow-900/20 border-yellow-500/50 text-yellow-200;
}

/* Enhanced success message styling */
.gr-success {
    @apply bg-green-900/20 border-green-500/50 text-green-200;
}

/* Enhanced info message styling */
.gr-info {
    @apply bg-blue-900/20 border-blue-500/50 text-blue-200;
}

/* Enhanced progress bar styling */
.gr-progress {
    @apply bg-slate-700 rounded-full h-4;
}

.gr-progress .progress {
    @apply bg-gradient-to-r from-blue-500 to-purple-500 rounded-full h-4;
}

/* Enhanced slider styling */
.gr-slider .range-wrap {
    @apply relative;
}

.gr-slider input[type="range"] {
    @apply w-full h-3 bg-gradient-to-r from-slate-600 to-slate-500 rounded-lg appearance-none;
}

.gr-slider input[type="range"]::-webkit-slider-thumb {
    @apply appearance-none w-5 h-5 bg-blue-500 rounded-full border-2 border-white shadow-lg cursor-pointer;
}

.gr-slider input[type="range"]::-moz-range-thumb {
    @apply w-5 h-5 bg-blue-500 rounded-full border-2 border-white shadow-lg cursor-pointer;
}

/* Enhanced textarea styling */
.gr-textbox textarea {
    @apply resize-none min-h-[120px];
}

/* Enhanced button group styling */
.gr-button-group {
    @apply flex gap-4;
}

/* Enhanced card styling */
.gr-card {
    @apply bg-gradient-to-br from-slate-800 to-slate-700 border border-slate-600 rounded-xl p-6 shadow-lg;
}

/* Enhanced modal styling */
.gr-modal {
    @apply bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-600 rounded-xl p-6 shadow-2xl;
}

/* Enhanced tooltip styling */
.gr-tooltip {
    @apply bg-slate-800 text-white px-3 py-1 rounded-lg shadow-lg border border-slate-600;
}

/* Enhanced notification styling */
.gr-notification {
    @apply bg-gradient-to-r from-blue-900 to-blue-800 border border-blue-500 text-blue-100 rounded-lg p-4 shadow-lg;
}

/* Enhanced loading spinner styling */
.gr-loading-spinner {
    @apply w-8 h-8 border-4 border-slate-600 border-t-blue-500 rounded-full animate-spin;
}

/* Enhanced skeleton loading styling */
.gr-skeleton {
    @apply bg-slate-700 animate-pulse rounded-lg;
}

/* Enhanced animation classes */
.animate-fade-in {
    animation: fadeIn 0.5s ease-in-out;
}

.animate-slide-up {
    animation: slideUp 0.6s ease-out;
}

.animate-pulse-slow {
    animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-float {
    animation: float 6s ease-in-out infinite;
}

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
    gr.Markdown("# <div class='dashboard-header'>Chatterbox AI Voice Studio</div>")
    gr.Markdown("### <div class='section-title'>A unified interface for all Chatterbox TTS and Voice Conversion features.</div>")
    
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
            gr.Markdown("### <div class='section-title'>Chatterbox Turbo</div>")

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
            gr.Markdown("# <div class='dashboard-header'>Chatterbox Multilingual Demo</div>")
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
    import os
    server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", 7860))
    root_path = os.getenv("GRADIO_ROOT_PATH", "")
    
    demo.queue(
        max_size=50,
        default_concurrency_limit=1,
    ).launch(
        server_name=server_name,
        server_port=server_port,
        root_path=root_path,
        share=False
    )