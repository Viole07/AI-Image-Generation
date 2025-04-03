from diffusers import StableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to(device)

# Enable attention slicing for lower memory usage
pipe.enable_attention_slicing()

prompt = "a cute puppy on the moon"
image = pipe(prompt).images[0]  

image.save("generated_image.png")