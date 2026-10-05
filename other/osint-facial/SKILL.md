---
name: osint-facial
description: FOSS facial recognition skill — DeepFace and InsightFace for identity verification, FAISS vector search for face matching, with ethical use guidelines and consent requirements.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [osint, facial-recognition, deepface, insightface, faiss, identity-verification, computer-vision, ethics, privacy]
    triggers: [facial-recognition, face-match, deepface, insightface, identity-verification, face-search, photo-identification]
    related_skills: [osint-social, osint-person]
---

# OSINT Facial Recognition (FOSS)

Open-source facial recognition for identity verification and matching — using DeepFace, InsightFace, and FAISS for large-scale face search. This skill focuses on **verification** (is this person who they say they are?) and **identification** (who is this person?), strictly within ethical and legal boundaries.

## Prerequisites

### Required Tools
```bash
# Python packages
pip install deepface
pip install insightface
pip install faiss-cpu  # or faiss-gpu for GPU
pip install opencv-python
pip install numpy pandas matplotlib
pip install fastapi uvicorn  # Optional for API serving
```

### Hardware Requirements
| Task | Minimum | Recommended |
|------|---------|-------------|
| Single face verification | CPU only | Any |
| 10-1000 face search | CPU | CPU with AVX2 |
| 1000-100K face search | 8GB RAM | 16GB RAM, GPU optional |
| 100K+ face search | 16GB RAM | 32GB+ RAM, GPU (FAISS) |

### Model Download
```bash
# DeepFace automatically downloads models on first use:
# - VGG-Face (default, ~500MB)
# - FaceNet (Google, ~90MB)
# - ArcFace (InsightFace, ~150MB)
# - DeepFace (Facebook, ~150MB)
# - OpenFace (CMU, ~100MB)

# InsightFace models:
# - buffalo_l (large, most accurate)
# - buffalo_s (small, fast)
# - antelope (best for Asian faces)
python -c "import insightface; model = insightface.app.FaceAnalysis(name='buffalo_l'); model.prepare(ctx_id=0)"
```

## Face Recognition Approaches

### Verification (1:1) — "Is this the same person?"
```
Input: Two face images
Output: Verified (True/False) + confidence score
Use case: Identity confirmation, access control
```

### Identification (1:N) — "Who is this person?"
```
Input: One face image + database of N known faces
Output: Top-K matches with confidence scores
Use case: Finding unknown persons in a gallery
```

### Clustering (N:N) — "Which faces belong to the same person?"
```
Input: N face images
Output: Groups of images belonging to same identity
Use case: Organizing large photo collections
```

## Step-by-Step Workflows

### 1. Single Face Verification

```python
from deepface import DeepFace

# Basic verification — compares two face images
result = DeepFace.verify(
    img1_path="photo_known.jpg",
    img2_path="photo_unknown.jpg",
    model_name="Facenet",      # Options: VGG-Face, Facenet, OpenFace, DeepFace, ArcFace
    detector_backend="opencv",  # Options: opencv, retinaface, mtcnn, ssd, yolov8
    distance_metric="cosine",   # Options: cosine, euclidean, euclidean_l2
    enforce_detection=True      # Raise error if no face found
)

print(f"Verified: {result['verified']}")
print(f"Distance: {result['distance']:.4f}")
print(f"Threshold: {result['threshold']:.4f}")
print(f"Model: {result['model']}")
print(f"Similarity: {(1 - result['distance']) * 100:.1f}%")

# Output:
# {
#   "verified": True,
#   "distance": 0.28,        # Lower = more similar
#   "threshold": 0.40,       # Default Facenet threshold
#   "model": "Facenet",
#   "detector_backend": "opencv",
#   "similarity_metric": "cosine",
#   "time": 2.15
# }
```

### 2. Find Face in Database

```python
import pandas as pd
from deepface import DeepFace
import os

# Build a face database
known_faces_dir = "/path/to/known/people/"
known_faces = []

for file in os.listdir(known_faces_dir):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        known_faces.append({
            "name": os.path.splitext(file)[0],
            "path": os.path.join(known_faces_dir, file)
        })

# Search for a query face in the database
dfs = DeepFace.find(
    img_path="query_face.jpg",
    db_path=known_faces_dir,
    model_name="Facenet",
    detector_backend="opencv",
    distance_metric="cosine",
    threshold=0.40,           # Match threshold (lower = stricter)
    silent=False
)

# Results — sorted by distance (closest match first)
if len(dfs) > 0 and not dfs[0].empty:
    print("Top matches:")
    for idx, row in dfs[0].iterrows():
        print(f"  {row['identity']} — distance: {row['distance']:.4f} — {row['Facenet_cosine_score']:.1%}")
else:
    print("No matches found in database")
```

### 3. FAISS Vector Search (Large-Scale)

```python
import numpy as np
import faiss
from deepface import DeepFace
import pickle

# Step 1: Generate embeddings for all known faces
def get_embeddings(image_path):
    """Extract face embedding vector from image."""
    embedding = DeepFace.represent(
        img_path=image_path,
        model_name="Facenet",
        detector_backend="opencv",
        enforce_detection=False
    )
    return np.array(embedding[0]["embedding"])

# Step 2: Build FAISS index
def build_face_index(face_embeddings, dimension=128):
    """
    Build FAISS index for fast face similarity search.
    Facenet produces 128-dim vectors.
    """
    # Convert to numpy array
    embeddings_array = np.array(face_embeddings).astype('float32')
    
    # Normalize for cosine similarity via inner product on unit vectors
    faiss.normalize_L2(embeddings_array)
    
    # Build index — Inner Product (cosine on normalized vectors)
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings_array)
    
    return index

# Step 3: Search for similar faces
def search_faces(query_image, index, face_list, k=5):
    """Search for top-K similar faces in the index."""
    # Get query embedding
    query_embedding = get_embeddings(query_image)
    query_embedding = query_embedding.astype('float32').reshape(1, -1)
    faiss.normalize_L2(query_embedding)
    
    # Search
    distances, indices = index.search(query_embedding, k)
    
    # Return results
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx != -1 and dist > 0.3:  # Filter low confidence
            results.append({
                "name": face_list[idx]["name"],
                "image_path": face_list[idx]["path"],
                "similarity": float(dist * 100)  # 0-100%
            })
    
    return results

# Step 4: Save/load index for reuse
# Save
with open("face_index.pkl", "wb") as f:
    pickle.dump({"index": faiss.serialize_index(index), "faces": face_list}, f)

# Load (after restart)
with open("face_index.pkl", "rb") as f:
    data = pickle.load(f)
    index = faiss.deserialize_index(data["index"])
    face_list = data["faces"]
```

### 4. InsightFace for High-Performance Detection

```python
import insightface
from insightface.app import FaceAnalysis
import cv2
import numpy as np

# Initialize InsightFace
app = FaceAnalysis(name='buffalo_l')  # buffalo_l = large, accurate
app.prepare(ctx_id=0)  # 0 = GPU, -1 = CPU

# Detect faces in an image
img = cv2.imread("group_photo.jpg")
faces = app.get(img)

print(f"Found {len(faces)} faces")

for i, face in enumerate(faces):
    # Face attributes
    print(f"\nFace {i+1}:")
    print(f"  Age: {face['age']:.1f}")          # Estimated age
    print(f"  Gender: {'Male' if face['gender'] == 1 else 'Female'}")
    print(f"  Bbox: {face['bbox']}")             # [x1, y1, x2, y2]
    print(f"  Detection Score: {face['det_score']:.4f}")
    
    # Face embedding (128-dim vector for recognition)
    embedding = face['embedding']
    print(f"  Embedding shape: {embedding.shape}")
    
    # Face quality
    print(f"  Pose: yaw={face['pose'][0]:.1f}, pitch={face['pose'][1]:.1f}, roll={face['pose'][2]:.1f}")

# Face comparison
if len(faces) >= 2:
    # Normalized embedding distance (cosine)
    emb1 = faces[0]['embedding'] / np.linalg.norm(faces[0]['embedding'])
    emb2 = faces[1]['embedding'] / np.linalg.norm(faces[1]['embedding'])
    similarity = np.dot(emb1, emb2)
    print(f"\nFace similarity: {similarity:.4f} ({similarity*100:.1f}%)")
```

### 5. Full Identity Verification Pipeline

```python
"""
Complete identity verification based on multiple sources.
Combines facial recognition with OSINT data.
"""

def verify_identity(known_photo: str, social_media_photos: list, name: str):
    """
    Verify if a person in social media photos matches a known identity.
    
    Args:
        known_photo: Path to photo of the known person
        social_media_photos: List of paths to social media profile photos
        name: Expected person's name (for cross-reference)
    
    Returns:
        dict: Verification results
    """
    
    results = []
    total_similarity = 0.0
    
    for photo in social_media_photos:
        try:
            result = DeepFace.verify(
                img1_path=known_photo,
                img2_path=photo,
                model_name="Facenet",
                detector_backend="retinaface",  # More accurate detection
                distance_metric="cosine",
                enforce_detection=True
            )
            total_similarity += (1 - result['distance'])
            results.append({
                "photo": photo,
                "verified": result['verified'],
                "confidence": (1 - result['distance']) * 100,
                "model": result['model']
            })
        except Exception as e:
            results.append({
                "photo": photo,
                "verified": False,
                "error": str(e),
                "confidence": 0
            })
    
    # Aggregate
    avg_confidence = (total_similarity / len(social_media_photos)) * 100 if social_media_photos else 0
    verified_count = sum(1 for r in results if r.get('verified'))
    
    return {
        "name": name,
        "total_photos_analyzed": len(social_media_photos),
        "verified_matches": verified_count,
        "average_confidence": avg_confidence,
        "determination": "CONFIRMED" if avg_confidence >= 70 and verified_count >= 2 else \
                         "LIKELY" if avg_confidence >= 50 else \
                         "INCONCLUSIVE" if avg_confidence >= 20 else \
                         "NO_MATCH",
        "individual_results": results
    }
```

### 6. Social Media Photo Cross-Reference

```python
"""
Cross-reference facial recognition across social media platforms.
Gather public profile photos and compare for identity verification.
"""

# Workflow:
# 1. Collect LinkedIn profile photo (if public)
# 2. Collect Facebook public profile photo
# 3. Collect Twitter/X profile photo
# 4. Collect Instagram profile photo (if public)
# 5. Run pairwise face verification between all photos
# 6. If all photos match same person → high confidence of single identity

def cross_reference_social_media(social_photos: dict):
    """
    Verify that multiple social media accounts belong to the same person.
    
    Args:
        social_photos: dict like {"linkedin": "path1.jpg", "facebook": "path2.jpg", ...}
    
    Returns:
        dict: Pairwise verification matrix
    """
    platforms = list(social_photos.keys())
    matrix = {}
    
    for i, p1 in enumerate(platforms):
        for p2 in platforms[i+1:]:
            if social_photos[p1] and social_photos[p2]:
                try:
                    result = DeepFace.verify(
                        img1_path=social_photos[p1],
                        img2_path=social_photos[p2],
                        model_name="ArcFace",  # ArcFace for cross-platform matching
                        detector_backend="retinaface"
                    )
                    matrix[f"{p1}↔{p2}"] = {
                        "same_person": result['verified'],
                        "similarity": (1 - result['distance']) * 100
                    }
                except:
                    matrix[f"{p1}↔{p2}"] = {"error": "Face detection failed"}
    
    # Overall assessment
    match_rate = sum(1 for v in matrix.values() if v.get('same_person', False)) / len(matrix) if matrix else 0
    
    return {
        "pairwise_results": matrix,
        "match_rate": match_rate,
        "verdict": "SAME_IDENTITY" if match_rate >= 0.8 else \
                   "PARTIAL_MATCH" if match_rate >= 0.5 else \
                   "DIFFERENT_IDENTITIES"
    }
```

## Performance Tuning

### Model Selection Guide
| Model | Accuracy | Speed | Vector Dim | Best For |
|-------|----------|-------|------------|----------|
| VGG-Face | Medium | Fast | 2622 | General use |
| Facenet | High | Medium | 128 | Best balance |
| OpenFace | Medium | Fast | 128 | Speed-critical |
| DeepFace | Medium | Slow | 4096 | Research |
| ArcFace | Very High | Slow | 512 | High-security verification |
| InsightFace | Very High | Fast (GPU) | 512 | Real-time detection |

### Threshold Tuning
```python
# Default thresholds may not fit your use case
thresholds = {
    "VGG-Face": {"cosine": 0.40, "euclidean": 0.60, "euclidean_l2": 0.85},
    "Facenet":  {"cosine": 0.40, "euclidean": 0.55, "euclidean_l2": 0.80},
    "OpenFace": {"cosine": 0.10, "euclidean": 0.35, "euclidean_l2": 0.55},
    "DeepFace": {"cosine": 0.23, "euclidean": 0.35, "euclidean_l2": 0.60},
    "ArcFace":  {"cosine": 0.40, "euclidean": 0.55, "euclidean_l2": 0.80},
}

# Stricter threshold (fewer false positives):
result = DeepFace.verify(
    img1_path="a.jpg",
    img2_path="b.jpg",
    model_name="Facenet",
    distance_metric="cosine",
    threshold=0.30  # Stricter than default 0.40
)

# Looser threshold (fewer false negatives):
result = DeepFace.verify(
    ...,
    threshold=0.50  # More permissive
)
```

### Batch Processing
```python
from concurrent.futures import ThreadPoolExecutor
import glob

def process_face_batch(face_dir, output_file):
    """Batch generate embeddings for all faces in a directory."""
    images = glob.glob(f"{face_dir}/*.jpg") + glob.glob(f"{face_dir}/*.png")
    
    def extract_embedding(img_path):
        try:
            embedding = DeepFace.represent(
                img_path=img_path,
                model_name="Facenet",
                detector_backend="retinaface",
                enforce_detection=False
            )
            name = os.path.splitext(os.path.basename(img_path))[0]
            return {"name": name, "path": img_path, "embedding": embedding[0]["embedding"]}
        except:
            return None
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(extract_embedding, images))
    
    results = [r for r in results if r is not None]
    
    # Save embeddings
    with open(output_file, "wb") as f:
        pickle.dump(results, f)
    
    print(f"Processed {len(results)} faces from {len(images)} images")
    return results
```

## Common Pitfalls

### False Positives / False Negatives
- **PITFALL**: Low-quality images cause false results.
- **SOLUTION**: Minimum image size: 200x200 pixels, face should be at least 80x80 pixels.
- **WORKAROUND**: Use `retinaface` detector backend for better detection of small/blurry faces.

### Lighting and Pose Variations
- **PITFALL**: Same person in different lighting → appears different to the model.
- **SOLUTION**: Use ArcFace model — most robust to lighting and pose variations.
- **WORKAROUND**: If possible, use multiple photos per person to build a profile, not a single reference photo.

### Age Progression
- **PITFALL**: Person at 20 vs. 60 may not match with default thresholds.
- **SOLUTION**: Lower the threshold for age-different comparisons. Use models trained on cross-age data.
- **WORKAROUND**: If age difference > 10 years, consider reducing threshold by 0.05-0.10.

### Facial Hair / Glasses / Masks
- **PITFALL**: Major appearance changes confuse recognition.
- **SOLUTION**: Use multiple reference photos showing different appearances.
- **WORKAROUND**: Focus on periocular region (eye area) which is more stable.

### Twins / Lookalikes
- **PITFALL**: Facial recognition can confuse identical twins and unrelated lookalikes.
- **SOLUTION**: Never rely SOLELY on facial recognition for identity confirmation.
- **WORKAROUND**: Combine with other OSINT data (location, employer, social media activity, voice).

### Ethnicity Bias
- **PITFALL**: Most models have lower accuracy on non-Caucasian faces.
- **SOLUTION**: Use ArcFace or InsightFace (trained on more diverse datasets).
- **WORKAROUND**: Models like `antelope` (InsightFace) are better for East Asian faces.

## Legal & Ethical Notes

> **⚠️ CRITICAL WARNING — FACIAL RECOGNITION HAS UNIQUE LEGAL RISKS:**
> - **Consent is REQUIRED** in many jurisdictions (EU GDPR, Illinois BIPA, Texas, Washington, California)
> - **BIPA (Illinois Biometric Information Privacy Act)**: $1,000-$5,000 per violation for collecting biometric data without consent
> - **GDPR Article 9**: Biometric data is "special category" — explicit consent required for processing
> - **EU AI Act (2024)**: Classifies facial recognition as "high-risk AI" — strict regulation
> - **No Warrantless Surveillance**: US Fourth Amendment limits government use of facial recognition
> - **Terms of Service**: Facebook/LinkedIn/etc prohibit bulk collection of profile photos
> - **Harassment**: Using facial recognition to track/stalk someone is illegal in all states
> - **Misidentification**: False positives can lead to false accusations — life-altering consequences

### Permissible Uses (with proper consent/authorization)
- Identity verification with subject's knowledge and consent (account recovery, KYC)
- Law enforcement with warrant (jurisdiction-dependent)
- Security research with IRB approval
- Personal photos where you own the rights
- Missing persons investigations (with family/law enforcement coordination)
- Access control (opt-in)

### Prohibited Uses
- ❌ Mass surveillance without warrant/authorization
- ❌ Live facial recognition in public spaces (banned in several cities/states)
- ❌ Creating face databases from social media without consent
- ❌ Categorizing people by race, religion, or political affiliation via facial analysis
- ❌ Using facial recognition to identify anonymous protesters or journalists
- ❌ Building face databases of minors
- ❌ Emotional state inference without explicit medical/research consent

### Best Practices for Ethical Use
1. **Always obtain consent** before adding someone to a face database
2. **Provide opt-out** mechanism for any deployed system
3. **Be transparent** — disclose when facial recognition is being used
4. **Human-in-the-loop** — never make automated decisions based solely on facial recognition
5. **Use confidence thresholds** that minimize false positives (stricter = better)
6. **Delete data** when no longer needed for the stated purpose
7. **Audit for bias** — test your system across demographic groups
8. **Document use cases** and legal basis for each deployment

## Cross-References

- `security/osint-recon` — Integrating facial recognition into full investigation pipeline
- `security/osint-person` — Verifying person identity with facial recognition
- `security/osint-social` — Cross-platform identity resolution via profile photos
- `security/osint-threat` — Threat actor identification via facial recognition
- `security/osint-redteam` — Physical penetration testing with facial recognition
- `software-development/building-mcp-servers` — Building MCP servers with facial recognition capabilities
- `mlops/models/segment-anything-model` — Complementary face detection and segmentation

## Verification Checklist

- [ ] DeepFace/InsightFace installed and models downloaded
- [ ] Face detection works on test images (single and group photos)
- [ ] Face verification works correctly on known-matching pairs
- [ ] Face verification correctly rejects known non-matching pairs
- [ ] Database built with proper embeddings for all known identities
- [ ] FAISS index built and searchable
- [ ] Threshold tuned for use case (balanced precision vs. recall)
- [ ] Batch processing tested with concurrent extraction
- [ ] Cross-platform photo matching tested
- [ ] Consent obtained for all faces in database (if required)
- [ ] Legal basis documented for use case
- [ ] Bias evaluation performed across demographic groups
- [ ] Human-in-the-loop review process defined
