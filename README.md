# MultiTool-CoT

This repository contains the code for the paper "MultiTool-CoT: GPT-3 Can Use Multiple External Tools with Chain of Thought Prompting (Inaba et al., ACL2023)".

## Environment

- Python: 3.7.1+

## Installation

```bash
python -m venv env
pip install -r requirements.txt
```

## Running MultiTool-GPT

```bash
export OPENAI_ORGANIZATION="OPENAI_ORGANIZATION"
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
python main.py \
    --question "Find the amount of Calcium hydroxide that is required to react with 2 moles of Carbon dioxide to form 2 moles of Calcium carbonate along with 2 moles of Water" \
    --few_shot "prompt/few_shot_5.txt" \
    --use_cal \
    --use_crp \
    --use_mml \
    --output "output.txt"
```

## Citation

```bibtex
@inproceedings{inaba-etal-2023-multi,
    title = "{M}ulti{T}ool-{C}o{T}: {GPT}-3 Can Use Multiple External Tools with Chain of Thought Prompting",
    author = "Inaba, Tatsuro  and
      Kiyomaru, Hirokazu  and
      Cheng, Fei  and
      Kurohashi, Sadao",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics",
    month = july,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
}
```

## References
- [NumGLUE](https://github.com/allenai/numglue) (Task2)
- [OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
