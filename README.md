# LLM_based_patch_filtering

## Directory Structure
* api_keys.py: Insert OpenAI API key, if needed
* convert.py: Has two methods, one to convert original MSR data into the right format for main.py, one to convert the raw output back into the MSR data format
* exp.py: Constructs the prompts based off of the provided hunk and description. Each prompting strategy has a different method
* finetune.py: Allows you to train models with the filtered data, like we did
* llm/llama.py: Used to send get requests in the specific format for Llama
* llm/gpt.py: Used to send get requests in the specific format for gpt-4o
* main.py: Driver file of this program. Features a command line interface described below (But more details can be found by running ```python main.py -h```). Allows users to run our experiments from the paper. Divided into RQ1 and RQ2, described below
* scorer.py: Used at the end of main.py to score RQ1 results

## Getting Started
If using GPT, please insert OpenAI API key in api_keys.py

1. Create virtual environment. We use Python 3.11
2. Activate virtual environment
3. Install dependencies. With pip it's ```pip install -r requirements.txt```
4. Download necessary datasets
   * (TODO: Link datasets. Wouldve done this myself, but wasn't sure how to anonymously upload them)
## Replicating RQ1
For Llama, start a session of Llama. In the command line you can specify the endpoint like so
```
python main.py http://whatever-your-uri-is smartshark.csv output.csv gen_know llama 1
```
Where:
  * http://whatever-your-uri-is is the URI/endpoint
  * smartshark.csv is the input dataset
  * output.csv is the output dataset
  * gen_know is the prompting strategy (there is also zeroshot, fewshot, cot)
  * llama is the model (refers to any llama)
  * 1 is the RQ
GPT-4o is very similar. The main difference is you don't need to specify the endpoint. You still need to provide something, as it is a required argument. Just put a 0. Also, say gpt instead of llama for the model.
```
python main.py 0 smartshark.csv output.csv gen_know gpt 1
```
Output will be the outputfile specified and metrics to the console. Consider submitting a SBATCH job, this will take a while.

## Replicating RQ2
Currently, RQ2 code is only tested with GPT and generated knowledge prompting, as this was the best combination from RQ1.
To run this experiment
```
python main.py -p -of final_output.csv 0 msr.csv output.csv gen_know gpt 2
```
Where:
  * 0 is a subsitute for the endpoint, which is hardcoded for GPT
  * msr.csv is the input MSR dataset, which will first be preprocessed because of the -p flag
  * output.csv is the intermediary output of the program, as discussed earlier
  * final_output.csv is the final output, in the MSR format
  * gen_know is the prompting strategy (there is also zeroshot, fewshot, cot)
  * gpt is the model (specifically gpt-4o as of now)
  * 2 is the RQ

After this, you can run ```python finetune.py``` to train the different models mentioned in the study on the filtered data. You will need [wandb](https://docs.wandb.ai/quickstart/) to view the results. Before running, please enter in the appropriate model/tokenizer names where the comments prompt you to. Same goes for the data, you need to enter in the path(s) to the datasets generated.

## Other Arguments
* ```-h``` Help
* ```-rp``` Preprocess Recovery (If this optional argument is given, convert will recover from a checkpoint. This is specifically for RQ2 when preprocessing is required. Please only specify this if an interruption occurs)
* ```-cp``` Checkpoint Recovery (If this optional argument is given, main.py will recover from a checkpoint. This is for RQ1 or RQ2. Please only specify this if an interruption occurs)
