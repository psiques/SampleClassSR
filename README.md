# Sample Classifier

This script allows users to view and classify images into different categories, moving them to specific folders. The interface is developed in Python using the Tkinter library.

## Features
- Loads images from a defined folder.
- Classifies images as "Approved," "Rejected," or "Uncertain."
- Navigates through images.
- Zoom and pan functionality.
- Keyboard shortcuts for quick classification.

## Requirements
- Python 3.x
- Required libraries:
  - `Pillow`
  - `tkinter`

## Project Structure
The script scans for images in the folder specified by the `pasta_amostras` variable and displays an interface for classification. Classified images are moved to their respective subfolders.

## How to Use
1. Set the image folder path in the `pasta_amostras` variable.
2. Run the script.
3. Choose the initial image.
4. Use buttons or keyboard shortcuts to classify images.
5. Classified images will be moved to their corresponding folders.

## Controls
- `A`: Classifies as "Approved"
- `R`: Classifies as "Rejected"
- `D`: Classifies as "Uncertain"
- `→`: Moves to the next image
- `←`: Moves to the previous image
- Mouse scroll: Zoom in/out
- Click and drag: Moves the image within the view

## Future Improvements
- Add support for undoing the last classification.
- Enhance the graphical interface with more visual options.
- Store a log of all classifications made.

---

This project was developed to facilitate the organization and review of sample images.
