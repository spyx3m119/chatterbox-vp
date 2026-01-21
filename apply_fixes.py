import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 1. Fix gr.Blocks inclusion of head
    if 'with gr.Blocks(' in content:
        # Move title and css into head or just add head
        # We'll use a regex-like approach for simplicity
        if 'gr.HTML(\'<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">\')' in content:
            content = content.replace('gr.HTML(\'<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">\')', '')
            
        if 'head=' not in content and 'with gr.Blocks(' in content:
            content = content.replace('with gr.Blocks(', 'with gr.Blocks(head=\'<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">\', ')
            
    # 2. Fix Tailwind injection (ensure it's via gr.HTML if not there)
    if 'gr.HTML(\'<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">\')' not in content:
        # Find gr.Blocks start and insert after
        lines = content.split('\n')
        new_lines = []
        inserted = False
        for line in lines:
            new_lines.append(line)
            if 'with gr.Blocks' in line and not inserted:
                # Add at next indentation level
                indent = line[:line.find('with')]
                new_lines.append(indent + '    gr.HTML(\'<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">\')')
                inserted = True
        content = '\n'.join(new_lines)

    # 3. Clean up LANGUAGE_CONFIG in specific files if they are large
    # For now, let's just make sure the subpaths are gone if we can't delete the whole block
    content = content.replace('mtl_prompts/ar_f/ar_prompts2.flac', 'mtl_prompts/ar_prompts2.flac')
    content = content.replace('mtl_prompts/ja/ja_prompts1.flac', 'mtl_prompts/ja_prompts1.flac')

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
