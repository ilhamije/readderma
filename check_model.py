from huggingface_hub import model_info
try:
    info = model_info("Jayanth2002/dinov2-base-finetuned-SkinDisease")
    print(f"Model found: {info.modelId}")
    print(f"Tags: {info.tags}")
    print(f"Config: {info.config}")
except Exception as e:
    print(f"Error: {e}")
