# LLM_based_patch_filtering

## Directory Structure
* api_keys.py: Insert OpenAI API key, if needed
* convert.py: Has two methods, one to convert original MSR data into the right format for main.py, one to convert the raw output back into the MSR data format
* exp.py: Constructs the prompts based off of the provided hunk and description. Each prompting strategy has a different method
* finetune.py: Allows you to train models with the filtered/unfiltered data, like we did for rq2
* llm/llama.py: Used to send get requests in the specific format for Llama
* llm/gpt.py: Used to send get requests in the specific format for gpt-4o
* main.py: Driver file of this program. Features a command line interface described below (But more details can be found by running ```python main.py -h```). Allows users to run our experiments from the paper. Divided into RQ1 and RQ2, described below
* scorer.py: Used at the end of main.py to score RQ1 results

## Getting Started
If using GPT, please insert OpenAI API key in api_keys.py

1. Create virtual environment. We use Python 3.11
2. Activate virtual environment
3. Install dependencies. With pip it's ```pip install -r requirements.txt```
4. Download [necessary datasets](https://drive.google.com/drive/folders/1lsVoGPOymIGkuKgi50UnGyvviglZ3Mrf?usp=sharing). Unfiltered MSR data used can be found [here (train)](https://drive.google.com/uc?id=1ldXyFvHG41VMrm260cK_JEPYqeb6e6Yw) and [here (val)](https://drive.google.com/uc?id=1yggncqivMcP0tzbh8-8Eu02Edwcs44WZ)

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
* 
## Results
### RQ1
| **Model**            | **Prompting**      | **Precision** | **Recall** | **F1**  | **Accuracy** |
|----------------------|------------------|-------------|--------|------|-----------|
| **Llama3**          | Gen. Knowledge   | **0.81**    | 0.60   | **0.69** | **0.75**  |
|                      | Zero-shot        | 0.71        | 0.52   | 0.60  | 0.68      |
|                      | Few-shot         | 0.83        | 0.23   | 0.37  | 0.62      |
|                      | COT              | 0.63        | **0.65** | 0.64  | 0.66      |
| **GPT4**            | Gen. Knowledge   | 0.71        | **0.77** | **0.73** | **0.74**  |
|                      | Zero-shot        | **0.81**    | 0.51   | 0.62  | 0.71      |
|                      | Few-shot         | 0.69        | 0.61   | 0.65  | 0.69      |
|                      | COT              | 0.62        | 0.64   | 0.63  | 0.65      |
| **CodeLlama**       | Gen. Knowledge   | **0.67**    | 0.00   | 0.01  | **0.54**  |
|                      | Zero-shot        | 0.32        | 0.04   | 0.07  | 0.52      |
|                      | Few-shot         | 0.53        | 0.17   | 0.26  | 0.54      |
|                      | COT              | 0.46        | **0.85** | **0.60** | 0.47      |
| **DeepSeek-R1**     | Gen. Knowledge   | 0.49        | 0.20   | 0.28  | 0.53      |
|                      | Zero-shot        | **0.71**    | **0.48** | **0.58** | **0.67**  |
|                      | Few-shot         | 0.00        | 0.00   | 0.00  | 0.54      |
|                      | COT              | 0.57        | 0.40   | 0.47  | 0.58      |

### RQ2

| **Model**   | **Training Data** | **Precision**       | **Recall**          | **F1**               | **MCC**              | **Accuracy**         | **AUC-ROC**         | **AUC-PR**          |
|------------|----------------|--------------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|
| **LineVul** | Unfiltered    | $0.668 \pm 0.033$ | $0.867 \pm 0.025$ | $0.754 \pm 0.023$ | $0.748 \pm 0.021$ | $0.976 \pm 0.003$ | $0.948 \pm 0.017$ | $0.692 \pm 0.030$ |
|            | Filtered      | $0.716 \pm 0.033$ | $0.798 \pm 0.033$ | $0.754 \pm 0.019$ | $0.740 \pm 0.019$ | $0.978 \pm 0.003$ | $0.948 \pm 0.014$ | $0.756 \pm 0.031$ |
|            | **+/-**       | **+7.19%**         | **-7.96%**         | **0.00%**         | **-1.07%**         | **+0.20%**         | **0.00%**         | **+9.25%**         |
|            | **p-value**    | $5.9e-05$         | $6.3e-11$         | $8.40e-02$        | $3.27e-02$        | $1.09e-01$        | $1.24e-01$        | $1.92e-08$        |
| **CodeBERT** | Unfiltered  | $0.475 \pm 0.027$ | $0.761 \pm 0.024$ | $0.556 \pm 0.023$ | $0.658 \pm 0.024$ | $0.955 \pm 0.005$ | $0.844 \pm 0.019$ | $0.835 \pm 0.005$ |
|            | Filtered      | $0.511 \pm 0.038$ | $0.739 \pm 0.023$ | $0.573 \pm 0.028$ | $0.683 \pm 0.023$ | $0.961 \pm 0.005$ | $0.840 \pm 0.020$ | $0.853 \pm 0.011$ |
|            | **+/-**       | **+7.58%**         | **-2.89%**         | **+3.06%**         | **+3.80%**         | **+0.63%**         | **-0.47%**         | **+2.16%**         |
|            | **p-value**    | $1.67e-3$         | $1.45e-2$         | $5.02e-2$         | $1.96e-3$         | $3.16e-3$         | $2.67e-1$         | $1.13e-4$         |
| **CodeT5**  | Unfiltered   | $0.532 \pm 0.022$ | $0.756 \pm 0.027$ | $0.594 \pm 0.017$ | $0.706 \pm 0.014$ | $0.964 \pm 0.004$ | $0.842 \pm 0.020$ | $0.846 \pm 0.006$ |
|            | Filtered      | $0.578 \pm 0.022$ | $0.732 \pm 0.028$ | $0.616 \pm 0.014$ | $0.738 \pm 0.014$ | $0.970 \pm 0.003$ | $0.841 \pm 0.020$ | $0.858 \pm 0.010$ |
|            | **+/-**       | **+8.65%**         | **-3.17%**         | **+3.70%**         | **+4.53%**         | **+0.62%**         | **-0.12%**         | **+1.42%**         |
|            | **p-value**    | $1.18e-5$         | $1.86e-2$         | $1.41e-3$         | $3.51e-6$         | $1.41e-4$         | $9.83e-1$         | $4.27e-3$         |


