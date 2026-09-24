import os
import time
import traceback
from pathlib import Path

from scripts.physton_prompt.get_lang import get_lang

model = None
tokenizer = None
model_name = "facebook/mbart-large-50-many-to-many-mmt"
loading = False

EXTENSION_ROOT = Path(__file__).resolve().parents[2]
cache_dir = os.path.normpath(str(EXTENSION_ROOT / "models"))

MODEL_FOLDER = "mbart-large-50-many-to-many-mmt"
MODEL_MARKERS = (
    "pytorch_model.bin",
    "model.safetensors",
    "pytorch_model.bin.index.json",
    "model.safetensors.index.json",
)


def _valid_local_model(path: Path) -> bool:
    if not path.is_dir():
        return False
    return any((path / marker).exists() for marker in MODEL_MARKERS)


def _find_local_model():
    # 1) Model stored inside this ForgeNeo extension.
    candidates = [
        EXTENSION_ROOT / "models" / MODEL_FOLDER,

        # 2) Reuse the model from the original extension if both versions
        #    are installed side by side in Forge's extensions folder.
        EXTENSION_ROOT.parent / "sd-webui-prompt-all-in-one" / "models" / MODEL_FOLDER,
    ]

    for candidate in candidates:
        if _valid_local_model(candidate):
            return candidate

    return None


def initialize(reload=False):
    global model, tokenizer, model_name, cache_dir, loading

    if loading:
        # Wait for an already running initialization instead of immediately
        # raising because model/tokenizer are still None.
        while loading:
            time.sleep(0.1)

        if model is None or tokenizer is None:
            raise Exception("mBART50 initialization failed")
        return

    if not reload and model is not None and tokenizer is not None:
        return

    loading = True
    model = None
    tokenizer = None

    local_model = _find_local_model()
    selected_model = str(local_model) if local_model else "facebook/mbart-large-50-many-to-many-mmt"

    print("[sd-webui-prompt-all-in-one] mBART50 diagnostics:")
    print(f"  extension: {EXTENSION_ROOT}")
    print(f"  cache dir: {cache_dir}")
    print(f"  selected model: {selected_model}")
    if local_model:
        print("  local model: FOUND")
    else:
        print("  local model: NOT FOUND; Hugging Face download/cache will be used")

    try:
        import torch
        import transformers
        from transformers import MBart50TokenizerFast, MBartForConditionalGeneration

        print(f"  torch: {getattr(torch, '__version__', 'unknown')}")
        print(f"  transformers: {getattr(transformers, '__version__', 'unknown')}")

        model_name = selected_model
        print(f"[sd-webui-prompt-all-in-one] Loading model {model_name} ...")

        model = MBartForConditionalGeneration.from_pretrained(
            model_name,
            cache_dir=cache_dir,
        )
        tokenizer = MBart50TokenizerFast.from_pretrained(
            model_name,
            cache_dir=cache_dir,
        )

        print(f"[sd-webui-prompt-all-in-one] Model {model_name} loaded.")
        loading = False
    except Exception:
        loading = False
        print("[sd-webui-prompt-all-in-one] mBART50 initialization FAILED:")
        traceback.print_exc()
        raise


def translate(text, src_lang, target_lang):
    global model, tokenizer

    if not text:
        if isinstance(text, list):
            return []
        return ""

    if model is None or tokenizer is None:
        raise Exception(get_lang("model_not_initialized"))

    if src_lang == target_lang:
        return text

    tokenizer.src_lang = src_lang
    encoded_input = tokenizer(text, return_tensors="pt", padding=True)

    generated_tokens = model.generate(
        **encoded_input,
        forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],
        max_new_tokens=500,
    )

    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
