def main():
    import os
    from services.file_handler import load_images, save_images
    from services.date_organizer import DateOrganizer
    from models.classifier import ImageClassifier
    from tqdm import tqdm

    # Initialize the image classifier
    classifier = ImageClassifier()

    # Get user input for folder selection
    input_folder = input("Please enter the path to the folder containing images: ")
    output_folder = input("Please enter the path to the output folder: ")

    # Load images from the specified folder
    images = load_images(input_folder)
    
    if not images:
        print("No images found in the specified folder.")
        return

    # Ask user for organization preference
    org_method = input("How would you like to organize images? (date/category): ").strip().lower()

    if org_method == 'category':
        print("Classifying images... This may take a moment.")
        
        # Add progress bar
        with tqdm(total=len(images), desc="Classifying images") as pbar:
            predictions = []
            for i in range(0, len(images), 32):  # Process in batches of 32
                batch = images[i:i+32]
                batch_predictions = classifier.predict_categories(batch)
                
                # Enhanced logging with top 3 predictions
                for img, pred in zip(batch, batch_predictions):
                    print(f"\nImage: {os.path.basename(img.filename)}")
                    print(f"Selected Category: {pred['category']}")
                    print(f"Confidence: {pred['confidence']:.2%}")
                    print("Top 3 predictions:")
                    for category, conf in pred['top_3']:
                        print(f"  - {category}: {conf:.2%}")
                
                predictions.extend(batch_predictions)
                pbar.update(len(batch))
        
        # Organize images with higher confidence threshold
        categorized_images = {}
        uncategorized = []
        
        for img, pred in zip(images, predictions):
            if pred['confidence'] < 0.45:  # Increased confidence threshold
                uncategorized.append(img)
                continue
                
            category = pred['category']
            if category not in categorized_images:
                categorized_images[category] = []
            categorized_images[category].append(img)

        # Save categorized images
        for category, category_images in categorized_images.items():
            category_path = os.path.join(output_folder, category)
            save_images(category_images, category_path)
            print(f"Saved {len(category_images)} images in category: {category}")

        if uncategorized:
            print(f"\nUncategorized images ({len(uncategorized)}): Low confidence predictions")
            save_images(uncategorized, os.path.join(output_folder, 'uncategorized'))
    
    else:  # date organization
        date_organizer = DateOrganizer(images)
        organized_images = date_organizer.organize_by_date()
        
        # Save images organized by date
        for year in organized_images:
            for month in organized_images[year]:
                month_path = os.path.join(output_folder, f"{year}-{month:02d}")
                save_images(organized_images[year][month], month_path)

    print("Image organization completed successfully!")

if __name__ == "__main__":
    main()