from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from diffusers import StableDiffusionPipeline
import torch
import base64
from io import BytesIO

# Define request body
class PromptRequest(BaseModel):
    prompt: str

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (adjust for your frontend in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 👈 Vite default dev URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/generate-image/")
async def options_handler(request: Request):
    return JSONResponse(content={"message": "CORS preflight passed"}, status_code=200)

# Global variable for pipeline
pipe = None

@app.on_event("startup")
def load_model():
    global pipe
    model_id = "runwayml/stable-diffusion-v1-5"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load model
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
    pipe.to(device)
    pipe.safety_checker = None 
    # Enable attention slicing for better performance on limited VRAM
    pipe.enable_attention_slicing()

@app.get("/")
def root():
    return {"message": "🚀 Stable Diffusion API is running!"}

@app.post("/generate-image/")
def generate_image(request: PromptRequest):
    try:
        image = pipe(request.prompt, num_inference_steps=100).images[0]
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return {"image_base64": img_str}
    except Exception as e:
        return {"error": f"Image generation failed: {str(e)}"}
