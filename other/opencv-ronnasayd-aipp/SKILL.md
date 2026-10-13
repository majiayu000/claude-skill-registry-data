---
name: opencv
description: "Use this skill whenever the user asks about Python OpenCV, computer vision, or image/video processing with cv2. Triggers include reading/writing/displaying images, drawing on images, image transformations (resize, rotate, warp, crop), thresholding, edge detection, feature detection, color space conversion, smoothing/blurring, morphological operations, working with video or webcam feeds, camera calibration, and object detection with OpenCV. Apply this skill even if the user just mentions cv2, imread, imshow, or asks how to do anything visual/image-related in Python. Always use this skill before writing any OpenCV code — it contains critical syntax reminders, common parameter patterns, and usage notes."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Python OpenCV Skill

A comprehensive reference for image and video processing with Python's OpenCV (`cv2`) library.

**Important notes:**

- OpenCV stores color images in **BGR** order (not RGB)
- Images are NumPy arrays; use array slicing for cropping
- Always call `cv2.destroyAllWindows()` after `cv2.waitKey()` in desktop scripts
- Install: `pip install opencv-python`

---

## Core I/O

```python
import cv2
import numpy as np

img = cv2.imread("path/to/image.jpg", cv2.IMREAD_COLOR)   # BGR
img = cv2.imread("path.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.imread("path.png", cv2.IMREAD_UNCHANGED)         # with alpha

cv2.imshow("Window Title", img)
cv2.waitKey(0)          # 0 = wait forever; N = wait N ms
cv2.destroyAllWindows()

cv2.imwrite("output.jpg", img)

# Cropping (numpy slicing: [y1:y2, x1:x2])
cropped = img[100:300, 100:300]
```

| Flag                   | Meaning                     |
| ---------------------- | --------------------------- |
| `cv2.IMREAD_COLOR`     | Read as BGR (default)       |
| `cv2.IMREAD_GRAYSCALE` | Read as single-channel gray |
| `cv2.IMREAD_UNCHANGED` | Keep alpha channel          |

---

## Drawing & Text

```python
cv2.line(img, (x1,y1), (x2,y2), (B,G,R), thickness)
cv2.rectangle(img, (x1,y1), (x2,y2), (B,G,R), thickness)   # thickness=-1 fills
cv2.circle(img, (cx,cy), radius, (B,G,R), thickness)
cv2.polylines(img, [pts], isClosed=True, color=(B,G,R), thickness=2)
cv2.putText(img, "text", (x,y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (B,G,R), thickness, cv2.LINE_AA)
```

---

## Arithmetic & Bitwise Operations

```python
dst = cv2.add(img1, img2)                                  # saturating add
dst = cv2.subtract(img1, img2)
dst = cv2.addWeighted(img1, α, img2, β, γ)                 # alpha blend

dst = cv2.bitwise_and(img1, img2, mask=mask)
dst = cv2.bitwise_or(img1, img2, mask=mask)
dst = cv2.bitwise_not(img, mask=mask)
dst = cv2.bitwise_xor(img1, img2, mask=mask)
```

---

## Geometric Transformations

```python
# Resize
resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
# Interpolation: INTER_AREA (shrink), INTER_CUBIC (quality zoom), INTER_LINEAR (default)

# Translation
T = np.float32([[1, 0, tx], [0, 1, ty]])
translated = cv2.warpAffine(img, T, (w, h))

# Rotation
M = cv2.getRotationMatrix2D(center=(cx,cy), angle=45, scale=1.0)
rotated = cv2.warpAffine(img, M, (w, h))

# Affine (3 point pairs)
M = cv2.getAffineTransform(src_pts, dst_pts)  # pts shape: (3,2) float32
dst = cv2.warpAffine(img, M, (cols, rows))

# Perspective (4 point pairs)
M = cv2.getPerspectiveTransform(src_pts, dst_pts)  # pts shape: (4,2) float32
dst = cv2.warpPerspective(img, M, (w, h))
```

---

## Morphological Operations

Operate on binary (thresholded) images; foreground should be white.

```python
kernel = np.ones((5,5), np.uint8)

eroded   = cv2.erode(img, kernel, iterations=1)
dilated  = cv2.dilate(img, kernel, iterations=1)
opened   = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)       # remove noise
closed   = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)      # fill holes
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)   # outline
tophat   = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
```

---

## Thresholding

```python
_, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
# Types: THRESH_BINARY, THRESH_BINARY_INV, THRESH_TRUNC, THRESH_TOZERO, THRESH_TOZERO_INV

# Adaptive (handles uneven lighting)
thresh = cv2.adaptiveThreshold(gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize=11, C=2)

# Otsu (auto threshold)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

---

## Edge & Feature Detection

```python
# Canny edges
edges = cv2.Canny(img, T_lower=100, T_upper=200, apertureSize=3)

# Hough lines (on edge image)
lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=200)

# Hough circles
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                            param1=50, param2=30, minRadius=1, maxRadius=40)

# Harris corners
dst = cv2.cornerHarris(gray_float32, blockSize=2, ksize=3, k=0.04)

# Shi-Tomasi corners
corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.3, minDistance=7)

# Keypoints (e.g. ORB/SIFT)
orb = cv2.ORB_create()
kp, des = orb.detectAndCompute(gray, None)
out = cv2.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)
```

---

## Color Space Conversion

```python
gray    = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv     = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lab     = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
ycrcb   = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
rgb     = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # for matplotlib

# Color masking (e.g. detect blue)
lower = np.array([110, 50, 50])
upper = np.array([130, 255, 255])
mask  = cv2.inRange(hsv, lower, upper)

# Find HSV value of a known BGR color
color_bgr = np.uint8([[[0, 255, 0]]])   # green in BGR
print(cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV))
```

---

## Smoothing / Blurring

```python
blurred  = cv2.blur(img, (5,5))                               # box blur
gaussian = cv2.GaussianBlur(img, (5,5), sigmaX=0)            # Gaussian
median   = cv2.medianBlur(img, ksize=5)                       # median (salt/pepper)
bilateral= cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)  # edge-preserving
custom   = cv2.filter2D(img, ddepth=-1, kernel=kernel_array) # custom kernel

# Gaussian kernel only
gk = cv2.getGaussianKernel(ksize=5, sigma=1.0)
```

---

## Image Pyramids

```python
smaller = cv2.pyrDown(img)    # halve resolution
larger  = cv2.pyrUp(img)      # double resolution
```

---

## Video / Webcam

```python
cap = cv2.VideoCapture(0)          # 0 = first webcam
cap = cv2.VideoCapture("video.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps=30.0, (width, height))
out.write(frame)
out.release()

# Extract frames
ret, frame = cap.read()
cv2.imwrite(f"frame_{i}.jpg", frame)
```

---

## Camera Calibration (Quick Reference)

```python
# Find chessboard corners
ret, corners = cv2.findChessboardCorners(gray, (cols, rows), None)
cv2.drawChessboardCorners(img, (cols, rows), corners, ret)

# Calibrate
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Undistort
undistorted = cv2.undistort(img, K, dist, None, newcameramtx)
```

---

## Common Patterns

```python
# Read → process → display → save
img   = cv2.imread("input.jpg")
gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)
cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("edges.jpg", edges)

# Binary mask + bitwise to isolate region
mask   = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
result = cv2.bitwise_and(img, img, mask=mask)

# Contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0,255,0), 2)
area = cv2.contourArea(contours[0])
x,y,w,h = cv2.boundingRect(contours[0])
```

---

## Tips & Gotchas

- BGR vs RGB: OpenCV uses BGR; matplotlib/PIL expect RGB — convert with `cv2.COLOR_BGR2RGB`
- Kernel size for blur/morphology must be **odd** (3, 5, 7, …)
- `cv2.threshold` returns a tuple `(retval, thresh_image)` — unpack with `_, thresh = …`
- For `warpAffine`/`warpPerspective`, source points must be `np.float32`
- `cv2.waitKey(0)` blocks; `cv2.waitKey(1)` is non-blocking (use in video loops)
- Check `img is None` after `imread` to catch missing file errors
