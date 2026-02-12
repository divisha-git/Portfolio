import cv2
import numpy as np
import os
import sys

def remove_rings_from_image(image_path, output_path=None):
    """
    Remove circular/elliptical rings/borders from an image
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image from {image_path}")
        return False
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Detect circles using Hough Circle Transform
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=100,
        param1=50,
        param2=30,
        minRadius=50,
        maxRadius=min(img.shape[0], img.shape[1]) // 2
    )
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        # Create a mask to keep only the content inside the largest circle
        mask = np.zeros(gray.shape, dtype=np.uint8)
        
        # Find the largest circle (assuming it's the main ring)
        if len(circles) > 0:
            # Sort circles by radius and take the largest
            circles = sorted(circles, key=lambda x: x[2], reverse=True)
            x, y, r = circles[0]
            
            # Create circular mask
            cv2.circle(mask, (x, y), r - 10, 255, -1)  # Slightly smaller radius to avoid ring
            
            # Apply mask to original image
            result = cv2.bitwise_and(img, img, mask=mask)
            
            # Create a white background
            white_bg = np.ones_like(img) * 255
            white_bg = cv2.bitwise_and(white_bg, white_bg, mask=cv2.bitwise_not(mask))
            
            # Combine the masked image with white background
            final_result = cv2.add(result, white_bg)
            
            # Save the result
            if output_path is None:
                name, ext = os.path.splitext(image_path)
                output_path = f"{name}_no_rings{ext}"
            
            cv2.imwrite(output_path, final_result)
            print(f"Successfully removed rings. Saved to: {output_path}")
            return True
    
    print("No circular rings detected in the image.")
    return False

def remove_elliptical_border(image_path, output_path=None):
    """
    Alternative method for elliptical borders
    """
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find contours
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Create mask
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.drawContours(mask, [largest_contour], -1, 255, -1)
        
        # Erode mask slightly to avoid border
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        
        # Apply mask
        result = cv2.bitwise_and(img, img, mask=mask)
        
        # White background
        white_bg = np.ones_like(img) * 255
        white_bg = cv2.bitwise_and(white_bg, white_bg, mask=cv2.bitwise_not(mask))
        
        final_result = cv2.add(result, white_bg)
        
        if output_path is None:
            name, ext = os.path.splitext(image_path)
            output_path = f"{name}_no_rings{ext}"
        
        cv2.imwrite(output_path, final_result)
        print(f"Successfully removed border. Saved to: {output_path}")
        return True
    
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_rings.py <image_path> [output_path]")
        print("Available images in directory:")
        for file in os.listdir('.'):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                print(f"  - {file}")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        sys.exit(1)
    
    # Try circular ring removal first
    if not remove_rings_from_image(image_path, output_path):
        # Fallback to elliptical border removal
        if not remove_elliptical_border(image_path, output_path):
            print("Could not remove rings/borders from the image.")
