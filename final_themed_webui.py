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

# Common configurations are now imported from samples.sample_config


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

# Create a very simple, compatible theme
def create_chatterbox_theme():
    return gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="purple",
        neutral_hue="slate",
        font=["Inter", "system-ui", "-apple-system", "Segoe UI", "Roboto", "sans-serif"],
    ).set(
        # Background colors
        body_background_fill="#0f172a",
        body_background_fill_dark="#0f172a",
        block_background_fill="#1e293b",
        block_background_fill_dark="#1e293b",
        panel_background_fill="#1e293b",
        panel_background_fill_dark="#1e293b",
        
        # Text colors
        body_text_color="#e2e8f0",
        body_text_color_dark="#e2e8f0",
        block_label_text_color="#94a3b8",
        block_label_text_color_dark="#94a3b8",
        
        # Border colors
        block_border_color="#334155",
        block_border_color_dark="#334155",
        panel_border_color="#334155",
        panel_border_color_dark="#334155",
        
        # Button colors
        button_primary_background_fill="#3b82f6",
        button_primary_background_fill_dark="#3b82f6",
        button_primary_background_fill_hover="#2563eb",
        button_primary_background_fill_hover_dark="#2563eb",
        button_primary_text_color="#ffffff",
        button_primary_text_color_dark="#ffffff",
        
        button_secondary_background_fill="#475569",
        button_secondary_background_fill_dark="#475569",
        button_secondary_background_fill_hover="#64748b",
        button_secondary_background_fill_hover_dark="#64748b",
        button_secondary_text_color="#e2e8f0",
        button_secondary_text_color_dark="#e2e8f0",
        
        # Input colors
        input_background_fill="#334155",
        input_background_fill_dark="#334155",
        input_border_color="#475569",
        input_border_color_dark="#475569",
        
        # Slider colors
        slider_color="#3b82f6",
        slider_color_dark="#3b82f6",
    )

# Enhanced CSS for additional styling
CUSTOM_CSS = """
/* Additional custom styles for the Chatterbox theme */
.gradio-container {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
}

/* Enhanced button styling */
.gr-button-primary {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%) !important;
    border: none !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.gr-button-primary:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 35px -5px rgba(59, 130, 246, 0.5), 0 0 30px rgba(139, 92, 246, 0.3) !important;
    filter: brightness(1.1) !important;
}

.gr-button-secondary {
    background: linear-gradient(135deg, #475569 0%, #334155 100%) !important;
    border: 2px solid #64748b !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.gr-button-secondary:hover {
    background: linear-gradient(135deg, #64748b 0%, #475569 100%) !important;
    border-color: #94a3b8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 20px -4px rgba(100, 116, 139, 0.3) !important;
}

/* Enhanced input styling */
.gr-textbox, .gr-dropdown, .gr-audio {
    background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;
    border: 2px solid #475569 !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

.gr-textbox:focus, .gr-dropdown:focus, .gr-audio:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
    transform: translateY(-2px) !important;
}

/* Event tags styling */
.tag-btn {
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

.tag-btn:hover {
    background: linear-gradient(135deg, #64748b 0%, #475569 100%) !important;
    border-color: #94a3b8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 16px -3px rgba(100, 116, 139, 0.3) !important;
}

/* Progress bar styling */
.gr-progress-bar {
    background: #334155 !important;
    border-radius: 9999px !important;
    height: 8px !important;
    overflow: hidden !important;
}

.gr-progress-bar .progress {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899) !important;
    height: 100% !important;
    width: 0% !important;
    transition: width 0.3s ease !important;
    border-radius: 9999px !important;
}

/* Info and warning messages */
.gr-info {
    background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%) !important;
    border: 2px solid #3b82f6 !important;
    color: #bfdbfe !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.2) !important;
}

.audio-note {
    background: linear-gradient(135deg, #7c2d12 0%, #451a03 100%) !important;
    border: 2px solid #f59e0b !important;
    color: #fed7aa !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.2) !important;
}

/* Accordion styling */
.gr-accordion {
    background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;
    border: 2px solid #475569 !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2) !important;
    overflow: hidden !important;
}

.gr-accordion .gr-accordion-header {
    background: linear-gradient(135deg, #475569 0%, #334155 100%) !important;
    border-bottom: 2px solid #64748b !important;
    color: #e2e8f0 !important;
    font-weight: 700 !important;
    padding: 16px !important;
    transition: all 0.3s ease !important;
}

.gr-accordion .gr-accordion-content {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    padding: 20px !important;
    border-top: 1px solid #334155 !important;
}

/* Tab navigation styling */
.gr-tab-nav {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    border-bottom: 2px solid #334155 !important;
}

.gr-tab-nav button {
    background: transparent !important;
    border: none !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    padding: 16px 20px !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
    border-radius: 8px !important;
}

.gr-tab-nav button.active {
    color: #ffffff !important;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
    border-bottom: 3px solid #ffffff !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

.gr-tab-nav button:hover {
    color: #ffffff !important;
    background: rgba(59, 130, 246, 0.1) !important;
}

/* Loading states */
.gr-loading {
    animation: pulse 1.5s ease-in-out infinite !important;
}

@keyframes pulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .gr-textbox, .gr-dropdown, .gr-audio {
        font-size: 14px !important;
        padding: 12px !important;
    }
    
    .gr-button-primary, .gr-button-secondary {
        padding: 12px 20px !important;
        font-size: 14px !important;
    }
    
    .tag-btn {
        padding: 8px 12px !important;
        font-size: 12px !important;
        margin: 2px !important;
    }
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

.animate-fade-in {
    animation: fadeIn 0.5s ease-in-out;
}

.animate-slide-up {
    animation: slideUp 0.6s ease-out;
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

# Create the theme
chatterbox_theme = create_chatterbox_theme()

with gr.Blocks(
    title="Chatterbox AI - Beautiful Theme", 
    theme=chatterbox_theme,
    css=CUSTOM_CSS,
    head='<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">'
) as demo:
    
    gr.HTML('<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">')
    gr.Markdown("# <div class='animate-fade-in'>Chatterbox AI Voice Studio</div>")
    gr.Markdown("### <div class='animate-slide-up'>A unified interface for all Chatterbox TTS and Voice Conversion features.</div>")
    
    # Model states for lazy loading
    tts_model_state = gr.State(None)
    turbo_model_state = gr.State(None)
    mtl_model_state = gr.State(None)
    vc_model_state = gr.State(None)

    with gr.Tabs():
        # Tab 1: Chatterbox TTS (Original)
        with gr.TabItem("🎤 Classic TTS"):
            with gr.Row():
                with gr.Column():
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
                    
                    gr.Markdown(
                        "💡 **Note**: When switching to a sample voice, your current reference audio will be cleared. You can control this behavior with the checkbox below.",
                        elem_classes=["audio-note"]
                    )
                    
                    tts_clear_confirmation = gr.Checkbox(
                        label="Clear existing reference audio when switching to sample voice",
                        value=True,
                        info="Uncheck this to keep your current reference audio when selecting a sample voice"
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

                with gr.Column():
                    tts_audio_output = gr.Audio(label="Output Audio", elem_classes=["gr-audio"])

        # Tab 2: Chatterbox Turbo TTS
        with gr.TabItem("⚡ Turbo TTS"):
            gr.Markdown("### <div class='animate-slide-up'>Chatterbox Turbo</div>")

            with gr.Row():
                with gr.Column():
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

                with gr.Column():
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
        with gr.TabItem("🌍 Multilingual TTS"):
            gr.Markdown("# <div class='animate-fade-in'>Chatterbox Multilingual Demo</div>")
            gr.Markdown("Generate high-quality multilingual speech from text with reference audio styling, supporting 23 languages.")
            gr.Markdown(get_supported_languages_display())

            with gr.Row():
                with gr.Column():
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

                with gr.Column():
                    mtl_audio_output = gr.Audio(label="Output Audio", elem_classes=["gr-audio"])

        # Tab 4: Voice Conversion
        with gr.TabItem("🔀 Voice Conversion"):
            with gr.Row():
                with gr.Column():
                    vc_input_audio = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Input audio file", elem_classes=["gr-audio"])
                    vc_target_voice = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Target voice audio file (if none, the default voice is used)", value=None, elem_classes=["gr-audio"])
                    vc_run_btn = gr.Button("Convert", variant="primary", elem_classes=["gr-button-primary"])

                with gr.Column():
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

    # TTS sample voice change handler with confirmation
    def on_tts_voice_change(voice_selection, current_ref, clear_confirmation):
        print(f"🔄 TTS Dropdown change triggered: '{voice_selection}'")
        print(f"   Type: {type(voice_selection)}")
        print(f"   Clear confirmation: {clear_confirmation}")
        
        # Check if there's an existing reference audio that would be cleared
        has_existing_audio = current_ref is not None
        
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
            
            # If there's existing audio and user wants to clear it, load the sample
            if has_existing_audio and clear_confirmation:
                print(f"   🗑️  Clearing existing audio and loading sample: {audio_path}")
                return audio_path
            # If there's existing audio but user doesn't want to clear it, keep existing
            elif has_existing_audio and not clear_confirmation:
                print(f"   ⏸️  Keeping existing audio, not loading sample")
                return current_ref
            # If no existing audio, directly load the sample
            else:
                print(f"   📥 No existing audio, loading sample: {audio_path}")
                return audio_path
        
        print(f"   ❌ No audio found for: {voice_selection}")
        return current_ref

    tts_sample_voice.change(
        fn=on_tts_voice_change,
        inputs=[tts_sample_voice, tts_ref_wav, tts_clear_confirmation],
        outputs=[tts_ref_wav],
        show_progress=False
    )

if __name__ == "__main__":
    import os
    import uvicorn
    from fastapi import FastAPI
    import gradio as gr
    
    server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", 7860))
    root_path = os.getenv("GRADIO_ROOT_PATH", "")
    
    # Setup queue for progress bars and async events
    demo.queue(max_size=50, default_concurrency_limit=1)
    
    # Create a FastAPI app to handle proxy headers more robustly
    app = FastAPI()
    
    # Force HTTPS scheme if X-Forwarded-Proto is https
    @app.middleware("http")
    async def force_https_middleware(request, call_next):
        if request.headers.get("x-forwarded-proto") == "https":
            request.scope["scheme"] = "https"
        return await call_next(request)
    
    # Mount the Gradio app
        app = gr.mount_gradio_app(app, demo, path=root_path, allowed_paths=["/app/samples", "samples", "./samples"])
    
    print(f"🚀 Starting server on {server_name}:{server_port}")
    if root_path:
        print(f"📍 Root path: {root_path}")
        
    uvicorn.run(
        app, 
        host=server_name, 
        port=server_port, 
        forwarded_allow_ips="*",
        proxy_headers=True
    )