import gzip
import shutil
import os
import sys

def compress_model(input_file, output_file):
    """Compress a model file using gzip compression"""
    print(f"Compressing {input_file}...")
    
    # Get original file size
    original_size = os.path.getsize(input_file)
    print(f"Original size: {original_size / (1024*1024):.2f} MB")
    
    # Compress the file
    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # Get compressed file size
    compressed_size = os.path.getsize(output_file)
    print(f"Compressed size: {compressed_size / (1024*1024):.2f} MB")
    
    # Calculate compression ratio
    compression_ratio = (1 - compressed_size / original_size) * 100
    print(f"Compression ratio: {compression_ratio:.1f}%")
    
    return compressed_size

def decompress_model(compressed_file, output_file):
    """Decompress a gzipped model file"""
    print(f"Decompressing {compressed_file} to {output_file}...")
    
    with gzip.open(compressed_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    print("Decompression complete!")

def setup_git_lfs():
    """Instructions for setting up Git LFS"""
    print("\n" + "="*60)
    print("GIT LFS (Large File Storage) SETUP INSTRUCTIONS")
    print("="*60)
    print("\n1. Install Git LFS:")
    print("   - Download from: https://git-lfs.github.io/")
    print("   - Or use: git lfs install")
    
    print("\n2. Track large files:")
    print("   git lfs track \"*.h5\"")
    print("   git lfs track \"*.h5.gz\"")
    
    print("\n3. Add .gitattributes file:")
    print("   git add .gitattributes")
    
    print("\n4. Add and commit your large files:")
    print("   git add model_phase1.h5.gz")
    print("   git commit -m \"Add compressed model file\"")
    print("   git push")
    
    print("\n5. To download LFS files in a new clone:")
    print("   git lfs pull")

if __name__ == "__main__":
    input_model = "model_phase1.h5"
    compressed_model = "model_phase1.h5.gz"
    
    if len(sys.argv) > 1 and sys.argv[1] == "decompress":
        if os.path.exists(compressed_model):
            decompress_model(compressed_model, input_model)
        else:
            print(f"Compressed file {compressed_model} not found!")
    else:
        # Compress the model
        if os.path.exists(input_model):
            compressed_size = compress_model(input_model, compressed_model)
            
            # Check if it's still too large for GitHub (100MB limit)
            if compressed_size > 100 * 1024 * 1024:
                print(f"\nWarning: Compressed file is still {compressed_size / (1024*1024):.2f}MB.")
                print("This exceeds GitHub's 100MB file size limit.")
                setup_git_lfs()
            else:
                print("\nCompressed file is suitable for GitHub upload!")
        else:
            print(f"Model file {input_model} not found!")