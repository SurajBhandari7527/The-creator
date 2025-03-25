import torch
import os
from PIL import Image
from diffusers import BitsAndBytesConfig, SD3Transformer2DModel, StableDiffusion3Pipeline
import json

# Environment variable for memory management
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Model ID for Medium version
model_id = "stabilityai/stable-diffusion-3.5-medium"

# Configure Bits and Bytes for 4-bit quantization
nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Load the 2D Transformer model with quantization
model_nf4 = SD3Transformer2DModel.from_pretrained(
    model_id,
    subfolder="transformer",
    quantization_config=nf4_config,
    torch_dtype=torch.bfloat16
)

# Load the Stable Diffusion pipeline
pipeline = StableDiffusion3Pipeline.from_pretrained(
    model_id,
    transformer=model_nf4,
    torch_dtype=torch.bfloat16
)

# Enable model CPU offloading for better memory management
pipeline.enable_model_cpu_offload()

# Load prompts from a JSON file
try:
    with open('D:\models\english\content_creator\prompts.json','r') as f:
        promptss=json.load(f)

    prompts=promptss[0]
    with open('D:\models\english\content_creator\prompts.json','w') as f:
        json.dump(promptss,f)
    # with open("D:\models\english\prompts.json", "r") as f:
    #     prompts = json.load(f)
except FileNotFoundError:
    print("prompts.json not found. Please provide a valid file.")
    exit()

# Generate images for prompts
count = 10
for prompt in prompts:
    try:
        # Get prompt and negative prompt
        negative_prompt = "low quality, blurry, incomplete face, distorted,incomplete fingers"  # Default to empty if not provided

        # Generate the image using the pipeline
        result = pipeline(
            prompt="(anime style) masculine darkish shadow  " + prompt,
            negative_prompt=negative_prompt,  # Pass the negative prompt
            num_inference_steps=20,  # Steps from JSON
            guidance_scale=4.5,         # Default guidance scale
            height=896,              # Height from JSON
            width=1600,                # Width from JSON
            max_sequence_length=512
        )

        # Save the generated image
        result.images[0].save(f"D:\models\english\photos\{count}.png")
        print(f"Generated image saved as result_{count}.png")
        count += 1

        # Free up GPU memory after each inference
        torch.cuda.empty_cache()

    except Exception as e:
        print(f"Error generating image ")
        print(f"Details: {e}")
