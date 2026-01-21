import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix mount_gradio_app path and allowed_paths
    old_line = 'app = gr.mount_gradio_app(app, demo, path=root_path, allowed_paths=["/app/samples"])'
    # Try multiple variations since previous edits might have changed spacing
    content = content.replace('path=root_path, allowed_paths=["/app/samples"]', 'path=root_path or "/", allowed_paths=["/app/samples", "samples", "./samples"]')
    
    # Also handle the one with extra spaces if it exists
    content = content.replace('path=root_path, allowed_paths=["/app/samples"]', 'path=root_path or "/", allowed_paths=["/app/samples", "samples", "./samples"]')
    
    # Ensure correct indentation for app = gr.mount_gradio_app
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'gr.mount_gradio_app' in line:
            # Normalize indentation: should be 4 spaces inside the if block
            indent = line[:line.find('app =')]
            if 'app =' in line:
                lines[i] = '    app = gr.mount_gradio_app(app, demo, path=root_path or "/", allowed_paths=["/app/samples", "samples", "./samples"])'

    content = '\n'.join(lines)

    with open(filepath, 'w') as f:
        f.write(content)

files = [
    '/Users/vladimirparole/Projects/chatterbox/unified_webui.py',
    '/Users/vladimirparole/Projects/chatterbox/enhanced_unified_webui.py',
    '/Users/vladimirparole/Projects/chatterbox/final_themed_webui.py'
]

for f in files:
    if os.path.exists(f):
        print(f"Fixing {f}")
        fix_file(f)
    else:
        print(f"File not found: {f}")
