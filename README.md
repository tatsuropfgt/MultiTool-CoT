# MultiTool-CoT
This repository contains the code for the paper "MultiTool-CoT: GPT-3 Can Use Multiple External Tools with Chain of Thought Prompting (Inaba et al., ACL2023)". 
[paper](https://arxiv.org/abs/2305.16896)

## Environment

- Python: 3.7.1+

## Installation

```bash
python -m venv env
pip install -r requirements.txt
```

## Running MultiTool-CoT

```bash
export OPENAI_ORGANIZATION="OPENAI_ORGANIZATION"
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
python main.py \
    --question "Find the mass percentage of C in Aluminum carbonate" \
    --few_shot "prompt/few_shot_5.txt" \
    --use_cal \
    --use_crp \
    --use_mml \
    --output "output.txt"
```

## Evaluating MultiTool-CoT on NumGLUE task2

```bash
git clone https://github.com/allenai/numglue.git
python eval.py \
    --filepath "numglue/data/NumGLUE_test.json" \
    --num_examples 3 \
    --few_shot "prompt/few_shot_5.txt" \
    --use_cal \
    --use_crp \
    --use_mml \
    --output "output.csv"
```

## Citation

```bibtex
@inproceedings{inaba-etal-2023-multitool,
    title = "{M}ulti{T}ool-{C}o{T}: {GPT}-3 Can Use Multiple External Tools with Chain of Thought Prompting",
    author = "Inaba, Tatsuro  and
      Kiyomaru, Hirokazu  and
      Cheng, Fei  and
      Kurohashi, Sadao",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.acl-short.130",
    pages = "1522--1532",
}
```

## References
- [NumGLUE](https://github.com/allenai/numglue) (Task2)
- [OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
