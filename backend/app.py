from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
import shutil
import os
import sys

# Allow backend to import ml folder
sys.path.append("../ml")

from process_bank_excel import process_excel
from masked import apply_masking

app = FastAPI()

UPLOAD_DIR = "../uploads"
OUTPUT_DIR = "../outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("../frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

# ---------------- FILE UPLOAD ----------------
@app.post("/upload")
async def upload_bank_statement(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run your existing ML pipeline
    output_df = process_excel(file_path)

    output_path = os.path.join(OUTPUT_DIR, "classified_output.xlsx")
    output_df.to_excel(output_path, index=False)

    masked_df = apply_masking(output_df)
    masked_path = os.path.join(OUTPUT_DIR, "classified_output_masked.xlsx")
    masked_df.to_excel(masked_path, index=False)

    return {
        "status": "success",
        "message": "Bank statement processed successfully"
    }

# ---------------- DOWNLOAD ----------------
@app.get("/download/classified")
def download_classified():
    return FileResponse(
        "../outputs/classified_output.xlsx",
        filename="classified_output.xlsx"
    )

@app.get("/download/masked")
def download_masked():
    return FileResponse(
        "../outputs/classified_output_masked.xlsx",
        filename="classified_output_masked.xlsx"
    )
