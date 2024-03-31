import streamlit as st
# from rembg import remove
from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO
# import base64
import os

PATH_TO_TASK_RESULTS = ""

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Visual Macros results")
st.write(
    # ":dog: Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available [here](https://github.com/tyler-simons/BackgroundRemoval) on GitHub. Special thanks to the [rembg library](https://github.com/danielgatis/rembg) :grin:"
    "Pick your task and other parameters to visualize results!"
)
st.sidebar.write("Pick a task")


# Download the fixed image
# def convert_image(img):
#     buf = BytesIO()
#     img.save(buf, format="PNG")
#     byte_im = buf.getvalue()
#     return byte_im

from PIL import Image
import streamlit as st

# Assuming 'train_output_paths' is a list of paths to your images
# Example: train_output_paths = ['path/to/img1.jpg', 'path/to/img2.jpg', ...]
def create_image_grid(image_paths, target_size):
    images = [Image.open(img_path).resize(target_size) for img_path in image_paths]
    
    # Assuming all images have the same width and different or same heights
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)
    
    # Create a new image with the appropriate height and width
    grid_img = Image.new('RGB', (max_width, total_height))
    
    # Paste each image into the grid
    y_offset = 0
    for img in images:
        grid_img.paste(img, (0, y_offset))
        y_offset += img.height
    
    return grid_img

def create_three_column_grid(paths1, paths2, paths3, target_size):
    triples = []
    
    for path1, path2, path3 in zip(paths1, paths2, paths3):
        # Load the first image and ensure it's the target size
        img1 = Image.open(path1).resize(target_size)
        
        # Load and resize the second and third images to match the target size
        img2 = Image.open(path2).resize(target_size)
        img3 = Image.open(path3).resize(target_size)
        
        # Create a new image to hold this triple side by side
        triple_width = target_size[0] * 3
        triple_height = target_size[1]
        triple_img = Image.new('RGB', (triple_width, triple_height))
        
        # Paste the three images next to each other
        triple_img.paste(img1, (0, 0))
        triple_img.paste(img2, (target_size[0], 0))
        triple_img.paste(img3, (target_size[0] * 2, 0))
        
        triples.append(triple_img)
    
    # Now, create the final grid by stacking triples vertically
    total_height = sum(img.height for img in triples)
    grid_img = Image.new('RGB', (triple_width, total_height))
    
    y_offset = 0
    for img in triples:
        grid_img.paste(img, (0, y_offset))
        y_offset += img.height
    
    return grid_img

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def create_three_column_grid_with_captions(paths1, paths2, paths3, target_size, captions):
    font_size = 50  # Adjust as needed
    top_padding = 30  # Space at the top of the grid for column captions
    
    # Attempt to load a font - adjust path as needed for your environment
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    triple_images = []
    
    # Process each set of images
    for path1, path2, path3 in zip(paths1, paths2, paths3):
        img1 = Image.open(path1).resize(target_size)
        img2 = Image.open(path2).resize(target_size)
        img3 = Image.open(path3).resize(target_size)
        
        triple_width = target_size[0] * 3
        triple_height = target_size[1]
        
        # Create an image for each row
        triple_img = Image.new('RGB', (triple_width, triple_height))
        triple_img.paste(img1, (0, 0))
        triple_img.paste(img2, (target_size[0], 0))
        triple_img.paste(img3, (target_size[0] * 2, 0))
        
        triple_images.append(triple_img)
    
    # Calculate total grid height with padding for captions
    total_height = sum(img.height for img in triple_images) + top_padding
    grid_width = triple_width
    grid_img = Image.new('RGB', (grid_width, total_height), "white")
    
    # Draw the column captions on the grid
    draw = ImageDraw.Draw(grid_img)
    for i, caption in enumerate(captions):
        text_width, text_height = textsize(caption, font=font)
        text_x = target_size[0] * i + (target_size[0] - text_width) / 2
        draw.text((text_x, (top_padding - text_height) / 2), caption, fill="black", font=font)
    
    # Paste each row image into the grid, below the captions
    y_offset = top_padding
    for img in triple_images:
        grid_img.paste(img, (0, y_offset))
        y_offset += img.height
    
    return grid_img

from PIL import Image, ImageDraw, ImageFont

def create_four_column_grid_with_captions(paths1, paths2, paths3, paths4, target_size, captions):
    font_size = 100  # Adjust as needed
    top_padding = 30  # Space at the top of the grid for column captions
    
    # Attempt to load a font - adjust path as needed for your environment
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    quad_images = []
    
    # Process each set of images
    for path1, path2, path3, path4 in zip(paths1, paths2, paths3, paths4):
        img1 = Image.open(path1).resize(target_size)
        img2 = Image.open(path2).resize(target_size)
        img3 = Image.open(path3).resize(target_size)
        img4 = Image.open(path4).resize(target_size)
        
        quad_width = target_size[0] * 4
        quad_height = target_size[1]
        
        # Create an image for each row
        quad_img = Image.new('RGB', (quad_width, quad_height))
        quad_img.paste(img1, (0, 0))
        quad_img.paste(img2, (target_size[0], 0))
        quad_img.paste(img3, (target_size[0] * 2, 0))
        quad_img.paste(img4, (target_size[0] * 3, 0))
        
        quad_images.append(quad_img)
    
    # Calculate total grid height with padding for captions
    total_height = sum(img.height for img in quad_images) + top_padding
    grid_width = quad_width
    grid_img = Image.new('RGB', (grid_width, total_height), "white")
    
    # Draw the column captions on the grid
    draw = ImageDraw.Draw(grid_img)
    for i, caption in enumerate(captions):
        text_width, text_height = textsize(caption, font=font)
        text_x = target_size[0] * i + (target_size[0] - text_width) / 2
        draw.text((text_x, (top_padding - text_height) / 2), caption, fill="black", font=font)
    
    # Paste each row image into the grid, below the captions
    y_offset = top_padding
    for img in quad_images:
        grid_img.paste(img, (0, y_offset))
        y_offset += img.height
    
    return grid_img

# Example usage
# Make sure paths1, paths2, paths3, and paths4 are defined lists of image paths.
# target_size should be a tuple like (width, height), and captions a list of four strings.
# grid_img = create_four_column_grid_with_captions(paths1, paths2, paths3, paths4, target_size, captions)
# Note: You'd display the grid_img using your preferred method, e.g., in a Jupyter notebook or saving to a file.


def segmentation():
    segmentation_results_path = PATH_TO_TASK_RESULTS+"segmentation-task/results/"
    seggpt_results_path = PATH_TO_TASK_RESULTS+"segmentation-task/seggpt_results/cheese/9.jpg"

    folders = [d for d in os.listdir(segmentation_results_path) if os.path.isdir(os.path.join(segmentation_results_path, d))]
    class_names = list(set([folder.split("-")[0] for folder in folders]))
    list_number_training_samples = list(set([folder.split("-")[1] for folder in folders]))
    seg_class = st.sidebar.selectbox(
    "Class",
    options=class_names
    )
    num_training_samples = st.sidebar.selectbox(
    "number of training samples",
    options=list_number_training_samples
    )
    path_to_image = segmentation_results_path+f"{seg_class}-{num_training_samples}/"
    num_epochs = st.sidebar.selectbox(
    "epochs",
    options=[s for s in os.listdir(path_to_image) if s.isdigit()]
    )
    train_output_paths = [path_to_image+f"{num_epochs}/0/train/" + img_file_name for img_file_name in os.listdir(path_to_image+f"{num_epochs}/0/train/")]
    train_data_before_paths = [PATH_TO_TASK_RESULTS+"segmentation-task/"+f"{seg_class}/train-a/" + img_file_name for img_file_name in os.listdir(path_to_image+f"{num_epochs}/0/train/")]
    train_data_after_paths = [PATH_TO_TASK_RESULTS+"segmentation-task/"+f"{seg_class}/train-b/" + img_file_name for img_file_name in os.listdir(path_to_image+f"{num_epochs}/0/train/")]
    
    target_img = Image.open(train_output_paths[0])
    target_size = target_img.size


    test_output_paths = [path_to_image+f"{num_epochs}/0/test/" + img_file_name for img_file_name in os.listdir(path_to_image+f"{num_epochs}/0/test/")]
    test_data_before_paths = [PATH_TO_TASK_RESULTS+"segmentation-task/"+f"{seg_class}/train-a/" + img_file_name for img_file_name in os.listdir(path_to_image+f"{num_epochs}/0/test/")]
    test_data_after_paths = [PATH_TO_TASK_RESULTS+"segmentation-task/"+f"{seg_class}/train-b/" + img_file_name for img_file_name in os.listdir(path_to_image+f"{num_epochs}/0/test/")]
    
    seggpt_output_paths = [PATH_TO_TASK_RESULTS+"segmentation-task/seggpt_results/"+f"{seg_class}/" + img_file_name for img_file_name in os.listdir(path_to_image+f"{num_epochs}/0/test/")]

    train_captions = ["Train input", "Train ground truth", "VisualMacros output"] 
    test_captions = ["Test input", "Test ground truth", "VisualMacros output", "SegGpt"] 
    grid_img_train = create_three_column_grid_with_captions(train_data_before_paths, train_data_after_paths, train_output_paths, target_size, train_captions)
    # grid_img_test = create_three_column_grid_with_captions(test_data_before_paths, test_data_after_paths, test_output_paths, target_size, captions)
    grid_img_test = create_four_column_grid_with_captions(test_data_before_paths, test_data_after_paths, test_output_paths, seggpt_output_paths, target_size, test_captions)
    # grid_img_seggpt = create_image_grid(seggpt_output_paths, target_size)

    return grid_img_train, grid_img_test
        

task = st.sidebar.selectbox(
"Tasks",
options=["",'segmentation-task']
)
img_train = None
if task == 'segmentation-task':
    img_train, img_test= segmentation()
    
# st.image(img, caption='Sunrise by the mountains')
if img_train:
    col1, col2= st.columns(2)
    col1.markdown("**Train Samples**")
    col1.image(img_train, caption="train samples")
    col2.markdown("**Test Samples**")
    col2.image(img_test, caption="test samples")
    
