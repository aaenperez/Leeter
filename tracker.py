import json


def load_patterns(file_path):
    with open(file_path) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}
        
def save_patterns(file_path, patterns):
    with open(file_path, 'w') as f:
        json.dump(patterns, f)


def update_patterns(file_path, pattern_name, outcome):
    patterns = load_patterns(file_path)
    
    if pattern_name not in patterns:
        patterns[pattern_name] = {"solved": 0, "struggled": 0}
    
    patterns[pattern_name][outcome] += 1
    
    save_patterns(file_path, patterns)

def get_summary(file_path):
    patterns = load_patterns(file_path)

    sorted_patterns = dict(sorted(patterns.items(), key=lambda item: item[1]["struggled"], reverse=True))
    return sorted_patterns