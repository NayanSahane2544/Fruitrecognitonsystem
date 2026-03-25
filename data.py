import os
import shutil

# 1. Setup your paths
# Update these paths to where your downloaded Fruits-360 dataset is located

original_dataset_path = r'F:\Fruits\fruits-360_100x100\fruits-360'
new_dataset_path = 'custom_dataset'

# 2. Define the 6 overarching classes you want to keep
target_classes = ['Almond','Ananas','Apple','Banana','Grape','Guava', 'Mango','Orange','Pomegranate','Strawberry','Walnut','Watermelon']

def merge_classes(split_type):
    """Merges sub-directories into a main class directory for Train/Test splits."""
    orig_split_dir = os.path.join(original_dataset_path, split_type)
    new_split_dir = os.path.join(new_dataset_path, split_type)
    
    # Create the new base directory (e.g., custom_dataset/Training)
    os.makedirs(new_split_dir, exist_ok=True)
    
    # Create the 6 target class folders
    for target in target_classes:
        os.makedirs(os.path.join(new_split_dir, target), exist_ok=True)

    # Loop through the original folders
    for folder_name in os.listdir(orig_split_dir):
        # Check if the original folder name starts with one of our target classes
        for target in target_classes:
            if folder_name.startswith(target):
                source_folder = os.path.join(orig_split_dir, folder_name)
                dest_folder = os.path.join(new_split_dir, target)
                
                # Copy all images from the sub-class to the merged class
                for image_file in os.listdir(source_folder):
                    src_image_path = os.path.join(source_folder, image_file)
                    # Rename slightly to avoid overwriting files with the same name from different sub-classes
                    new_image_name = f"{folder_name}_{image_file}" 
                    dest_image_path = os.path.join(dest_folder, new_image_name)
                    
                    shutil.copy2(src_image_path, dest_image_path)
                print(f"Merged {folder_name} into {target}")

# Run for both Training and Test directories
print("Merging Training Data...")
merge_classes('Training')
print("Merging Test Data...")
merge_classes('Test')
print("Done! Data is ready.")