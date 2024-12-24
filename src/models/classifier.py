import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB4, ResNet50V2
from tensorflow.keras.applications.efficientnet import preprocess_input as efficientnet_preprocess
from tensorflow.keras.applications.resnet_v2 import preprocess_input as resnet_preprocess
from tensorflow.keras.applications.efficientnet import decode_predictions as efficientnet_decode
from tensorflow.keras.applications.resnet_v2 import decode_predictions as resnet_decode
from PIL import Image

class ImageClassifier:
    def __init__(self):
        # Initialize multiple models for ensemble
        self.models = {
            'efficientnet': {
                'model': EfficientNetB4(weights='imagenet'),
                'preprocess': efficientnet_preprocess,
                'size': (380, 380),
                'decode': efficientnet_decode
            },
            'resnet': {
                'model': ResNet50V2(weights='imagenet'),
                'preprocess': resnet_preprocess,
                'size': (224, 224),
                'decode': resnet_decode
            }
        }
        
        # Custom category mapping for better organization
        self.category_mapping = {
            'golden_retriever': 'Dogs',
            'labrador': 'Dogs',
            'german_shepherd': 'Dogs',
            'persian_cat': 'Cats',
            'siamese_cat': 'Cats',
            'tabby_cat': 'Cats',
            'seashore': 'Landscapes',
            'mountain': 'Landscapes',
            'valley': 'Landscapes',
            # Add more mappings as needed
        }

    def preprocess_image(self, image, model_name):
        if isinstance(image, Image.Image):
            # Enhanced preprocessing
            image = image.convert('RGB')  # Ensure RGB
            image = image.resize(self.models[model_name]['size'], Image.LANCZOS)  # Better resize
            image = np.array(image)
            
        # Handle grayscale images
        if len(image.shape) == 2:
            image = np.stack([image] * 3, axis=-1)
        elif image.shape[2] == 1:
            image = np.concatenate([image] * 3, axis=-1)
        
        # Ensure image has 3 channels and convert to RGB if necessary
        if image.shape[2] == 4:  # RGBA
            image = image[:, :, :3]
        
        # Expand dimensions and preprocess
        image = np.expand_dims(image, axis=0)
        return self.models[model_name]['preprocess'](image)

    def predict_category(self, image):
        """Predict category using model ensemble."""
        all_predictions = {}
        
        try:
            # Get predictions from each model
            for model_name, model_info in self.models.items():
                processed_image = self.preprocess_image(image, model_name)
                predictions = model_info['model'].predict(processed_image, verbose=0)  # Suppress progress bar
                decoded = model_info['decode'](predictions, top=3)[0]
                
                for _, category, confidence in decoded:
                    if category in all_predictions:
                        all_predictions[category] += confidence
                    else:
                        all_predictions[category] = confidence

            # If no predictions were made, return uncategorized
            if not all_predictions:
                return {
                    'category': 'uncategorized',
                    'confidence': 0.0,
                    'top_3': []
                }

            # Average the predictions
            for category in all_predictions:
                all_predictions[category] /= len(self.models)
            
            # Get the best prediction
            best_category = max(all_predictions.items(), key=lambda x: x[1])
            category, confidence = best_category
            
            # Map to custom category if available
            mapped_category = self.category_mapping.get(category, category.replace('_', ' ').title())
            
            return {
                'category': mapped_category,
                'confidence': float(confidence),
                'top_3': sorted(all_predictions.items(), key=lambda x: x[1], reverse=True)[:3]
            }

        except Exception as e:
            print(f"Warning: Error during prediction: {e}")
            return {
                'category': 'uncategorized',
                'confidence': 0.0,
                'top_3': []
            }

    def predict_categories(self, images, batch_size=32):
        """Predict categories for multiple images using ensemble."""
        results = []
        for image in images:
            results.append(self.predict_category(image))
        return results