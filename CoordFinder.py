import cv2
import argparse

def mouse_callback_savetxt(event, x, y, flags, param):
    data = param 
    img = data["img"].copy()
    points = data["points"]

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f" Coordinate: ({x}, {y})")
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(img, f"({x},{y})", (x+10, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv2.imshow("Image", img)
        points.append((x, y))

def mouse_callback_view(event, x, y, flags, param):
    img = param.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f" Coordinate: ({x}, {y})")
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(img, f"({x},{y})", (x+10, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv2.imshow("Image", img)

def save_txt(points, output_path):
    if not output_path:
        raise ValueError("Output path not set!")
    with open(output_path, 'w') as f:
        for point in points:
            f.write(f"{point[0]},{point[1]}\n")
    print(f"Coordinates saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Image Coordinate Finder")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("--save", action="store_true", help="Save clicked coordinates to txt")
    parser.add_argument("--out", default="coords.txt", help="Output file path for coordinates")
    args = parser.parse_args()

    img = cv2.imread(args.image)
    if img is None:
        raise FileNotFoundError(f"Image not found at {args.image}")

    points = []

    cv2.namedWindow("Image")
    if args.save:
        data = {"img": img, "points": points}
        cv2.setMouseCallback("Image", mouse_callback_savetxt, data)
    else:
        cv2.setMouseCallback("Image", mouse_callback_view, img)

    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if args.save:
        save_txt(points, args.out)

if __name__ == "__main__":
    main()
