import torch
import pandas as pd
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import lightning as L
from lightning.pytorch import Trainer, seed_everything
import torch
from torch.utils.data import DataLoader, Dataset
import pytorch_lightning as pl
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
from torchmetrics.classification import BinaryAccuracy, BinaryPrecision,BinaryRecall, BinaryMatthewsCorrCoef, BinaryF1Score, MulticlassAUROC, MulticlassAveragePrecision
from torcheval.metrics.functional import binary_auprc
from torchsampler import ImbalancedDatasetSampler
from lightning.pytorch.loggers import WandbLogger
import wandb
class CustomDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        text = self.texts[index]
        label = self.labels[index]
        encoding = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        input_ids = encoding['input_ids'].squeeze(0)
        attention_mask = encoding['attention_mask'].squeeze(0)
        
        return {
            'text':text,
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': torch.tensor(label, dtype=torch.long)
        }
    def get_labels(self):   
        return self.labels

class CodeBERTFineTuner(L.LightningModule):
    def __init__(self,iteration, fold,model_name="Salesforce/codet5-base", num_labels=2, learning_rate=2e-7):#replace with actual model name
        super().__init__()
        self.save_hyperparameters()
        self.acc = BinaryAccuracy()
        self.precision = BinaryPrecision()
        self.recall = BinaryRecall()
        self.mcc = BinaryMatthewsCorrCoef()
        self.f1 =BinaryF1Score()
        self.auroc = MulticlassAUROC(2)
        self.auprc = MulticlassAveragePrecision(2)
        self.iteration = iteration
        self.fold = fold
        # Load CodeBERT model for sequence classification
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.learning_rate = learning_rate

    def forward(self, input_ids, attention_mask, labels=None):
        return self.model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)

    def training_step(self, batch, batch_idx):
        outputs = self(batch['input_ids'], batch['attention_mask'], labels=batch['labels'])
        loss = outputs.loss
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        outputs = self(batch['input_ids'], batch['attention_mask'], labels=batch['labels'])
        val_loss = outputs.loss
        logits = outputs.logits
        preds = torch.argmax(logits, dim=1)
        acc = torch.sum(preds == batch['labels']).item() / len(batch['labels'])

        val_precision =self.precision(preds, batch['labels'])
        val_recall =self.recall(preds, batch['labels'])
        val_mcc = self.mcc(preds, batch['labels'])
        val_f1 =self.f1(preds, batch["labels"])
        val_auroc=self.auroc(logits, batch["labels"])
        val_auprc = self.auprc(logits, batch["labels"])
        self.log("val_precision", val_precision, prog_bar=True)
        self.log("val_recall", val_recall, prog_bar=True)
        self.log("val_f1", val_f1, prog_bar=True)
        self.log("val_mcc", val_mcc, prog_bar=True)
        self.log("val_AUROC", val_auroc, prog_bar=True)
        self.log("val_auprc", val_auprc, prog_bar=True)
        self.log("val_loss", val_loss, prog_bar=True)
        self.log("val_acc", acc, prog_bar=True)
        return val_loss

    def test_step(self, batch, batch_idx):
        outputs = self(batch['input_ids'], batch['attention_mask'], labels=batch['labels'])
        test_loss = outputs.loss
        logits = outputs.logits
        preds = torch.argmax(logits, dim=1)
        val_acc = self.acc(preds, batch['labels'])
        val_precision =self.precision(preds, batch['labels'])
        val_recall =self.recall(preds, batch['labels'])
        val_mcc = self.mcc(preds, batch['labels'])
        val_f1 =self.f1(preds, batch["labels"])
        val_auroc=self.auroc(logits, batch["labels"])
        val_auprc = self.auprc(logits, batch["labels"])
        self.log("test_loss", test_loss, on_epoch=True,prog_bar=True)
        self.log("test_acc", val_acc, prog_bar=True,on_epoch=True)
        self.log("test_precision", val_precision, prog_bar=True,on_epoch=True)
        self.log("test_recall", val_recall, prog_bar=True,on_epoch=True)
        self.log("test_f1", val_f1, prog_bar=True,on_epoch=True)
        self.log("test_mcc", val_mcc, prog_bar=True, on_epoch=True)
        self.log("test_loss", test_loss, prog_bar=True, on_epoch=True)
        self.log("test_AUROC", val_auroc, prog_bar=True, on_epoch=True)
        self.log("test_auprc", val_auprc, prog_bar=True, on_epoch=True)
        return {
            "loss": test_loss, 
            "preds": preds, 
            "labels": batch['labels'],  # for metrics calculation later
            "acc": val_acc, 
            "precision": val_precision, 
            "recall": val_recall, 
            "f1": val_f1, 
            "mcc": val_mcc, 
            "auroc": val_auroc, 
            "auprc": val_auprc
            }
    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=self.learning_rate)

for iteration in range(2,3):
    for fold in range(5):

        wandb_logger = WandbLogger(name=f"cleaned_codet5_iter_{iteration}_fold_{fold}",log_model=True)
        # Example dataset setup (you would replace these with your actual data)
        path = f"llmclean/data/fold5r1/split_{fold}/"
        df = pd.read_csv(path+"cleaned_func_train_by_commit.csv")
        texts = df["processed_func"].tolist()
        labels =  df["target"].tolist()
        tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-base")#replace with actual tokenizer
        train_dataset = CustomDataset(texts, labels, tokenizer)
        train_dataloader = DataLoader(train_dataset,sampler=ImbalancedDatasetSampler(train_dataset),  batch_size=50, shuffle=False)
        df = pd.read_csv(path+"cleaned_func_val_by_commit.csv")
        texts = df["processed_func"].tolist()
        labels =  df["target"].tolist()

        val_dataset = CustomDataset(texts, labels, tokenizer)

        val_dataloader = DataLoader(val_dataset, batch_size=50, shuffle=False)

        # Example dataset setup (you would replace these with your actual data)
        df = pd.read_csv(path+"cleaned_func_test_by_commit.csv")
        texts = df["processed_func"].tolist()
        labels =  df["target"].tolist()
        test_dataset = CustomDataset(texts, labels, tokenizer)
        test_dataloader = DataLoader(test_dataset, batch_size=50, shuffle=False)

        model = CodeBERTFineTuner(iteration,fold)

        trainer =Trainer(max_epochs=10, devices=4,accelerator="gpu",strategy="deepspeed_stage_2", precision=16, logger=wandb_logger)#you can experiment with different numbers of GPUs
        trainer.fit(model, train_dataloader, val_dataloader)
        trainer.test(dataloaders=test_dataloader)
        wandb.finish()

