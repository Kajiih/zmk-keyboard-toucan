import re
import os

def render_layer(name, bindings_text, col_width, sep_line, thumb_sep):
    tokens = re.findall(r"&[a-zA-Z0-9_]+(?:\s+[a-zA-Z0-9_]+)*", bindings_text)
    
    clean_tokens = []
    for token in tokens:
        t = token.replace("&kp ", "").replace("&", "")
        t = t.replace("hm_l ", "").replace("hm_r ", "").replace("hm_fast_l ", "").replace("hm_fast_r ", "").replace("hm_comma_r ", "").replace("hm_dot_r ", "")
        clean_tokens.append(t)
        
    if len(clean_tokens) < 42:
        print(f"Warning: Found {len(clean_tokens)} keys instead of 42 in layer {name}.")
        return

    print("\n" + "="*43 + f" TOUCAN {name} LAYER " + "="*43)
    print("\n   LEFT HAND keys cluster:                           RIGHT HAND keys cluster:")
    print("   " + sep_line + "     " + sep_line)
    
    for row in range(3):
        left_part = " | ".join(f"{clean_tokens[row*12 + col]:<{col_width}}" for col in range(6))
        right_part = " | ".join(f"{clean_tokens[row*12 + col]:<{col_width}}" for col in range(6, 12))
        print(f"   [ {left_part} ]     [ {right_part} ]")
        print("   " + sep_line + "     " + sep_line)
            
    print("\n" + " "*35 + "LEFT THUMBS:" + " "*42 + "RIGHT THUMBS:")
    print(" "*19 + thumb_sep + "     " + thumb_sep)
    left_thumbs = " | ".join(f"{clean_tokens[36 + col]:<{col_width}}" for col in range(3))
    right_thumbs = " | ".join(f"{clean_tokens[39 + col]:<{col_width}}" for col in range(3))
    print(" "*19 + f"[ {left_thumbs} ]     [ {right_thumbs} ]")
    print(" "*19 + thumb_sep + "     " + thumb_sep)
    print("\n" + "="*105 + "\n")

def parse_and_visualize():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    keymap_path = os.path.abspath(os.path.join(script_dir, "..", "config", "toucan.keymap"))
    
    if not os.path.exists(keymap_path):
        print(f"Error: Keymap file not found at {keymap_path}")
        return
        
    with open(keymap_path, "r") as f:
        content = f.read()
    
    col_width = 13
    sep_line = "-" * (col_width * 6 + 13)
    thumb_sep = "-" * 47

    # Parse and render BASE layer
    base_match = re.search(r"base\s*\{.*?bindings\s*=\s*<(.*?)>;", content, re.DOTALL)
    if base_match:
        render_layer("BASE", base_match.group(1), col_width, sep_line, thumb_sep)
        
    # Parse and render NAV layer
    nav_match = re.search(r"nav\s*\{.*?bindings\s*=\s*<(.*?)>;", content, re.DOTALL)
    if nav_match:
        render_layer("NAV", nav_match.group(1), col_width, sep_line, thumb_sep)

if __name__ == "__main__":
    parse_and_visualize()
