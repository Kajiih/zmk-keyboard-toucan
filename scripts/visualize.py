import re
import os

def parse_and_visualize():
    # Locate the keymap file dynamically relative to this script's folder for cross-computer portability
    script_dir = os.path.dirname(os.path.abspath(__file__))
    keymap_path = os.path.abspath(os.path.join(script_dir, "..", "config", "toucan.keymap"))
    
    if not os.path.exists(keymap_path):
        print(f"Error: Keymap file not found at {keymap_path}")
        return
        
    with open(keymap_path, "r") as f:
        content = f.read()
    
    base_match = re.search(r"base\s*\{.*?bindings\s*=\s*<(.*?)>;", content, re.DOTALL)
    if not base_match:
        print("Could not find base layer bindings.")
        return
    
    bindings_text = base_match.group(1)
    tokens = re.findall(r"&[a-zA-Z0-9_]+(?:\s+[a-zA-Z0-9_]+)*", bindings_text)
    
    clean_tokens = []
    for token in tokens:
        t = token.replace("&kp ", "").replace("&", "")
        t = t.replace("hm_l ", "").replace("hm_r ", "").replace("hm_fast_l ", "").replace("hm_fast_r ", "").replace("hm_comma_r ", "").replace("hm_dot_r ", "")
        clean_tokens.append(t)
        
    if len(clean_tokens) < 42:
        print(f"Warning: Found {len(clean_tokens)} keys instead of 42.")
        return

    col_width = 13
    sep_line = "-" * (col_width * 6 + 13)

    print("\n" + "="*43 + " TOUCAN BASE LAYER " + "="*43)
    print("\n   LEFT HAND alpha & outer columns:                  RIGHT HAND alpha & punctuation columns:")
    print("   " + sep_line + "     " + sep_line)
    
    for row in range(3):
        left_part = " | ".join(f"{clean_tokens[row*12 + col]:<{col_width}}" for col in range(6))
        right_part = " | ".join(f"{clean_tokens[row*12 + col]:<{col_width}}" for col in range(6, 12))
        print(f"   [ {left_part} ]     [ {right_part} ]")
        print("   " + sep_line + "     " + sep_line)
            
    print("\n" + " "*35 + "LEFT THUMBS:" + " "*42 + "RIGHT THUMBS:")
    thumb_sep = "-" * 47
    print(" "*19 + thumb_sep + "     " + thumb_sep)
    left_thumbs = " | ".join(f"{clean_tokens[36 + col]:<{col_width}}" for col in range(3))
    right_thumbs = " | ".join(f"{clean_tokens[39 + col]:<{col_width}}" for col in range(3))
    print(" "*19 + f"[ {left_thumbs} ]     [ {right_thumbs} ]")
    print(" "*19 + thumb_sep + "     " + thumb_sep)
    print("\n" + "="*105 + "\n")

if __name__ == "__main__":
    parse_and_visualize()
