import cv2
import numpy as np
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='find and save checkerboard coordinates in .pgm images.')
    parser.add_argument('directory', help='directory containing .pgm images')
    parser.add_argument('--rows', type=int, required=True, help='number of internal corners in the checkerboard (rows, vertical direction)')
    parser.add_argument('--cols', type=int, required=True, help='number of internal corners in the checkerboard (cols, horizontal direction)')
    parser.add_argument('--square_size', type=float, required=True, help='length of one square in the checkerboard (in mm)')
    args = parser.parse_args()

    directory = args.directory
    rows = args.rows
    cols = args.cols
    square_size = args.square_size

    if not os.path.isdir(directory):
        print(f"ERROR: '{directory}' directory not found.")
        sys.exit(1)

    image_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pgm'):
                image_paths.append(os.path.join(root, file))

    if not image_paths:
        print(f"From '{directory}' can't find .pgm file.")
        sys.exit(0)

    print(f"From '{directory}'.pgm found {len(image_paths)}.")

    criteria = (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)

    for img_path in image_paths:
        print(f"processing: {img_path}...")
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Can't open image: {img_path}")
            continue

        pattern_size = (cols, rows)
        ret, corners = cv2.findChessboardCorners(img, pattern_size, None)
        print(f"results: {ret}")
        if not ret:
            print(f"Can't find conner skip.")
            continue

        corners = cv2.cornerSubPix(img, corners, (11, 11), (-1, -1), criteria)
        corners = corners.reshape(-1, 2)

        base_name = os.path.splitext(os.path.basename(img_path))[0]
        pixel_file = f"pixelpoint_{base_name}.txt"
        global_file = f"globalcoord_{base_name}.txt"

        try:
            with open(pixel_file, 'w') as f_px:
                for (x, y) in corners:
                    f_px.write(f"{x:.6f} {y:.6f}\n")

            with open(global_file, 'w') as f_gl:
                for i in range(rows):
                    for j in range(cols):
                        x_global = j * square_size
                        y_global = i * square_size
                        f_gl.write(f"{x_global:.6f} {y_global:.6f} 0\n")

        except Exception as e:
            print(f"Error: {e}")

    print("Finish.")

if __name__ == "__main__":
    main()
