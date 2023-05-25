# MultiTool-CoT
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

## Running MultiTool-CoT

```bash
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


## References
- [NumGLUE](https://github.com/allenai/numglue) (Task2)
- [OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
