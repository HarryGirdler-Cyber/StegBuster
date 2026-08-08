# StegBuster
StegBuster is an automated digital forensics tool written in Python, designed to detect steganographic data hidden within digital image files. By parsing and analysing pixel data across RGB colour channels, Stegbuster is able to identify structural anomalies and Least Significant Bit (LSB) alterations, indicative of steganographic embedding.

Scope, Research Context and Limitations
StegBuster was developed as an experimental proof-of-concept for an academic research dissertation. While effective at detecting Least Significant Bit (LSB) anomalies in uncompressed or specific image formats, users and recruiters should note its experimental scope:

-Proof-of-Concept Status: Developed to evaluate specific steganalysis methodologies rather than serve as a production-grade enterprise security tool.
-Format Sensitivity: Detection accuracy varies based on image compression (e.g., JPEG compression artifacts can introduce false positives compared to raw PNG/BMP files).
-Algorithmic Scope: Optimised primarily for spatial domain steganography; transform domain techniques (such as DCT coefficient manipulation) are currently out of scope.
-Future Work: Planned improvements include integrating machine learning classifiers to lower false-positive rates across heavily compressed media.
