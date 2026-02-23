import cairosvg
import os

def convert_all_svg(svg_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(svg_folder):
        if filename.endswith(".svg"):
            svg_path = os.path.join(svg_folder, filename)
            png_path = os.path.join(output_folder, filename.replace(".svg", ".png"))
            
            # Convertit en PNG avec une haute résolution (512px)
            cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=512, output_height=512)
            print(f"Converti : {filename}")

# Utilisation
convert_all_svg("assets/svg", "assets/icons")
