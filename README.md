# Image Organizer

## Overview
Image Organizer is an application designed to help users organize their images efficiently. Users can send a folder filled with images, and the application provides two options for organizing them: by chronological order and by category. The application utilizes state-of-the-art AI models for image classification.

## Features
- Organize images chronologically by year and month.
- Categorize images based on their content using AI.
- Toggle between chronological and category organization.

## Project Structure
```
image-organizer
├── src
│   ├── main.py          # Entry point of the application
│   ├── models
│   │   ├── classifier.py # AI model for image classification
│   │   └── utils.py      # Utility functions for model handling
│   ├── services
│   │   ├── file_handler.py # File operations for loading and saving images
│   │   ├── image_processor.py # Image processing functionalities
│   │   └── date_organizer.py # Organizing images by date
│   ├── config
│   │   └── settings.py   # Configuration settings for the application
│   └── tests
│       └── test_organizer.py # Unit tests for the application
├── requirements.txt      # Dependencies for the project
└── README.md             # Documentation for the project
```

## Setup Instructions
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python src/main.py
   ```
2. Follow the prompts to select the folder containing images and choose the organization method.

## AI Model
The application uses EfficientNetB4 pre-trained on ImageNet, which can recognize 1000 different categories of images out of the box. No additional training is required. The model will automatically download when you first run the application (approximately 75MB).

Key features:
- Pre-trained on over 1.4 million images
- Can recognize 1000 different categories
- Includes common objects, animals, scenes, and more
- ~83% top-1 accuracy on ImageNet validation set

## License
This project is licensed under the MIT License.
