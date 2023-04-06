import cv2
import os
import glob

def load_n_crop(img_path):
    
    # Load the image
    img = cv2.imread(img_path)

    # Determine the window size
    window_width = 800
    window_height = 600

    if img.shape[1]<img.shape[0]:
        window_width = 600
        window_height = 800

    # Determine the scaling factor
    scale_width = window_width / img.shape[1]
    scale_height = window_height / img.shape[0]
    scale = min(scale_width, scale_height)

    # Resize the image
    img_resized = cv2.resize(img, None, fx=scale, fy=scale)

    # Display the image in a window
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image", window_width, window_height)
    cv2.imshow("Image", img_resized)

    # Define the ROI
    roi = cv2.selectROI("Image", img_resized, False)

    # Unscale the ROI coordinates
    x, y, w, h = roi
    x_unscaled = int(x / scale)
    y_unscaled = int(y / scale)
    w_unscaled = int(w / scale)
    h_unscaled = int(h / scale)

    # Crop the image
    img_cropped = img[y_unscaled:y_unscaled+h_unscaled, x_unscaled:x_unscaled+w_unscaled]

    # Check the aspect ratio of the cropped image
    height, width, channels = img_cropped.shape
    if width > height:
        # Rotate the image by 90 degrees counterclockwise
        img_cropped = cv2.rotate(img_cropped, cv2.ROTATE_90_CLOCKWISE)

    # Save the cropped image
    filename = os.path.basename(img_path)
    dest_dir = os.path.dirname(img_path)+"_sopclassified"
    os.makedirs(dest_dir, exist_ok=True)
    cv2.imwrite(os.path.join(dest_dir, filename), img_cropped)

    # Wait for a key press and then close the window
    # cv2.waitKey(0)
    cv2.destroyAllWindows()


def main(dirpath):
    print(dirpath)
    img_files = os.listdir(dirpath)
    print("Total number of files:", len(img_files))

    for ind, imfile in enumerate(img_files):
        imfile_path = os.path.join(dirpath, imfile)
        load_n_crop(imfile_path)
        print(f"Files processed: {ind+1}", end="\r")
    

if __name__=="__main__":
    folder_path = str(input("Enter the directory path: ")).lstrip(" ")
    main(folder_path)