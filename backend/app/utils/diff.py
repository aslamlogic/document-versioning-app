from difflib import unified_diff
def generate_diff_html(original: str, modified: str) -> str:
    diff = list(unified_diff(original.splitlines(), modified.splitlines(), lineterm=''))
    html = []
    for line in diff:
        if line.startswith('+'): html.append(f'<span style="background:#c8e6c9">{line}</span><br>')
        elif line.startswith('-'): html.append(f'<span style="background:#ffcdd2">{line}</span><br>')
        else: html.append(f'{line}<br>')
    return ''.join(html)
