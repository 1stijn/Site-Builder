import os
import re

TEMPLATE_PATH = 'templates/base.html'

def sanitize_filename(title):
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title).strip()
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized

def parse_color(color_input):
    if re.match(r'^#?[0-9A-Fa-f]{6}$', color_input):
        return f'style="background-color: #{color_input.lstrip("#")};"'
    
    elif re.match(r'^rgb\(\d{1,3}, *\d{1,3}, *\d{1,3}\)$', color_input):
        return f'style="background-color: {color_input};"'
    
    elif color_input in ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']:
        return f'class="bg-{color_input} text-white"'
    
    elif re.match(r'^[a-zA-Z]+$', color_input):
        return f'style="background-color: {color_input.lower()};"'
    
    else:
        return f'style="background-color: {color_input};"'

def easy_mode():
    print("\nEasy Mode:")
    title = input("Enter the title of the website: ")
    header_text = input("Enter the text for the header: ")
    primary_color = input("Enter the primary color (hex, rgb, or Bootstrap class): ")
    secondary_color = input("Enter the secondary color (hex, rgb, or Bootstrap class): ")

    sanitized_title = sanitize_filename(title)
    output_path = f'output/{sanitized_title}.html'

    modify_template(title, header_text, primary_color, secondary_color, output_path=output_path)

def hard_mode():
    print("\nHard Mode:")
    title = input("Enter the title of the website: ")
    header_text = input("Enter the text for the header: ")
    primary_color = input("Enter the primary color (hex, rgb, or Bootstrap class): ")
    secondary_color = input("Enter the secondary color (hex, rgb, or Bootstrap class): ")
    footer_text = input("Enter the footer text: ")
    parallax_text = input("Enter the text for the parallax section: ")
    image1_description = input("Enter description for Image 1: ")
    image2_description = input("Enter description for Image 2: ")
    image3_description = input("Enter description for Image 3: ")

    sanitized_title = sanitize_filename(title)
    output_path = f'output/{sanitized_title}.html'

    modify_template(title, header_text, primary_color, secondary_color, footer_text, parallax_text, image1_description, image2_description, image3_description, output_path=output_path)

def modify_template(title, header_text, primary_color, secondary_color, footer_text="&copy; 2024 Bootstrap Showcase | All rights reserved", parallax_text="Parallax Section", img1_desc="Description for Image 1", img2_desc="Description for Image 2", img3_desc="Description for Image 3", output_path='output/generated_site.html'):
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Error: Template file '{TEMPLATE_PATH}' not found.")
        return

    with open(TEMPLATE_PATH, 'r') as file:
        content = file.read()

    primary_color_class = parse_color(primary_color)
    secondary_color_class = parse_color(secondary_color)

    if 'class="' in primary_color_class: 
        content = content.replace('class="bg-primary text-white text-center py-4"', f'class="{primary_color_class} text-center py-4"')
    else:  
        content = content.replace('class="bg-primary text-white text-center py-4"', f'class="text-center py-4" {primary_color_class}')

    if 'class="' in secondary_color_class:  
        content = content.replace('class="bg-dark text-white text-center py-3"', f'class="{secondary_color_class} text-center py-3"')
    else:  
        content = content.replace('class="bg-dark text-white text-center py-3"', f'class="text-center py-3" {secondary_color_class}')

    content = content.replace('<title>Bootstrap Modern Website</title>', f'<title>{title}</title>')
    content = content.replace('<h1>Bootstrap Showcase</h1>', f'<h1>{header_text}</h1>')
    content = content.replace('<h2 class="text-info">Parallax Section</h2>', f'<h2 class="text-info">{parallax_text}</h2>')
    content = content.replace('<p>Description for Image 1</p>', f'<p>{img1_desc}</p>')
    content = content.replace('<p>Description for Image 2</p>', f'<p>{img2_desc}</p>')
    content = content.replace('<p>Description for Image 3</p>', f'<p>{img3_desc}</p>')
    content = content.replace('&copy; 2024 Bootstrap Showcase | All rights reserved', footer_text)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        file.write(content)

    print(f"Website generated successfully at '{output_path}'.")

def main():
    print("Welcome to the Website Generator!")
    mode = input("Choose a mode: 'easy' or 'hard': ").strip().lower()

    if mode == 'easy':
        easy_mode()
    elif mode == 'hard':
        hard_mode()
    else:
        print("Invalid option. Please choose 'easy' or 'hard'.")

if __name__ == "__main__":
    main()
