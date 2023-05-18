# GPTaug
Use multiple external tools during reasoning of LLMs (GPT-3).
Prompt and external tools are dedicated to solving [NumGLUE Task2](https://github.com/allenai/numglue).

## Setting up environments
- python 3.7.1+

### Set environment variables

```bash
export OPENAI_ORGANIZATION="OPENAI_ORGANIZATION"
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

### Create virtualenv

```bash
python -m venv env
pip install -r requirements.txt
```

## Running GPTaug

```bash
python main.py \
    --question "Find the amount of Calcium hydroxide that is required to react with 2 moles of Carbon dioxide to form 2 moles of Calcium carbonate along with 2 moles of Water" \
    --few_shot "prompt/few_shot_5.txt" \
    --use_cal \
    --use_crp \
    --use_mml \
    --output "output.txt"
```

## References
- [NumGLUE](https://github.com/allenai/numglue) (Task2)
- [OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
