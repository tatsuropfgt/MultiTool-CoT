# GPT3withTools
Use multiple external tools during reasoning of LLMs (GPT-3). Prompt and external tools dedicated to solving [NumGLUE task2](https://github.com/allenai/numglue) are given.

## Setting up environments
- python 3.7.1+

### Set environment variables
```
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

### Create virtualenv
```
python -m venv env
pip install -r requirements.txt
```

## Running GPT3withTools
```
./main.sh
```

## References
- [NumGLUE](https://github.com/allenai/numglue) (Task2)
- [OpenAI API](https://platform.openai.com/docs/api-reference/introduction)