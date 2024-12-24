import os

def load_images(folder_path):
    import os
    from PIL import Image

    images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            img_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(img_path)
                img.filename = img_path  # Store the original path
                images.append(img)
            except Exception as e:
                print(f"Warning: Could not load image {filename}: {e}")
    return images

def save_images(images, output_folder):
    import os

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for idx, img in enumerate(images):
        img.save(os.path.join(output_folder, f'image_{idx}.png'))  # Save as PNG for consistency

def organize_images_by_date(images):
    from datetime import datetime

    organized_images = {}
    for img in images:
        creation_date = datetime.fromtimestamp(os.path.getctime(img.filename))
        year_month = (creation_date.year, creation_date.month)
        if year_month not in organized_images:
            organized_images[year_month] = []
        organized_images[year_month].append(img)
    return organized_images