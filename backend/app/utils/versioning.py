import re
def generate_next_version(previous: str, manual: str = None, is_automatic: bool = True) -> str:
    if not is_automatic and manual:
        if not re.match(r'^v\d+(\.\d+){1,2}$', manual): raise ValueError("Invalid format")
        return manual
    parts = previous.split('.')
    if parts[-1].isdigit():
        parts[-1] = str(int(parts[-1]) + 1)
    else:
        match = re.search(r'(\d+)$', previous)
        if match: parts[-1] = re.sub(r'\d+$', str(int(match.group(1))+1), parts[-1])
        else: parts.append('1')
    return '.'.join(parts)
